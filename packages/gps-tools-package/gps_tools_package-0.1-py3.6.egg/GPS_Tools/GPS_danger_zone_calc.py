from shapely.geometry import Polygon, mapping
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import json
import pdb
from GPS_Tools.loc_calculations import (calculate_azimuth, calculate_azimuth_points,
                              calculate_distance, calculate_distance_points,
                              calculate_pix_meter_coef, calculate_pix_meter_coef_points,
                              calculate_point_geographic_coordinates,
                              calculate_side_point_azimuth, calculate_object_gps)

from GPS_Tools.loc_utils import (GPS, GPS_extended, deg_to_radians, get_photos_names_from_dir,
                       radians_to_deg, transform_to_cartesian,
                       transform_to_gps, visualize_image_group, create_polygon_from_gps_points)
import geojson

class Piping():
    """Class responsible for piping and global danger zone generation based on gps positions. Class offers functionality to
    find common area between danger zone and images polygon.
    
    """
    def __init__(self):
        self.piping_raw_gps_points = {}
        self.azimuths = []
        self.geojson_danger_zone = None
        self.global_piping_polygon = Polygon()
    
    def read_piping_data(self, file_path, delimeter = " "):

        """Read piping data from prepared file (csv or geojson) depending on extention
        :param file_path: path to txt with list of points with header as [Name Latitude Longitude] or geojson
        :type file_path: str
        :param delimeter: data delimeter, default to " "
        :param delimeter: str, optional
        """
        _ , file_extension = os.path.splitext(file_path)

        # ?HARD CODED DATA TYPE MAY BE CHANGED LATER HOWEVER IT IS EASE TO EXTEND
        if file_extension == '.txt' or file_extension == '.csv':
            self._read_piping_data_from_csv(file_path, delimeter)

        elif file_extension == '.geojson':
            self._read_piping_data_from_geojson(file_path)
            
        else:
            print("Data type not valid. Load proper data file")
            return 

    def _read_piping_data_from_csv(self, file_path, delimeter):
        """Read raw piping (danger zone data) from text file (or csv). Unlike reading from geojson
        this function requires further calculation to create danger zone. Required steps are presented in 
        appropriate factory method below (create_global_piping_polygon())
        
        :param file_path: path to txt with list of points with header as [Name Latitude Longitude]
        :type file_path: string
        :param delimeter: data separator, default to " "
        :type delimeter: string
        """
        pipe_df = pd.read_csv(file_path, delimeter)

        for index, row in pipe_df.iterrows():
                gpsRawData = GPS() 
                img_name = str(row['Name'])
                gpsRawData.latitude = row['Latitude']
                gpsRawData.longitude = row['Longitude']

                self.piping_raw_gps_points[img_name] = gpsRawData

    def _read_piping_data_from_geojson(self, file_path):
        """Read piping (danger zone) polygon information from geojson file. While using this function (that is gejson extention) danger zone is already
        calculated so further operations are not reqiored. Danger zone can already be used for drawing mask on real images.
        
        :param file_path: geojson file
        :type file_path: string
        """
    
        with open(file_path, 'r') as f:
            danger_zone_data = json.load(f)

        self.geojson_danger_zone = danger_zone_data
        
        danger_zone_cart = []
        for danger_zone_point in danger_zone_data["geometry"]["coordinates"][0]:
            gps_raw_point = GPS()
            gps_raw_point.latitude = danger_zone_point[1]
            gps_raw_point.longitude = danger_zone_point[0]
            
            cartesian_point = transform_to_cartesian(gps_raw_point)

            danger_zone_cart.append(cartesian_point)

        self.global_piping_polygon = Polygon(danger_zone_cart)

    def approx_global_polygon(self):
        """Approximate created global piping polygon with convex hull to prevent holes in polygon. May generate excessive
        danger zone, but less errors
        """
        self.global_piping_polygon = self.global_piping_polygon.convex_hull


    def _prepare_danger_polygon(self):
        """Generate danger polygons based on calculated side points ()
        
        """

        left_side, right_side = self.convert_to_cart()

        merged_sides = left_side + right_side[::-1]
        self.global_piping_polygon = Polygon(merged_sides)
 
    
 
    def _calculate_gps_side_points(self, distance):
        """calculate gps points on the left and right of the pipe gps based on azimuth of danger zone points to generate danger zone

        :param distance: distance to side points in meters
        :type distance: float
        """

        self.left_points = []
        self.right_points = []
        # 90 and 270 from current point
        left_absolute_angle = 270
        right_absolute_angle = 90
        for point, azim in zip(list(self.piping_raw_gps_points.values()), self.azimuths):

            right_point = calculate_point_geographic_coordinates(
                calculate_side_point_azimuth(right_absolute_angle, azim),
                point.latitude,
                point.longitude,
                distance
                )
            left_point = calculate_point_geographic_coordinates(
                calculate_side_point_azimuth(left_absolute_angle, azim),
                point.latitude,
                point.longitude,
                distance
                )
            
            self.left_points.append(left_point)
            self.right_points.append(right_point)
            

    def convert_to_cart(self):
        """Convert gps coords to cartesian coordinate system
        """

        cart_left_points = []
        cart_right_points = []
        for left_point, right_point in zip(self.left_points, self.right_points):
            
            cart_left_points.append(transform_to_cartesian(left_point))
            cart_right_points.append(transform_to_cartesian(right_point))
            
        return cart_left_points, cart_right_points
    
    def calculate_azimuth(self):
        """Calculate azimuths of piping consecutvive points
        """
        gps_pipe_points = list(self.piping_raw_gps_points.values())
        for index, items in enumerate(zip(gps_pipe_points, gps_pipe_points[1:])):
            azimuth = calculate_azimuth_points(items[0], items[1])
            self.azimuths.append(azimuth)

        #Treat last point
            if index + 1 == len(gps_pipe_points) - 1:
                self.azimuths.append(azimuth) 

    def get_intersection_area(self, image_polygon):
        """Return intersection polygon between piping and image area polygon
        
        :param piping_polygon: shapely polygon created from piping gps points
        :type piping_polygon: Shapely Polygon
        :param image_polygon: Image polygon created from image corners
        :type image_polygon: Shapely Polygon
        :return: intersection polygon between piping and image area polygon
        :rtype: shapely Polygon
        """

        if self.global_piping_polygon.intersects(image_polygon):
            return self.global_piping_polygon.intersection(image_polygon)
        else:
            return Polygon()
    
    def clean(self):
        del self.global_piping_polygon
        del self.left_points
        del self.right_points
        del self.piping_raw_gps_points


def locate_polygon_vertex_in_world(polygon):
    """Extract xyz cart polygon points and convert to gps vertex
    
    :param polygon: shapely polygon with cartesian coordinates vertex
    :type intersecion_polygon: shapely polygon
    """
    mapped_dict = mapping(polygon)
    polygon_cords = mapped_dict['coordinates']
    gps_cord = []
    for point in polygon_cords[0]:
        gps_cord.append(transform_to_gps(point))
    return gps_cord



def calculate_distances_and_azimuth_to_gps_vertex(insta_image, intersection_gps):
    """Calculate real distance from left gps corner considered as pixel [0,0] to corners of intersection polygon
    
    :param insta_image: Image to draw danger zone on
    :type insta_image: InstaPhoto
    :param intersection_gps: Intersection polygon points in gps coordinates
    :type intersection_gps: list (GPS)
    """

    distances = []
    for point in intersection_gps:
        distances.append((calculate_distance_points(insta_image.left_upper_corner, point), calculate_azimuth_points(insta_image.left_upper_corner, point)))
    return distances


def calculate_danger_zone_pixel_position(insta_image, intersection_gps, distances, img_resolution_width, image_azimuth):
    """Convert GPS of intersection danger to image pixel coordinate system
    
    :param insta_image: image with gps data on which intersection polygon was examined with "locate_polygon_vertex_in_world" method
    :type insta_image: InstaPhoto
    :param intersection_gps: list of intersection polygon gps coords
    :type intersection_gps: list of GPS points
    :param distances: list of distances to intersection gps coords
    :type distances: list of floats
    :param img_resolution_width: width of the image
    :type img_resolution: float
    :param image_azimuth: image azimuth
    :type image_azimuth: float
    """

    pix_met_coef = calculate_pix_meter_coef_points(insta_image.left_upper_corner, insta_image.right_upper_corner, img_resolution_width)

    pixel_pos = []
    for point, distance in zip(intersection_gps, distances):
        real_distance_to_point, azimuth_to_point = distance[0], distance[1]
        angle_to_point =  180  - (azimuth_to_point - image_azimuth)
        point_distance_px = real_distance_to_point * pix_met_coef
        pixel_pos.append((point_distance_px * math.sin(deg_to_radians(angle_to_point)), point_distance_px * math.cos(deg_to_radians(angle_to_point))))

    return pixel_pos
 

def clip_pixel_to_res(danger_zone_pixel_pos, x_resolution, y_resolution):
    """Clip danger zone pixel position to image resolution. Used to avoid drawing outside image
    
    :param danger_zone_pixel_pos: list of pixel posotion of calculated danger zone
    :type danger_zone_pixel_pos: list of tuples
    :param x_resolution: image width
    :type x_resolution: float
    :param y_resolution: image height
    :type y_resolution: float
    """

    danger_zone_pixels = np.array(danger_zone_pixel_pos)

#     danger_zone_pixels = danger_zone_pixels[:,::-1]
    danger_zone_pixels[:,0] = np.clip(danger_zone_pixels[:,0],0, x_resolution)
    danger_zone_pixels[:,1] = np.clip(danger_zone_pixels[:,1],0, y_resolution)
    danger_zone_pixels = np.round(danger_zone_pixels).astype(int)
    
    return danger_zone_pixels

def get_danger_zone_pixel_mask(pixels, img):
    """Generate image shape mask based on pixel danger zone coordinates
    
    :param pixels: pixel positions of polygon vertex 
    :type pixels: list of tuples
    :param img: image 
    :type img: numpy array
    """

    mask = np.zeros_like(img)
    cv2.fillConvexPoly(mask, pixels, (255, 0, 0), 1)
    return mask

def visualize_danger_zone(img, pixel_mask, alpha = 1, beta =0.6):
    """Visualize danger zone on image
    
    :param img: image to draw danger zone one
    :type img: numpy array
    :param pixel_mask: pixel mask with shape same as img
    :type pixel_mask: numpy array
    :param alpha: image weight, defaults to 1
    :param alpha: int, optional
    :param beta: danger zone weight, defaults to 0.6
    :param beta: float, optional
    """

    img_trans = cv2.addWeighted(img, alpha, pixel_mask, 0.6, 0)
    plt.imshow(img_trans)
    return img_trans
    
def create_global_piping_polygon(piping_data, danger_zone_dist):
    """Create global piping polygon for given flight data from file. This method is used by gejson parser to create danger zone geojson.
    
    :param piping_data: path to file data csv
    :type piping_data: string
    :param danger_zone_dist: width of the danger zone
    :type danger_zone_dist: float
    """
    piping = Piping()
    piping.read_piping_data(piping_data)
    piping.calculate_azimuth()

    #Calculate danger zone polygon (meters)
    piping._calculate_gps_side_points(danger_zone_dist)
    piping._prepare_danger_polygon()
    
    if piping.global_piping_polygon.is_empty:
        print ("Danger zone global polygon empty!. Area not created !")
        return

    return piping 

def create_global_danger_zone(piping_data_geojson):
    """Create global danger zone from geojson file.

    :param piping_data_geojson: geosjon file with created danger zone polygon
    :type piping_data_geojson: string
    :return: Piping class with prepared global polygon to calculations
    :rtype: Piping class
    """

    danger_zone = Piping()
    danger_zone.read_piping_data(piping_data_geojson)

    return danger_zone

def generate_danger_zone(photo_gps, piping_data, resolution, visualize = False, danger_zone_dist = 10):
    """Generate danger zone based on piping gps data specyfied on file. This function is integral part of Scenario notebook together with
    utils_scenario module.
    
    :param photo_gps: image to detect danger zone on
    :type photo_gps: class insta_photo
    :param piping_data: text file with GPS coordinates of piping
    :type piping_data: string
    :param resolution: image resolution
    :type resolution: named_touple
    :param visualize: determine if visualisation is needed, defaults to False
    :param visualize: bool, optional
    :param danger_zone_dist: danger zone radious in meters, defaults to 10
    :param danger_zone_dist: int, optional

    :return pixel mask of danger zone with given image shape
    :return piping polygon (shapely type) in image pixel coordinates

    EXAMPLE USE OF FUNCTION
    pixel_mask, polygon_pixel_mask  = generate_danger_zone(photo_gps, pipe_100, resolution, True, 10)

    """

    #Generate global piping polygon
    piping = create_global_piping_polygon(piping_data, danger_zone_dist)
    
    #WARNING USE CONVEX HULL TO PREVENT HOLES
    piping.approx_global_polygon()
    #piping.global_piping_polygon =  piping.global_piping_polygon.convex_hull
    
    #Calculate intersecion polygon between global piping and image
    inter_sec = piping.get_intersection_area(photo_gps.get_polygon())
 
    if inter_sec.is_empty:
        print("No intersection between given image and piping. Danger zone not generated.")
        sys.exit()

    if visualize:
        
        #visualize intersection in regard to piping polygon
        data = [inter_sec ,photo_gps.get_polygon()]
        visualize_image_group(data, piping.global_piping_polygon)

    #Extract intersection polygon vertex and convert to gps coordinates
    gps_inter = locate_polygon_vertex_in_world(inter_sec)

    #Calculate distances and azimuths to gps intersection corners
    distances = calculate_distances_and_azimuth_to_gps_vertex(photo_gps, gps_inter)

    #Conver gps intersection polygon corners to pixel positions on given image
    danger_zone_pixels = calculate_danger_zone_pixel_position(photo_gps, gps_inter, distances ,resolution.width,photo_gps.azimuth )

    #Clip danger zone pixels to image resolution
    danger_zone_pixels_cliped = clip_pixel_to_res(danger_zone_pixels, resolution.width, resolution.height)

    polygon_mask = Polygon(danger_zone_pixels_cliped)
    #Get danger zone pixel mask
    pixel_mask = get_danger_zone_pixel_mask(danger_zone_pixels_cliped, photo_gps.image)

    if visualize:
        #Visualize danger zone on image
        vis_image = visualize_danger_zone(photo_gps.image, pixel_mask)
        cv2.imwrite(os.path.join(os.curdir, "dagner_zone_vis.jpg"), vis_image)
    
    return pixel_mask, polygon_mask
    

def generate_danger_zone_on_image(photo_gps, global_danger_zone, resolution, visualize = False):
    """Generate danger zone based on piping gps data specyfied on file.
    
    :param photo_gps: image to detect danger zone on
    :type photo_gps: class Insta_photo
    :param piping_data: Piping class object with prepared global danger polygon, obj needs to be created with create_global_danger_zone
    :type piping_data: Piping class
    :param resolution: image resolution
    :type resolution: named_touple
    :param visualize: determine if visualisation is needed, defaults to False
    :param visualize: bool, optional

    :return pixel mask of danger zone with given image shape
    :return piping polygon (shapely type) in image pixel coordinates

    EXAMPLE USE OF FUNCTION
    global_danger_zone = create_global_danger_zone()
    pixel_mask, polygon_pixel_mask  = generate_danger_zone(photo_gps, pipe_100, resolution, True, 10)

    """
    
    #Calculate intersecion polygon between global piping and image
    inter_sec = global_danger_zone.get_intersection_area(photo_gps.get_polygon())
 
    if inter_sec.is_empty:
        print("No intersection between given image and piping. Danger zone not generated.")
        sys.exit()

    if visualize:  
        #visualize intersection in regard to piping polygon
        data = [inter_sec ,photo_gps.get_polygon()]
        visualize_image_group(data, [global_danger_zone.global_piping_polygon])

    #Extract intersection polygon vertex and convert to gps coordinates
    gps_inter = locate_polygon_vertex_in_world(inter_sec)

    #Calculate distances and azimuths to gps intersection corners
    distances = calculate_distances_and_azimuth_to_gps_vertex(photo_gps, gps_inter)

    #Conver gps intersection polygon corners to pixel positions on given image
    danger_zone_pixels = calculate_danger_zone_pixel_position(photo_gps, gps_inter, distances ,resolution.width, photo_gps.azimuth )

    #Clip danger zone pixels to image resolution
    danger_zone_pixels_cliped = clip_pixel_to_res(danger_zone_pixels, resolution.width, resolution.height)

    polygon_mask = Polygon(danger_zone_pixels_cliped)
    #Get danger zone pixel mask
    pixel_mask = get_danger_zone_pixel_mask(danger_zone_pixels_cliped, photo_gps.image)

    if visualize:
        #Visualize danger zone on image
        vis_image = visualize_danger_zone(photo_gps.image, pixel_mask)
        cv2.imwrite(os.path.join(os.curdir, "dagner_zone_vis.jpg"), vis_image)
    
    return pixel_mask, polygon_mask

def draw_danger_zone(img, danger_zone_mask, alpha, beta):
    """Ilustrate examined danger zone on image.

    :param img: Image to draw danger zone on
    :type img: numpy array
    :param danger_zone_mask: [description]
    :type danger_zone_mask: numpy array
    :param alpha: alpha of the image
    :type alpha: int
    :param beta: alpha of danger zone
    :type beta: int
    """
    img_alarm_zoned = img.copy()
    img_alarm_zoned = cv2.addWeighted(img_alarm_zoned, alpha, danger_zone_mask, beta, 0)
    plt.figure()
    plt.axis('off')
    plt.imshow(img_alarm_zoned)
