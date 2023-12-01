import sqlite3
import pandas as pd

actors = pd.read_csv('../../data/separated_dfs/actors.csv')
genres = pd.read_csv('../../data/separated_dfs/genres.csv')
movies = pd.read_csv('../../data/separated_dfs/movies.csv')
movies_actors = pd.read_csv('../../data/separated_dfs/movies_actors.csv')
movies_genres = pd.read_csv('../../data/separated_dfs/movies_genres.csv')

conn = sqlite3.connect('../../data/movies.db')
cursor = conn.cursor()

# create database schema
tables_script = """
    CREATE TABLE movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        date TEXT,
        original_lang TEXT,
        country TEXT,
        overview TEXT,
        score REAL);
    CREATE TABLE genres (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT
    );
    CREATE TABLE movies_genres (
        movie_id INTEGER,
        genre_id INTEGER,
        PRIMARY KEY (movie_id, genre_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
    );
    CREATE TABLE actors (
        actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor_name TEXT
    );
    CREATE TABLE movies_actors(
        movie_id INTEGER,
        actor_id INTEGER,
        PRIMARY KEY (movie_id,actor_id),
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE,
        FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
    );
    CREATE table your_ratings(
        movie_title TEXT,
        rating REAL,
        date TEXT);
        """

cursor.executescript(tables_script)
movies.to_sql('movies',conn,index=False,if_exists='append')
genres.to_sql('genres',conn,index=False,if_exists='append')
actors.to_sql('actors',conn,index=False,if_exists='append')
movies_genres.to_sql('movies_genres',conn,index=False,if_exists='append')
movies_actors.to_sql('movies_actors',conn,index=False,if_exists='append')

conn.commit()

conn.close()






