from unicodedata import name
import streamlit as st
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go
import sys
import matplotlib
import altair as alt





#with open('style.css')as f : 
    #st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html = True)



#admin_text = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">The movie recommender will recommend movies by comparing the genres and keywords of the movies selected. I hope you find a good movie! </p>'
#st.markdown(admin_text, unsafe_allow_html=True)



st.title("Gian's Movie Recommender :clapper:")

st.markdown(" The movie recommender will recommend movies by comparing the _genres_ and _keywords_ of the movies selected. I hope you find a good movie! ")
#read file convert it into a dataframe

df_movies = pd.read_csv("5000Movies.csv")



df_movies = pd.DataFrame().assign(Title=df_movies['movie_title'],Director=df_movies['director_name'],ActorTwo=df_movies['actor_2_name'],ActorOne= df_movies['actor_1_name'],Genres = df_movies['genres'], Keywords=df_movies['plot_keywords']          )



#movies_genres = df_movies['Genres']

#converting the text data to feature vectors
#tfVectorized = TfidfVectorizer()


#movies_genres_vectorized = tfVectorized.fit_transform(movies_genres)

#the attributes that will be compared 
attributes = ['Genres','Keywords']


for x in attributes:
    df_movies[x] = df_movies[x].fillna('')
    
# a dataframe of genres and keywords attributes 
attributes_merged = df_movies['Genres']+df_movies['Keywords']


#creating a vertor variable
tfVectorized = TfidfVectorizer()

#converting the attributes into combined values 
movies_genres_vectorized = tfVectorized.fit_transform(attributes_merged)



#getting the similarity score using cosine similarity
cos_similarity = cosine_similarity(movies_genres_vectorized)





#this method sends input to the recommender function
def ifMatched():
    
    
    #input_movie = input(" Please enter a movie title: ")
    input_movie = st.text_input('Please enter a movie title (case sensitive): ',"Forrest Gump")

    #if input_movie == "":

        #input_movie = "batman"
        

    input_movie = input_movie.capitalize()+" "
    #closest_similar_movies.loc[closest_similar_movies.title == str(input_movie)]


    movie_title_list= df_movies['Title'].tolist()
    movies_searched = difflib.get_close_matches(input_movie, movie_title_list)

 
    #st.write(movies_searched)
    
    movie_matched = movies_searched[0]
    
      
      

    #st.write(movie_matched)

       
    return movie_matched


def recommended_movies(movie_matched):

    #finding the index of the movie with title
    movie_index = df_movies.index[df_movies.Title == movie_matched].values[0]

    # getting a list of similar movies
    similarityScoreList = list(enumerate(cos_similarity[movie_index]))

    
 
    sorted_ScoreList = sorted(similarityScoreList, key = lambda x:x[1], reverse = True)

    ScoreArr  = []
    TitleArr  = []
    GenrArr   = []
    actorArr = []
    AccuracyArr = [0,0,0,0,0]

    i = 1
    w = 1

    for movies in sorted_ScoreList:
        a = movies[0]
        title = df_movies[df_movies.index == a]['Title'].values[0] 
        genres = df_movies[df_movies.index == a]['Genres'].values[0]
        actor = df_movies[df_movies.index == a]['ActorOne'].values[0] 

        b = movies[1]*100
        b = b.round(1)

        

        

        

        #--------------------------------------------------
       
        if(i<=11):
            TitleArr.append(title)
            ScoreArr.append(b)
            GenrArr.append(genres)
            actorArr.append(actor)
           
            i+=1


       
        if(w <=100):
             #--------------values for recommendation accuracy------------------------
            if b >= 50:
                AccuracyArr[0] += 1
            elif b < 50 and b >= 40:
                AccuracyArr[1] += 1
            elif b < 40 and b >=20:
                AccuracyArr[2] += 1
            elif b < 20 and b >= 10:
                AccuracyArr[3] += 1
            elif b < 10 and b > 0:
                AccuracyArr[4] += 1

            w+=1
            #-------

           



     
    #-----------------------------Table of movies------------------------------------------
    prep_data = {'Movie Titles':TitleArr,'Actors':actorArr,'Genres':GenrArr,'Similarity Scores':ScoreArr}
    table_movies = pd.DataFrame(prep_data)

    st.write(" Movie you selected:")
    st.write(table_movies.head(1))

    st.write(" Table of Movies Recommended:  ")
    st.write(table_movies.iloc[1:11])


     #-----------------------bar chart------------------------------------------


    df_for_barChart = {'Movie Titles':TitleArr,'Similarity Scores':ScoreArr}
    df_barChart = pd.DataFrame(df_for_barChart)
    

    bars = alt.Chart(df_barChart).mark_bar().encode(
        #x='Similarity Scores',
        #y='Movie Titles'
        alt.X('Movie Titles',
        sort=alt.EncodingSortField(field='Similarity Scores', order='descending')),

        y='Similarity Scores')

    text = bars.mark_text(
        align='left',
        baseline='middle',
        color = 'white',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text ='Similarity Scores'
    )

    bars = (bars + text).properties(height=600)
    st.header("Bar chart")

    st.altair_chart(bars, use_container_width=True)


     #-----------------------------------------Scatterplot-----------------------------------

    SScoreArr = []
    M_indexArr = []
    scTitleArr  = []
    for a in sorted_ScoreList:


        z = a[1] * 100
        SScoreArr.append(z.round(1))
        M_indexArr.append(a[0])
        title =  df_movies[df_movies.index == a[0]]['Title'].values[0] 
        scTitleArr.append(title)
         
    
    prep_dataTesting = {'Movie Index':M_indexArr,'Similarity Scores':SScoreArr, 'Film Title':scTitleArr}

    
    
    df_for_scatter = pd.DataFrame(prep_dataTesting)
    st.header("Scatterplot")
    st.write(" You can predict the 10 most similar movies by using this graph. ")

    c = alt.Chart(df_for_scatter).mark_circle().encode(
        x='Movie Index', y='Similarity Scores', size='Similarity Scores', color='Similarity Scores', tooltip=['Similarity Scores', 'Film Title','Movie Index'])
                

    st.altair_chart(c, use_container_width=True)

     #--------------------------pie chart---------------------------------------
    
    AccuracyTypes = ['High', 'Med/High','Medium','Med/Low','Low']


    #The plot
    fig = go.Figure(
            go.Pie(
            
        labels = AccuracyTypes,
        values = AccuracyArr,
        hoverinfo = "label+percent",
        textinfo = "value"
                ))
    st.header("Pie Chart")
    st.plotly_chart(fig)
    
    #---------------end of method----------------------



    

    




try:
  name_of_movie = ifMatched()
except:
  st.markdown('**_Please try a different movie title. Remember it is case sensitive_**. :performing_arts:')

try:
  recommended_movies(name_of_movie)
except Exception as e:
  print(e)

print('Done')
  











