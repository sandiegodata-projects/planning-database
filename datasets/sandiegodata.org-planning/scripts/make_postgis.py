import metapack as mp
import subprocess as sp
from os.path import exists, join
from os import remove, mkdir

pkg = mp.open_package('_packages/sandiegodata.org-planning-1')

print("Package: ", pkg.package_url)

package_dir = 'package'

if not exists(package_dir):
    mkdir(package_dir)

for r in pkg.resources():
    t = r.resolved_url.get_resource().get_target()
    
    
    if r.headers and 'geometry' in  r.headers:
        pass
        
        print("Adding to postgis: ", r.name)
        command = ('ogr2ogr -f PostgreSQL -overwrite -a_srs "EPSG:4326" PG:"host=localhost port=25432  user=docker password=$PG_PASSWORD dbname=gis"  \'{}\' '
                  '-oo GEOM_POSSIBLE_NAMES=geometry -oo AUTODETECT_TYPE=YES').format(t.fspath)
        sp.run(command, shell=True)
        
        break