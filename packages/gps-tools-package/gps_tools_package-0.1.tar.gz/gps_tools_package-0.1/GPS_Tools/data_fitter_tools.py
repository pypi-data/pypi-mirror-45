from GPS_Tools.GPS_module import InstaObjectsPhoto
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import geojson

def read_csv_as_gdf(object_csv_path):
    objects_df = pd.read_csv(object_csv_path)
    objects_gdf = gpd.GeoDataFrame(objects_df)
    objects_gdf['geometry'] = objects_gdf.apply(lambda z: Point(z.longitude, z.latitude), axis=1)
    return objects_gdf

def parse_data_for_MD(objects_gdf, img_path, resolution, altitude):
    insta_obj_photo = InstaObjectsPhoto([4864, 3648], 100)
    insta_obj_photo.read_data_from_only_objects_df(objects_gdf, img_path)
    insta_obj_photo.load_crops()
    insta_obj_photo.load_rotated_crops()
    orig_crops = insta_obj_photo.orig_crops
    rotated_crops = insta_obj_photo.rotated_crops
    return orig_crops, rotated_crops

def geodataframe2geojson(geodataframe, flight_name, output_geojson_path):
    features = []
    df = geodataframe.fillna('yimir')
    for i, row in df.iterrows():
        properties = {}
        for column_name in list(df.columns):
            if row[column_name] != 'yimir' and column_name is not 'geometry':
                properties[column_name] = row[column_name]

        features.append(geojson.Feature(geometry = row['geometry'], properties = properties))


    feature_collection = geojson.FeatureCollection(features, properties= {"flight_name": flight_name} )

    with open(output_geojson_path, 'w') as f:
        geojson.dump(feature_collection,  f, indent = 4,  sort_keys = True)