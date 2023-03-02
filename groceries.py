# from OSMPythonTools.nominatim import Nominatim
# nominatim = Nominatim(waitBetweenQueries=2)
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
# from geojson_length import calculate_distance, Unit
# from geojson import Feature, LineString
# from area import area
import json
import csv
import datetime

# GET CURRENT DATETIME
datetime = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

# LOAD DATA FILES
cities_us = json.load(open('cities_us_150k.json', 'r', encoding='utf-8-sig'))
cities_eu = json.load(open('cities_eu.json', 'r', encoding='utf-8-sig'))

# INITIATE CSV FILE CONTAINING RESULTS
data = open(f"results/groceries_{datetime}.csv", 'w', newline='', encoding='utf-8')
writer = csv.writer(data)
writer.writerow(['city', 'subregion', 'groceries', 'population', 'lat', 'lon', 'region', 'cumulative_population', 'cumulative_groceries'])

groceriesUS = 0
groceriesEU = 0
popUS = 0
popEU = 0

geojsonUS = {
    "type": "MultiPoint",
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
        result = overpass.query(f"node(around:3218,{lat},{lon})['shop'='supermarket']; out geom; way(around:3218,{lat},{lon})['shop'='supermarket']; out geom; relation(around:3218,{lat},{lon})['shop'='supermarket']; out geom; node(around:3218,{lat},{lon})['shop'='greengrocer']; out geom; way(around:3218,{lat},{lon})['shop'='greengrocer']; out geom; relation(around:3218,{lat},{lon})['shop'='greengrocer']; out geom;")
    except:
        print("Could not request data")

    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    groceries = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
    while j < len(result.elements()):
        try:
            geojsonUS['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            groceries += 1
            groceriesUS += 1
            j += 1
        except:
            print("Could not get geometry")
            j += 1

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['city'], cities_us[i]['state'], groceries, cities_us[i]['pop2021'], lat, lon, 'US', popUS, groceriesUS])

    i += 1

# # WRITE TO US GEOJSON FILE
# with open(f"results/groceries_us_{datetime}.json", 'w') as outfile:
#     json.dump(geojsonUS, outfile)

geojsonEU = {
    "type": "MultiPoint",
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
        result = overpass.query(f"node(around:3218,{lat},{lon})['shop'='supermarket']; out geom; way(around:3218,{lat},{lon})['shop'='supermarket']; out geom; relation(around:3218,{lat},{lon})['shop'='supermarket']; out geom; node(around:3218,{lat},{lon})['shop'='greengrocer']; out geom; way(around:3218,{lat},{lon})['shop'='greengrocer']; out geom; relation(around:3218,{lat},{lon})['shop'='greengrocer']; out geom;")
    except:
        print("Could not request data")
    
    # DEFINE VARS FOR LOOPING THROUGH INDIVIDUAL FEATURES
    j = 0
    groceries = 0

    # LOOPING THROUGH INDIVIDUAL FEATURES
    try:
        while j < len(result.elements()):
            geojsonEU['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            groceries += 1
            groceriesEU += 1
            j += 1
    except:
        print("Could not get geometry")

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_eu[i]['city'], cities_eu[i]['country'], groceries, cities_eu[i]['pop'], lat, lon, 'EU', popEU, groceriesEU])

    i += 1

# # WRITE TO EU GEOJSON FILE
# with open(f"results/groceries_eu_{datetime}.json", 'w') as outfile:
#     json.dump(geojsonEU, outfile)

data.close()
