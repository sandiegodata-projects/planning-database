

def link_code(type, code):
    return "{}-{}".format(type, code).lower()


def generate_tracts(resource, doc, env, *args, **kwargs):
    
    """Just the tracts for San Diego county"""

    from metapack import get_cache
    from metapack.rowgenerator import PandasDataframeSource
    from geoid.tiger import Tract
    from geoid.acs import AcsGeoid

    tracts = doc.reference('california_tracts').geoframe()

    tracts.columns = [c.lower() for c in tracts.columns]
    tracts = tracts[(tracts.statefp == '06') & (tracts.countyfp == '073')]

    tracts['geoid'] = tracts.geoid.apply( lambda v: Tract.parse(str(v).zfill(11)).convert(AcsGeoid) )

    tracts.set_index('geoid', inplace=True)

    yield from PandasDataframeSource('<df>',tracts , get_cache())    


def generate_boundaries(resource, doc, env, *args, **kwargs):
    """All cities and communities. Has both San Diego citm and the communities in San Diego"""
    from rowgenerators.rowproxy import RowProxy
     

    class LowerCaseRP(RowProxy):

        def __init__(self, keys):
            super().__init__([e.lower() for e in keys])
     
    yield 'type name name_code city link_code geometry'.split()
    
    for row in doc.reference('cities').iterrowproxy(LowerCaseRP): 
         
        if row.code == 'CN':
            yield ['county', row.name, row.code, row.code, link_code('county',row.code), row.geometry]
        else:
            yield ['city', row.name, row.code, row.code, link_code('city',row.code), row.geometry]
    
    for row in doc.reference('sd_communities').iterrowproxy(LowerCaseRP): 
        yield ['sd_community', row.cpname, row.cpcode, 'SD', link_code('sdc',row.cpcode), row.geometry]
        
    for row in doc.reference('county_communities').iterrowproxy(LowerCaseRP): 
        yield ['county_community', row.cpasg_labe, row.cpasg, 'CN', link_code('cnc',row.cpasg), row.geometry]
    

def clean_comm_name(s):
    import re
    return re.compile('[^a-zA-Z]').sub('',s.lower())  

def tract_links(resource, doc, env, *args, **kwargs):
    from metapack.rowgenerator import PandasDataframeSource
    from metapack import get_cache  
    from shapely.geometry import Point
    import geopandas as gpd

    # First, geo join the tracts into the communities and cities. 

    comm = doc.resource('cities_communities').geoframe()
    tracts = doc.resource('tracts').dataframe()

    tracts['intp'] = tracts.apply(lambda r: Point(float(r.intptlon), float(r.intptlat)), axis=1)

    tract_pt = gpd.GeoDataFrame(tracts, geometry = 'intp')

    tract_community = gpd.sjoin(comm, tract_pt, op='contains')

    columns = [ 'geoid', 'type', 'name', 'name_code', 'city', 'link_code' ]

    tc = tract_community.rename({'name_left':'name'}, axis=1)[columns]
    
    # Now link everything together. 
    
    acronyms = doc.reference('acronyms')
    acro_map = dict(list(acronyms)[1:])
    acro_map[''] = ''


    _1 = tc[['geoid']].drop_duplicates().set_index('geoid').join(tracts[['geoid', 'geometry']].set_index('geoid'))
    _2 = tc.set_index('geoid')

    _3  = _2[_2.type == 'city'][['name','name_code']]
    _4  = _2[_2.type == 'county'][['name','name_code']]
    _5  = _2[_2.type == 'sd_community'][['name','name_code']]
    _6  = _2[_2.type == 'county_community'][['name','name_code']]

    _7 = _1.join(_3, rsuffix='_city').join(_4, rsuffix='_county')\
           .join(_5, rsuffix='_sdc').join(_6, rsuffix='_cnc')

    _7.columns =\
    [
     'geometry',
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

     # move geometry to the end
    _7 = _7[ list(_7.columns)[1:]+ list(_7.columns)[:1]]

    
    yield from PandasDataframeSource('<df>',_7 , get_cache())