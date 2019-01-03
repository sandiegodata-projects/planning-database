

def link_code(type, code):
    return "{}-{}".format(type, code).lower()


def prepare_tracts(resource, doc, env, *args, **kwargs):
    
    
    from geoid.tiger import Tract
    from geoid.acs import AcsGeoid

    tracts = doc.reference('california_tracts').geoframe()

    tracts.drop(columns=['geoid'], inplace=True)
    tracts.index.name = 'geoid'

    tracts.columns = [c.lower() for c in tracts.columns]
    tracts = tracts[(tracts.statefp == '06') & (tracts.countyfp == '073')]

    #tracts['geoid'] = tracts.geoid.apply( lambda v: str(Tract.parse(str(v).zfill(11)).convert(AcsGeoid)) )

    return tracts.reset_index().sort_values('geoid')


def generate_tracts_boundaries(resource, doc, env, *args, **kwargs):
    
    """Just the geoid and boundaries for tracts for San Diego county"""

    tracts = prepare_tracts(resource, doc, env, *args, **kwargs)
    
    return tracts[['geoid', 'geometry']]
  

def generate_tracts(resource, doc, env, *args, **kwargs):
    
    """Just the  information for tracts for San Diego county"""

    tracts = prepare_tracts(resource, doc, env, *args, **kwargs)

    # Convert to NAD83 / California zone 6, which is in units of 
    # meters, so the area calculateion is in square meters. 
    # tracts = tracts.to_crs({'init':'EPSG:26946'})
    

    columns = list(tracts.columns)
    columns.remove('geometry')

    return tracts[columns]


def mk_city_geoid_map(pkg):
    from shapely.geometry import Point
    import geopandas as gpd

    places_df = pkg.reference('places').geoframe()
    places = gpd.GeoDataFrame(places_df, geometry=
                            [Point(float(x),float(y)) for x,y in zip( places_df.intptlon, places_df.intptlat)],
                             crs = places_df.crs)


    cities = pkg.reference('cities').geoframe().to_crs(places_df.crs)

    t = gpd.sjoin(places, cities[cities.CODE != 'CN'])

    d = t[['CODE','geoid']].set_index('CODE').to_dict()['geoid']

    from geoid.acs import County

    d['CN'] = str(County(6,73))

    return d

def generate_boundaries(resource, doc, env, *args, **kwargs):
    """All cities and communities. Has both San Diego citm and the communities in San Diego"""
    from rowgenerators.rowproxy import RowProxy
     
    city_geoid_map = mk_city_geoid_map(doc)

    class LowerCaseRP(RowProxy):

        def __init__(self, keys):
            super().__init__([e.lower() for e in keys])
     
    yield 'type name name_code city link_code geoid geometry'.split()
    
    for row in doc.reference('cities').iterrowproxy(LowerCaseRP): 
         
        geoid = city_geoid_map.get(row.code)
         
        if row.code == 'CN':
            yield ['county', row.name, row.code, row.code, link_code('county',row.code), geoid, row.geometry]
        else:
            yield ['city', row.name, row.code, row.code, link_code('city',row.code), None, row.geometry]
    
    for row in doc.reference('sd_communities').iterrowproxy(LowerCaseRP): 
        yield ['sd_community', row.cpname, row.cpcode, 'SD', link_code('sdc',row.cpcode), None, row.geometry]
        
    for row in doc.reference('county_communities').iterrowproxy(LowerCaseRP): 
        yield ['county_community', row.cpasg_labe, row.cpasg, 'CN', link_code('cnc',row.cpasg), None, row.geometry]
    
    for row in doc.reference('promise_zone').iterrowproxy(LowerCaseRP): 
        yield ['sd_district', row.name, None, 'SD', 'promise_zone', None, row.geometry]
    
    

def clean_comm_name(s):
    import re
    return re.compile('[^a-zA-Z]').sub('',s.lower())  



def tract_links(resource, doc, env, *args, **kwargs):
    from metapack.rowgenerator import PandasDataframeSource
    from metapack import get_cache  
    from shapely.geometry import Point
    import geopandas as gpd

    # First, geo join the tracts into the communities and cities.  

   

    comm = doc.resource('community_boundaries').geoframe()
    tracts = doc.resource('tracts').dataframe()

    tracts['intp'] = tracts.apply(lambda r: Point(float(r.intptlon), float(r.intptlat)), axis=1)

    tract_pt = gpd.GeoDataFrame(tracts, geometry = 'intp')

    tract_pt.crs = comm.crs

    tract_community = gpd.sjoin(comm, tract_pt, op='contains')

    columns = [ 'geoid', 'type', 'name', 'name_code', 'city', 'link_code' ]

  
    tc = tract_community.rename({'name_left':'name', 'geoid_right':'geoid'}, axis=1)[columns]

    # Now link everything together. 

    acronyms = doc.reference('acronyms')

    acro_map = dict(list(acronyms)[1:])
    acro_map[''] = ''

    _2 = tc.set_index('geoid')

    _3  = _2[_2.type == 'city'][['name','name_code']]
    _4  = _2[_2.type == 'county'][['name','name_code']]
    _5  = _2[_2.type == 'sd_community'][['name','name_code']]
    _6  = _2[_2.type == 'county_community'][['name','name_code']]

    _7 = _3.join(_4, rsuffix='_county')\
           .join(_5, rsuffix='_sdc').join(_6, rsuffix='_cnc')


    _7.columns =\
    [
     'city_name',
     'city_code',
     'county_name',
     'county_code',
     'community_name',
     'community_cpcode',
     'cnc_name',
     'cnc_code']

    # Move the county name into the city columns, then drop it
    _7['city_name'] = _7.city_name.where(~((_7.city_name.isnull()) & (_7.county_code == 'CN')),'COUNTY' )
    _7['city_code'] = _7.city_code.where(~((_7.city_code.isnull()) & (_7.county_code == 'CN')),'CN' )

    _7.drop(['county_name','county_code'], axis=1, inplace=True)


    # Move the  county community names into the community columns
    _7['community_name'] =  _7.community_name.where( _7.city_code != 'CN' ,  _7.cnc_name ).fillna('')
    _7['community_cpcode'] =_7.community_cpcode.where( _7.city_code != 'CN' ,  _7.cnc_code ).fillna('0')

    _7.drop(['cnc_name','cnc_code'], axis=1, inplace=True)

    _7 = _7.fillna('')

    _7['city_name'] = _7.city_name.apply(lambda v : v.title())
    _7['community_name'] = _7.community_name.apply(lambda v : str(v).title()).fillna('')

    _7['community_code'] = _7.community_name.apply(lambda v: acro_map[clean_comm_name(v)].upper() )

    _7.replace('','NA',inplace=True)


    return _7

def sd_county_boundary(resource, doc, env, *args, **kwargs):
    
    for row in doc.reference('county_boundaries').iterdict:
        if int(row['statefp']) == 6 and int(row['countyfp']) == 73:
            yield list(row.keys())
            yield list(row.values())
            break
    
