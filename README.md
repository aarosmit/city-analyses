# OpenStreetMap analyses

This repository serves as a reference and guide to my analyses of features within the OpenStreetMap database. 

## Purpose

The main purpose of these analyses are to point out the glaring flaws with American cities and their associated fragility. My goal is to further the message of [Strong Towns](https://www.strongtowns.org/about) and help create more resilient communities across America.

Most of my analyses look at things on a national level, with each city being a data point. But for each data point there is a community that is in need of support, so [please get involved in yours](https://www.strongtowns.org/local).

## Data sources

The current city lists / population data used in this repository are from Wikipedia:

- [List of cities in the European Union by population within city limits](https://en.wikipedia.org/wiki/List_of_cities_in_the_European_Union_by_population_within_city_limits)
- [List of United States cities by population](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population)

The scripts are written in Python and heavily utilize the package [OSMPythonTools](https://github.com/mocnik-science/osm-python-tools) which provides access to the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API) and [Nominatim](https://nominatim.org). The features retrieved are from the [OpenStreetMap](https://www.openstreetmap.org) database.
