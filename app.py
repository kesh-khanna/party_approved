import os

from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from connect import *
import csv

app = Flask(__name__)

load_dotenv(".env")

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Set up Spotipy client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Flask stuff...

@app.route('/')
def index():
    """
    Flask route for the index page
    :return:
    """
    return render_template('index.html')


@app.route('/leaderboard', methods=['POST'])
def leaderboard():
    """
    Flask route for the leaderboard page
    :return:
    """
    # # Refresh Tables
    # clear_tables()
    # # Initalise databases
    connect()

    # Regular Flask stuff
    username = request.form['username']
    playlists = get_user_playlists(username)
    sorted_playlists = sort_playlists_by_pop(playlists)

    # Insert username into database -- working
    insert_user(username)
    # Insert playlist into database -- working for 0amest not 22sadawwaw77gdas
    insert_playlists(playlists, username)
    # get the top 25 global playlists from the database
    rows = get_top_playlists()
    global_playlists = []
    for row in rows:
        global_playlists.append({'name': row[0], 'user': row[1], 'pop': row[2], 'cover_image': row[3]})

    return render_template('full_leaderboard.html', username=username, playlists=sorted_playlists,
                           global_playlists=global_playlists)


def get_user_playlists(username):
    """
    Get the test playlists for the user given, from the Spotify API
    :return:
    """
    playlists = []
    results = sp.user_playlists(username)

    while results:
        for playlist in results['items']:
            playlists.append(playlist)
            if len(playlists) >= 10:
                break
        if results['next']:
            results = sp.next(results)
        else:
            results = None

    return playlists


def sort_playlists_by_pop(playlists):
    """
    Sort the playlists by spotify popularity metric
    :param playlists:
    :return:
    """
    sorted_playlists = []

    for playlist in playlists:
        playlist_id = playlist['id']
        playlist['pop'] = calculate_playlist_pop(playlist_id)
        playlist['cover_image'] = get_playlist_cover_image(playlist_id)
        sorted_playlists.append(playlist)

    sorted_playlists.sort(key=lambda x: x['pop'], reverse=True)
    return sorted_playlists


def calculate_playlist_pop(playlist_id):
    """
    Calculate the average popularity of the tracks in the playlist
    :param playlist_id:
    :return:
    """
    tracks = sp.playlist_items(playlist_id)['items']
    if len(tracks) == 0:
        return 0

    pop_sum = 0
    num_tracks = 0

    for track in tracks:
        if track is not None and track['track'] is not None:
            pop = track['track']['popularity']
            pop_sum += pop
            num_tracks += 1

    if num_tracks > 0:
        average_popularity = round(pop_sum / num_tracks, 2)
        return average_popularity
    else:
        return 0


def get_playlist_cover_image(playlist_id):
    """
    Get the cover image URL for the playlist
    """
    playlist = sp.playlist(playlist_id, fields='images')
    if 'images' in playlist and len(playlist['images']) > 0:
        return playlist['images'][0]['url']
    else:
        return None


if __name__ == '__main__':
    app.run(debug=True)
