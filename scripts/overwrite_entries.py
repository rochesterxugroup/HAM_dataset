import os
import glob
import sys
import json
import shutil

if len(sys.argv) != 7:
    print('Usage: overwrite_entries.py [data directory] [new record directory]'
    ' [directory for removed] [your initials] [record-start] [record-end]')
    exit()
data_path = sys.argv[1]
new_data_path = sys.argv[2]
b_path = sys.argv[3]
initials = sys.argv[4]
start, end = int(sys.argv[5]), int(sys.argv[6])
os.makedirs(b_path, exist_ok=True)
existing = dict()
for f in glob.glob(os.path.join(data_path, '*json')):
    record = os.path.basename(f)
    rs = record.split('_')
    with open(f) as jf:
        data = json.load(jf)
    index = int(rs[0])
    if index < start or index >= end:
        continue
    smiles = data['smiles']
    if smiles not in existing:
        existing[smiles] = []
    else:
        other = existing[smiles][0]['f']
        raise ValueError(f'Found multiples smiles in your id range: {f} and {other}')
    existing[smiles].append({'i': rs[0], 'f': f})

for f in glob.glob(os.path.join(new_data_path, '*json')):
    with open(f) as jf:
        data = json.load(jf)
    smiles = data['smiles']
    records = existing[smiles]
    print('Will backup following records:')
    for r in records:
        print(r)
        shutil.copyfile(r['f'], os.path.join(b_path, os.path.basename(r['f'])))
    new_name = r['i'] + '_' + initials + os.path.basename(f)
    print(new_name)
    #shutil.copyfile(f, os.path.join(data_path, new_name))