import pandas as pd
import pprint
import requests
import json
import os.path

# Taken from this thread on Twitter: https://twitter.com/APhilosophae/status/1325592240194981888
# I've fixed it up for Python 3.0 and added some logic so it only hits the NYTimes website once
# Saving the raw data as it goes along. There's some duplications.

def collapse_results_by_party(results_by_candidate, candidates):
    results_by_party = {}
    for candidate, count in results_by_candidate.items():
        party = candidates[candidate]['party']
        results_by_party[party] = results_by_party.get(party, 0) + count

    return results_by_party



states = [
 'Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California', 'Colorado',
 'Connecticut', 'Delaware', 'Florida', 'Georgia',
 'Hawaii', 'Iowa', 'Idaho', 'Illinois', 'Indiana', 'Kansas', 'Kentucky',
 'Louisiana', 'Massachusetts', 'Maryland', 'Maine', 'Michigan',
 'Minnesota', 'Missouri', 'Mississippi', 'Montana', 'North Carolina',
 'North Dakota', 'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico',
 'Nevada', 'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
 'Utah', 'Virginia', 'Vermont', 'Washington', 'Wisconsin',
 'West Virginia', 'Wyoming',
]

all_results = {}
all_senate_results = {}
folders = ['data','senate','states']
for fol in folders:
    if not os.path.exists(fol):
        os.mkdir(fol)

reload = True

if os.path.exists('data/all_results.json') and not reload:
    with open('data/all_results.json') as fl:
        all_results = json.load(fl)
else:
    for state in states:
        print(f'Downloading Presidential Results {state}')
        formatted_state = state.lower().replace(' ', '-')
        urlToGet = f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{formatted_state}/president.json'
        state_results = requests.get(urlToGet).json()
        all_results[formatted_state] = state_results

        with open(f'states/{state}.json', 'w') as jsfile:
            json.dump(state_results, jsfile, indent=2) 

        print(f'Downloading Senate Results {state}')
        urlToGet = f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/race-page/{formatted_state}/senate.json'
        r = requests.get(urlToGet)
        if r.status_code == 200:
            state_results = r.json()
            all_senate_results[formatted_state] = state_results
            with open(f'senate/{state}.json', 'w') as jsfile:
                json.dump(state_results, jsfile, indent=2) 


        
    with open(f'data/all_results.json', 'w') as jsfile:
        json.dump(all_results, jsfile, indent=2)
    with open(f'data/all_senate_results.json', 'w') as jsfile:
        json.dump(all_senate_results, jsfile, indent=2)
    
    
    
    

records = []
for state, state_results in all_results.items():
    race = state_results['data']['races'][0]

    for candidate in race['candidates']:
        if candidate['party_id'] == 'republican':
            candidate['party'] = 'rep'
        elif candidate['party_id'] == 'democrat':
            candidate['party'] = 'dem'
        else:
            candidate['party'] = 'trd'
    candidates = { candidate['candidate_key']: candidate for candidate in race['candidates'] }

    for data_point in race['timeseries']:
        data_point['state']             = state
        data_point['expected_votes']    = race['tot_exp_vote']
        data_point['trump2016']         = race['trump2016']
        data_point['votes2012']         = race['votes2012']
        data_point['votes2016']         = race['votes2016']

        vote_shares = collapse_results_by_party(data_point['vote_shares'], candidates)
        for party in ['rep', 'dem', 'trd']:
            data_point['vote_share_{}'.format(party)] = vote_shares.get(party, 0)

        data_point.pop('vote_shares')
        records.append(data_point)

time_series_df = pd.DataFrame.from_records(records)
time_series_df.to_csv('data/nyt_ts.csv', encoding='utf-8')