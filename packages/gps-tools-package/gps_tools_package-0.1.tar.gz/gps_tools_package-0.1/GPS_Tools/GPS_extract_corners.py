import math
import os
import pdb
from enum import Enum

import cv2
import pandas as pd
from geojson import Feature, FeatureCollection, Point, Polygon, dump

from GISS_Tools.GPS_parser.GPS_parser import read_exif_xmp_metadata
from GPS_Tools.loc_calculations import (calculate_azimuth_points,
                                        calculate_point_geographic_coordinates)
from GPS_Tools.loc_utils import (GPS, deg_to_radians,
                                 get_photos_names_from_dir, radians_to_deg)

#HELPER ELEMENTS
#region

class DroneCoordinateSystemQuadrant(Enum):
    """Enum defining on which quadrant in regard to drone movement direction (azimuth), center image point is placed
    """
    INVALID_STATUS = 1
    I_QUADRANT = 2
    II_QADRANT = 3
    III_QUADRANT = 4
    IV_QUADRANT = 5
    CENTER = 6
    ROLL_AXIS_NEGATIVE = 7   # //270 do kierunku ruchu //pitch = 0 roll > 0
    ROLL_AXIS_POSITIVE = 8   # //90 do kierunku ruchu drona // pitch = 0 roll < 0
    PITCH_AXIS_NEGATIVE = 9 #// w przeciwnym kierunku do ruchu 180 // pitch < 0 roll = 0
    PITCH_AXIS_POSITIVE = 10 #// zgodnie z kierunkiem ruchu drona 0 // pitch > 0 roll =0;


def check_coordinate_system_quadrant(pitchDeg, rollDeg):
    """Determine coordinates system quadrant of point based on rotation angles of the drone
    
    :param pitchDeg: raw pitch angle of the drone in order to zero position  
    :type pitchDeg: float
    :param rollDeg: raw roll angle of the drone
    :type rollDeg: float
    :return: Enum determinig coordinate system quadrang
    :rtype: class DroneCoordinateSystemQuadrant
    """

    if pitchDeg > 0 and rollDeg < 0:        #I quadrant
	    return DroneCoordinateSystemQuadrant.I_QUADRANT
	
    elif pitchDeg > 0 and rollDeg > 0:    #II quadrant
	    return DroneCoordinateSystemQuadrant.II_QADRANT
	
    elif pitchDeg < 0 and rollDeg > 0: #III quadrant
	    return DroneCoordinateSystemQuadrant.III_QUADRANT
	
    elif pitchDeg < 0 and rollDeg < 0: #IV quadrant
	    return DroneCoordinateSystemQuadrant.IV_QUADRANT

    if pitchDeg == 0 and rollDeg > 0: # roll negative
	    return DroneCoordinateSystemQuadrant.ROLL_AXIS_NEGATIVE
	
    elif pitchDeg == 0 and rollDeg < 0:    #roll positive 
	    return DroneCoordinateSystemQuadrant.ROLL_AXIS_POSITIVE
	
    elif pitchDeg > 0 and rollDeg == 0: # pitch axis in front of drone
        return DroneCoordinateSystemQuadrant.PITCH_AXIS_POSITIVE
	
    elif pitchDeg < 0 and rollDeg == 0: # pitch axis form behind drone
	    return DroneCoordinateSystemQuadrant.PITCH_AXIS_NEGATIVE
	#f both angles are 0
    return DroneCoordinateSystemQuadrant.CENTER

#endregion
class RotationDataHolder():
    """Class for holding rotation and azimuth
    """
    
    # __slots__ = ('pitch',
    #             'yaw',
    #             'roll',
    #             'azimuth')
        
    def __init__(self, pit = 0, yaw= 0, roll = 0, azi = 0):
        self.pitch = pit
        self.yaw = yaw
        self.roll = roll
        self.azimuth = azi
        
    def assign_rotation(self, pit, yaw, roll):
        self.pitch = pit
        self.yaw = yaw
        self.roll = roll
        
    def assign_azimuth(self, azimuth):
        self.azimuth = azimuth
        
    def __repr__(self):
        return "GPS: " + str(self.pitch) + " pitch " + str(self.yaw) + " yaw "+ str(self.roll) + " roll" + str(self.azimuth) + " azimuth"

class GPSCornersHolder():
    """Class holding GPS corners
    """
    # __slots__ = ('right_up',
    #              'right_down',
    #              'left_up',
    #              'left_down',
    #              'polygon_corners'
    #             )
    
    def __init__(self, polygon_corners =[]):
        self.right_up = GPS()
        self.right_down =  GPS()
        self.left_up =  GPS()
        self.left_down =  GPS()   
        self.polygon_corners = polygon_corners        

    def assign_corners(self, ru, rd, ld, lu):
        self.right_up = ru
        self.right_down =  rd
        self.left_up =  lu
        self.left_down =  ld  


"""Base flight parameters"""
RZ = 6371008.8

class CameraParams:
    """Static class holding information about camera durring flight
    """
    #Default parameters
    sensorWidth = 12.8
    sensorHeight = 9.6
    focalLength = 8.8
    xResolution = 4864
    yResolution = 3648
#12.8,9.6,8.8,4864,3648 maj

def set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution):
    """Set global flight parameters
    
    :param sensorWidth: physical width of the sensor in [mm]
    :type sensorWidth: float
    :param sensorHeight: physical height of the sensor in [mm]
    :type sensorHeight: float
    :param focalLength: focal length in [mm]
    :type focalLength: float
    :param xResolution: image resolution width
    :type xResolution: int
    :param yResolution: [description]
    :type yResolution: [type]
    """

    CameraParams.sensorWidth = sensorWidth
    CameraParams.sensorHeight = sensorHeight
    CameraParams.focalLength = focalLength
    CameraParams.xResolution = xResolution
    CameraParams.yResolution = yResolution


def calculate_field_of_view(sensor_width, sensor_height, focal_length):
    """Calculate field of view for given camera

    :param sensor_width: physical width of the sensor in [mm]
    :type sensor_width: float
    :param sensor_height: physical height of the sensor in [mm]
    :type sensor_height: float
    :param focal_length: focal length in [mm]
    :type focal_length: float
    :return: horizontal and vertical field of view
    :rtype: float, float
    """
    
    horiz_field = sensor_width / (2 * focal_length)
    horizontal_FOV = 2 * math.atan(horiz_field)
    
    vertic_field = sensor_height / (2*focal_length)
    vertical_FOV = 2 * math.atan(vertic_field) 
    
    return horizontal_FOV, vertical_FOV


class GPSDataManager(RotationDataHolder):
    """Class holding gps whole information for one image
    
    :param RotationDataHolder: class holding data rotation
    """
    
    # __slots__ =('image_name',
    #         'gps',
    #         'gps_corrners')
    
    def __init__ (self, image_name = " "):
        self.image_name = " "
        self.flight_name = " "
        self.gps = GPS()
        self.gps_corected = GPS()
        self.gps_corrners = GPSCornersHolder()
        #self.rotation = Rotation()
        
   
    def calculate_image_center_with_rotation_correction(self, azimuth):
        """Correct image center gps position based on rotation data
        
        :param azimuth: image azimuth
        :type azimuth: float
        :return: return GPSCornersHolder with new image center position
        :rtype: GPSCornersHolder
        """

        #Calculate distance on ground between image center point and drone position
        image_center_distance = self._calculate_image_center_real_distance()

        #Calculate image center point displacement azimuth
        image_center_point_azimuth = self._calculate_image_center_azimuth_change(azimuth)

        #Calculate gepgraphic coordinates of the image center point displacement
        result_point = calculate_point_geographic_coordinates(image_center_point_azimuth, self.gps.latitude, self.gps.longitude, image_center_distance)
        if(result_point):
            self.gps_corected = result_point
        else:
            print("Wrong new point calculation in calculate_point_geo_coordinates")

        return self

    def _calculate_image_center_real_distance(self):
        """Calculate absolute distance from given image gps center to true image center base on drone rotation from angle 0 position
        
        :return: absolute distance
        :rtype: float 
        """

        pitch_distance = abs(math.tan(deg_to_radians(self.pitch))) * self.gps.altitude
        roll_distance = abs(math.tan(deg_to_radians(self.roll))) * self.gps.altitude

        absolute_distance = math.sqrt(pitch_distance**2 + roll_distance**2)

        return absolute_distance

    def _calculate_image_center_azimuth_change(self, drone_azimuth):
        """Calculate azimuth of the corrected image gps point in regard to old point (given in data)

        :param drone_azimuth: global azimuth of the image
        :type drone_azimuth: float
        :return: azimuth from gps point in given data to corected point
        :rtype: float

        """
        pitch_distance = abs(math.tan(deg_to_radians(self.pitch))) * self.gps.altitude
        roll_distance = abs(math.tan(deg_to_radians(self.roll))) * self.gps.altitude

        # angle of displacement direction in regard of drone movement direction
        angle_absolute_value = 0

        if pitch_distance != 0:
            angle_absolute_value = radians_to_deg(math.atan(roll_distance/pitch_distance))

        # determine absolute angle value
        status = check_coordinate_system_quadrant(self.pitch, self.roll)

        image_center_from_drone_direction_angle = 0.0

        #Check in which coordinate system quadrand corrected point was moved in regard to original point
        if status == DroneCoordinateSystemQuadrant.I_QUADRANT:
            image_center_from_drone_direction_angle = angle_absolute_value

        elif status == DroneCoordinateSystemQuadrant.II_QADRANT:
            image_center_from_drone_direction_angle = 360 - angle_absolute_value

        elif status == DroneCoordinateSystemQuadrant.III_QUADRANT:
            image_center_from_drone_direction_angle = 180 + angle_absolute_value

        elif status == DroneCoordinateSystemQuadrant.IV_QUADRANT:
            image_center_from_drone_direction_angle = 180 - angle_absolute_value

        elif status == DroneCoordinateSystemQuadrant.ROLL_AXIS_NEGATIVE:
            image_center_from_drone_direction_angle = 270

        elif status == DroneCoordinateSystemQuadrant.ROLL_AXIS_POSITIVE:
            image_center_from_drone_direction_angle = 90

        elif status == DroneCoordinateSystemQuadrant.PITCH_AXIS_POSITIVE:
            image_center_from_drone_direction_angle = 0

        elif status == DroneCoordinateSystemQuadrant.PITCH_AXIS_NEGATIVE:
            image_center_from_drone_direction_angle = 180

        elif status == DroneCoordinateSystemQuadrant.CENTER:
            image_center_from_drone_direction_angle = 0


        #Determine azimuth of displacement
        image_center_point_azimuth = image_center_from_drone_direction_angle + drone_azimuth
        #normalization to 0-360
        image_center_point_full_angle = math.fmod(image_center_point_azimuth + 360, 360)

        return image_center_point_full_angle

    def calculate_image_corner_coordinates(self):
        """calculate current image corner gps coordinates based on basic gps and camera parameters"""

        horiz, vert = self.calculate_fov_for_height(CameraParams.sensorWidth, CameraParams.sensorHeight, CameraParams.focalLength)
        
        #Calculate  distance from middle to corners based on field of view in meters
        distance_to_corner_x = horiz * 0.5
        distance_to_corner_y = vert * 0.5
        real_distace_to_corner = math.sqrt(distance_to_corner_x**2 + distance_to_corner_y**2)
        
        #Calculate corners angles
        angle_to_right_up_corner = radians_to_deg(math.atan(CameraParams.xResolution / CameraParams.yResolution))
        angle_to_right_downner = 180 - angle_to_right_up_corner
        angle_to_left_downner = 180 + angle_to_right_up_corner
        angle_to_left_up_corner = 360 - angle_to_right_up_corner
        
        self.gps_corrners.right_up = calculate_point_geographic_coordinates(
        self._calculate_corner_azimuth(angle_to_right_up_corner),
        self.gps.latitude,
        self.gps.longitude,
        real_distace_to_corner
        )
        
        self.gps_corrners.right_down = calculate_point_geographic_coordinates(
        self._calculate_corner_azimuth(angle_to_right_downner),
        self.gps.latitude,
        self.gps.longitude,
        real_distace_to_corner
        )
        
        self.gps_corrners.left_down = calculate_point_geographic_coordinates(
        self._calculate_corner_azimuth(angle_to_left_downner),
        self.gps.latitude,
        self.gps.longitude,
        real_distace_to_corner
        )
        
        self.gps_corrners.left_up = calculate_point_geographic_coordinates(
        self._calculate_corner_azimuth(angle_to_left_up_corner),
        self.gps.latitude,
        self.gps.longitude,
        real_distace_to_corner
        )
        
        return self
        
    
    def _calculate_corner_azimuth(self, absolute_angle_to_corner):
        """Calculate azimuth based on real distance in image
        
        :param absolute_angle_to_corner: absolute corner angle. Angle to point which azimuth is kntown
        :type absolute_angle_to_corner: float
        """
        """"""
        #Determine azimuth of the corner based on image (drone) azimuth
        corner_image_azimuth = absolute_angle_to_corner + self.azimuth
        
        #normalize do 0 - 360
        corner_point_azim_full_angle = (corner_image_azimuth + 360) % 360
        
        return corner_point_azim_full_angle
    
    def calculate_fov_for_height(self, sensor_width, sensor_height, focal_length):
        """Calculate vertical an horizontal field of view for given height
        
        :param sensor_width: physical width of the sensor in [mm]
        :type sensor_width: float
        :param sensor_height: physical height of the sensor in [mm]
        :type sensor_height: float
        :param focal_length: focal length in [mm]
        :type focal_length: float
        """

        horizontal_FOV, vertical_FOV =  calculate_field_of_view(sensor_width, sensor_height, focal_length)
        self.horizontalFieldOfView = 2 * (self.gps.altitude * math.tan(horizontal_FOV / 2));
        self.verticalFieldOfView = 2 * (self.gps.altitude  * math.tan(vertical_FOV / 2));
        
        return self.horizontalFieldOfView, self.verticalFieldOfView
        
        
    def __repr__(self):
        return "Image_name: " + str(self.image_name) +"\n" \
        + "Flight_name: " + str(self.flight_name) + "\n" \
        + "General Latitude " + str(self.gps.latitude) + "\n" \
        + "General Longitude " + str(self.gps.longitude) + "\n" \
        + "Height " + str(self.gps.altitude) + "\n" \
        + "Pitch " + str(self.pitch) + "\n" \
        + "Yaw " + str(self.yaw) + "\n" \
        + "Roll " + str(self.roll) + "\n" \
        + "Azimuth " + str(self.azimuth)+ "\n" \
        + "Right Upper Corr Latitude " + str(self.gps_corrners.right_up.latitude) + "\n" \
        + "Right Upper Corr Longitude " + str(self.gps_corrners.right_up.longitude) + "\n" \
        + "Right Down Corr Latitude  " + str(self.gps_corrners.right_down.latitude) + "\n" \
        + "Right Down Corr Longitude  " + str(self.gps_corrners.right_down.longitude) + "\n" \
        + "Left Upper Corr Latitude  " + str(self.gps_corrners.left_up.latitude) + "\n" \
        + "Left Upper Corr Longitude  " + str(self.gps_corrners.left_up.longitude) + "\n" \
        + "Left Down Corr Latitude  " + str(self.gps_corrners.left_down.latitude) + "\n" \
        + "Left Down Corr Longitude  " + str(self.gps_corrners.left_down.longitude) + "\n" 


def read_gps_data_from_file(file_path, delimeter = " "):
    """Read basic GPS data from file with specyfied header
   HEADER: Img_name Latitude Longitude Altitude Pitch Yaw Roll

    :param file_path: path to file with raw gps data
    :type file_path: string
    :param delimeter: data delimeter, defaults to " "
    :param delimeter: str, optional
    """
    
    gps_df = pd.read_csv(file_path, delimeter)
    flight_raw_data = {}
    
    for index, row in gps_df.iterrows():

        gpsRawData = GPSDataManager()
        gpsRawData.image_name = row['Img_name']
        gpsRawData.gps.latitude = row['Latitude']
        gpsRawData.gps.longitude = row['Longitude']
        gpsRawData.gps.altitude = row['Altitude']
        gpsRawData.pitch = row['Pitch']
        gpsRawData.roll = row['Roll']
        gpsRawData.yaw = row['Yaw']

        flight_raw_data[gpsRawData.image_name] = gpsRawData
            
    return flight_raw_data

def read_gps_data_from_xmp_parser(metadata):
    """Read basic GPS data from xmp parser

    :param metadata: list of dicts with combined exif and xmp data
    :type metadata: list
    """
    
    flight_raw_data = {}
    
    for metadata_single in metadata:

        gpsRawData = GPSDataManager()
        gpsRawData.image_name = metadata_single['Img_name']
        gpsRawData.flight_name = metadata_single['Flight_name']
        gpsRawData.gps.latitude = float(metadata_single['Latitude'])
        gpsRawData.gps.longitude = float(metadata_single['Longitude'])
        gpsRawData.gps.altitude = float(metadata_single['Altitude'])
        gpsRawData.pitch = float(metadata_single['Pitch'])
        gpsRawData.roll = float(metadata_single['Roll'])
        gpsRawData.yaw = float(metadata_single['Yaw'])
        gpsRawData.azimuth = float(metadata_single['Yaw'])

        flight_raw_data[gpsRawData.image_name] = gpsRawData

    return flight_raw_data

class FlightGPSManipulator():

    """
    Class responsible for gps corner calculations for dataset. Contains every calculation to calculate corners
    
    """
    slots =('gps_dict')
            
    def __init__ (self, data_dict = {}):
        self.gps_dict = data_dict

    def assign_drone_azimuth(self, calculate_azimuth):
        """Assign calculated or (read from file if exists) drone azimuth
        
        :param calculate_azimuth: bool determining if perform azimuth calculation from consecitive images or read from file
        :type calculate_azimuth: bool
        """
        if calculate_azimuth:
            items_collection = list(self.gps_dict.values())
            item_last_index = len(items_collection) - 1

            for index, items in enumerate(zip(items_collection, items_collection[1:])):
                azimuth = calculate_azimuth_points(items[0].gps, items[1].gps)
                items_collection[index].azimuth = azimuth

                #Treat last point
                if index + 1 == len(items_collection) - 1:
                    items_collection[item_last_index].azimuth = azimuth  

            dict_elem = {}
            for item in items_collection:
                dict_elem[item.image_name] = item        
            self.gps_dict = dict_elem
            
        else: 

            items_collection = list(self.gps_dict.values())
            for index, items in enumerate(items_collection):
                #* assign yaw angle from file as azimuth
                items_collection[index].azimuth = items.yaw
            dict_elem = {}

            for item in items_collection:
                dict_elem[item.image_name] = item 
            self.gps_dict = dict_elem
        
         
    def assign_gps_points_to_image(self):
        try:
            for key, item in self.gps_dict.items():
                self.gps_dict[key] = item.calculate_image_corner_coordinates()
                self.gps_dict[key] = item.calculate_image_center_with_rotation_correction(item.azimuth)
        except:
            print("Error assigning corner gps coordinates to image")

            
    def extract_corner_data(self):
        """Prepare calculated corner points list to save to file

        :return: gps corners list  
        :rtype: list 
        """
        corner_list = []
        for key, item in self.gps_dict.items():
            corner_list.append([key, item.gps.latitude, item.gps.longitude, item.gps_corrners.right_up.latitude, item.gps_corrners.right_up.longitude,
                           item.gps_corrners.right_down.latitude, item.gps_corrners.right_down.longitude,
                           item.gps_corrners.left_down.latitude, item.gps_corrners.left_down.longitude,
                           item.gps_corrners.left_up.latitude, item.gps_corrners.left_up.longitude,
                            item.azimuth, item.gps_corected.latitude, item.gps_corected.longitude])
            
        return corner_list



    def _convert_to_geoJSON(self, path, filename):
        """Convert image corners metadata to geojson format and saves it
        
        :param path: path to save file
        :type path: string
        :param filename: name of the geojson file
        :type filename: string
        :return: geojson file with flight data
        :rtype: dict
        """

        geoJSON = {}

        for key, item in self.gps_dict.items():
            features = []

            center = Point((item.gps.longitude, item.gps.latitude))
            right_up = Point((item.gps_corrners.right_up.longitude, item.gps_corrners.right_up.latitude))
            right_down = Point((item.gps_corrners.right_down.longitude, item.gps_corrners.right_down.latitude))
            left_down = Point((item.gps_corrners.left_down.longitude, item.gps_corrners.left_down.latitude))
            left_up = Point((item.gps_corrners.left_up.longitude, item.gps_corrners.left_up.latitude))
            center_corr = Point((item.gps_corected.longitude, item.gps_corected.latitude))
            #testi
            #features.append(Feature( properties = {"image name": key}))
            features.append(Feature(geometry = center, properties = {"shapely_type": "Center",
                                                                    "Azimuth": item.azimuth}))
            features.append(Feature(geometry = right_up, properties = {"shapely_type": "Right_up"}))
            features.append(Feature(geometry = right_down, properties = {"shapely_type": "Right_down"}))
            features.append(Feature(geometry = left_down, properties = {"shapely_type": "Left_down"}))
            features.append(Feature(geometry = left_up, properties = {"shapely_type": "Left_up"}))
            features.append(Feature(geometry = center_corr, properties = {"shapely_type": "Center_corected"}))

            polygon_corners = Polygon([[(item.gps_corrners.right_up.longitude,item.gps_corrners.right_up.latitude),
            (item.gps_corrners.right_down.longitude, item.gps_corrners.right_down.latitude),
            (item.gps_corrners.left_down.longitude, item.gps_corrners.left_down.latitude),
            (item.gps_corrners.left_up.longitude, item.gps_corrners.left_up.latitude),
            (item.gps_corrners.right_up.longitude,item.gps_corrners.right_up.latitude)]])

            features.append((Feature(geometry= polygon_corners, properties={"shapely_type": "Corner_polygon"})))
            #prepare feature collection
            feature_collection = FeatureCollection(features)
            #Assign feature colection to 
            #geoJSON[key] =  feature_collection
            geoJSON[key] =  feature_collection


        with open(os.path.join(path, filename)[:-4] + ".geojson", 'w') as f:
            dump(geoJSON,  f, indent = 4,  sort_keys = True)

        return geoJSON

    def _convert_to_native_geoJSON(self, path, filename, save=True):
        """Convert image corners metadata to geojson format and saves it
        
        :param path: path to save file
        :type path: string
        :param filename: name of the geojson file
        :type filename: string
        :return: geojson file with flight data
        :rtype: FeatureColleciton
        """
        features = []
        for key, item in self.gps_dict.items():
            
            center = Point((item.gps.longitude, item.gps.latitude))
            right_up = Point((item.gps_corrners.right_up.longitude, item.gps_corrners.right_up.latitude))
            right_down = Point((item.gps_corrners.right_down.longitude, item.gps_corrners.right_down.latitude))
            left_down = Point((item.gps_corrners.left_down.longitude, item.gps_corrners.left_down.latitude))
            left_up = Point((item.gps_corrners.left_up.longitude, item.gps_corrners.left_up.latitude))
            center_corr = Point((item.gps_corected.longitude, item.gps_corected.latitude))
            #testi
            #features.append(Feature( properties = {"image name": key}))
            features.append(Feature(geometry = center, properties = {"shapely_type": "Center",
                                                                    "Azimuth": item.azimuth,
                                                                    "Filename": key,
                                                                    "Name": key + "_Center"}))
            features.append(Feature(geometry = right_up, properties = {"shapely_type": "Right_up",
                                                                        "Name": key + "_Right_up"}))
            features.append(Feature(geometry = right_down, properties = {"shapely_type": "Right_down",
                                                                        "Name": key + "_Right_down",}))
            features.append(Feature(geometry = left_down, properties = {"shapely_type": "Left_down",
                                                                        "Name": key + "_Left_down"}))
            features.append(Feature(geometry = left_up, properties = {"shapely_type": "Left_up",
                                                                        "Name": key + "_Left_down"}))
            features.append(Feature(geometry = center_corr, properties = {"shapely_type": "Center_corected",
                                                                            "Name": key + "Center_corected"}))

            polygon_corners = Polygon([[(item.gps_corrners.right_up.longitude,item.gps_corrners.right_up.latitude),
            (item.gps_corrners.right_down.longitude, item.gps_corrners.right_down.latitude),
            (item.gps_corrners.left_down.longitude, item.gps_corrners.left_down.latitude),
            (item.gps_corrners.left_up.longitude, item.gps_corrners.left_up.latitude),
            (item.gps_corrners.right_up.longitude,item.gps_corrners.right_up.latitude)]])

            features.append((Feature(geometry= polygon_corners, properties={"shapely_type": "Corner_polygon",
                                                                            "Name": key + "_Corner_polygon"})))
            #prepare feature collection
           # 
            #Assign feature colection to 
            #geoJSON[key] =  feature_collection
            #geoJSON[key] =  feature_collection


        feature_collection = FeatureCollection(features, properties= {"flight_name": item.flight_name} )


        if save:
            with open(os.path.splitext(os.path.join(path, filename))[0] + ".geojson", 'w') as f:
                dump(feature_collection,  f, indent = 4,  sort_keys = True)

        return feature_collection

        
    def save_corner_metadata(self, path, filename):
        """Save corners metadata to text file
        
        :param path: Save file path
        :type path: string
        :param filename: save filename
        :type filename: string
        :return: corner metadata dataframe
        :rtype: pandas df
        """

        columns_list = ["Img_name", "Center_lat", "Center_lon", "Right_up_lat", "Right_up_lon", "Right_down_lat", "Right_down_lon","Left_down_lat",  "Left_down_lon", "Left_up_lat", "Left_up_lon", "Azimuth", "Center_lat_cor", "Center_lon_cor" ]
        corner_data = self.extract_corner_data()
        corner_df = pd.DataFrame(corner_data, columns=columns_list)
        corner_df.to_csv(os.path.join(path, filename), float_format='%.8f', sep=" ", index = False)
        
        return corner_df


def generate_corners_for_images(gps_base_file, sensorWidth, sensorHeight, focalLength, xResolution, yResolution, calculate_azimuth = True):
    """Generate gps corner files from base gps data
    
    :param gps_base_file: base gps file to process
    :type gps_base_file: string
    :param sensorWidth: sensor width in mm
    :type sensorWidth: float
    :param sensorHeight: sensor height in mm
    :type sensorHeight: float
    :param focalLength: camera focal length in mm
    :type focalLength: type
    :param xResolution: images x resolutions
    :type xResolution: int
    :param yResolution: images y resolution
    :type yResolution: int
    :return: corner gps data frame
    :rtype: pandas dataframe

    Example use:
    generate_corners_for_images("2018-05-08_original_deg0_100m_part1_wiadukt.txt", 12.8, 9.6, 8.8, 4864, 3648)

    """

    #Set default flight parameters
    set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution)

    output_filename = "corners_" + os.path.basename(gps_base_file)
    output_folder = os.path.dirname(gps_base_file)

    #read gps raw data to data structure
    raw_gps = read_gps_data_from_file(gps_base_file)
    gps_coll = FlightGPSManipulator(raw_gps)

    #Calculate azimuth based on consecutive data
    gps_coll.assign_drone_azimuth(calculate_azimuth)

    # Assign gps corners
    gps_coll.assign_gps_points_to_image()

    #Save corners to file
    corners_df = gps_coll.save_corner_metadata(output_folder, output_filename)

    return corners_df

def generate_corners_for_images_GEOJSON(gps_base_file, sensorWidth, sensorHeight, focalLength, xResolution, yResolution, calculate_azimuth = True):
    """Generate gps corner files from base gps data
    
    :param gps_base_file: base gps file to process
    :type gps_base_file: string
    :param sensorWidth: sensor width in mm
    :type sensorWidth: float
    :param sensorHeight: sensor height in mm
    :type sensorHeight: float
    :param focalLength: camera focal length in mm
    :type focalLength: type
    :param xResolution: images x resolutions
    :type xResolution: int
    :param yResolution: images y resolution
    :type yResolution: int
    :return: corner gps data frame
    :rtype: pandas dataframe
    """

    #Set default flight parameters
    set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution)

    output_filename = "corners_" + os.path.basename(gps_base_file)
    output_folder = os.path.dirname(gps_base_file)

    #read gps raw data to data structure
    raw_gps = read_gps_data_from_file(gps_base_file)
    gps_coll = FlightGPSManipulator(raw_gps)

    #Calculate azimuth based on consecutive data or rad from yaw angle
    gps_coll.assign_drone_azimuth(calculate_azimuth)

    # Assign gps corners
    gps_coll.assign_gps_points_to_image()

    #Save corners to file
    corners_df = gps_coll._convert_to_geoJSON(output_folder, output_filename)

    return corners_df



def generate_corners_for_images_native_GEOJSON(gps_base_file, sensorWidth, sensorHeight, focalLength, xResolution, yResolution, calculate_azimuth = True):
    """Generate gps geojson corner file from base gps data
    
    :param gps_base_file: base gps file to proce
    :type gps_base_file: string
    :param sensorWidth: sensor width in mm
    :type sensorWidth: float
    :param sensorHeight: sensor height in mm
    :type sensorHeight: float
    :param focalLength: camera focal length in mm
    :type focalLength: type
    :param xResolution: images x resolutions
    :type xResolution: int
    :param yResolution: images y resolution
    :type yResolution: int
    :return: corner gps data frame
    :rtype: pandas dataframe

    Corner generation examples
    corners_data = CorGen.generate_corners_for_images_GEOJSON(r"D:\Praca\KSM\Repos\GPS_Tools\data\100m_data_pres\2018-05-08_original_deg0_100m_part1_wiadukt.txt", 12.8, 9.6, 8.8, 4864, 3648)
    corsers_data_test = CorGen.generate_corners_for_images(r"D:\Praca\KSM\Repos\GPS_Tools\data\100m_data_pres\2018-05-08_original_deg0_100m_part1_wiadukt.txt", 12.8, 9.6, 8.8, 4864, 3648)
    native_geoJSON = CorGen.generate_corners_for_images_native_GEOJSON(r"D:\Praca\KSM\Repos\GPS_Tools\GEOJSON_test\gps_metadata_plaza.txt", 12.8, 9.6, 8.8, 4864, 3648)
    

    """

    #Set default flight parameters
    set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution)

    output_filename = "corners_" + os.path.basename(gps_base_file)
    output_folder = os.path.dirname(gps_base_file)

    #read gps raw data to data structure
    raw_gps = read_gps_data_from_file(gps_base_file)
    gps_coll = FlightGPSManipulator(raw_gps)

    #Calculate azimuth based on consecutive data
    gps_coll.assign_drone_azimuth(calculate_azimuth)

    # Assign gps corners
    gps_coll.assign_gps_points_to_image()

    #Save corners to file
    corners_df = gps_coll._convert_to_native_geoJSON(output_folder, output_filename)

    return corners_df

def generate_full_metadata_for_image_native_GEOJSON(image_path, flight_name, sensorWidth, sensorHeight, focalLength, xResolution, yResolution, save=True):
    set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution)

    output_folder = os.path.dirname(image_path)

    #read gps raw data to data structure
    raw_gps = read_exif_xmp_metadata(image_path, flight_name)
    raw_gps = read_gps_data_from_xmp_parser(raw_gps)

    gps_coll = FlightGPSManipulator(raw_gps)

    # Assign gps corners
    gps_coll.assign_gps_points_to_image()

    #Save corners to file
    output_folder = os.path.dirname(image_path)
    output_filename = os.path.splitext(os.path.basename(image_path))[0] + '_corners.geojson'

    corners_df = gps_coll._convert_to_native_geoJSON(output_folder, output_filename, save)

    return corners_df

def generate_full_metadata_for_image_native_GEOJSON_folder(images_folder_path, flight_name, sensorWidth, sensorHeight, focalLength, xResolution, yResolution, save=True):
    set_camera_params(sensorWidth, sensorHeight, focalLength, xResolution, yResolution)

    images_paths_list = get_photos_names_from_dir(images_folder_path)
    corners_df_list = []

    for image_path in images_paths_list:

        #read gps raw data to data structure
        raw_gps = read_exif_xmp_metadata(image_path, flight_name)
        raw_gps = read_gps_data_from_xmp_parser(raw_gps)

        gps_coll = FlightGPSManipulator(raw_gps)

        # Assign gps corners
        gps_coll.assign_gps_points_to_image()

        #Save corners to file

        output_folder = os.path.dirname(image_path)
        output_filename = os.path.splitext(os.path.basename(image_path))[0] + '_corners.geojson'

        corners_df = gps_coll._convert_to_native_geoJSON(output_folder, output_filename, save)
        corners_df_list.append(corners_df)

    return corners_df_list