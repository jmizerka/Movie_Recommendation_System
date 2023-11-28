import sqlite3
import pandas as pd
from queries import *

def db_connector(func):
    def wrapper(*args,**kwargs):
        conn = sqlite3.connect('../../data/movies.db')
        cursor = conn.cursor()
        result = func(cursor,*args,**kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper

@db_connector
def show_all(cursor,query,params=None):

    if params:
        cursor.execute(query,params)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    df = pd.DataFrame(data,columns=column_names)
    return df

@db_connector
def remove(cursor,table,col,id):
    cursor.execute(f"DELETE FROM {table} WHERE {col} = ?;",(id,))
@db_connector
def update(cursor,table,col_name,value,cond):
    cursor.execute(f"UPDATE {table} SET {col_name} = ? WHERE {cond}",(value,))


@db_connector
def add_movie(cursor, title, date, original_lang, country, overview, score, genres):
    # Sprawdź, czy film o takim samym tytule i roku nie istnieje już w tabeli
    cursor.execute("SELECT COUNT(*) FROM movies WHERE title = ? AND date = ?", (title, date))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO movies (title, date, original_lang, country, overview, score) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, date, original_lang, country, overview, score))
        movie_id = cursor.lastrowid

        for genre_name in genres:
            cursor.execute("SELECT genre_id FROM genres WHERE genre_name = ?", (genre_name,))
            genre_id = cursor.fetchone()
            if genre_id:
                genre_id = genre_id[0]
                cursor.execute("INSERT INTO movies_genres (movie_id, genre_id) VALUES (?, ?)", (movie_id, genre_id))
            else:
                print(f"Uwaga: Gatunek {genre_name} nie istnieje w bazie danych.")
        print("Film został dodany.")
    else:
        print("Film o takim samym tytule i roku już istnieje.")

@db_connector
def add_actor_or_genre(cursor, params):
    if params[1] == 'actors':
        cursor.execute(f"SELECT COUNT(*) FROM {params[1]} WHERE actor_name = ?", (params[0],))
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO actors (actor_name) VALUES (?)", (params[0],))
    else:
        cursor.execute(f"SELECT COUNT(*) FROM {params[1]} WHERE genre_name = ?", (params[0],))
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (params[0],))

@db_connector
def add_rating(cursor,params):
    cursor.execute(f"INSERT INTO your_ratings (movie_title,rating,date) VALUES (?, ?, ?)", (params[0],params[1],params[2]))
