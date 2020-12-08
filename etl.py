import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
     """Insert records into songs and artists tables using data from a single song_data file."""
    
    # open song file 
    df = pd.read_json(filepath,  typ='serious')

    # insert song record
    song_data = pd.DataFrame(df, index=["song_id","title","artist_id", "year", "duration"] )
    song_data = song_data.values.tolist()
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e: 
        print("Error:this line has corrupted data")
        print (e)
    
    # insert artist record
    artist_data = pd.DataFrame(df, index=['artist_id', 'artist_name', 'artist_location', 'artist_latitude ', 'artist_longitude'])
    artist_data = artist_data.values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Insert records into dimension tables time,user tables and the fact table-songplays using data from a single log_data file."""
    
    # open log file - log file contains everything except for song_id and artisti_id
    df = pd.read_json(filepath, lines=True) 

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t =  pd.to_datetime(df['ts'], unit='ms')
    time_data_list = t.tolist()
    time_data_list2 = []
    for i in time_data_list:
        time_data_list2.append([i, i.hour, i.day,i.weekofyear,i.month, i.year,i.strftime('%A')])
    
    # insert time data records
    time_data = time_data_list2
    column_labels = ('timestamp','hour','day','week_of_year','month','year','weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels  )
    
    #Insert data intothe time table with a loop since we have more than 1 row
    for i, row in time_df.iterrows():
        #print(list(row))
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame(df, columns=["userId","firstName", "lastName","gender","level"])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        # (row.song and row.artist and row.length):
   
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, str(row.length)))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = ( t[index], row.userId, row.level,songid, artistid, row.sessionId , row.location, row.userAgent )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Retrieve files path as a list-all_files and iterate through each file with both process_log_file and process_song_file mehtod
        Parameters:
        cur: the cursor of postgre database
        conn: postgre database connection
        filepath: log/song files location
        func: name of the function: process_song_file/process_log_file
        
        Ouput:
        Fact table: singplays 
        Dimension table: time, users, songs, artists
    
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    cur = conn.cursor()
    conn.set_client_encoding('UTF8') # enforced the encode of string with UTF8

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()