""" Example pylib functions"""

from metapack.rowgenerator import PandasDataframeSource
from metapack import get_cache




def select_acs(resource, doc, env, *args, **kwargs):
    """ Copy the planning database, but exclude the census 2010 columns

    """

    pdb = doc.reference('planning_db_sd').dataframe()
    
    
    columns = [ c for c in pdb.columns if 'cen_2010' not in c]
    
    c_map = {c:c.replace('_acs_12_16','').replace('_acsmoe_12_16','_m90') for c in columns }
    
    yield from PandasDataframeSource('<df>',pdb[columns].rename(columns=c_map), get_cache()) 
    
def select_cen10(resource, doc, env, *args, **kwargs):
    """ Copy the planning database, but exclude the acs columns

    """

    pdb = doc.reference('planning_db_sd').dataframe()
    
    columns = [ c for c in pdb.columns if '_acs' not in c]
    
    c_map = {c:c.replace('_cen_2010','') for c in columns }
    
    yield from PandasDataframeSource('<df>',pdb[columns].rename(columns=c_map), get_cache()) 
    

