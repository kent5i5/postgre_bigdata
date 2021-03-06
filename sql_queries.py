# DROP TABLES

songplay_table_drop = "DROP TABLE if EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = "CREATE TABLE IF NOT EXISTS songplays(songplay_id SERIAL PRIMARY KEY, start_time text NOT NULL,user_id text NOT NULL, level text NOT NULL, song_id text , artist_id text, session_id int NOT NULL, location text, user_agent text)"

user_table_create = "CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, first_name text , last_name text , gender text, level text)"

song_table_create = "CREATE TABLE IF NOT EXISTS songs (song_id text PRIMARY KEY, title text NOT NULL, artist_id text, year text, duration float)"

artist_table_create = "CREATE TABLE IF NOT EXISTS artists(artist_id text PRIMARY KEY, artist_name text NOT NULL, location text, latitude float, longitude float)"

time_table_create = "CREATE TABLE IF NOT EXISTS time (start_time text PRIMARY KEY, hour int, day int, week int, month text, year text, weekday text)"


# INSERT RECORDS

songplay_table_insert = "INSERT INTO songplays (start_time , user_id, level, song_id, artist_id,session_id, location, user_agent ) VALUES (%s,%s,%s,%s, %s,%s, %s,%s) "

user_table_insert = "INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s ,%s ,%s, %s) ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level"

song_table_insert = "INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s,%s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING"

artist_table_insert = "INSERT INTO artists (artist_id, artist_name, location, latitude, longitude) VALUES (%s, %s ,%s ,%s, %s) ON CONFLICT (artist_id) DO NOTHING"


time_table_insert ="INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s,%s, %s ,%s ,%s, %s,%s) ON CONFLICT (start_time) DO NOTHING "

# FIND SONGS

# song_select = "SELECT  a.song_id , b.artist_id FROM songs as a JOIN artists as b ON a.artist_id = b.artist_id WHERE title=(%s) OR artist_name=(%s) OR duration=(%s)"
song_select = ("""select songs.song_id, artists.artist_id from songs join artists on(songs.artist_id = artists.artist_id)where songs.title = %s AND artists.artist_name = %s AND songs.duration = %s;""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]