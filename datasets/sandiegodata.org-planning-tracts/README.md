# San Diego Planning Database

The Planing Database is a Census product that combines a range of data from the
American Community Survey and 2010 Decenial Census into a single file, with one
row per census tract. This version of the file includes only tracts in San
Diego County. The file is linked to ACS format geoids to identify tracts, so it
can be easily linked to other tracts data. This data package includes links to
two such files, one for San Diego communities, and one for tract geographics.

The planning database has about 450 columns. For full definitions of the columns, refer to the [upstream documentation for the source file](https://www.census.gov/research/data/planning_database/2018/docs/2018_Tract_PDB_Documentation_V4.pdf
). In general, the column names in the documentation must be lowercased for use with the file in this data package. 

## Use patterns

In Python, use metapack to open the data package. 


	import metapack as mp
	pkg = mp.open_package('http://library.metatab.org/sandiegodata.org-planning-tracts-1.zip')

To display a simple map, link in the tract boundaries from the communities
dataset and use the Geopandas .plot() function. The ``column`` argument names
the column to use for coloring regions. Note that the column name is copied
from the documentation with mixed case, then lowercased to index the dataset.


	tracts = pkg.reference('communities').geoframe().set_index('geoid').fillna('')
	df = tracts.join(cpdb)
	
	fig, ax = plt.subplots(1, figsize=(15,10))
	df.plot(ax=ax, column='pct_MLT_U10p_ACS_12_16'.lower())


After linking in the communities, you can also use the [community id columns](https://data.sandiegodata.org/dataset/sangis-org-communities-2018/resource/668d9a6a-a7a7-4c01-9fb9-a5121c1a622f) to group by city or community: 


	seniors = dfg.df.groupby('city_name').pop_65plus_acs_12_16.sum()

# Versions

2. First Release
3. Clean more currency columns