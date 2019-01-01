# Copy metadata that can't be copied with mp update -P

import metapack as mp
import subprocess as sp
from os.path import exists, join
from os import remove, mkdir

pkg = mp.open_package('.')

print("Package: ", pkg.package_url)

pdb = pkg.reference('planning_db_sd')

col_map = { c['header'].replace('_acs_12_16','').replace('_acsmoe_12_16','_m90'):c 
            for c in pdb.columns()}

acs_pdb = pkg.resource('acs_pdb')


for c in acs_pdb.schema_term.children:
    ch = c.get_or_new_child('Description')
    ch.value = col_map.get(c.name)['description']


pkg.write_csv()
