import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Insert records into songs and artists tables using data from a single song_data file."""
        
    # open song file
    df = pd.read_json(filepath,  lines=True) 

    # create song dataframe and  change the data to list
    song_data = df[["song_id","title",
                    "artist_id","year",
                    "duration"
                   ]].values.tolist()
    
    song_data = (song_data[0][0],song_data[0][1],
                 song_data[0][2],song_data[0][3],
                 song_data[0][4])
    
    # insert songplay record 
    try:
        cur.execute(song_table_insert, song_data)
    except psycopg2.Error as e: 
        print("Error:this line has corrupted data")
        print (e)
    
    # create artist dataframe
    artist_data = df[["artist_id", "artist_name", 
                      "artist_location", "artist_latitude", 
                      "artist_longitude"
                    ]].values.tolist()
    
    artist_data = (artist_data[0][0], artist_data[0][1], 
                   artist_data[0][2], artist_data[0][3], 
                   artist_data[0][4])
    
    # Change the data to list and run cur.execute to insert data
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """Insert records into time and user tables using data from a single log_data file."""
    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert datetime column to timestamp, hour, day,
    # weekofyear, month, year, weekday
    t =  pd.to_datetime(df['ts'], unit='ms')
    time_data_list = t.tolist()
    time_data_list2 = []
    for i in time_data_list:
        time_data_list2.append([i, i.hour, 
                                i.day,i.weekofyear,
                                i.month, i.year,
                                i.strftime('%A')
                               ])
    
    # Create time dataframe before insert time data records
    time_data = time_data_list2
    column_labels = (
            'timestamp','hour',
            'day','week_of_year',
            'month','year','weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels  )
    
    # Loop through each time row and insert into time table
    for i, row in time_df.iterrows():
        #print(list(row))
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame(df, columns=["userId","firstName", 
                                        "lastName","gender",
                                        "level"
                                       ])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Loop through each log files for data and insert songplay records
    for index, row in df.iterrows():
        # get songid and artistid from song and artist tables
        cur.execute(song_select,(row.song , row.artist ,row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None
        #print(songid + " "+ artistid)
        # insert songplay record
        songplay_data = ( 
                    t[index], row.userId, 
                    row.level,songid, artistid, 
                    row.sessionId , row.location, 
                    row.userAgent )
        
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
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
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()
    
    """ This line fix a encoding problem during the runtime """
    conn.set_client_encoding('UTF8')

     
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()