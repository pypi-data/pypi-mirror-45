import math
import glob
import os
from shapely.geometry import Point
import descartes
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.ops import transform
from functools import partial
import pyproj


#GEO TOOLS
RZ = 6371008.8

#region Basic operation

def deg_to_radians(degValue):
    return (degValue * math.pi) / 180

def radians_to_deg(radValue):
    return (radValue * 180) / math.pi

#endregion

def transform_to_cartesian(geo_point):
    """ Transform GPS point to cartesian coordinate system

    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    z = R *sin(lat)

    :param geo_point: instance of GPS class
    :type geo_point: GPS class
    :return: cartesian coordinates as (x, y, z)
    :rtype: tuple
    """

    # ! Old way but works
    # cart_point = (RZ * math.cos(deg_to_radians(geo_point.longitude)) * math.cos(deg_to_radians(geo_point.latitude)),
    #               RZ * math.sin(deg_to_radians(geo_point.longitude)) * math.cos(deg_to_radians(geo_point.latitude)),
    #               RZ * math.sin(deg_to_radians(geo_point.latitude)))

    # return cart_point
    point = Point([geo_point.longitude, geo_point.latitude])
    proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2180'))
    out = transform(proj, point)
    return (out.x, out.y)

def transform_to_gps(cart_point):
    """ Transform cartesian points to gps system
    
    lat = asin(z / R)
    lon = atan2(y, x)
    
    :param cart_point: cartesian coordinates as (x, y, z)
    :type cart_point: tuple
    :return: instance of GPS class
    :rtype: GPS class
    """
    
    # ! Old way but works
    # geo_point = GPS()
    # geo_point.latitude = radians_to_deg(math.asin(cart_point[2] / RZ))
    # geo_point.longitude = radians_to_deg(math.atan2(cart_point[1], cart_point[0]))
    # return geo_point

    point = Point([cart_point[0], cart_point[1]])
    proj = partial(pyproj.transform, pyproj.Proj(init='epsg:2180'),
                      pyproj.Proj(init='epsg:4326'))
    out = transform(proj, point)
    gps_point = GPS(out.y, out.x)
    return gps_point

class GPS():
    """Base class responsible for holding gps coordinates of single point
    """

    # __slots__ = ('longitude',
    #             'latitude',
    #             'altitude')
    
    def __init__(self, lat = 0, lon= 0, hei = 0):
        self.latitude = lat
        self.longitude = lon
        self.altitude = hei
        
    def __repr__(self):
        return "GPS: " + " latitude: " + str(self.latitude) + ", longitude: " + str(self.longitude) + ", altitude: " + str(self.altitude) 

class GPS_extended(GPS):
    # __slots__ = ('longitude',
    #             'latitude',
    #             'altitude',
    #             'shapely_point')

    def __init__(self, lat = 0, lon= 0, hei = 0):
        super().__init__(lat, lon, hei)
        self.shapely_point = Point(transform_to_cartesian(self)[0:2])

def get_photos_names_from_dir(images_path, extentions=['*.JPG', '*.png']):
    """ Get image paths from folder
    
    :param images_path: folder path
    :type images_path: string
    """
    filenames = []
    #extentions=['*.JPG', '*.png']
    for ext in extentions:
        filenames_temp = glob.glob(os.path.join(images_path, ext))
        filenames += filenames_temp
    if len(filenames) == 0:
        print('No images found in {}!!!'.format(images_path))
    return filenames

def visualize_image_group(dataset, reference):
    """Visualize polygons placed in dataset(list) save to disc. Used in jupyter notebook
    
    :param dataset: shapely polygons to visualize (works in jupyter notebook)
    :type dataset: list of shapely Polygons
    :param reference: other shapely polygons to visualize (works in jupyter notebook)
    :type dataset: list of shapely Polygons
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for item in dataset:
        ax.add_patch(descartes.PolygonPatch(item, fc='blue', alpha=0.2))
    for item in reference:
        ax.add_patch(descartes.PolygonPatch(item, fc='red', alpha=0.5))
    ax.axis('equal')
    plt.show()
    plt.savefig('Visualisation.png')
    print(len(dataset))

    return fig 


def create_polygon_from_gps_points(gps_area_points):
    """ Create polygon from given gps points
    
    :param gps_area_points: list of GPS objects
    :type gps_area_points: class GPS list
    :return: shapely polygon in cartesian coordinates
    :rtype: shapely polygon
    """
    polygon_cart_vertexs = []

    for point in gps_area_points:
        polygon_cart_vertexs.append(transform_to_cartesian(point))

    area_polygon = Polygon(polygon_cart_vertexs)
    area_polygon = area_polygon.convex_hull
    return area_polygon