import geopandas as gpd
import pandas as pd
import os
import zipfile
import requests
import io

url = 'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/MB_2021_AUST_SHP_GDA2020.zip'

response = requests.get(url, stream=True)

if response.status_code == 200:
    
    with zipfile.ZipFile(io.BytesIO(response.content)) as shp_zip:

        # Save the shp_zip to a temporary folder
        shp_zip.extractall('local')

gdf : gpd.GeoDataFrame = gpd.read_file('local/MB_2021_AUST_SHP_GDA2020/MB_2021_AUST_GDA2020.shp')

os.makedirs('data/mb-geojson', exist_ok=True)

gdf.groupby('SA4_CODE21').apply(lambda x: x.to_file(f'data/mb-geojson/MB-SA4-{x.name}.geojson', driver='GeoJSON'))
