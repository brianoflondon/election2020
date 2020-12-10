import requests
import urllib.request
import json
import os
from pathlib import Path
from pathvalidate import sanitize_filename


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

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 

for data in rjs['ProceedingsandOrder']:
    if 'Links' in data:
        for link in data['Links']:
            fileN = sanitize_filename(link['File'])
            url = link['DocumentUrl']
            outF = os.path.join(outFol,fileN)
            try:
                print(fileN,url)
                req = urllib.request.Request(url,None,headers)
                response = urllib.request.urlopen(req)
                data = response.read()
                with open(outF, 'wb') as fl:
                    fl.write(data)
            except OSError as err:
                print(f'fail  {err}')
                pass

# user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# headers={'User-Agent':user_agent,} 
# url = 'https://www.supremecourt.gov/DocketPDF/22/22O155/163215/20201209144914203_2020.12.09%20Certificate%20of%20Service.pdf'
# req = urllib.request.Request(url,None,headers) #The assembled request
        
# response = urllib.request.urlopen(req)
# data = response.read()
# f = open('test.pdf','wb')
# f.write(data)
# f.close



