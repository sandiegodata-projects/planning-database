import metapack as mp
import subprocess as sp
from os.path import exists, join
from os import remove, mkdir

pkg = mp.open_package('_packages/sandiegodata.org-planning-1')

print("Package: ", pkg.package_url)

package_dir = 'package'

if not exists(package_dir):
    mkdir(package_dir)

tracts = pkg.resource('tract_boundaries').geoframe().set_index('geoid')

for r in pkg.resources():

    if r.headers and 'geometry' not in  r.headers and 'geoid' in r.headers:
        print("Writing GeoJSON: ",r.name)
        df = r.read_csv()
        
        gdf = tracts.join(df.set_index('geoid'))
        
        gjpath = join(package_dir, r.name+'.geojson')
        
        if exists(gjpath):
            remove(gjpath)
        gdf.to_file(gjpath, 'GeoJSON')  