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
    
    print("Adding to geopackage: ", r.name)
    command = "ogr2ogr -f GPKG -overwrite -update -a_srs "EPSG:4326"  {}/planning.gpkg '{}' -oo GEOM_POSSIBLE_NAMES=geometry -oo AUTODETECT_TYPE=YES".format(package_dir, t.fspath)
    sp.run(command, shell=True)
    
    if r.headers and 'geometry' in  r.headers:
        print("Writing GeoJSON: ",r.name)
        gdf = r.geoframe()
        gjpath = join(package_dir, r.name+'.geojson')
        if exists(gjpath):
            remove(gjpath)
        gdf.to_file(gjpath, 'GeoJSON')  