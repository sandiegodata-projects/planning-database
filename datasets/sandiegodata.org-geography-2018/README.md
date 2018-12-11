# Community, City and Tract Boundaries in San Diego County


This package combines three SANGIS datasets for communities and cities in San Diego county into a single file, in the ``communities`` resource, with Census tract definitions for San Diego count. The source files are: 

* Municipal boundaries, of incorporated cities and the rest of the county
* Communities in unincorporated county areas
* Communities in San Diego. 
* Census tract boundaries for 2016

In addition to simply combining these four boundary files, the dataset also
links tracts into the other three regions, in the ``tracts_links`` and
``tracts_all_regions`` datasets. Using these datasets, you can get all of the
tracts in Escondido, or all of the tracts in the San Diego community of
Clairemont. The join is performed by containment of the Internal Point, which
is defined by the census for each tract. Because tract boundaries are not
always coincident with municipal boundaries, there are many cases where the
collection of tracts for a city or community will have a different boundary
than the actual region. Smaller, less densely populated regions, like San
Marcos, or particuarly afected.

The ``tracts_links`` dataset is probably the most useful. It joins tracts to regions,
and has two sets of columns, for city and community. This dataset includes
every tract in the county, and each appears only once. If a tract is included
in both a city and community, then there is a name and code for both the city
columns and the community columns. Regions not in a city have a city value of
"County" and a city code of "CN".

The ``communities`` dataset, has a ``type`` field to distinguish the types of area, which is one of: 

* city
* county_community
* sd_community
* community

The ``tracts_all_regions`` dataset may have more than one row for each tract;
the tract will appear once for each of the four region types that it is in, but
no tract is in more than 2 regions. For instance, a tract in a community of San
Diego will appear twice, once for the community, and once for the City.
