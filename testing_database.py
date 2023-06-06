import psycopg2

hostname = 'localhost'
database = 'PartyApprovedPlaylist'
username = 'postgres'
pwd = 'jazz'
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(host=hostname, user=username, password=pwd, dbname=database, port=port_id)
    cur = conn.cursor()

    create_script_2 = '''CREATE TABLE IF NOT EXISTS users (
        user_id CHAR(22) PRIMARY KEY,
        USERNAME VARCHAR(50)
    )'''


    create_script = '''CREATE TABLE IF NOT EXISTS playlist (
        playlist_id CHAR(22) PRIMARY KEY,
        playlist_name VARCHAR(50),
        user_id CHAR(22) REFERENCES users (user_id),
        score FLOAT,
        Image VARCHAR(255)
    )'''
   
    cur.execute(create_script_2)
    cur.execute(create_script)
    

    insert_script = '''INSERT INTO playlist (playlist_id, playlist_name, owner_name, score) VALUES (%s, %s, %s, %s)'''
    #insert_value = ('1', 'test', 'test', 1.0) # TESTING


    #cur.exe

    #cur.execute(insert_script, insert_value) 
except Exception as error:
    print(error)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()