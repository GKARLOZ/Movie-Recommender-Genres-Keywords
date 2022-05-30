import streamlit as st
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import sys
import matplotlib


st.title("Movie Recommender")

st.write(" Movies are recommended based on the genres and keywords compared. I hope you find a good movie! ")
#read file convert it into a dataframe

df_movies = pd.read_csv("5000Movies.csv")



df_movies = pd.DataFrame().assign(Title=df_movies['movie_title'],Director=df_movies['director_name'],ActorTwo=df_movies['actor_2_name'],ActorOne= df_movies['actor_1_name'],Genres = df_movies['genres'], Keywords=df_movies['plot_keywords']          )



#
movies_genres = df_movies['Genres']

#converting the text data to feature vectors
tfVectorized = TfidfVectorizer()


movies_genres_vectorized = tfVectorized.fit_transform(movies_genres)

#the attributes that will be compared 
attributes = ['Genres','Keywords']


for x in attributes:
    df_movies[x] = df_movies[x].fillna('')
    
# a dataframe of genres and keywords attributes 
attributes_merged = df_movies['Genres']+''+df_movies['Keywords']


#creating a vertor variable
tfVectorized = TfidfVectorizer()

#converting the attributes into combined values 
movies_genres_vectorized = tfVectorized.fit_transform(attributes_merged)


#getting the similarity score using cosine similarity
cos_similarity = cosine_similarity(movies_genres_vectorized)



#this method sends input to the recommender function
def ifMatched():
    
    
    #input_movie = input(" Please enter a movie title: ")
    input_movie = st.text_input("Please enter a movie title: ","Batman")

    #if input_movie == "":

        #input_movie = "batman"
        

    input_movie = input_movie.capitalize()+" "
    #closest_similar_movies.loc[closest_similar_movies.title == str(input_movie)]


    movie_title_list= df_movies['Title'].tolist()
    movies_searched = difflib.get_close_matches(input_movie, movie_title_list)

    #print(movies_searched)
    #st.write(movies_searched)

    movie_matched = movies_searched[0]

    #st.write(movie_matched)

       
    return movie_matched


def recommended_movies(movie_matched):

    #finding the index of the movie with title
    movie_index = df_movies.index[df_movies.Title == movie_matched].values[0]

    # getting a list of similar movies
    similarityScoreList = list(enumerate(cos_similarity[movie_index]))

    len(similarityScoreList)

    sorted_ScoreList = sorted(similarityScoreList, key = lambda x:x[1], reverse = True)

    ScoreArr  = []
    TitleArr  = []
    GenrArr   = []
    actorArr = []

    i = 1

    for movies in sorted_ScoreList:
        a = movies[0]
        title = df_movies[df_movies.index == a]['Title'].values[0] 
        genres = df_movies[df_movies.index == a]['Genres'].values[0]
        actor = df_movies[df_movies.index == a]['ActorOne'].values[0] 

        b = movies[1]*100
        b = b.round(1)
        if(i<=10):
            TitleArr.append(title)
            ScoreArr.append(b)
            GenrArr.append(genres)
            actorArr.append(actor)
            i+=1
    #Table of movies
    prep_data = {'Movie Titles':TitleArr,'Actors':actorArr,'Genres':GenrArr,'Similarity Scores':ScoreArr}
    table_movies = pd.DataFrame(prep_data)
    st.write(table_movies.head(10))


    #The plot
    fig = go.Figure(
            go.Pie(
            
        labels = TitleArr,
        values = ScoreArr,
        hoverinfo = "label+percent",
        textinfo = "value"
                ))

    st.header("Pie Chart")
    st.plotly_chart(fig)
    st.stop()

recommended_movies(ifMatched())













