# DROP TABLES

songplay_table_drop = "DROP table songplay"
user_table_drop = "DROP table users"
song_table_drop = "DROP table songs"
artist_table_drop = "DROP table artists"
time_table_drop = "DROP table time"

# CREATE TABLES

songplay_table_create = "CREATE TABLE IF NOT EXISTS songplay(songplay_id SERIAL PRIMARY KEY, start_time text ,user_id text, level text, song_id text, artist_id text, session_id int, location text, user_agent text)"

user_table_create = "CREATE TABLE IF NOT EXISTS users (user_id int, first_name text, last_name text, gender text, level int)"

song_table_create = "CREATE TABLE IF NOT EXISTS songs (song_id text, title text, artist_id text, year text, duration text)"

artist_table_create = "CREATE TABLE IF NOT EXISTS artists(artist_id text, artist_name text, location text, latitude float[], longitude float[])"

time_table_create = "CREATE TABLE IF NOT EXISTS time (start_time text, hour int, day int, week int, month text, year text, weekday text)"


# INSERT RECORDS

songplay_table_insert = "INSERT INTO songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)"

user_table_insert = "INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s ,%s ,%s, %s)"

song_table_insert = "INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s,%s, %s, %s, %s) "

artist_table_insert = "INSERT INTO artists (artist_id, artist_name, location, latitude, longitude) VALUES (%s, %s ,%s ,%s, %s)"


time_table_insert ="INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s,%s, %s ,%s ,%s, %s,%s) "

# FIND SONGS

song_select = "SELECT  a.song_id , b.artist_id FROM songs as a JOIN artists as b ON a.artist_id = b.artist_id WHERE title=(%s) AND artist_name=(%s) AND duration=(%s)"

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]