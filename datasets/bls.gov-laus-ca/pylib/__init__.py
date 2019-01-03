""" Example pylib functions"""



from publicdata.bls.seriesid import LauSeriesId

def mk_geoid_map(pkg):
    
    from geoid.acs import County
    import geopandas as gpd
    import pandas as pd

    # California Counties
    counties = pkg.reference('counties').geoframe()
    counties = counties[counties.statefp == '06']
    counties

    # Convert places to their centroid, so they can be located to countyes. 
    places = pkg.reference('places').geoframe()
    cplaces = places.copy()
    cplaces['geometry'] = cplaces.centroid
    cplaces.head()

    cbsa = pkg.reference('cbsa').geoframe()
    ccbsa = cbsa.copy()
    ccbsa['geometry'] = ccbsa.centroid
    ccbsa.head()

    csa = pkg.reference('csa').geoframe()
    ccsa = csa.copy()
    ccsa['geometry'] = ccsa.centroid
    ccsa.head()

    # Assign each place to a county, by the place centroid. The
    # base Census data doesnt do this, because a lot of places cross county boundaries. 
    place_county_map  = gpd.sjoin(cplaces, counties)[['geoid_left', 'geoid_right']]

    # Likewise for CBSAs and CSAa

    cbsa_county_map  = gpd.sjoin(ccbsa, counties)[['geoid_left', 'geoid_right']]

    csa_county_map  = gpd.sjoin(ccsa, counties)[['geoid_left', 'geoid_right']]

    # final map 

    geoid_county_map = pd.concat([place_county_map, cbsa_county_map, csa_county_map])

    geoid_county_map.columns = ['geoid', 'county_geoid']

    geoid_county_map['county'] = geoid_county_map.county_geoid.apply(lambda v: County.parse(v).county )
    
    return { e[1]:e[3] for e in geoid_county_map.to_records() }

def generate_laus(resource, doc, env, *args, **kwargs):
    """ 
    """

    county_map = mk_geoid_map(doc)

    for i, r in enumerate(doc.reference('laus_ca_source')):
        sr =  [ e.strip() for e in r]
        
        if i == 0:
            series_id, year, period, value, footnote_codes = "series_id year period value footnote_codes".split()
            sa_code = 'sa_code'
            area_type_code = 'area_type_code'
            area_code = 'area_code'
            measure_code = 'measure_code'
            month = 'month'
            annual_average = 'is_ann_avg'
            geoid = 'geoid'
            stusab = 'stusab'
            census_region = 'census_region'
            county = 'county'
        else:
            series_id, year, period, value, footnote_codes = sr
            sa_code = series_id[2]
            area_type_code = series_id[3]
            area_code = series_id[3:18]
            measure_code = series_id[18:20]

            period = sr[2]
            month = 0 if period == 'M13' else int(period[1:])
            annual_average = '1' if  period == 'M13' else  0
            
            geoid = LauSeriesId(series_id).geoid
            stusab = geoid.stusab if geoid is not None else None
            county = geoid.county if geoid is not None and hasattr(geoid, 'county') else None
            
            census_region = geoid.level if geoid is not None else None
            
            if not county:
                county = county_map.get(geoid)
        
        yield [year, month, annual_average, period, geoid, stusab, county, census_region, series_id, sa_code, area_code, measure_code, value, footnote_codes] 

