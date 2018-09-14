from geoid.tiger import Tract as TigerTract
from geoid.acs import AcsGeoid

def acs_tract(v):
    

    return TigerTract.parse(v.zfill(11)).convert(AcsGeoid)
    