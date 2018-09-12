
from geoid.tiger import Tract as TigerTract
from geoid.acs import AcsGeoid


def acs_tract(v):
    
    return TigerTract(v).convert(AcsGeoid)
    