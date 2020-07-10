import os
import glob
import sys
import json

if len(sys.argv) != 3:
    print('Usage: make_table.py [data directory] [output csv file]')
    exit()
data_path = sys.argv[1]
parsed = []
for f in glob.glob(os.path.join(data_path, '*json')):
    record = os.path.basename(f)
    rs = record.split('_')
    with open(f) as f:
        data = json.load(f)
    author = rs[1].split('cgmap')[0]
    index = int(rs[0])
    smiles = data['smiles']
    parsed.append(f'{index}, {smiles}, {author}')

with open(sys.argv[2], 'w') as f:
    f.write('\n'.join(parsed))
