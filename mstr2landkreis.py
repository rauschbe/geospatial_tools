import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
filtering = False

#read in mastr with geocoded columns
mstr_geocoded = pd.read_csv('mstr_bing.csv', encoding = 'utf8')

#create geometry list
geometry = [(xy) for xy in zip(mstr_geocoded['1'].astype(float), mstr_geocoded['0'].astype(float))]

#convert each coordinate tuple to shapely.Point
geometry = [Point(x) for x in geometry]

#convert pandas DataFrame to geopandas DataFrame
mstr_geocoded = gpd.GeoDataFrame(mstr_geocoded[['EinheitMastrNummer', 'Standort', 'EegInbetriebnahmedatum',
                                               'InstallierteLeistung', 'VerknuepfteEinheit',
                                               ]], geometry = geometry, crs = {'init': 'epsg:4326'})

#read in administrative zone shape file
landkreise = gpd.read_file('landkreise/reprojected_landkreise.shp', encoding = 'UTF-8', crs = {'init': 'epsg:4326'})
landkreise = landkreise[['GN', 'geometry']]

#create spatial join between geocoded MaStR and administrative zone polygons --> determination in which AZ MaStR points lie
mstr_geocoded = gpd.sjoin(mstr_geocoded, landkreise, how = 'inner', op = 'within')

admin_zones = mstr_geocoded.GN.unique().tolist()

#iterate over administrative zones and create distinct mastr file per administrative zone
for zone in sorted(admin_zones):
    print(zone)
    mstr_geocoded_helper = mstr_geocoded[mstr_geocoded.GN == zone]
    mstr_geocoded_helper.to_file('mstr_split_landkreise/mstr_{}.shp'.format(zone), encoding = 'ISO-8859-1')







