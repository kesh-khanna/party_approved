from configparser import ConfigParser
import psycopg2


def config(filename='database.ini', section='postgresql'):
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
    """ Connect to the PostgreSQL database server """
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


def insert_playlists(playlists):
    for playlist in playlists:
        insert_playlist(playlist)

def insert_playlist(playlists):
    sql = """ INSERT INTO Playlists (PlaylistID, Username, PlaylistName, Image, Score)
            VALUES(%s, %s, %s, %s, %s);"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        for playlist in playlists:

            playlist_ID = playlist['id']
            Username_char = playlist['owner']['display_name']
            playlist_Name = playlist['name']
            image = 000000000000
            score = playlist['pop']

            cur.execute(sql, (playlist_ID, Username_char, playlist_Name, image, score))
        #cur.execute(sql, ('22zlrw75elsb2d2i3ftjdybly', 'asdasd', 'asdasd', 0, 2))

        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_user(username):
    sql = """INSERT INTO Users (Username)
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


if __name__ == '__main__':
    connect()