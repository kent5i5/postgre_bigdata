# Project1 : Postgre database project 

* In this project, I am to create star scheme ( fact + dimension tables) which is a better format for data wirehouse.

* It provides better query efficiency  as well as easy understand of the tables by forgoing some relation database requirements. 

* I follow the steps and finish etl.ipynb where I am able to create songs, artists, time, users tables

* ***During the process, etl.ipynb have problem to renew sql_queries so I copy all create and insert queries over to etl.ipynb***


* For songplay table, I try to find the song and artist data with its length, song id, and artiest id. 

* I didn't enter any data into songplay table if there are no match for the single song in a log_data file.

* The end result is that It ran through one song_data file and one log_data file. 

* etl.py has big for loop covering evetyhing etl.ipyng does and repeat the same thing on all files.

* etl.py will read  process_song_file 

* There are mirror issue such as string format. I added conn.set_client_encoding('UTF8') to solve the problem.

* I ran etl.py with python etl.py command and finish the run.

* I double check the data with test.ipynb and songplays has all the datas.


    