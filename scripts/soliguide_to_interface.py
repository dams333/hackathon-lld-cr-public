# this tool creates ...

from sys import argv
import pandas as pd
import json

fname = './soliguide_paris.json'
f = open(fname)
ds = json.load(f)
places = pd.DataFrame(ds)
soliguide_ids = places['_id']
soliguide_ids.name = 'soliguide_id'

dsf = pd.concat([soliguide_ids, pd.Series(data=['']*len(ds), name='rna', dtype=str)], axis=1)
print('[' + dsf.T.to_json() + ']')