import streamlit as st
import pandas as pd
import numpy as np
from google.cloud import firestore
from google.oauth2 import service_account

import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

st.title('Netflix App')
@st.cache
def load_data():
    data_ref= list(db.collection(u'movies').stream())
    data_dict=list(map(lambda x: x.to_dict(), data_ref))
    data= pd.DataFrame(data_dict)
    return data

data_load_state= st.text('Loading movies data...')
data= load_data()
data_load_state.text('Done! (using st.cache)')

sidebar=st.sidebar

agreeAllMovies=sidebar.checkbox('Mostrar todos los filmes')
if agreeAllMovies:
    st.header('Todos los filmes')
    st.dataframe(data)

def load_data_byname(nameSearch):
    filtered_by_name= data[data['name'].str.contains(nameSearch, case=False)]
    return filtered_by_name

mynameSearch=sidebar.text_input('Titulo del filme: ')
searchFilm=sidebar.button('Buscar filmes')
if mynameSearch and searchFilm:
    filterbyname=load_data_byname(mynameSearch)
    count_row=filterbyname.shape[0] #Da el número de filas
    st.write(f"Total filmes mostrados : {count_row}")
    st.dataframe(filterbyname)

def load_data_bydirector(director):
    filtered_by_director= data[data['director'].str.contains(director)]
    return filtered_by_director

selected_director = sidebar.selectbox("Seleccionar director", data['director'].unique())
searchDirector=sidebar.button('Filtrar director')

if selected_director and searchDirector:
    filterbydirector=load_data_bydirector(selected_director)
    count_row=filterbydirector.shape[0] #Da el número de filas
    st.write(f"Total filmes mostrados : {count_row}")
    st.dataframe(filterbydirector)
sidebar.markdown('_____')

sidebar.subheader('Nuevo filme')
name=sidebar.text_input('Name:')
company=sidebar.selectbox("Company:", data['company'].unique())
director= sidebar.selectbox("Director:", data['director'].unique())
genre= sidebar.selectbox("Genre:", data['genre'].unique())
submit= sidebar.button('Crear nuevo filme')

if name and company and director and genre and submit:
    doc_ref = db.collection('movies').document(name)
    doc_ref.set({
        'name':name,
        'company':company,
        'director':director,
        'genre': genre
    })
    sidebar.write('¡Registro insertado correctamente!')