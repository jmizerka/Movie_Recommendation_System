import pandas as pd
#nltk.download('stopwords')
#nltk.download('punkt')
import numpy as np
import pickle
from text_processing import stem_data, vectorize
from recommenders import calc_cos_sim



movies = pd.read_csv('../../data/separated_dfs/movies.csv')
genres = pd.read_csv('../../data/separated_dfs/genres.csv')
actors = pd.read_csv('../../data/separated_dfs/actors.csv')
movies_actors = pd.read_csv('../../data/separated_dfs/movies_actors.csv')
movies_genres = pd.read_csv('../../data/separated_dfs/movies_genres.csv')

grouped_df = movies_actors.groupby('movie_id')['actor_id'].agg(list).reset_index()
grouped_df['actor_names'] = grouped_df['actor_id'].apply(lambda ids: [actors[actors['actor_id'] == actor_id]['actor_name'].values[0] for actor_id in ids])
grouped_df['actor_names_joined'] = grouped_df['actor_names'].apply(lambda names: [name.replace(" ","") for name in names])
grouped_df2 = movies_genres.groupby('movie_id')['genre_id'].agg(list).reset_index()
grouped_df2['genres_names'] = grouped_df2['genre_id'].apply(lambda ids: [genres[genres['genre_id'] == genre_id]['genre_name'].values[0] for genre_id in ids])
grouped_df2['genres_names_joined'] = grouped_df2['genres_names'].apply(lambda names: [name.replace(" ","") for name in names])
merged_df = pd.merge(pd.merge(movies,grouped_df, on='movie_id', how='outer'), grouped_df2, on='movie_id', how='outer')
features_df = merged_df[['title','country','overview','actor_names_joined','genres_names_joined']]
features_df = features_df.replace('nan', np.nan)
features_df.loc[:,'overview'] = features_df.loc[:,'overview'].str.lower()
features_df.loc[:,'country'] = features_df.loc[:,'country'].str.lower()
features_df.loc[:,'features']=''
features_df.loc[:,'actor_names_joined'] = features_df.loc[:,'actor_names_joined'].apply(lambda x: ' '.join(x) if type(x) != float else x)
features_df.loc[:,'genres_names_joined'] = features_df.loc[:,'genres_names_joined'].apply(lambda x: ' '.join(x) if type(x) != float else x)
features_df.loc[:,'features'] = features_df.T.apply(lambda x: x['country']+' '+x['overview']+' '+x['actor_names_joined'] if type(x['actor_names_joined']) != float else x['country']+' '+x['overview'])
features_df.loc[:,'features'] = features_df.T.apply(lambda x: x['features']+' '+x['genres_names_joined'] if type(x['genres_names_joined']) != float else x['features'])
stemmed = stem_data(features_df['features'])
vectorized = vectorize(stemmed,vec_type='tfidf')
cos_sim = calc_cos_sim(vectorized)
indices = pd.Series(features_df.index,index=features_df['title']).drop_duplicates()

pickle_dict = {'indices':indices, 'similarity':cos_sim}


with open('../../data/my_variables.pkl', 'wb') as file:
    pickle.dump(pickle_dict, file)