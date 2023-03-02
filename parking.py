from cmath import pi
# from OSMPythonTools.nominatim import Nominatim
# nominatim = Nominatim(waitBetweenQueries=2)
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
from area import area
import json
import csv
import datetime

# GET CURRENT DATETIME
datetime = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

# LOAD DATA FILES
cities_us = json.load(open('cities_us_150k.json', 'r', encoding='utf-8-sig'))
cities_eu = json.load(open('cities_eu.json', 'r', encoding='utf-8-sig'))

# INITIATE CSV FILE CONTAINING RESULTS
data = open(f"results/parking_{datetime}.csv", 'w', newline='', encoding='utf-8')
writer = csv.writer(data)
writer.writerow(['city', 'subregion', 'parking', 'population', 'lat', 'lon', 'region', 'cumulative_population', 'cumulative_parking'])

parkingUS = 0
parkingEU = 0
popUS = 0
popEU = 0

geojsonUS = {
    "type": "MultiPolygon",
    "coordinates": []
}

# FOR US CITIES
i = 0
while i < len(cities_us):

    # GET LOCATION OF CITY
    city = cities_us[i]['city'] + ", " + cities_us[i]['state']
    print(city)
    lat = cities_us[i]['lat']
    lon = cities_us[i]['lon']

    popUS += cities_us[i]['pop2021']

    # QUERY OVERPASS
    try:
        result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;relation(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;")
    except:
        print("Could not request data")

    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    parking = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
    while j < len(result.elements()):
        try:
            geojsonUS['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            print("Could not calculate geometry of feature")
            j += 1

    # ADD TO TOTAL FOR US
    parkingUS += parking

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['city'], cities_us[i]['state'], round(parking, 1), cities_us[i]['pop2021'], lat, lon, 'us', popUS, round(parkingUS, 1)])

    i += 1

# WRITE TO US GEOJSON FILE
with open(f"geojsons/parking_us_{datetime}.json", 'w') as outfile:
    json.dump(geojsonUS, outfile)

geojsonEU = {
    "type": "MultiPolygon",
    "coordinates": []
}

# FOR EUROPE CITIES
i = 0
while i < len(cities_eu):

    # GET LOCATION OF CITY
    city = cities_eu[i]['city'] + ", " + cities_eu[i]['country']
    print(city)
    lat = cities_eu[i]['lat']
    lon = cities_eu[i]['lon']

    popEU += cities_eu[i]['pop']

    # QUERY OVERPASS
    try:
        result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;relation(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;")
    except:
        print("Could not request data")
    
    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    parking = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
    while j < len(result.elements()):
        try:
            geojsonEU['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            print("Could not calculate geometry of feature")
            j += 1

    # ADD TO TOTAL FOR EU
    parkingEU += parking

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_eu[i]['city'], cities_eu[i]['country'], round(parking, 1), cities_eu[i]['pop'], lat, lon, 'eu', popEU, round(parkingEU, 1)])

    i += 1

# WRITE TO EU GEOJSON FILE
with open(f"geojsons/parking_eu_{datetime}.json", 'w') as outfile:
    json.dump(geojsonEU, outfile)

data.close()
