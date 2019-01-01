# SANGIS Business Sites

This dataset is based on the SANGIS BUSINESS_SITES data file, which is compiled from the Assessors Business Property Account Master file. This file is different from the City of San Diego's business list, in that it includes records for the whole county, it categorizes businesses differently ( not using NAICS codes ) and for some categories, it does not appear to be very accurate. 

This package includes two additional files, which link counts of businesses by categories to tracts. 

* `tract_counts_rows` presents the counts of businesses as rows. There is one row for each combination of type of business and census tract. 
* `tract_counts_columns` presents the counts of businesses as columns. There is one row per tract, and one column for each type of business. 

The row oriented file is easier to use in tools that have good support for filtering, such as Pandas and Tableau. The column oriented form is easier to use in tools where selecting a column is easier than filtering, such as QGIS. 

## Caveats

The  upstream documentation warns:

  Data should be used with caution as not all addresses and/or APN numbers are
  correct, and certain business sites do not have precise addresses so that
  locations are approximate. Certain business sites could not be located but
  remain in the dataset.
