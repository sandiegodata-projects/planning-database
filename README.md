# San Diego Planning Database

This project collects, processes and publishes datasets with information linked
to tracts, communities and cities in San Diego County. The core of the project
is the [Census Planning
Database](https://www.census.gov/research/data/planning_database/), with
modifications to restrict the data to San Diego County and and make it easier
to link in other datasets.

The Goals of this project are to: 

* Develop a broad collection of data and maps with important indicators about the San Diego region.
* Train volunteers, journalists and nonprofit staff in using the datasets to answer questions. 


## Datasets

* [San Diego Planning
  Database](https://data.sandiegodata.org/dataset/sandiegodata-org-planning-trac
  ts) The San Diego County version of the Census Planning Database 
* [Cities, Communities and Tracts](https://data.sandiegodata.org/dataset/sangis-org-communities-2018)
  Geographic boundaries and link files for cities, communities and tracts in
  San Diego County.

These datasets are organized around geographic index files, files that link a code for a region to a regio identifier and the geometry for the region. For instance, the tracts file has one record per tract in the county, and for each tract includes: 

* A Geoid that identifies the tract, like '14000US06073017813'
* The name of the tract, such as 'Census Tract 100.14'
* The geographic shape for the tract, for mapping in GIS applications. 

There are index files for tracts, cities and communities in San Diego County.
There is also a link file that links cities and communities to tracts and zip
codes.

Additional data, such as census demographics or crime counts, are aggregated to
the greographic region, and given the same geoids as in the index files, allowing users to easily link a data file to an index file. THen users can either report statistics for the regions, or create thematic maps. 

## Future Work

Planned work for this project primarily involves adding new datasets that can be linked to the indexes, such as crime counts, wakability scores, health metrics, trasportation statistics, or anything else that local datausers need. 

For a complete list of work that is being planned or executed, [refer to our issues list. ](https://github.com/sandiegodata/planning-database/issues) and [projecs board](https://github.com/sandiegodata/planning-database/projects)

## How to Join the Project

To join the project you can: 

* Attend some of our regular meeting, [which are announced on Meetup.com](https://www.meetup.com/San-Diego-Regional-Data-Library/)
* Submit an issue, or [work on an issue](https://github.com/sandiegodata/planning-database/issues)
* Contribute analysis by [forking the repo](https://github.com/sandiegodata/planning-database) and making a pull request. 