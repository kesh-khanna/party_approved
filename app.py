from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('leaderboard', username=username))
    return render_template('index.html')


@app.route('/leaderboard/<username>')
def leaderboard(username):
    # make calls to the Spotify API HERE
    # Replace the code below with actual implementation
    playlists = [
        {'name': 'Playlist 1', 'rank': 1},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 2', 'rank': 2},
        {'name': 'Playlist 3', 'rank': 3}
    ]
    return render_template('leaderboard.html', username=username, playlists=playlists)


if __name__ == '__main__':
    app.run(debug=True)
