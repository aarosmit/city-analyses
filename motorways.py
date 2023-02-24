# from cmath import pi
# from logging import lastResort
# from pdb import lasti2lineno
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.api import Api
overpass = Overpass()
from geojson_length import calculate_distance, Unit
from geojson import Feature, LineString
import json
import csv

api = Api(waitBetweenQueries=5)

cities_us = json.load(open('cities_us.json'))
cities_europe = json.load(open('cities_europe_noRussia.json'))

data = open('output/motorways_20230224.csv', 'w', newline='')
writer = csv.writer(data)
writer.writerow(['city', 'subregion', 'lane-miles', 'population', 'lat', 'lon', 'lane-feet_per_pop', 'region'])

motorwayGeo = {
        "type": "MultiLineString",
        "coordinates": []
}

# FOR US CITIES
i = 0
while i < len(cities_us):

    # DETERMINE LOCATION OF CITY
    city = cities_us[i]['name'] + ", " + cities_us[i]['usps']
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
            # motorwayGeo['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            # lanes = result.elements()[j].tags()['lanes']
            lanemiles += float(calculate_distance(Feature(geometry=LineString(result.elements()[j].geometry()['coordinates'])), Unit.feet)) * lanes / 5280
            j += 1
    except:
        print("Could not get parking geometry")

    # CALCULATING PARKING PER 100K POP
    lanefeet_per_pop = lanemiles * 5280 / cities_us[i]['pop2022']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['name'], cities_us[i]['usps'], round(lanemiles, 1), cities_us[i]['pop2022'], lat, lon, lanefeet_per_pop, 'us'])

    # WRITE TO JSON FILES FOR EACH CITY



    i += 1

# with open("output/motorways_us.json", 'w') as outfile:
#     json.dump(motorwayGeo, outfile)



# FOR EUROPE CITIES
i = 0
while i < len(cities_europe):

    # DETERMINE LOCATION OF CITY
    city = cities_europe[i]['name'] + ", " + cities_europe[i]['country']
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
    # motorwayGeo = {
    #     "type": "MultiPolygon",
    #     "coordinates": []
    # }

    # LOOPING THROUGH INDIVIDUAL PARKING LOTS
    try:
        while j < len(result.elements()):
            if 'lanes' in result.elements()[j].tags():
                lanes = float(result.elements()[j].tags()['lanes'])
                print(lanes)
            else:
                lanes = 1
            # motorwayGeo['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            # lanes = result.elements()[j].tags()['lanes']
            lanemiles += float(calculate_distance(Feature(geometry=LineString(result.elements()[j].geometry()['coordinates'])), Unit.feet)) * lanes / 5280
            j += 1
    except:
        print("Could not get parking geometry")

    # CALCULATING PARKING PER 100K POP
    lanefeet_per_pop = lanemiles * 5280 / cities_europe[i]['pop']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_europe[i]['name'], cities_europe[i]['country'], round(lanemiles, 1), cities_europe[i]['pop'], lat, lon, lanefeet_per_pop, 'europe'])

    # WRITE TO JSON FILES FOR EACH CITY
    # with open(f"data/{cities_europe[i]['name']} {cities_europe[i]['country']}.json", 'w') as outfile:
    #     json.dump(parkingGeo, outfile)

    i += 1

# i = 0
# while i < len(cities_europe) - 287 - 199:
#     city = cities_europe[i]['name'] + ", " + cities_europe[i]['country']
#     print(city)
#     location = nominatim.query(city)
#     if location.toJSON() == []:
#         i += 1
#         continue
#     lat = float(location.toJSON()[0]['lat'])
#     lon = float(location.toJSON()[0]['lon'])
#     result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']; out geom;")

#     j = 0
#     parking = 0
#     while j < len(result.elements()):
#         parking += area(result.elements()[j].geometry()) / 4046.86
#         j += 1
#     parking_per_pop = parking / (cities_europe[i]['pop'] / 100000)
#     writer.writerow([cities_europe[i]['name'], cities_europe[i]['country'], round(parking, 1), cities_europe[i]['pop'], lat, lon, parking_per_pop, 'europe'])
#     i += 1

data.close()

# ### FOR EUROPE CITIES
# data_europe = open('data_europe.csv', 'w', newline='')
# writer_europe = csv.writer(data_europe)
# writer_europe.writerow(['city', 'country', 'parking', 'population', 'lat', 'lon', 'parking_per_pop', 'country'])

# i = 0
# while i < len(cities_europe):
#     city = cities_europe[i]['name'] + ", " + cities_europe[i]['country']
#     print(city)
#     location = nominatim.query(city)
#     if location.toJSON() == []:
#         i += 1
#         continue
#     lat = float(location.toJSON()[0]['lat'])
#     lon = float(location.toJSON()[0]['lon'])
#     result = overpass.query(f"way(around:1609,{lat},{lon})['amenity'='parking']['parking'!~'underground']; out geom;")

#     j = 0
#     parking = 0
#     while j < len(result.elements()):
#         parking += area(result.elements()[j].geometry()) / 4046.86
#         j += 1
#     parking_per_pop = parking / (cities_europe[i]['pop'] / 100000)
#     writer_europe.writerow([cities_europe[i]['name'], cities_europe[i]['country'], round(parking, 1), cities_europe[i]['pop'], lat, lon, parking_per_pop, 'europe'])
#     i += 1

# data_europe.close()