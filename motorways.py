# from OSMPythonTools.nominatim import Nominatim
# nominatim = Nominatim(waitBetweenQueries=2)
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
writer.writerow(['city', 'subregion', 'lane-miles', 'population', 'lat', 'lon', 'lane-feet_per_pop', 'region', 'cumulative_population', 'cumulative_lane-miles'])

lanemilesUS = 0
lanemilesEU = 0
popUS = 0
popEU = 0

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
    lat = cities_us[i]['lat']
    lon = cities_us[i]['lon']

    popUS += cities_us[i]['pop2021']

    # QUERY OVERPASS
    try:
        result = overpass.query(f"way(around:1609,{lat},{lon})['highway'='motorway']['tunnel'!~'yes'];out geom;way(around:1609,{lat},{lon})['highway'='motorway_link']['tunnel'!~'yes'];out geom;")
    except:
        print("Could not request data")

    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    lanemiles = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
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

    lanemilesUS += lanemiles

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['city'], cities_us[i]['state'], round(lanemiles, 1), cities_us[i]['pop2021'], lat, lon, lanefeet_per_pop, 'US', popUS, lanemilesUS])

    i += 1

# WRITE TO US GEOJSON FILE
with open(f"geojsons/motorways_us_{datetime}.json", 'w') as outfile:
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
    lat = cities_eu[i]['lat']
    lon = cities_eu[i]['lon']

    popEU += cities_eu[i]['pop']

    # QUERY OVERPASS
    try:
        result = overpass.query(f"way(around:1609,{lat},{lon})['highway'='motorway']['tunnel'!~'yes'];out geom;way(around:1609,{lat},{lon})['highway'='motorway_link']['tunnel'!~'yes'];out geom;")
    except:
        print("Could not request data")
    
    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    lanemiles = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
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

    # CALCULATING LANE-FEET PER PERSON
    lanefeet_per_pop = lanemiles * 5280 / cities_eu[i]['pop']

    lanemilesEU += lanemiles

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_eu[i]['city'], cities_eu[i]['country'], round(lanemiles, 1), cities_eu[i]['pop'], lat, lon, lanefeet_per_pop, 'EU', popEU, lanemilesEU])

    i += 1

# WRITE TO EU GEOJSON FILE
with open(f"geojsons/motorways_eu_{datetime}.json", 'w') as outfile:
    json.dump(geojsonEU, outfile)

data.close()
