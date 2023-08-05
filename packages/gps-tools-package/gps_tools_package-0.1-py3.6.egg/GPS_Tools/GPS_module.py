import collections
import glob
import json
import math
import os
import sys
import time

import cv2
import descartes
import geopandas as gpd
import imutils
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shapely as sha
from PIL import Image
from shapely.geometry import Polygon, mapping, Point
from shapely.ops import cascaded_union
from tqdm import tqdm
from shutil import copyfile
from shapely import affinity

from GISS_Tools.global_giss_tools import safely_extend_bb, convert_corners_2_centroids
from GPS_Tools.loc_calculations import (calculate_azimuth,
                                        calculate_azimuth_points,
                                        calculate_distance,
                                        calculate_distance_points,
                                        calculate_object_gps,
                                        calculate_object_gps_center_reference, 
                                        calculate_pix_meter_coef,
                                        calculate_pix_meter_coef_points,
                                        calculate_point_geographic_coordinates,
                                        calculate_side_point_azimuth,
                                        divide_flight)
from GPS_Tools.loc_utils import (GPS, GPS_extended,
                                 create_polygon_from_gps_points,
                                 deg_to_radians, get_photos_names_from_dir,
                                 radians_to_deg, transform_to_cartesian,
                                 transform_to_gps, visualize_image_group)

from GPS_Tools.GPS_danger_zone_calc import locate_polygon_vertex_in_world

plt.rcParams['figure.figsize'] = [20, 12]
# https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
# https://www.movable-type.co.uk/scripts/latlong.html

"""
Attention: CONSIDER USING PYGeoodesy library if more precise calculations are needed !!!!

TODOS to consider: 10.12.2018
1. Calculate pixel/meter coef including height of the image (mean value)
2. Test this module on proper data - avoid gps shifting

"""

class InstaPhoto():
    """
    Class holding information about image and its GPS features


    Attributes:
        :filename: [str] name of the image 
        :image: [np.array] image data
        :resolution: [(int, int)] - resolution of image (width, height)
        :center_gps: [GPS] - image center gps coordinates
        :right_upper_corner: [GPS] - image right upper corner gps coordinates
        :right_down_corner: [GPS] - image right down corner gps coordinates
        :left_down_corner: [GPS] - image left dow corner gps coordinates
        :left_upper_corner: [GPS] - image left upper corner gps coordinates
        :azimuth: [float] - image azimuth (angle to north of image direction)
        :image_path: [string] - path to image file 
        :polygon: [shapely.polygon] - shapely polygon object created from gps corners (in cartesian coordinates)
    """

    
    # __slots__ = ('filename',
    #              'image',
    #              'resolution',
    #              'center_gps',
    #              'right_upper_corner',
    #              'right_down_corner',
    #              'left_down_corner',
    #              'left_upper_corner',
    #              'azimuth',
    #              'image_path',
    #              'polygon')
    
    def __init__(self, resolution, alt = 100):
        
        """ Initialize new InstaPhoto object
        
        :param resolution: resolution of image as (x, y)
        :type resolution: tuple
        :param alt: altitude of camera, defaults to 100
        :param alt: int, optional
        """
        self.resolution = resolution
        self.image = None
        self.image_path = ""
        self.alt = alt

    def read_data_from_df_row(self, metadata):
        """Read data from pandas dataframe row
        
        :param metadata: image information as [Img_name Center_lat Center_lon Right_up_lat Right_up_lon Right_down_lat Right_down_lon Left_down_lat Left_down_lon Left_up_lat Left_up_lon Azimuth]
        :type metadata: pd.Series
        """
        self.filename = metadata["Img_name"]
        self.center_gps = GPS(metadata['Center_lat'], metadata['Center_lon'], self.alt)
        self.right_upper_corner = GPS(metadata['Right_up_lat'], metadata['Right_up_lon'], self.alt)
        self.right_down_corner =  GPS(metadata['Right_down_lat'], metadata['Right_down_lon'], self.alt)
        self.left_down_corner =  GPS(metadata['Left_down_lat'], metadata['Left_down_lon'], self.alt)
        self.left_upper_corner =  GPS(metadata['Left_up_lat'], metadata['Left_up_lon'], self.alt)   
        self.azimuth = metadata['Azimuth']
        self._prepare_insta_polygon()

    def read_data_from_geoJSON(self, img_name, geojson_path):
        #TODO read single instaphoto data from geoJSON file

        metadata = gpd.read_file(geojson_path)
        metadata = metadata.set_index('shapely_type')

        self.filename = img_name

        center_upper_lon, center_upper_lat = list(metadata.loc['Center']['geometry'].coords)[0]
        self.center_gps = GPS(center_upper_lat, center_upper_lon, self.alt)

        right_upper_lon, right_upper_lat = list(metadata.loc['Right_up']['geometry'].coords)[0]
        self.right_upper_corner = GPS(right_upper_lat, right_upper_lon, self.alt)

        right_down_lon, right_down_lat = list(metadata.loc['Right_down']['geometry'].coords)[0]
        self.right_down_corner =  GPS(right_down_lat, right_down_lon, self.alt)

        left_down_lon, left_down_lat = list(metadata.loc['Left_down']['geometry'].coords)[0]
        self.left_down_corner =  GPS(left_down_lat, left_down_lon, self.alt)

        left_upper_lon, left_upper_lat = list(metadata.loc['Left_up']['geometry'].coords)[0]
        self.left_upper_corner =  GPS(left_upper_lat, left_upper_lon, self.alt)  

        self.azimuth = metadata.loc['Center']['Azimuth']
        self._prepare_insta_polygon()

    def set_image_path(self, image_path):
        self.image_path = image_path
        
    def get_image_path(self):
        return self.image_path
        
    def get_corners_gps_raw(self):

        photo_corners = ((self.left_down_corner.latitude, self.left_down_corner.longitude),
                        (self.right_down_corner.latitude, self.right_down_corner.longitude),
                        (self.left_upper_corner.latitude, self.left_upper_corner.longitude),
                        (self.right_upper_corner.latitude, self.right_upper_corner.longitude))  
                        
        return photo_corners

    def get_corners_gps(self):

        photo_corners = (self.left_down_corner,
                        self.right_down_corner,
                        self.left_upper_corner,
                        self.right_upper_corner)  
                        
        return photo_corners

    def _prepare_insta_polygon(self):
        """Create shapely polygon from gps corner points. Need for danger zone calculations
        
        """

        self.polygon = Polygon(self._prepare_polygon_corners())    

    def get_polygon(self):
        return self.polygon
    
    def check_point_in_image(self, gps_point):
        """Checks if given gps point is on image
        
        :param gps_point: gps point in world
        :type gps_point: GPS class
        :return: True if point is in image polygon otherwise false
        :rtype: bool
        """

        cart_point = transform_to_cartesian(gps_point)  
        return self.polygon.contains(Point(cart_point))

    def _prepare_polygon_corners(self):

        polygon_corners = []
        polygon_corners.append(transform_to_cartesian(self.right_upper_corner))
        polygon_corners.append(transform_to_cartesian(self.right_down_corner))
        polygon_corners.append(transform_to_cartesian(self.left_down_corner ))
        polygon_corners.append(transform_to_cartesian(self.left_upper_corner))
        
        return polygon_corners
      
    def load_image(self):
        """Load image from path. Image_path must be set first.
        """
        if self.image_path =="":
            print("Image path empty. Cannot load image !")
        else:
            self.image = np.asarray(Image.open(self.image_path))

    def shift_gps(self, latitude_shift, longitude_shift):
        """Shift gps points by given amount to correct data
        
        :param latitude_shift: latitude shift
        :type latitude_shift: float
        :param longitude_shift: longitude shifr
        :type longitude_shift: float
        """

        self.left_down_corner.latitude += latitude_shift
        self.left_down_corner.longitude += longitude_shift
        self.left_upper_corner.latitude += latitude_shift
        self.left_upper_corner.longitude += longitude_shift
        self.right_down_corner.latitude += latitude_shift
        self.right_down_corner.longitude += longitude_shift
        self.right_upper_corner.latitude += latitude_shift
        self.right_upper_corner.longitude += longitude_shift

        self.polygon = Polygon()
        self._prepare_insta_polygon()

    def visualize_image(self, show_title=True):
        try:
            if show_title:
                plt.title(self.filename)
            plt.imshow(self.image)
            plt.axis('off')
        except ValueError:
            print('Load image first.')

    def __repr__(self): #TODO add rest of the fields
        try:
            return "Filename " + str(self.filename) + "\n" \
            + "Image resolution " + str(self.resolution) + "\n" \
            + "Right Upper corner Latitude " + str(self.right_upper_corner.latitude) + "\n" \
            + "Right Upper corner Longitude " + str(self.right_upper_corner.longitude) + "\n" \
            + "Right Down corner Latitude  " + str(self.right_down_corner.latitude) + "\n" \
            + "Right Down corner Longitude  " + str(self.right_down_corner.longitude) + "\n" \
            + "Left Upper corner Latitude  " + str(self.left_upper_corner.latitude) + "\n"    \
            + "Left Upper corner Longitude  " + str(self.left_upper_corner.longitude) + "\n"   \
            + "Left Down corner Latitude  " + str(self.left_down_corner.latitude) + "\n"     \
            + "Left Down corner Longitude  " + str(self.left_down_corner.longitude) + "\n" \
            + "Azimuth " + str(self.azimuth)
        except:
            return "Cannot print class representation"
   # Example use of image gps filtration to stitch

class InstaObjectsPhoto(InstaPhoto):
    """ Class holding information like InstaPhoto object but contains detected objects info.
    
    Attributes:
        :filename: [str] name of the image 
        :image: [np.array] image data
        :resolution: [(int, int)] - resolution of image (width, height)
        :center_gps: [GPS] - image center gps coordinates
        :right_upper_corner: [GPS] - image right upper corner gps coordinates
        :right_down_corner: [GPS] - image right down corner gps coordinates
        :left_down_corner: [GPS] - image left dow corner gps coordinates
        :left_upper_corner: [GPS] - image left upper corner gps coordinates
        :azimuth: [float] - image azimuth (angle to north of image direction)
        :image_path: [string] - path to image file 
        :polygon: [shapely.polygon] - shapely polygon object created from gps corners (in cartesian coordinates)
        :objects_data: [OrderedDict] - dict of CropObject objects
    """

    def __init__(self, resolution, alt):

        """ Initialize new InstaObjectsPhoto object
        
        :param resolution: resolution of image as (x, y)
        :type resolution: tuple
        :param alt: altitude of camera, defaults to 100
        :param alt: int, optional
        """
        super().__init__(resolution, alt)
        self.objects_data = collections.OrderedDict()

    def read_data_from_df_row(self, metadata_gps, metadata_objects):
        """Read data from two pandas dataframe rows
        
        :param metadata_gps: image information as [Img_name Center_lat Center_lon Right_up_lat Right_up_lon Right_down_lat Right_down_lon Left_down_lat Left_down_lon Left_up_lat Left_up_lon Azimuth]
        :type metadata: pd.Series
        :param metadata_objects: objects information as [filename, class, xmin, ymin, xmax, ymax, width, height]
        :type metadata: pd.Series
        """
        super().read_data_from_df_row(metadata_gps)
        self._load_objects_from_df_row(metadata_objects)

    def read_data_from_only_objects_df(self, metadata_objects, img_path):
        self._load_objects_from_df_row(metadata_objects)
        self.image_path = img_path

    def get_crops_df(self):
        crop_data = []
        for key, value in self.objects_data.items():
            crop_data.append(value.get_crop_data())

        crop_data_df = pd.DataFrame(crop_data).reset_index(drop=True)

        return crop_data_df


    def convert_IP_to_IOP(self, instaphoto, metadata_objects):
        """Convert InstaPhoto to InstaObjectsPhoto.
        
        :param instaphoto: InstaPhoto object
        :type instaphoto: [InstaPhoto]
        :param metadata_objects: objects information as [filename, class, xmin, ymin, xmax, ymax, width, height]
        :type metadata: pd.Series
        """

        self.filename = instaphoto.filename
        self.center_gps = instaphoto.center_gps
        self.right_upper_corner = instaphoto.right_upper_corner
        self.right_down_corner = instaphoto.right_down_corner
        self.left_down_corner = instaphoto.left_down_corner
        self.left_upper_corner = instaphoto.left_upper_corner
        self.azimuth = instaphoto.azimuth
        self.polygon = instaphoto.polygon
        self.image_path = instaphoto.image_path
        self.image = instaphoto.image

        self._load_objects_from_df_row(metadata_objects)

    def _load_objects_from_df_row(self, metadata_objects):

        calculate_gps = 'latitude' not in metadata_objects.columns or 'longitude' not in metadata_objects.columns 

        for index, row in metadata_objects.iterrows():
            if 'filename' in row.index:
                img_name = row['filename']
            elif 'img_name' in row.index:
                img_name = row['img_name']
            else:
                print('No image name in dataframe!')

            if 'crop_name' in row.index:
                object_ID = row['crop_name']
            else:
                base_filename = os.path.splitext(os.path.basename(img_name))[0]
                object_ID = f'{base_filename}_{index:05}'

            bounding_box = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            object_class = row['class']
            ssd_conf = row['conf']
            orig_image_resolution = [row['width'], row['height']]

            if not calculate_gps:
                longitude = row['longitude']
                latitude = row['latitude']
            else:
                longitude = None
                latitude = None

            curr_object = CropObject(img_name, 
                                    object_ID,
                                    ssd_conf,
                                    bounding_box,
                                    object_class,
                                    orig_image_resolution,
                                    longitude,
                                    latitude)
            
            self.objects_data[object_ID] = curr_object
            
        #self.objects_data = objects
        if calculate_gps:
            self._calculate_objects_gps()

    @property
    def orig_crops(self):
        orig_crops = []
        for crop_id, crop_object in self.objects_data.items():
            orig_crops.append(np.asarray(crop_object.crop_image))
        return orig_crops

    @property
    def rotated_crops(self):
        rotated_crops = []
        for crop_id, crop_object in self.objects_data.items():
            rotated_crops.append(crop_object.rotated_crop_image_instances)
        return rotated_crops

    def _calculate_objects_gps(self):
        """Calculate GPS coordinates for all objects based on original image GPS corners
        
        """

        for key, crop in self.objects_data.items():
            bb_centroids = convert_corners_2_centroids(crop.bounding_box)
            obj_loc_centroid = bb_centroids[:2]
            # obj_loc = calculate_object_gps(self.left_upper_corner, self.right_upper_corner,
            #                                obj_loc_centroid, self.azimuth, self.resolution[0])
            obj_loc = calculate_object_gps_center_reference(self.left_upper_corner, self.right_upper_corner, self.left_down_corner, self.center_gps, obj_loc_centroid, self.azimuth, self.resolution[0], self.resolution[1])
            crop.set_gps_loc(obj_loc.longitude, obj_loc.latitude)

    def save_original_crops(self, save_path):
        """Save detected objects as images with original bounding boxes values 
        
        :param save_path: path to save directory
        :type save_path: str
        """

        crops_list = []
        original_image = Image.open(self.image_path)
        for crop_id, crop_object in self.objects_data.items():
            crop = crop_object.get_original_crop(original_image) 
            crops_list.append(crop)
            crop_path = os.path.join(save_path, crop_id+'.jpg')
            crop.save(crop_path)

    def load_crops(self, output_resolution=(160, 160)):
        """Load crops inside InstaObjectPhoto (single instance of each object).
        """

        original_image = Image.open(self.image_path)
        for crop_object in list(self.objects_data.values()):
            crop_object.load_original_crop(original_image, output_resolution)

    def load_rotated_crops(self):
        """Load rotated instances of crops inside InstaObjectPhoto (multiple instances of each object).
        """
        original_image = Image.open(self.image_path)
        for crop_object in list(self.objects_data.values()):
            crop_object.generate_rotated_crop_image_instances(original_image, scale=2)
    

class CropObject:
    """[summary]
    
        :crop_filename: [str] unique crop ID
        :bounding_box: [list] bounding box as [xmin, ymin, xmin, xmax]
        :crop_class: [int] class of detectd object
        :orig_image_resolution: [list] original image resolution
        :measure: [float] similarity measure between this crop and another crop
        :prediction: [float] output of feature extractor
        :rotated_crop_image_instances: [list] list of rotated instances of crop
        :longitude: [float] longitude of centroid of crop
        :latitude: [float] latitude of centroid of crop
    """

    def __init__(self, img_name, object_ID, ssd_conf, bounding_box,  crop_class, orig_image_resolution, longitude=None, latitude=None):
        """Initialize new CropObject object
        
        :param crop_filename: unique crop ID
        :type crop_filename: str
        :param bounding_box: bounding box as [xmin, ymin, xmin, xmax]
        :type bounding_box: list
        :param crop_class: class of detectd object
        :type crop_class: int
        :param orig_image_resolution: original image resolution
        :type orig_image_resolution: list
        """

        self.img_name = img_name
        self.crop_name = object_ID
        self.ssd_conf = ssd_conf
        self.bounding_box = bounding_box
        self.crop_class = crop_class
        self.orig_image_resolution = orig_image_resolution
        self.measure = 0
        self.prediction = None
        self.rotated_crop_image_instances = []
        self.longitude = longitude
        self.latitude = latitude

    def load_original_crop(self, full_image, output_resolution=(160, 160), resize=True):
        """Load inside object crop image
        
        :param full_image: image as PIL.Image
        :type full_image: PIL.Image
        :param output_resolution: output resolution of crop, defaults to (160, 160)
        :param output_resolution: tuple, optional
        :param resize: wheter resize or not, defaults to True
        :param resize: bool, optional
        """

        self.crop_image = self._load_any_crop(full_image, self.bounding_box)
        if resize:
            self.crop_image = self.crop_image.resize(output_resolution)


    def get_crop_data(self):
        crop_data_dict = {"img_name": self.img_name,
                        "crop_name": self.crop_name,
                        "conf": self.ssd_conf,
                        "class": self.crop_class,
                        "width": self.orig_image_resolution[0],
                        "height": self.orig_image_resolution[1],
                        "xmin":self.bounding_box[0],
                        "xmax":self.bounding_box[2],
                        "ymin":self.bounding_box[1],
                        "ymax":self.bounding_box[3],
                        "latitude":self.latitude,
                        "longitude":self.longitude,
                        "geometry": sha.geometry.Point((self.longitude, self.latitude))
                        }

        return crop_data_dict

    def get_original_crop(self, full_image):
        """ Return crop with original bounding box resolution
        
        :param full_image: full image as PIL.Image
        :type full_image: PIL.Image
        :return: crop image as PIL.Image
        :rtype: PIL.Image
        """

        crop_image = self._load_any_crop(full_image, self.bounding_box)
        return crop_image

    def _load_any_crop(self, full_image, bounding_box):
        '''[summary]

        :param full_image: Original full size image, must be PIL.Image object
        :type full_image: PIL.Image
        '''
        crop_image = full_image.crop(bounding_box)
        return crop_image    

    def _get_extended_bounding_box(self, scale):
        """Prepare and return bounding box values for safely rotating crops
        
        :param scale: parameter describes area from which crop rotated crop
        :type scale: int
        :return: new extended bounding box values
        :rtype: list
        """

        bounding_box_extended = safely_extend_bb(self.bounding_box, self.orig_image_resolution, scale)
        return bounding_box_extended

    def set_distance(self, distance):
        self.distance = distance

    def set_measure(self, measure):
        self.measure = measure
        
    def set_prediction(self, prediction):
        self.prediction = prediction

    def set_gps_loc(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    def generate_rotated_crop_image_instances(self, original_image, scale=2, output_resolution=(160, 160)):
        """Generate rotated crop instances
        
        :param original_image: Original full size image, must be PIL.Image object
        :type original_image: PIL.Image
        :param scale: parameter describes area from which crop rotated crop, defaults to 2
        :param scale: int, optional
        :param output_resolution: output resolution of crop, defaults to (160, 160)
        :param output_resolution: tuple, optional
        """

        bounding_box_extended = self._get_extended_bounding_box(scale)
        big_crop = self._load_any_crop(original_image, bounding_box_extended)
        big_crop_resolution = (scale*output_resolution[0], scale*output_resolution[1])
        # big_crop = big_crop.resize(big_crop_resolution)
        
        new_bb = [big_crop_resolution[0]//4, 
                    big_crop_resolution[1]//4, 
                    big_crop_resolution[0]//4+output_resolution[0], 
                    big_crop_resolution[1]//4+output_resolution[1]]

        rotated_crop_image_instances = []
        
        for angle in range(0, 360, 30):
            big_crop = big_crop.rotate(angle)
            big_crop_resized = big_crop.resize(big_crop_resolution)   
            big_crop_cropped = big_crop_resized.crop(new_bb)
            big_crop_resized = big_crop_cropped.resize(output_resolution)   
            rotated_crop_image_instances.append(np.asarray(big_crop_resized))
        
        self.rotated_crop_image_instances = rotated_crop_image_instances
        self.rotations_number = len(rotated_crop_image_instances)
        
    def destroy_rotated_crop_image_instances(self):
        self.rotated_crop_image_instances = []

    def __lt__(self, other):    
        return self.distance < other.distance

class GPSImagesContainer():
    """Class responsible for managing collection of InstaPhoto objects.

    Attributes:
        :images_data: [collections.OrderedDict()] - ordered dict of insta photo objects
        :filtered_area_data: [collections.OrderedDict()] - ordered dict of insta photo objeccts after area gps filtration
        :filtered_point_data: [collections.OrderedDict()] - orddered dict of insta photo objects after points gps filtration  

    :Example:

        insta_photos = GPS_module.GPSImagesContainer(gps_path_100, resolution.width, resolution.height)

        insta_photos.load_images_path(path_to_folder_with_images)  (optional)

    Filtration methods:
    
        1. Polygon area
            :Example:

            gps_points = [GPS_module.GPS(54.388009, 18.687562), GPS_module.GPS(54.387480, 18.689352), GPS_module.GPS(54.386098, 18.686113), GPS_module.GPS(54.385736, 18.688291)]

            res = insta_photos.filter_images_in_area_of_interest(gps_points, 0.5)

        2. Points in range (get images in range from list of points)
            :Example:

            gps_points = [GPS_module.GPS(54.388009, 18.687562), GPS_module.GPS(54.387480, 18.689352)]

            result = insta_photos.get_neighbours_group_distant_from_points(gps_points, 25)

    """

    # __slots__ = ("images_data", "filtered_area_data", "filtered_point_data")

    def __init__(self):

        self.images_data = collections.OrderedDict()

    def read_objects_image_data_with_gps_from_csv(self, gps_corners_txt, objects_csv, image_width, image_height):
        """Read gps image data and objects data from prepaired files. 
        GPS Corners file is generated with GPS_extract_corners module.
        Objects file is received from Object Detection Model.
        New records saved as OrderedDict.
        
        :param gps_corners_txt: path to file with gps corners
        :type gps_corners_txt: [type]
        :param objects_csv: [description]
        :type objects_csv: path to file with objects data
        :param image_width: image width
        :type image_width: int
        :param image_height: image height
        :type image_height: int
        """

        insta_objects_photos = collections.OrderedDict()
        gps_df = pd.read_csv(gps_corners_txt, delimiter=' ')
        gps_df.set_index('Img_name', drop=False, inplace=True)

        objects_df = pd.read_csv(objects_csv)

        unique_photos_ids = np.unique(objects_df['filename'])

        for unique_photo_id in unique_photos_ids:
            
            base_photo_id = os.path.basename(unique_photo_id)

            try:
                gps_row = gps_df.loc[base_photo_id]#[gps_df['Img_name'] == base_photo_id]
            except:
                print(f'No photo with ID: {base_photo_id}')

            some_id_df = objects_df[objects_df['filename'] == unique_photo_id]

            curr_object = InstaObjectsPhoto((image_width, image_height), 100)
            curr_object.read_data_from_df_row(gps_row, some_id_df)

            insta_objects_photos[base_photo_id] = curr_object
            
        self.images_data = insta_objects_photos

    def read_GPSimage_data_from_csv(self, gps_corners_txt, image_width, image_height):
        """ Read gps image data from prepaired file. File is generated with GPS_extract_corners module.
        
        :param gps_corners_txt: path to file
        :type gps_corners_txt: string
        :param image_width: image width
        :type image_width: int
        :param image_height: image height
        :type image_height: int
        :return: dict with InstaPhoto objects. Image names as keys
        :rtype: dict of InstaPhoto objects 
        """

        insta_photos = collections.OrderedDict()
        gps_df = pd.read_csv(gps_corners_txt, delimiter=' ')

        for index, row in gps_df.iterrows():

            curr_insta = InstaPhoto((image_width, image_height))
            curr_insta.read_data_from_df_row(row)
            insta_photos[row["Img_name"]] = curr_insta
            
        self.images_data = insta_photos

    def read_GPSimage_data_from_geojson(self, geojson_path, image_width, image_height):
        
        insta_photos = collections.OrderedDict()

        # with open(geojson_path, 'r') as f:
        #     corners_data = json.load(f)
        
        for img_name, geojson_gdf in corners_data.items():
            # some_gdf = gpd.GeoDataFrame.from_features(geojson_gdf)
            curr_insta = InstaPhoto([image_width, image_height])
            curr_insta.read_data_from_geoJSON(img_name, geojson_path)
            insta_photos[img_name] = curr_insta

        self.images_data = insta_photos

#region Method  operating on GPSImagemManager objects dict

    def load_images_path(self, path_to_images_folder):
        """Load images path to GPS_image_manager_dict 
        
        :param path_to_images_folder: path to folder with images
        :type path_to_images_folder: string
        """

        for image in list(self.images_data.values()):
            image.image_path = os.path.join(path_to_images_folder, image.filename)        

    def get_image_data(self, image_name):
        return self.images_data[image_name]

class ObjectsImageManager():
    """Class responsible for managing images from single flight.
    Hold data as GPSImagesContainer and can manipulate a whole bunch of images in one time.
    
    Attributes:
        :data: [GPSImagesContainer] container with images data contains objects info
    """

    def __init__(self):
        self.data = GPSImagesContainer()

    def read_from_csv(self, corners_gps_txt_path, objects_csv_path, image_width, image_height):
        self.data.read_objects_image_data_with_gps_from_csv(corners_gps_txt_path, objects_csv_path, image_width, image_height)

    def load_crops(self, images_folder_path, output_resolution):
        """Load crops to all crop instances.
        
        :param images_folder_path: path to folder with original images of the flight
        :type images_folder_path: str
        :param output_resolution: output resolution of crop
        :type output_resolution: list
        """

        self.data.load_images_path(images_folder_path)
        for image in list(self.data.images_data.values()):
            original_image = Image.open(image.image_path)
            for crop_object in list(image.objects_data.values()):
                crop_object.load_original_crop(original_image, output_resolution)

    def get_all_crops(self, output_resolution=None):
        """Get all crops from flight.
        
        :param output_resolution: output resolution of crop, defaults to None
        :type output_resolution: list, optional
        :return: array of all crops
        :rtype: np.array
        """

        crops_array = []
        for key in list(self.data.images_data.keys()):
            crops = self.get_single_image_crops(key, output_resolution)
            crops_array.extend(crops)
        return np.array(crops_array)

    def get_single_image_crops(self, image_id, output_resolution):
        """Get crops from image with particular ID.
        
        :param image_id: unique image ID
        :type image_id: str
        :param output_resolution: output resolution of crop
        :type output_resolution: list, optional
        :return: array of all crops
        :rtype: np.array
        """

        crops_array = []

        image = self.data.images_data[image_id]

        for crop in list(image.objects_data.values()):
            if output_resolution is None:
                crop = np.asarray(crop.crop_image)
            else:
                crop = np.asarray(crop.crop_image.resize(output_resolution))
            crops_array.append(crop)
        return np.array(crops_array)

    def get_single_image_rotated_crops_instances(self, image_id, output_resolution):
        """Get rotated instances of crops from image with particular ID.
        
        :param image_id: unique image ID
        :type image_id: str
        :param output_resolution: output resolution of crop
        :type output_resolution: list, optional
        :return: array of all crops
        :rtype: np.array
        """

        crops_array = np.empty((0, output_resolution[1], output_resolution[0], 3))

        image = self.data.images_data[image_id]
        original_image = Image.open(image.image_path)

        for crop in tqdm(list(image.objects_data.values())):
            crop.generate_rotated_crop_image_instances(original_image, 2)
            crops_batch = np.asarray(crop.rotated_crop_image_instances)
            crop.destroy_rotated_crop_image_instances
            crops_array = np.concatenate([crops_array, crops_batch])
        return crops_array


#### TODO CHANGE NAME OF THIS CLASS 
class GPSImageManagerFiltration():
    """Class responsible for managing images from a flight.
    Provides methods for filtration images based on GPS coordinates and returning only these overlapping particular region.
    
    :return: [description]
    :rtype: [type]
    """


    def __init__(self):

        self.data = GPSImagesContainer()
        self.filtered_area_data = collections.OrderedDict()
        self.filtered_point_data = collections.OrderedDict()

    def read_from_csv(self, gps_corners_path, image_width, image_height):
        self.data.read_GPSimage_data_from_csv(gps_corners_path, image_width, image_height) 

    def read_from_geojson(self, geojson_path, image_width, image_height):
        self.data.read_GPSimage_data_from_geojson(geojson_path, image_width, image_height) 

    def load_images_path(self, images_folder_path):
        self.data.load_images_path(images_folder_path)

    def get_filtered_area_data(self):
        return self.filtered_area_data

    def get_filtered_point_data(self):
        return self.filtered_point_data

    def get_images_polygons(self):
        """Get gps polygon list from every image in images_data
        
        :return: list of images shapely polygons
        :rtype: [shapely.Polygon]
        """

        polygon_list = []
        for key, value in self.data.images_data.items():
            polygon_list.append(value.get_polygon())

        return polygon_list

    def get_images_filtered_area_polygons(self):
        """Get gps polygon list from every image in filtered_area_data
        
        :return: list of images shapely polygons
        :rtype: [shapely.Polygon]
        """
        polygon_list = []
        for key, value in self.filtered_area_data.items():
            polygon_list.append(value.get_polygon())

        return polygon_list

    def get_filtered_image_data(self, image_name):
        return self.filtered_area_data[image_name]

    def get_image_data(self, image_name):
        return self.data.images_data[image_name]
                
    def _get_neighbour_by_distance_from_point(self, gps_point, distance_threshold):
        """Get list path to images distant from given gps_point less than threshold
        
        :param gps_point: lat and lon of GPS point
        :type gps_point: GPS class
        :param distance_threshold:
        :type distance_threshold:
        :return: oredered dicts of Insta Photo objects
        :rtype: OrderedDict

        """
        out_neighbour_collection = []
        out_insta_collection = []
        
        for key, image in self.data.images_data.items():
            curr_distance = calculate_distance_points(gps_point, image.center_gps) 
            
            if curr_distance < distance_threshold:
                out_neighbour_collection.append(image.image_path) #TODO change to IMAGE PATH
                out_insta_collection.append(image)
                
        return out_neighbour_collection, out_insta_collection

    def get_neighbours_group_distant_from_points(self, gps_points, distance_threshold):
        """Divide whole flight by given gps points. Used to divide image by distance to stitch.
        
        :param gps_points: list of gps points to find neighbours to 
        :type gps_points: list of GPS objects
        :param distance_threshold: 
        :type distance_threshold: 
        :return: touple of gps points and assigned image filenames
        :rtype: [(GPS point, [string])]

        """
        out_group_neighbours = []
        out_group_insta_collection = []

        for point in gps_points:
            one_point_neighbours, one_point_insta_neighbours = self._get_neighbour_by_distance_from_point(point, distance_threshold)
            out_group_neighbours.append((point, one_point_neighbours))
            out_group_insta_collection.append((point, one_point_insta_neighbours))

        self.filtered_point_data = out_group_insta_collection
        
        return out_group_neighbours

    def shift_flight_gps(self, latitude_shift, longitude_shift):
        """Shift gps points by given amount to correct data
        
        :param latitude_shift: latitude shift
        :type latitude_shift: float
        :param longitude_shift: longitude shifr
        :type longitude_shift: float
        """
        for key, insta_image in self.data.images_data.items():
            insta_image.shift_gps(latitude_shift, longitude_shift)


    def find_photos_contain_point(self, geo_point):
        """Get all insta_images containing given gps coordinates
        
        :param geo_point: latitude and longitude of point
        :type geo_point: (float, float)
        :return: dict with insta_photos containing point with image_name as key
        :rtype: {string: InstaPhoto}
        """
        gps_point = GPS_extended(geo_point[0],geo_point[1])
        insta_images_with_point = {}

        for key, insta_image in self.data.images_data.items():
            insta_polygon = insta_image.get_polygon()
            if insta_polygon.contains(gps_point.shapely_point):
                insta_images_with_point[key] = insta_image

        return insta_images_with_point
        

    def filter_images_in_area_of_interest(self, gps_area_points, overlap_acceptance_threshold):
        """Get all images in given gps area with overlapp above acceptance threshold (used to chose images to stitch)
        
        :param gps_area_points: vertex of the region of interest in GPS coordinates
        :type gps_area_points: list of GPS objects
        :param overlapp_acceptance_threshold: overlap threshold above which image will be taked into consideration
        :type overlapp_acceptance_threshold: float
        :param distance_threshold: list of GPS class objects
        :type distance_threshold: class GPS list

        """
        if overlap_acceptance_threshold <= 0 or overlap_acceptance_threshold > 1 :
            print("Invalid threshold value. Try values in range 0-1.0 ")
            return
        
        interest_area_polygon = create_polygon_from_gps_points(gps_area_points)
        
        out_group_neighbours = collections.OrderedDict()

        for key, insta_image in self.data.images_data.items():
            #calculate intersection area
            if interest_area_polygon.intersects(insta_image.polygon):
                intersection_polygon = interest_area_polygon.intersection(insta_image.polygon)
            
                if intersection_polygon.area / insta_image.polygon.area >= overlap_acceptance_threshold:
                    out_group_neighbours[key] = insta_image
        self.filtered_area_data = out_group_neighbours

        return self.get_filtered_images_path(), out_group_neighbours


    def get_filtered_images_area(self):
        """Calculate filtered images to stitch area
        
        :return: Approximate stitch area 
        :rtype: float
        """
        stitch = self.prepare_filterd_stitch_polygon()
        return stitch.area


    def prepare_filterd_stitch_polygon(self):
        """Prepare filtered images stitch
        
        :return: Approximate stitch area 
        :rtype: float
        """
        image_polygons = []
        for key, insta_image in self.filtered_area_data.items():
            image_polygons.append(insta_image.polygon)
        return cascaded_union(image_polygons)     

    def create_polygon_from_images(self, filtered_insta_images):
        """Prepare stitch polygon from given insta photo objects ordered collection
        
        :param filtered_insta_images: [description]
        :type filtered_insta_images: [type]
        :return: [description]
        :rtype: [type]
        """

        image_polygons = []
        for key, insta_image in filtered_insta_images.items():
            image_polygons.append(insta_image.polygon)
        return cascaded_union(image_polygons)   

    def copy_filtered_area_images(self, destination_folder):
        """Copy filtered area images to destination folder
        
        :param destination_folder: path to destination folder
        :type destination_folder: string
        """

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        images_path = self.get_filtered_images_path()
        for path in images_path:
            image_path =  os.path.abspath(path)
            output_path =  os.path.join(os.path.abspath(destination_folder), os.path.basename(path))
            copyfile(image_path, output_path)


    def filter_flight_based_on_distance(self, start_image_index, end_image_index, distance_gap, distance_threshold):
        """Utilize flight split into points and finding images with certain distance from gps point to filter
        flight
        
        :param start_image: Index of image served as starting point to flight division
        :type start_image: int
        :param end_image: Index of image served as end point to flight division 
        :type end_image: int
        :param distance_gap: distance gap between consecutive gps points [ in meters]
        :type distance_gap: float
        :param distance_threshold: distance threshold from certain gps point deretminging which image from flight is assigned to given gps point
        :type distance_threshold: float
        :return: list of touples of gps points and assigned image filenames
        :rtype: [[(GPS class, [string])]
        """
        #cast list
        data_buffor = list(self.data.images_data.items())

        start_gps = data_buffor[start_image_index][1].center_gps
        end_gps = data_buffor[end_image_index][1].center_gps

        gps_points = divide_flight(start_gps, end_gps, distance_gap)
        out_group_neighbours = self.get_neighbours_group_distant_from_points(gps_points, distance_threshold)

        return out_group_neighbours

    def get_filtered_images_path(self):
        """ return images path afrer filtration
        
        :return: loaded images path
        :rtype: list of strings
        """

        images_path = []
        for key, image in self.filtered_area_data.items():
            images_path.append(os.path.abspath(image.image_path))
        return images_path

    def validate_stitch_size(self, stitch_area_threshold):
        """[summary]
        
        :param stitch_area_threshold: [description]
        :type stitch_area_threshold: [type]
        :return: [description]
        :rtype: [type]
        """

        stitch = self.prepare_filterd_stitch_polygon()   
        if stitch.area <= stitch_area_threshold:
            return True
        else:
            return False

    def filter_images_to_stitch_and_validate(self, filtered_area_gps ,stitch_area_threshold, overlap_acceptance_threshold, reduce_size_factor = 0.1, force_bigger_stitch = False, output_path =" ", filename="images_list"):
        """Filter images before stitching based on gps given area, additionaly use area threshold to restrict stitch size in meters
        
        :param filtered_area_gps: vertex of the region of interest in GPS coordinates
        :type filtered_area_gps: list of GPS objects
        :param stitch_area_threshold: Threshold of stitch area
        :type stitch_area_threshold: float
        :param overlap_acceptance_threshold: overlap threshold above which image will be taked into consideration
        :type overlap_acceptance_threshold: float
        :param reduce_size_factor: number from 0 to 1
        :type reduce_size_factor: float      
        :param force_bigger_stitch: Turn off area stitch restriction, defaults to False
        :param force_bigger_stitch: bool, optional
        :return: [description]
        :rtype: [type]
        """
        if reduce_size_factor < 0 or reduce_size_factor > 1:
            raise ValueError("Reduce size factor must be in <0,1>")

        if output_path == " ":
            output_path = os.getcwd() 

        # Create shapely polygon from gps points
        filtered_area_gps_polygon = create_polygon_from_gps_points(filtered_area_gps) 

        # Transform gps to polygon - scale it by affine transform by say 10% and return GPS and check repeat
        if not force_bigger_stitch:
            while filtered_area_gps_polygon.area > stitch_area_threshold:
                print("Area too big. Reducing size by {}% ".format(reduce_size_factor *100))
                filtered_area_gps_polygon = affinity.scale(filtered_area_gps_polygon, xfact=1.0 - reduce_size_factor, yfact=1.0 - reduce_size_factor, origin="center")
            
        scaled_area_gps_polygon_loc = locate_polygon_vertex_in_world(filtered_area_gps_polygon)
        _ , filtered_insta_images = self.filter_images_in_area_of_interest(scaled_area_gps_polygon_loc, overlap_acceptance_threshold)

        final_paths = []  
        for key, image in filtered_insta_images.items():
            final_paths.append(os.path.abspath(image.image_path))


        if not final_paths:
            raise ValueError("Stitch area threshold too small. Change it and try again.")

        self._save_to_file(final_paths, output_path, filename)

        print("Final images count {}".format(len(final_paths)))
        return final_paths 



    def _save_to_file(self, images_list, output_path, filename):
        '''Save string list to file
        
        :param images_list: [description]
        :type images_list: [type]
        :param output_path: [description]
        :type output_path: [type]
        :param filename: [description]
        :type filename: [type]
        '''

        with open(os.path.join(output_path, filename) + ".txt", 'w') as f:
            for path in images_list:
                f.write("{}\n".format(path))
