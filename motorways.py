from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim(waitBetweenQueries=2)
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
from geojson_length import calculate_distance, Unit
from geojson import Feature, LineString
import json
import csv
import datetime

# GET CURRENT DATETIME
datetime = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

# LOAD DATA FILES
cities_us = json.load(open('cities_us_150k.json', 'r', encoding='utf-8-sig'))
cities_eu = json.load(open('cities_eu.json', 'r', encoding='utf-8-sig'))

# INITIATE CSV FILE CONTAINING RESULTS
data = open(f"results/motorways_{datetime}.csv", 'w', newline='', encoding='utf-8')
writer = csv.writer(data)
writer.writerow(['city', 'subregion', 'lane-miles', 'population', 'lat', 'lon', 'lane-feet_per_pop', 'region'])

geojsonUS = {
        "type": "MultiLineString",
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

    # QUERY OVERPASS FOR PARKING LOT INFORMATION
    try:
        result = overpass.query(f"way(around:1609,{lat},{lon})['highway'='motorway']['tunnel'!~'yes'];out geom;way(around:1609,{lat},{lon})['highway'='motorway_link']['tunnel'!~'yes'];out geom;")
    except:
        print("Could not request data")

    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL PARKING LOTS
    j = 0
    lanemiles = 0

    # LOOPING THROUGH INDIVIDUAL PARKING LOTS
    try:
        while j < len(result.elements()):
            if 'lanes' in result.elements()[j].tags():
                lanes = float(result.elements()[j].tags()['lanes'])
                print(lanes)
            else:
                lanes = 1
            geojsonUS['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            lanemiles += float(calculate_distance(Feature(geometry=LineString(result.elements()[j].geometry()['coordinates'])), Unit.feet)) * lanes / 5280
            j += 1
    except:
        print("Could not get parking geometry")

    # CALCULATING PARKING PER 100K POP
    lanefeet_per_pop = lanemiles * 5280 / cities_us[i]['pop2021']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['city'], cities_us[i]['state'], round(lanemiles, 1), cities_us[i]['pop2021'], lat, lon, lanefeet_per_pop, 'us'])

    i += 1

# WRITE TO US GEOJSON FILE
with open(f"results/motorways_us_{datetime}.json", 'w') as outfile:
    json.dump(geojsonUS, outfile)

geojsonEU = {
    "type": "MultiLineString",
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

    # QUERY OVERPASS FOR PARKING LOT INFORMATION
    result = overpass.query(f"way(around:1609,{lat},{lon})['highway'='motorway']['tunnel'!~'yes'];out geom;way(around:1609,{lat},{lon})['highway'='motorway_link']['tunnel'!~'yes'];out geom;")
    
    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL PARKING LOTS
    j = 0
    lanemiles = 0

    # LOOPING THROUGH INDIVIDUAL PARKING LOTS
    try:
        while j < len(result.elements()):
            if 'lanes' in result.elements()[j].tags():
                lanes = float(result.elements()[j].tags()['lanes'])
                print(lanes)
            else:
                lanes = 1
            geojsonEU['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            lanemiles += float(calculate_distance(Feature(geometry=LineString(result.elements()[j].geometry()['coordinates'])), Unit.feet)) * lanes / 5280
            j += 1
    except:
        print("Could not get parking geometry")

    # CALCULATING PARKING PER 100K POP
    lanefeet_per_pop = lanemiles * 5280 / cities_eu[i]['pop']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_eu[i]['city'], cities_eu[i]['country'], round(lanemiles, 1), cities_eu[i]['pop'], lat, lon, lanefeet_per_pop, 'eu'])

    i += 1

# WRITE TO EU GEOJSON FILE
with open(f"results/motorways_eu_{datetime}.json", 'w') as outfile:
    json.dump(geojsonEU, outfile)

data.close()
