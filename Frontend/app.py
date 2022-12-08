# srcs/streamlit_app/app.py
import os
import sys
import streamlit as st
from elasticsearch import Elasticsearch
from PIL import Image
from tensorflow import keras
import keras
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras import Model, Sequential
import numpy as np
import keras
from numpy import array
from keras.applications.vgg16 import VGG16
from tensorflow.keras.utils import img_to_array
from keras import Model, Sequential
from keras.layers import Dense, Flatten
from PIL import Image
import requests
from io import BytesIO
import pickle
from keras.applications.vgg16 import preprocess_input
import pickle as pkl
import requests
import templates
import utils
import templates
from urllib import request
from io import BytesIO

INDEX = 'indexation_imen_toumi'
DOMAIN = '127.0.0.1'
es = Elasticsearch("http://127.0.0.1:9200")
sys.path.append('srcs')
headers = {'accept': 'application/json'}



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

def my_widget(key):
    #original_title = '<p style="font-family:Poppins; color:#3399ff; font-size: 20px;font-weight: bold; font-size: 40px">Welcome to the search engine !</p>'
    #st.markdown(original_title, unsafe_allow_html=True)
    st.image('icon.png')


# This works in the main area
clicked = my_widget("first")


# And within an expander
my_expander = st.expander("Search and Filters", expanded=True)
my_expander1 = st.expander("Filter", expanded=True)

   

with my_expander:
    cols = st.columns(3)
    cols[0].caption('Text options ')
    show_result = cols[1].slider('Show results', 1, 100)
 
    filter=cols[2].selectbox(
      'Filter',
       ('Image', 'Text', 'Text & Image'))


if filter == 'Image':
    sub_title2 = '<p style="font-family:Poppins; color: #3399ff;font-weight: bold;  font-size: 25px">Search your image here</p>'
    st.markdown(sub_title2, unsafe_allow_html=True)


    def load_image(image_file):
        img = Image.open(image_file)
        return img


    #urll= st.text_input("Tap down your image url",'')
    placeholder = st.empty()
    urll = placeholder.text_input('Tap down your image url')
    print('----------------------------------')
    print(urll)
    img_file = st.file_uploader("Or upload your image", type=["png", "jpg", "jpeg"],accept_multiple_files=False)
    button_clicked = st.button("Search")
    tt = {}
    if button_clicked :
        if len(urll)>0 :
            params = (('link', urll), ('num_resul', show_result))
            print('#############')
            res = request.urlopen(urll).read()
            image = Image.open(BytesIO(res))
            st.image(image, width=250)
            response = requests.post(f"http://127.0.0.1:8000/api/image_query_link/", headers=headers, params=params)
            print('-----------')
            print(response.text)
            tt = response.json()
            # for j in range(len(tt['hits']['hits'])):
            #     result = tt['hits']['hits'][j]
            #     res = result['_source']
            #     imgurl = res['imgUrl']
            #     title = res['title']
            #     author = res['author']
            #
            #     st.write(templates.search_result(imgurl, title, author), unsafe_allow_html=True)
        if img_file is not None :
            urll = placeholder.text_input('Tap down your image url  ', value='')
            # To See details
            file_details = {"filename": img_file.name, "filetype": img_file.type,
                            "filesize": img_file.size}
            st.write(file_details)
            # To View Uploaded Image
            st.image(load_image(img_file), width=250)
            # Saving upload
            with open(os.path.join("C:/Users/Lenovo/Desktop/INDP3/P2/Tebourbi/Frontend/Frontend/saved_images", img_file.name), "wb") as f:
                f.write((img_file).getbuffer())
            print(img_file.name)
            path = "C:/Users/Lenovo/Desktop/INDP3/P2/Tebourbi/Frontend/Frontend/saved_images/"+img_file.name
            params = (('path', path), ('num_resul', show_result))
            response = requests.post(f"http://127.0.0.1:8000/api/image_query/", headers=headers, params=params)
            tt = response.json()
        if tt!= {} :
            for j in range(len(tt['hits']['hits'])):
                result = tt['hits']['hits'][j]
                res = result['_source']
                imgurl = res['imgUrl']
                title = res['title']
                author = res['author']

                st.write(templates.search_result(imgurl,title,author), unsafe_allow_html=True)

if filter == 'Text':
    fuzzy = cols[0].checkbox('Fuzzy')
    sugg = cols[0].checkbox('Suggestions')
    if fuzzy:
        show_fuzzy = cols[0].slider('', 1, 5)
    else :
        show_fuzzy=1
    col1, col2 = st.columns([13, 1])

    with col1:
        sub_title = '<p style="font-family:Poppins; color: #3399ff; font-weight: bold; font-size: 25px">Search your text here</p>'
        st.markdown(sub_title, unsafe_allow_html=True)
    with col2:
        i = icon('search')

    select = st.text_input("", "")
    button_clicked = st.button("Search")


    if len(select)>0 :
        if sugg :
            params = (('text', select),)
            response_sugg = requests.post(f"http://127.0.0.1:8000/api/suggest_query/", headers=headers, params=params)
            responsess = response_sugg.json()

            l = []
            n = result = responsess['hits']['hits']
            for k in range(len(responsess['hits']['hits'])):
                result = responsess['hits']['hits'][k]
                res = result['_source']
                imgurl = res['imgUrl']
                title = res['title']
                l.append(title)

            option = st.selectbox("find suggestions here", l)
            select=option


            st.write('You selected:', option)
    params = (('text', select), ('fuzzy', fuzzy),('degree',show_fuzzy), ('num_resul', show_result))
    response = requests.post(f"http://127.0.0.1:8000/api/text_query/", headers=headers, params=params)
    results = response.json()
    st.write("The took is", results['took'], 'ms for a total hits of', len(results['hits']['hits']))
    total_hits = results
    for i in range(len(results['hits']['hits'])):
        result = results['hits']['hits'][i]
        res = result['_source']
        imgurl = res['imgUrl']
        title = res['title']
        author= res['author']
        st.write(templates.search_result(imgurl,title,author), unsafe_allow_html=True)


if filter == 'Text & Image':
    fuzzy = cols[0].checkbox('Fuzzy')
    if fuzzy:
        show_fuzzy = cols[0].slider('', 1, 5)
    else :
        show_fuzzy=1
    sub_title2 = '<p style="font-family:Poppins; color: #3399ff; font-weight: bold; font-size: 25px">Search your image here</p>'
    st.markdown(sub_title2, unsafe_allow_html=True)


    def load_image(image_file):
        img = Image.open(image_file)
        return img

    img_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])

    if img_file is not None:
        # To See details
        file_details = {"filename": img_file.name, "filetype": img_file.type,
                        "filesize": img_file.size}
        st.write(file_details)

        # To View Uploaded Image
        st.image(load_image(img_file), width=250)
        # Saving upload
        with open(os.path.join("C:/Users/Lenovo/Desktop/INDP3/P2/Tebourbi/Frontend/Frontend/saved_images", img_file.name), "wb") as f:
            f.write((img_file).getbuffer())
        path = "C:/Users/Lenovo/Desktop/INDP3/P2/Tebourbi/Frontend/Frontend/saved_images/" + img_file.name

    col1, col2 = st.columns([13, 1])

    with col1:
        sub_title = '<p style="font-family:Poppins; color: #3399ff; font-weight: bold; font-size: 25px">Search your text here</p>'
        st.markdown(sub_title, unsafe_allow_html=True)

    with col2:
        i = icon('search')

    select = st.text_input("", "")

    button_clicked = st.button("Search")
    if button_clicked :
        params = (('text', select), ('path', path), ('number_of_query', show_result))
        response = requests.post(f"http://127.0.0.1:8000/api/image_text_query/", headers=headers, params=params)
        tt = response.json()
        for j in range(len(tt['hits']['hits'])):
            result = tt['hits']['hits'][j]
            res = result['_source']
            imgurl = res['imgUrl']
            title = res['title']
            author = res['author']

            st.write(templates.search_result(imgurl, title,author), unsafe_allow_html=True)

with st.sidebar:

    st.title(' USER GUIDE : Image and text based search engine ')
    st.write('Filters : ')
    st.write('* image filter : upload an image and find similar images to it')
    st.write('* text filter : search image by title or tags')
    st.write('* image and text filter : search image and add a tag ')
    st.write('Fuzzy options :')
    st.write('Returns results that contain similar terms to the search query')
    st.write('* Fuziness : number of changed letters')
    st.write('Suggestions :')
    st.write('* Get some suggestion according to the input prefix')