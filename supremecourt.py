import requests
import json
import os

outFol = 'supcourt'
outFile = 'docket.json'
outFileJson = os.path.join(outFol,outFile)


if not os.path.exists(outFol):
    os.mkdir(outFol)
if os.path.exists(outFileJson):
    with open(outFileJson, 'r') as fl:
        lastR = json.load(fl)

caseURL = 'https://www.supremecourt.gov/RSS/Cases/JSON/22O155.json'
r = requests.get(caseURL)

rjs = r.json()

if rjs == lastR:
    print('no changes')
else:
    print('changes, file updated.')
    with open(outFileJson, 'w') as jsfile:
        json.dump(rjs, jsfile, indent=2)

proceedings = []

for data in rjs['ProceedingsandOrder']:
    if 'Links' in data:
        for link in data['Links']:
            print(link['File'])
            print(link['DocumentUrl'])
