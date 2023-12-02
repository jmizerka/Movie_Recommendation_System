from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

movies = pd.read_csv('data/separated_dfs/movies.csv')

# calculate similarity measure
def calc_cos_sim(matrix):
    return cosine_similarity(matrix, matrix)

# get 20 movie recommendations based on title
def get_recommendation(indices, title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]
