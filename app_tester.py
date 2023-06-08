import os

from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from connect import *
import csv

app = Flask(__name__)

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

    # get test playlists for the user given
    playlists = get_user_playlists(username)

    if playlists is None:
        print("User not found")
        return render_template('index.html')

    # Insert username into database
    insert_user(username)
    # Insert playlist into database
    insert_playlists(playlists, username)

    # get the top 25 global playlists from the database
    rows = get_top_playlists()
    global_playlists = []
    for row in rows:
        global_playlists.append({'name': row[0], 'user': row[1], 'pop': row[2], 'cover_image': row[3]})

    return render_template('full_leaderboard.html', username=username, playlists=playlists,
                           global_playlists=global_playlists)


def get_user_playlists(username):
    """
    Get the test playlists for the user given, from our static testing_data.csv file
    :return: playlist dictionary in our format
    """
    data = open('testing_data.csv', 'r')
    reader = csv.reader(data)
    playlists = []
    for row in reader:
        if row[1] == username:
            playlists.append({'name': row[0], 'user': row[1], 'pop': row[2], 'cover_image': row[3], 'id': row[4]})
    return playlists


if __name__ == '__main__':
    app.run(debug=True)
