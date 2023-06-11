# party_approved
DIS final project, KU Spring 2023
## Usage:
The Party Approved (PA) website allows users to rank their public Spotify playlist against their own playlists and playlists of other users who have submitted it to the website, in two tables: User playlist and Global leader board.
The schema of the database and website is that given the submitted Spotify username the 10 most recent playlists are submitted to the global database with an estimated popularity score, playlist cover and playlist ID as the primary key for the database and updating the user to the user list.
The key technologies utilised for this project is the spotifyAPI, Postgres and Flask.
The associated ER diagram for this database structuer is provided in the diagrams folder.


## Requirements:
Run the following code to install the necessary modules
> $ pip install -r requirements.txt

## Database initialisation:
To initialise the database, firstly create a new database in postgres, then create the file database.ini, this file should include the following:

[postgresql]
host=localhost
database= {DATABASE NAME}
user=postgres
password= {USER PASSWORD}

## SpotifyAPI authorization:
For Spotify authorisation, follow the instructions given on Spotify Developer and create an app. Once the app is created continue to the app dashboard, then settings, this will provide a client ID and a client secret. Create the file .env, which should include the following:

CLIENT_ID = '{CLIENT ID}'
CLIENT_SECRET = '{CLIENT SECRET}'

Note: This step is only required for app.py. Offline data is available for use with app_tester.py that doesn’t require the spotifyAPI.


## Running the program
### with SpotifyAPI authorization:
To launch the program, run app.py, then follow to the local web address. Here the user will be prompted to enter a Spotify username and select 'subimt'. Once submitted, the user will be able to see their 10 most recent playlists ordered by the popularity score and a global leader board of the top 25 ranked playlists. 

If the user does not wish to submit their spotify account and playlists, they can view the existing global leaderboard by selecting the 'View Global Leaderboard'.

If the user wishes to submit another spotify account or resubmit the current account, navigate back to the inital landing page and following the same prompts. If the user has changed any of their playlists this will be relfected by the upated popularilty score and potental ranking in the top 25.


### without SpotifyAPI authorization:
To launch the program, run app_tester.py, then follow to the webpage app instructions as detailed for with the spotifyAPI authorization. With the exception for the accesability of spotify data, as when promtpted to enter a Spotify username, the test version of the PA webapp, will only allow users to input the following usernames:
>t8dirk2ywdhlc05rskt372atf
>raef100
>9amest
As a test version of the program that doesn't require the spotify Authorization, the data for these spotify accounts is provided in testing_data.csv. The user will not be able to get live data from spotify about the accounts and assosciated playlists. I.e. the user will not be able to test features such as "re-submitting" playlist to observe any score/ranking changes once a playlist is changed by a user in spotify.


## Further developement/ Concluding comments

The PA webapp successfully delivers on integrating spotifyAPI with SQL to collect and compare users playlists. Further development of this webapp could involve greater data manipulation, such as creating a ranking and leader board for the users of the app, where users would be sorted by either their average or overall grade. Another possible inclusion is the ranking of songs in each users playlists, thus a user can see what specific songs are associated with giving their playlist a higher or lower score. Either of these added features would be a beneficial to the webapp, however given the time restriction and project scope were not implemented. 
