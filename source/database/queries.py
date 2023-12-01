MOVIES_OF_ACTOR = f"""SELECT
     movies.title,
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.date,
     movies.score
     FROM
     actors
     JOIN
     movies_actors ON actors.actor_id = movies_actors.actor_id
    JOIN
     movies ON movies.movie_id = movies_actors.movie_id
    JOIN
     movies_genres ON movies_genres.movie_id = movies.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    WHERE
     actors.actor_name = ?
    GROUP BY
     movies.title, movies.date, movies.score
    ORDER BY
     movies.title;"""

ACTORS_IN_MOVIE = f"""SELECT
     actors.actor_name as actor
     FROM actors
     JOIN
     movies_actors ON actors.actor_id = movies_actors.actor_id
    JOIN
     movies ON movies.movie_id = movies_actors.movie_id
    WHERE
     movies.title = ?
    ORDER BY
     actors.actor_name;"""

MOVIES_OF_GENRE=f"""SELECT
    movies.title
    FROM movies_genres
    JOIN genres ON movies_genres.genre_id = genres.genre_id
    JOIN movies ON movies_genres.movie_id = movies.movie_id
    WHERE genres.genre_name = ?;"""

# MOVIES_BY_TITLE
MOVIE_BY_TITLE = f"""SELECT
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.date,
     movies.original_lang,
     movies.country,
     movies.score
     FROM
     movies
     JOIN
     movies_genres ON movies.movie_id = movies_genres.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    WHERE 
     movies.title = ?
    GROUP BY
     movies.title
    ORDER BY
     movies.score DESC;"""


ALL_MOVIES = """SELECT
     movies.title,
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.date,
     movies.original_lang,
     movies.country,
     movies.score
     FROM
     movies
     JOIN
     movies_genres ON movies.movie_id = movies_genres.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    GROUP BY
     movies.title
    ORDER BY
     movies.score DESC;"""

ALL_GENRES = "SELECT * FROM genres"

ALL_ACTORS = "SELECT * FROM actors"

### TUTAJ TRZEBA POPRAWIĆ BO NA RAZIE WYSZUKUJE PO KONKRETNEJ DACIE
MOVIES_OF_YEAR = f"""SELECT
     movies.title,
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.original_lang,
     movies.country,
     movies.score
     FROM
     movies
     JOIN
     movies_genres ON movies.movie_id = movies_genres.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    WHERE 
     movies.date = ?
    GROUP BY
     movies.title
    ORDER BY
     movies.score DESC;"""

HIGHEST_RATED = """SELECT
     movies.title,
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.date,
     movies.original_lang,
     movies.country,
     movies.score
     FROM
     movies
     JOIN
     movies_genres ON movies.movie_id = movies_genres.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    GROUP BY
     movies.title
    ORDER BY
     movies.score DESC
     LIMIT 100;"""

LOWEST_RATED = """SELECT
     movies.title,
     GROUP_CONCAT(genres.genre_name) AS genres,
     movies.date,
     movies.original_lang,
     movies.country,
     movies.score
     FROM
     movies
     JOIN
     movies_genres ON movies.movie_id = movies_genres.movie_id
    JOIN
     genres ON movies_genres.genre_id = genres.genre_id
    GROUP BY
     movies.title
    ORDER BY
     movies.score ASC
     LIMIT 100;"""

NUM_MOVIES_BY_GENRE="""SELECT
    genres.genre_name,
    COUNT(movies.title)
    FROM movies_genres
    JOIN genres ON movies_genres.genre_id = genres.genre_id
    JOIN movies ON movies_genres.movie_id = movies.movie_id
    GROUP BY genres.genre_name ;"""

# MEAN RATE OF GENRE
AVG_RATE_BY_GENRE="""SELECT
    g.genre_name,
    AVG(m.score) AS average_score
    FROM
    genres g
    JOIN
    movies_genres mg ON g.genre_id = mg.genre_id
    JOIN
    movies m ON mg.movie_id = m.movie_id
    GROUP BY
    g.genre_name;"""



AVG_RATE_BY_ACTOR="""SELECT
    actors.actor_name,
    AVG(movies.score) AS average_score
    FROM
    actors
    JOIN
    movies_actors ON actors.actor_id = movies_actors.actor_id
    JOIN
    movies ON movies.movie_id = movies_actors.movie_id
    GROUP BY
    actors.actor_name;"""

ACTOR_STATS = """SELECT
    a.actor_name AS ActorName,
    COUNT(DISTINCT ma.movie_id) AS NumberOfMovies,
    MAX(m.score) AS MaxMovieScore,
    MIN(m.score) AS MinMovieScore,
    COUNT(DISTINCT g.genre_id) AS total_genres
FROM
    actors a
JOIN
    movies_actors ma ON a.actor_id = ma.actor_id
JOIN
    movies m ON ma.movie_id = m.movie_id
LEFT JOIN
    movies_genres mg ON m.movie_id = mg.movie_id
LEFT JOIN
    genres g ON mg.genre_id = g.genre_id
GROUP BY
    a.actor_id;"""


