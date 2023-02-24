from cmath import pi
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim(waitBetweenQueries=2)
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
writer.writerow(['city', 'subregion', 'parking', 'population', 'lat', 'lon', 'parking_per_pop', 'region', '%_parking'])

geojsonUS = {
    "type": "MultiPolygon",
    "coordinates": []
}

# FOR US CITIES
i = 0
while i < len(cities_us):

    # DETERMINE LOCATION OF CITY
    city = cities_us[i]['city'] + ", " + cities_us[i]['state']
    print(city)
    try:
        location = nominatim.query(city)
        lat = float(location.toJSON()[0]['lat'])
        lon = float(location.toJSON()[0]['lon'])
    except:
        print("Could not get location")

    # QUERY OVERPASS FOR PARKING LOT INFORMATION - RETRIEVES ALL SURFACE PARKING WITHIN 1-MILE RADIUS OF CITY CENTER
    result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;relation(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;")

    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL PARKING LOTS
    j = 0
    parking = 0

    # LOOPING THROUGH INDIVIDUAL PARKING LOTS
    while j < len(result.elements()):
        try:
            geojsonUS['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            parking += 0
            print("Could not calculate geometry of feature")
            j += 1

    # CALCULATING PARKING SQFT PER POP
    parking_per_pop = parking * 43560 / cities_us[i]['pop2021']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['city'], cities_us[i]['state'], round(parking, 1), cities_us[i]['pop2021'], lat, lon, parking_per_pop, 'us', parking / (pi * 640)])

    i += 1

# WRITE TO US GEOJSON FILE
with open(f"results/parking_us_{datetime}.json", 'w') as outfile:
    json.dump(geojsonUS, outfile)

geojsonEU = {
    "type": "MultiPolygon",
    "coordinates": []
}

# FOR EUROPE CITIES
i = 0
while i < len(cities_eu):

    # DETERMINE LOCATION OF CITY
    city = cities_eu[i]['city'] + ", " + cities_eu[i]['country']
    print(city)
    location = nominatim.query(city)
    if location.toJSON() == []:
        i += 1
        continue
    lat = float(location.toJSON()[0]['lat'])
    lon = float(location.toJSON()[0]['lon'])

    # QUERY OVERPASS FOR PARKING LOT INFORMATION - RETRIEVES ALL SURFACE PARKING WITHIN 1-MILE RADIUS OF CITY CENTER
    result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;relation(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']['parking'!~'multi-storey']['building'!~'yes']; out geom;")
    
    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL PARKING LOTS
    j = 0
    parking = 0
    # parkingGeo = {
    #     "type": "MultiPolygon",
    #     "coordinates": []
    # }

    # LOOPING THROUGH INDIVIDUAL PARKING LOTS
    while j < len(result.elements()):
        try:
            geojsonEU['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            parking += 0
            print("Could not calculate geometry of feature")
            j += 1

    # CALCULATING PARKING SQFT PER POP
    parking_per_pop = parking * 43560 / cities_eu[i]['pop']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_eu[i]['city'], cities_eu[i]['country'], round(parking, 1), cities_eu[i]['pop'], lat, lon, parking_per_pop, 'eu', parking / (pi * 640)])

    i += 1

# WRITE TO EU GEOJSON FILE
with open(f"results/parking_eu_{datetime}.json", 'w') as outfile:
    json.dump(geojsonEU, outfile)

data.close()
