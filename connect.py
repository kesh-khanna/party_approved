from configparser import ConfigParser
import psycopg2


def config(filename='database.ini', section='postgresql'):
    """
    Read the database.ini file and return a dictionary of the parameters.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """
    Connect to the PostgreSQL database server, create tables if they don't exist and ensure that
    the connection is working as expected.
    Initate the datasets as required
    :return:
    """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        print("Creating tables if not exists")
        tables = ["""
        CREATE TABLE IF NOT EXISTS Users (
          Username VARCHAR(255) PRIMARY KEY
        );
        """,
                  """   
                  CREATE TABLE IF NOT EXISTS Playlists (
                    PlaylistID CHAR(22) PRIMARY KEY,
                    Username VARCHAR(255),
                    PlaylistName VARCHAR(255) NOT NULL,
                    Image VARCHAR(255),
                    Score FLOAT
                  );"""]

        for table in tables:
            cur.execute(table)

        # close the communication with the PostgreSQL
        cur.close()

        # commit the changes
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert_playlists(playlists, username):
    """
    Inserts playlists into the database from our API calls
    :param playlists: list of dictionaries with our playlist data
    :param username: cur user
    """
    sql = """ INSERT INTO Playlists (PlaylistID, Username, PlaylistName, Image, Score)
            VALUES(%s, %s, %s, %s, %s)
            ON CONFLICT (PlaylistID)
            DO UPDATE 
                SET Score = EXCLUDED.Score, Image = EXCLUDED.Image;"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for playlist in playlists:
            playlist_ID = playlist['id']
            playlist_Name = playlist['name']
            image = playlist['cover_image']
            score = playlist['pop']

            cur.execute(sql, (playlist_ID, username, playlist_Name, image, score))

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: " + str(error))
    finally:
        if conn is not None:
            conn.close()


def insert_user(username):
    """
    adds a user to the database if they don't already exist
    :param username: spotify username
    """
    sql = """INSERT IGNORE INTO Users (Username)
            VALUES(%s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (username,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_top_playlists(top_num=25):
    """
    returns the top playlists in the database sorted by popularity score
    :param top_num: cap of how many playlists to return
    :return: rows of our playlist as a list of tuples, to be converted upon return in app.py
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """SELECT Playlistname, Username, Score, Image
        FROM Playlists
        ORDER BY SCORE
        DESC LIMIT %s;"""
        cur.execute(sql, (top_num,))

        rows = cur.fetchall()

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()
    return rows


def refresh_playlist(playlist):
    """
    Updates the score of a playlist in the database if a user logs into our app after
    previously logging in and the playlist has changed in popularity.
    :param playlist: playlist dictionary
    """
    # Playlists passed must already be sorted
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """ UPDATE Playlists
        SET Score = %s
        WHERE PlaylistID = %s;"""

        cur.execute(sql, (playlist['pop'], playlist['id'],))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def clear_tables():
    """
    Clears the tables in the database for testing purposes
    :return:
    """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = """ DROP TABLE IF EXISTS Playlists;
        DROP TABLE IF EXISTS Users;"""

        cur.execute(sql)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
    connect()
