from cmath import pi
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
from OSMPythonTools.overpass import Overpass
from OSMPythonTools.api import Api
overpass = Overpass()
from area import area
import json
import csv

api = Api(waitBetweenQueries=5)

# LOAD DATA FILES
cities_us = json.load(open('cities_us.json'))
cities_europe = json.load(open('cities_europe_noRussia.json'))

# INITIATE CSV FILE CONTAINING DATA
data = open('output/surfaceParking_20230224.csv', 'w', newline='')
writer = csv.writer(data)
writer.writerow(['city', 'subregion', 'parking', 'population', 'lat', 'lon', 'parking_per_pop', 'region', '%_parking'])



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
            # parkingGeo['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            parking += 0
            print("Could not calculate geometry of feature")
            j += 1

    # CALCULATING PARKING SQFT PER POP
    parking_per_pop = parking * 43560 / cities_us[i]['pop2022']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_us[i]['name'], cities_us[i]['usps'], round(parking, 1), cities_us[i]['pop2022'], lat, lon, parking_per_pop, 'us', parking / (pi * 640)])

    i += 1

# WRITE TO GEOJSON FILE
# with open("data/parking.json", 'w') as outfile:
#     json.dump(parkingGeo, outfile)



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
            # parkingGeo['coordinates'].append(result.elements()[j].geometry()['coordinates'])
            parking += area(result.elements()[j].geometry()) / 4046.86
            j += 1
        except:
            parking += 0
            print("Could not calculate geometry of feature")
            j += 1

    # CALCULATING PARKING SQFT PER POP
    parking_per_pop = parking * 43560 / cities_europe[i]['pop']

    # WRITE DATA FOR EACH CITY TO CSV FILE
    writer.writerow([cities_europe[i]['name'], cities_europe[i]['country'], round(parking, 1), cities_europe[i]['pop'], lat, lon, parking_per_pop, 'europe', parking / (pi * 640)])

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