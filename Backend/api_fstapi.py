from fastapi import FastAPI
import Es_functions
from PIL import Image
from tensorflow import keras
import keras
from tensorflow.keras.utils import load_img
from keras.applications.vgg16 import VGG16
from tensorflow.keras.utils import img_to_array
from keras import Model, Sequential
import numpy as np
import keras
import pickle as pkl
import Es_functions
app = FastAPI()
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
pca = pkl.load(open('pca.pkl','rb'))
from elasticsearch import Elasticsearch
INDEX = 'indexation_imen_toumi'
es = Elasticsearch("http://127.0.0.1:9200")


@app.get("/")
def root():
    return "Welcome to our project"


@app.post("/api/text_query/")
async def text_query(text : str, fuzzy : bool,degree=1, num_resul=10):
    return Es_functions.search_by_text(text,fuzzy,degree,num_resul)

@app.post("/api/suggest_query/")
async def get_suggestions(text):
    return Es_functions.suggestions(text)


@app.post("/api/image_query/")
async def image_query(path,num_resul=10,):
    return Es_functions.search_by_image(model,pca,path,num_resul)

@app.post("/api/image_text_query/")
async def image_text_query(text, path, number_of_query):
    return Es_functions.search_by_image_text(model,pca, text, path, number_of_query)

@app.post("/api/image_query_link/")
async def image_query(link,num_resul=10,):
    return Es_functions.search_by_image_by_link(model,pca,link,num_resul)