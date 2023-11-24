import sqlite3
import pandas as pd

actors = pd.read_csv('../../data/separated_dfs/actors.csv')
genres = pd.read_csv('../../data/separated_dfs/genres.csv')
movies = pd.read_csv('../../data/separated_dfs/movies.csv')
movies_actors = pd.read_csv('../../data/separated_dfs/movies_actors.csv')
movies_genres = pd.read_csv('../../data/separated_dfs/movies_genres.csv')

conn = sqlite3.connect('../../data/movies.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")


# create database schema
tables_script = """
    CREATE TABLE movies (
        movie_id INTEGER PRIMARY KEY,
        title TEXT,
        date TEXT,
        original_lang TEXT,
        country TEXT,
        overview TEXT,
        score REAL);
    CREATE TABLE genres (
        genre_id INTEGER PRIMARY KEY,
        genre_name TEXT
    );
    CREATE TABLE movies_genres (
        movie_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    );
    CREATE TABLE actors (
        actor_id INTEGER PRIMARY KEY,
        actor_name TEXT
    );
    CREATE TABLE movies_actors(
        movie_id INTEGER,
        actor_id INTEGER,
        PRIMARY KEY (movie_id,actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
    );
        """

cursor.executescript(tables_script)
movies.to_sql('movies',conn,index=False,if_exists='replace')
genres.to_sql('genres',conn,index=False,if_exists='replace')
actors.to_sql('actors',conn,index=False,if_exists='replace')
movies_actors.to_sql('movies_actors',conn,index=False,if_exists='replace')
movies_genres.to_sql('movies_genres',conn,index=False,if_exists='replace')
conn.commit()

conn.close()






