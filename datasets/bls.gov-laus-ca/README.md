# California Unemployment

This file is a conversion of the BLS Local Area Unemployment (LAUS) file for California. The conversion breaks out parts of the series_id code, and includes a Census ACS geoid for most areas. 

## Local Area Unemployment Statistics Series Identifier

The following is a sample format description of the Local Area Unemployment Statistics' series identifier:


	                      1         2
	             12345678901234567890
	Series ID    LAUCN281070000000003
	Positions    Value            Field Name
	1-2          LA               Prefix
	3            U                [Seasonal Adjustment Code](https://www.bls.gov/help/hlpseas.htm)
	4-18         CN2810700000000  [Area Code](https://www.bls.gov/help/def/la.htm#area)
	19-20        03               [Measure Code](https://www.bls.gov/help/def/la.htm#measure )
	
