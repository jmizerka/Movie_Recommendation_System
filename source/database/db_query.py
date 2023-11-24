import sqlite3

def show_all(table):
    conn = sqlite3.connect('../../data/movies.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    items = cursor.fetchall()

    for item in items:
        print(item)
    conn.close()

for table in ['movies','genres']:
    show_all(table)