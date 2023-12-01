# Movie Recommender System

## Overview
  This project is a Movie Recommender System I designed for fun. Feel free to adapt it to your own needs. It can provide the user with personalized movie recommendations based on their preferences. The system includes a database containing information about movies, actors, and user ratings. Additionally, it features a panel for querying the database, extracting basic information, and writing custom SQL queries. The system employs a basic content-based recommendation algorithm to suggest similar movies based on a given title.

## Components
### 1. Database

  The system utilizes a relational database with six main tables:

  - Movies Table: Contains information about each movie, such as title, release year, plot overview etc.

  - Actors Table: Stores details about actors.

  - Genres Table: Stores details about movie genres.

  - Ratings Table: Keeps track of user ratings for movies.

  - Movies_Genres Table: maps genres (may be more than one) to corresponding movies

  - Movies_Actors Table: maps actors (may be more than one) to corresponding movies

### 2. Database Panel

  The system includes a panel for interacting with the database. Users can:

  - Retrieve Basuc Information: Fetch details about movies, actors, the highest and lowest rated movies and many more.

  - Add Records: add movies, actors, genres and ratings data

  - Write Custom SQL Queries: Users can write their own SQL queries if the basic queries are insufficient for their needs.

### 3. Movie Recommender System
  The recommendation system suggests similar movies based on a given title. It employs very basic recommendation algorithm based on Count Vectorizer. I intend to build a more advanced algorithm in the future

## Requirements
  Make sure you have the required Python libraries installed. You can install them using the following command:

`pip install -r requirements.txt`

## Running the System

  To set up the system for the first time, use the following commands:
  
  `make first_run`
  
  This will execute the necessary scripts to clean the data, create the database, and generate movie vectors for recommendation.

  To run the main application, use:
  
  `make run`
  
  This command will execute the main.py script, launching the Movie Recommender System.

## Future improvements
  1. Cleaning, refactoring, optimizing code - this only the first functional version
  2. Changing GUI to something more advanced and modern - I am using tkinter which is not the best
  3. Better recommendation algoritm
  4. Increase and update database - for now it is only about 10000 movies

## Data
This app was built using [IMDB movies Kaggle Dataset](https://www.kaggle.com/datasets/ashpalsingh1525/imdb-movies-dataset).
