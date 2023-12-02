import sqlite3
import pandas as pd
from source.database.queries import *

# decorator to handle database connection and cursor management
def db_connector(func):
    def wrapper(*args, **kwargs):
        # establish connection to sqlite database
        conn = sqlite3.connect('data/movies.db')
        cursor = conn.cursor()

        # execute action
        result = func(cursor, *args, **kwargs)

        # commiting changed and closing
        conn.commit()
        conn.close()
        return result

    return wrapper

# function to execute a query and return the result as dataframe
@db_connector
def show_all(cursor, query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    df = pd.DataFrame(data, columns=column_names)
    return df


@db_connector
def remove(cursor, params):
    cursor.execute(f"DELETE FROM {params[0]} WHERE {params[1]} = ?;", (params[2],))


# update data in a table based on condition
@db_connector
def update(cursor, params):
    cursor.execute(f"UPDATE {params[0]} SET {params[1]} = ? WHERE {params[3]}", (params[2],))


@db_connector
def add_movie(cursor, params):
    cursor.execute("SELECT COUNT(*) FROM movies WHERE title = ? AND date = ?", (params[0], params[1]))
    count = cursor.fetchone()[0]
    print(count)
    # check if entered movie is already in the database
    if count == 0:
        # if not, insert record
        cursor.execute(
            "INSERT INTO movies (title, date, original_lang, country, overview, score) VALUES (?, ?, ?, ?, ?, ?)",
            (params[0], params[1], params[2], params[3], params[4], params[5],))
        movie_id = cursor.lastrowid

        # add genres to genres table
        for genre_name in params[6].split(','):
            cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre_name,))
            genre_id = cursor.fetchone()
            if genre_id:
                genre_id = genre_id[0]
                cursor.execute("INSERT INTO movies_genres (movie_id, genre_id) VALUES (?, ?)", (movie_id, genre_id))
            # skip if the genre already is in the database
            else:
                print(f"Warning: Genre {genre_name} does not exists in the database")
        print("Movie added")
    else:
        print("A movie with same title and release year already exists.")

@db_connector
def add_actor(cursor, params):
    cursor.execute(f"SELECT COUNT(*) FROM actors WHERE actor_name = ?", (params[0],))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO actors (actor_name) VALUES (?)", (params[0],))

@db_connector
def add_genre(cursor, params):
    cursor.execute(f"SELECT COUNT(*) FROM genres WHERE genre_name = ?", (params[0],))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (params[0],))


# function to store user's movie ratings
@db_connector
def add_rating(cursor, params):
    cursor.execute(f"INSERT INTO your_ratings (movie_title,rating,date) VALUES (?, ?, ?)",
                   (params[0], params[1], params[2]))


# dictionary to store queries and their corresponding parameters
query_dict = {
    'all_actors': {'query': show_all(ALL_ACTORS), 'parameter_name': None},
    'all_movies': {'query': show_all(ALL_MOVIES), 'parameter_name': None},
    'all_genres': {'query': show_all(ALL_GENRES), 'parameter_name': None},
    'actors_stats': {'query': show_all(ACTOR_STATS), 'parameter_name': None},
    'all_movies_actor': {'query':  MOVIES_OF_ACTOR, 'parameter_name': ('actor_name',)},
    'all_actors_movie': {'query': ACTORS_IN_MOVIE, 'parameter_name': ('title',)},
    'all_movies_genre': {'query': MOVIES_OF_GENRE, 'parameter_name': ('genre_name',)},
    'movie_info': {'query': MOVIE_BY_TITLE, 'parameter_name': ('movie_title',)},
    'movies_from_year': {'query': MOVIES_OF_YEAR, 'parameter_name': ('release_year',)},
    'highest_rated': {'query': show_all(HIGHEST_RATED), 'parameter_name': None},
    'lowest_rated': {'query': show_all(LOWEST_RATED), 'parameter_name': None},
    'num_movies_genre': {'query': show_all(NUM_MOVIES_BY_GENRE), 'parameter_name': None},
    'avg_score_genre': {'query': show_all(AVG_RATE_BY_GENRE), 'parameter_name': None},
    'avg_score_actor': {'query': show_all(AVG_RATE_BY_ACTOR), 'parameter_name': None},
    'new_actor': {'query': add_actor, 'parameter_name': ('actor_name',)},
    'new_genre': {'query': add_genre, 'parameter_name': ('genre_name',)},
    'new_movie': {'query': add_movie, 'parameter_name': ('title', 'date', 'original_lang',
                                                         'country', 'overview', 'score', 'genres',)},
    'remove_data': {'query': remove, 'parameter_name': ('table_name', 'col', 'id',)},
    'update_data': {'query': update, 'parameter_name': ('table_name', 'col_name', 'value', 'condition',)},
    'custom': {'query': show_all, 'parameter_name': ('query',)}}
