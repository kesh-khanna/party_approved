from dotenv import load_dotenv
import os
import base64
import requests
from requests import post
import json
from statistics import mean 

# Tutorial from https://www.youtube.com/watch?v=WAmEZBEeNmg

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8") 

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Counter-Type": "application/x-www-form-urlencoded"
    } 
    data = {"grant_type": "client_credentials"}
    results = post(url, headers=headers, data=data)
    json_results = json.loads(results.content)
    token = json_results["access_token"]
    return token 

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_playlists(token, playlist_name):
    url = 'https://api.spotify.com/v1/search'
    header = get_auth_header(token)


    param = {
        'q': playlist_name,
        'type': 'playlist',
        'limit': 1  # Limit the results to 1 playlist
    }

    result = requests.get(url, headers=header, params=param)
    json_result = json.loads(result.content)
    return json_result

def get_user_id(token):
    url = 'https://api.spotify.com/v1/me'
    header = get_auth_header(token)

    result = requests.get(url, headers=header)
    if result.status_code == 200:
        data = result.json()
        spotify_id = data['id']
        return spotify_id
    else:
        print("Error: " + str(result.status_code) + ' - ' + result.text)
        return None


def get_users_playlist(token, user_id):

    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    header = get_auth_header(token)
    param = {
        'limit': 10,
        'offset': 5
    }

    result = requests.get(url, headers=header, params=param)
    json_result = json.loads(result.content)
    return json_result


def get_playlist_tracks(token, playlist_id):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    header = get_auth_header(token)
    param = {
        'limit': 10,
        'offset': 5
    }

    result = requests.get(url, headers=header, params=param)
    json_result = json.loads(result.content)
    return json_result

def get_tracklist_array(tracklist):
    track_ids = []
    for track in tracklist['items']:
        track_ids.append(track['track'])
    
    return track_ids

def get_track_dance_energy(token, track_id):
    url = f'https://api.spotify.com/v1/audio-features/{track_id}'
    header = get_auth_header(token)
    result = requests.get(url, headers=header)
    json_result = json.loads(result.content)
    dance = json_result['danceability']
    energy = json_result['energy']
    loudness = json_result['loudness']
    return dance, energy, loudness



token = get_token()
playlist = search_playlists(token, "Cordae: The Complete Collection")
#print("Name: ", playlist['playlists']['items'][0]['name'])
#print("Author: ", playlist['playlists']['items'][0]['owner']['display_name'])
playlist_id = playlist['playlists']['items'][0]['id']
#print("Playlist Id: ", playlist_id)
tracklist = get_playlist_tracks(token, playlist_id)
track_in_array = get_tracklist_array(tracklist)


playlist_rating = []
for track in track_in_array:
    pop = track['popularity']/100
    dance, energy, loudness = get_track_dance_energy(token, track['id'])
    # print(pop, dance, energy, loudness)
    rating = (pop + dance + energy) / 4
    playlist_rating.append(rating)

print(mean(playlist_rating))

#print(track_in_array[0]['id'])

