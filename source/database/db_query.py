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
pd.set_option('display.expand_frame_repr', False)

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
def add_actor(cursor, actor_name):
    # Sprawdź, czy aktor o takim samym imieniu nie istnieje już w tabeli
    cursor.execute("SELECT COUNT(*) FROM actors WHERE actor_name = ?", (actor_name,))
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.execute("INSERT INTO actors (actor_name) VALUES (?)", (actor_name,))
        actor_id = cursor.lastrowid
        print("Aktor został dodany.")
    else:
        print("Aktor o takim samym imieniu już istnieje.")
