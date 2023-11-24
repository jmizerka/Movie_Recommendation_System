import pandas as pd
import numpy as np

def encode(column, unique_values, id_column_name):
    encoded_column = column.astype(str)
    temp_list = []

    for i in encoded_column:
        i.replace(',\xa0',',')
        values = i.split(',')
        ids = [str(unique_values.index[unique_values == j.strip()].values[0]) for j in values if unique_values.isin([j.strip()]).any()]
        new_list = ', '.join(ids) if ids else 'nan'
        temp_list.append(new_list)
    enc_series = pd.Series(temp_list, name=id_column_name)
    enc_series.replace('', 'nan', inplace=True)
    return enc_series

data = pd.read_csv('../../data/imdb_movies.csv')

movies_df = data[['names', 'date_x', 'orig_lang', 'country', 'overview', 'score']]
movies_df.columns = ['title', 'date', 'original_lang', 'country', 'overview', 'score']  # rename columns

# save movies data to separate csv
movies_df.to_csv('../../data/separated_dfs/movies.csv', index=True)

# create np.array of unique movie genres
unique_genres = data['genre'].astype(str).str.split(',\xa0', expand=True).stack().unique()
# remove NaN and convert to series
unique_genres = pd.Series(unique_genres[unique_genres != 'nan'], name='genre_name')
# save genres data to separate csv
unique_genres.to_csv('../../data/separated_dfs/genres.csv', index=True)

actors_list = []
# remove some bad formatting and drop cells with mistakes in the data
for element in data['crew'].astype(str):
    text = element.replace(', Sr.', ' Sr.').replace(', Jr.', ' Jr.').replace(', ,', ', ').rstrip(', ').strip()
    splitted_text = text.split(',')
    if len(splitted_text) % 2 == 0:
        actors_list.extend(splitted_text)
# remove unnecessary spaces
actors_list = [actor.strip() for actor in actors_list]
# return np.array with unique values and number of occurences
unique = np.unique(actors_list, return_counts=True)

# format of the data is wrong so there is no way to infer which entity is a character from structure of data
# that's why I needed to remove by hand most of characters I came across

keywords = ['(voice)', '/', 'The ', 'Agent', 'Aunt', 'Brothel Girl', 'Adolf Hitler', 'Age 10', 'Basil Exposition',
            'Baby Oliver', 'Casting Director', 'Big Bob', 'Bridget Jones', ' Dr. ', 'Dr. ', 'Self', 'self', 'Pilot',
            'Johnny English', 'Man in Dance Hall', 'USA Phantom Dancer', 'Wednesday Addams', 'Skull Island',
            'Dancer: Valinese Tari Legong Dancers', 'Él mismo', 'Minnie Driver',
            '(', 'Albus Dumbledore', 'Skywalker', 'Bellatrix Lestrange', 'Cao Cao',
            'Captain', 'Blind Al', 'Fairy Godmother', 'Fake Shemp', 'Fat Man', 'Harry Potter',
            'Ron Weasley', 'Hermione Granger', 'Jesus Christ', "Jim's", 'Lord', 'Mad Dog', 'Mad Hatter',
            'Meat Loaf', 'Mr.', 'Mrs', 'News', 'Newt Scamander', 'Sexy Girl', 'Sheriff', "Ship's Cook",
            'Snow White', 'Tall Man', 'Tantoo Cardinal', 'Thin Man', 'Thor Odinson', 'Uncle', 'Winston Churchill',
            'Young Frank', 'Young Joe', 'Young Man', 'Young Michael', 'Young Woman', 'Young Girl', 'Cab Driver',
            'Cop #1', 'Commissioner James Gordon', 'Commissaire Juve', 'Cousin Eddie']

### keep name if length >= 3 (as most names), consists of more than 1 word (name and surname) and is not in keywords
name = [unique[0][i] for i in range(len(unique[0]))
        if unique[1][i] >= 3 and len(unique[0][i].split()) > 1
        and all(keyword not in unique[0][i] for keyword in keywords)]

# save actors data to separate csv
actors = pd.Series(name, name='actor_name')
actors.to_csv('../../data/separated_dfs/actors.csv', index=True)

# save movies_and_genres data to separate csv
genres_series = encode(data['genre'], unique_genres, 'genre_id')
genres_series.to_csv('../../data/separated_dfs/movies_genres.csv', index=True)

# save movies_and_actors data to separate csv
actors_series = encode(data['crew'], actors, 'actor_id')
actors_series.to_csv('../../data/separated_dfs/movies_actors.csv', index=True)