# City analyses

This repository serves as a reference and guide to my analyses of features within cities (primarily using the OpenStreetMap database). 

## Purpose

The main purpose of these analyses are to point out the glaring flaws with American cities and their associated fragility. My goal is to further the message of [Strong Towns](https://www.strongtowns.org/about) and help create more resilient communities across America.

Most of my analyses look at things on a national level, with each city being a data point. But for each data point there is a community that is in need of support, so [get involved in yours](https://www.strongtowns.org/local).

## Existing analyses

| Category | Date performed | Results | Details |
| -------- | :------------: | ------- | ------- |
| Surface parking (US vs EU) | 2023-03-02 | [Tableau chart](https://public.tableau.com/views/Cityparking/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link), [raw data](results/parking_20230302T152521Z.csv) | Within one mile of city centers; [Example of Chattanooga (Overpass Turbo)](https://overpass-turbo.eu/s/1tGz) |
| Highways/motorways (US vs EU) | 2023-02-28 | [Tableau chart](https://public.tableau.com/views/Cityhighways/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link), [raw data](results/motorways_20230228T200310Z.csv) | Within one mile of city centers (highways may extend outside of one mile radius); [Example of Kansas City (Overpass Turbo)](https://overpass-turbo.eu/s/1tGx) |
| Grocery stores (US vs EU) | 2023-02-28 | [Tableau chart](https://public.tableau.com/views/Citygrocerystores/Sheet1?:language=en-US&:display_count=n&:origin=viz_share_link), [raw data](results/groceries_20230228T183627Z.csv) | Within two miles of city centers; [Example of Barcelona (Overpass Turbo)](https://overpass-turbo.eu/s/1tGt) |

## Attributions

[**OpenStreetMap**](https://www.openstreetmap.org) is the source of all of the queried data.

The current city lists / population data used in this repository are from Wikipedia:

- [List of cities in the European Union by population within city limits](https://en.wikipedia.org/wiki/List_of_cities_in_the_European_Union_by_population_within_city_limits)
- [List of United States cities by population](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population)

The scripts are written in Python and heavily utilize the package [OSMPythonTools](https://github.com/mocnik-science/osm-python-tools) which provides access to the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API).
