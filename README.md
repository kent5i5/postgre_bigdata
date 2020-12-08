# Project1 : Postgre database project 

###### In this project, I am to create star scheme ( fact + dimension tables) which is a better format for data wirehousing. It provides better query efficiency  as well as easy understand of the tables by forgoing some relation database requirements. 

***I follow the steps and finish etl.ipynb where I am able to create songs, artists, time, users tables***

    I want to explain time and songplays table 

* For time table, I need to convert the timestamp from log file to 'timestamp','hour','day','week_of_year','month','year','weekday'

    ```
    def process_log_file(cur, filepath):
        ...
         # convert timestamp column to datetime with panda
        t =  pd.to_datetime(df['ts'], unit='ms') 
        time_data_list = t.tolist()
        time_data_list2 = []
        for i in time_data_list:
            time_data_list2.append([i, i.hour, i.day,i.weekofyear,i.month, i.year,i.strftime('%A')])

        # tiem_data_list2 now has all data. Next, insert time_data_list2 into time table
        time_data = time_data_list2
        column_labels = ('timestamp','hour','day','week_of_year','month','year','weekday')
        time_df = pd.DataFrame(time_data, columns=column_labels  )
        
        ...
    ```

* For songplay table, I try to find the song and artist data with its length, song id, and get the rest of data from log file

    ```
    def process_log_file(cur, filepath):
        for index, row in df.iterrows():
            df = pd.read_json(filepath, lines=True) # log file contains everything except for song_id and artisti_id

            df = df.loc[df['page'] == 'NextSong'] # as requested, I filtered the file as the action 'NextSong'

            t =  pd.to_datetime(df['ts'], unit='ms') # t contains a list of timestamps from the log file. 
            ...
            songplay_data = ( t[index], row.userId, row.level,songid, artistid, row.sessionId , row.location, row.userAgent )
            cur.execute(songplay_table_insert, songplay_data)
    ```


***Each process_log_file and process_song_file run through one song_data file and one log_data file.***

***etl.py has big for loop covering evetyhing etl.ipyng does and repeat the same thing on all files.***
    ```
    def process_data(cur, conn, filepath, func):
          # iterate over files and process
        for i, datafile in enumerate(all_files, 1):
            func(cur, datafile)
            conn.commit()
            print('{}/{} files processed.'.format(i, num_files))
    ```

***func(cur, datafile) will run process_song_file or process_log_file based on the func argument***

***There are mirror issue such as string format. I added the follow to solve the problem.:***
    ```
    def main():
        conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
        cur = conn.cursor()  
        conn.set_client_encoding('UTF8')  
    ```
    
***I run both create_tables.py and etl.py successfully***

***I double check the data with test.ipynb and songplays has all the datas.***

    