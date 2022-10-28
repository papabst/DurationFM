# DurationFM
import pandas

API_KEY = 'd4277889b2fd629b518c0a575d91360d'
USER_AGENT = 'DurationFM'
# Shared secret 	3d253aa982ee9f02d22629b058e1b205


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================

import json
import pandas as pd
import requests
import openpyxl
import requests_cache
from requests_cache import CachedSession
import time
import datetime
from IPython.core.display import clear_output



#f = open('the-patient_lb-2022-09-24.json')
#data = json.load(f)
#whatevs = pd.read_json('the-patient_lb-2022-09-24.json', orient='records')
#whatevs = pd.read_json('test_json.json', orient='records')

#detailed = whatevs['track_metadata'].to_json('test_json.json')
#detailedjson = pd.read_json(detailed)
#print(detailed)
#whatevs.to_csv('test_csv.csv')
#whatevs.to_excel("test_excel.xlsx")
#r = requests.

# ==============================================================================
# -- Functions -----------------------------------------------------------------
# ==============================================================================

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================

def main():
    session = CachedSession()
    #print(session.cache.urls)
    #session.cache.clear()

    # remove when done debugging
    #if not requests_cache.is_installed():
    requests_cache.install_cache()

    list_df = {
        'list_dfmid': [],
        'track_name': [],
        'track_mbid': [],
        'track_lfmid': [],
        'artist_name': [],
        'artist_mbid': [],
        'album_name': [],
        'album_mbid': [],
        'images_s': [],
        'images_m': [],
        'images_l': [],
        'images_xl': [],
        'count': [],
        'duration': [],
        'isrc': []
    }

    date_df = {
        'date_dfmid': [],
        'date_utc': []
    }

    responses = []
    durationfmid = 1
    page = 1
    total_pages = 2 # this is just a dummy number so the loop starts
    payload = {
        'method': 'user.getRecentTracks',
        # 'limit': 500,
        'user': 'the-patient666',
        'extended': '0',
        'page': page
    }

    while page <= total_pages:

        # print some output so we can see the status
        print("Requesting page {}/{}".format(page, total_pages))
        # clear the output to make things neater
        clear_output(wait = True)

        # make the API call
        response = lastfm_get(payload)
        jprint(response.json())

        # if we get an error, print the response and halt the loop
        if response.status_code != 200:
            print(response.text)
            break

        # extract pagination info
        #page = int(response.json()['recenttracks']['@attr']['page'])
        #total_pages = int(response.json()['recenttracks']['@attr']['totalPages']) # wieder einkommentieren

        # append response
        responses.append(response)
        #df = pd.DataFrame(response.json()['recenttracks']['track'])



        for t in response.json()['recenttracks']['track']:
            if t['mbid'] not in list_df['track_lfmid'] or len(t['mbid']) == 0:
                list_df['list_dfmid'].append(durationfmid)
                list_df['track_name'].append(t['name'])
                list_df['track_lfmid'].append(t['mbid'])
                list_df['artist_name'].append(t['artist']['#text'])
                list_df['artist_mbid'].append(t['artist']['mbid'])
                list_df['album_name'].append(t['album']['#text'])
                list_df['album_mbid'].append(t['album']['mbid'])
                list_df['images_s'].append(t['image'][0]['#text'])
                list_df['images_m'].append(t['image'][1]['#text'])
                list_df['images_l'].append(t['image'][2]['#text'])
                list_df['images_xl'].append(t['image'][3]['#text'])
                list_df['count'].append(1)

                date_df['date_dfmid'].append(durationfmid)
                durationfmid += 1

                list_df['track_mbid'].append('dummy')
                list_df['duration'].append('dummy')
                list_df['isrc'].append('dummy')

            else:
                df_index = list_df['track_lfmid'].index(t['mbid'])
                list_df['count'][df_index] += 1
                date_df['date_dfmid'].append(list_df['list_dfmid'][df_index])

            date_df['date_utc'].append(t['date']['uts'])

        # if it's not a cached result, sleep
        if not getattr(response, 'from_cache', False):
            time.sleep(0.25)

        # increment the page number
        page += 1
        payload.update({'page': page})

    test = 3
    finalbreakpoint = test + 1
    #df = pd.DataFrame(list_df)


    #tracks = pd.concat(frames)
    #tracks = tracks.drop(['artist', 'streamable', 'image', 'album', 'url', 'date'], axis=1)
    #tracks.head()
    #tracks.info()
    #tracks.describe()
    #track_counts = [len(r.json()['recenttracks']['track']) for r in responses]
    #pd.Series(track_counts).value_counts()
    tracks = pandas.DataFrame.from_dict(list_df)
    tracks.to_csv('tracks.csv')

if __name__ == '__main__':

    main()
