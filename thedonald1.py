import json
import glob, os

# Taken from : https://pastebin.com/Q6nTP04N
 
csv_content="state,timestamp,votes,eevp,trumpd,bidenj\r\n"
 
#read json files
for file in glob.glob("states/*.json"):
    with open(file, encoding="utf8") as f:
        x = json.load(f)        
    xts = x["data"]["races"][0]["timeseries"]
    for i in range(len(xts)):
        csv_content=csv_content+f'{file[7:-5]},{xts[i]["timestamp"]},{xts[i]["votes"]},{xts[i]["eevp"]},{xts[i]["vote_shares"]["trumpd"]},{xts[i]["vote_shares"]["bidenj"]}\r\n'
 
#write csv table
with open('thedonald/theresult.csv', 'w', newline='') as f:
    f.write(csv_content)
    
    
    