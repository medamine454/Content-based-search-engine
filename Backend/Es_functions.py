from elasticsearch import Elasticsearch
INDEX = 'indexation_imen_toumi'
es = Elasticsearch("http://127.0.0.1:9200")
INDEX = 'indexation_imen_toumi'
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from PIL import Image
from keras.applications.vgg16 import preprocess_input
import numpy as np
from PIL import Image
import requests
from urllib import request
from io import BytesIO

def suggestions(text):
    query_suggt = {
        "size": 20,
        "query": {
            "match_phrase_prefix": {
                "title": {
                    "query": text
                }
            }
        }
    }
    return es.search(index=INDEX, body=query_suggt)


def search_by_text(text,fuziness = False,fuzzy_degree=1,number_of_query=10):
    if fuziness==True :
            body = {
                "size": number_of_query,
                "query": {

            "fuzzy": {
                "tags": {
                    "value": text,
                    "fuzziness": fuzzy_degree

                }
            }

        }}


    else :
            body = {
                "size": number_of_query,
                'query': {

                    'match': {
                        'tags':  text
                    }

                }
            }
    return es.search(index=INDEX, body=body)

def search_by_image_text(model,pca, text, path, number_of_query):
    image = load_img(path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)[0]
    feature = feature / np.linalg.norm(feature)
    vec = pca.transform(feature.reshape(1, -1))[0].tolist()
    tc = {
        "size" : number_of_query,
        "query": {
            "bool": {
                "must": {
                    "elastiknn_nearest_neighbors": {
                        "field": "featureVec",
                        "similarity": "l2",
                        "model": "lsh",
                        "candidates": 100,
                        "vec": {
                            "values": vec
                        }
                    }
                },
                "filter": {
                    "match": {"tags": text}
                }
            }
        }
    }
    return es.search(index=INDEX, body=tc)

def search_by_image(model,pca,path, number_of_query):
    image = load_img(path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)[0]
    feature = feature / np.linalg.norm(feature)
    vec = pca.transform(feature.reshape(1, -1))[0].tolist()
    body = {
        "size": number_of_query,
        "query": {
            "elastiknn_nearest_neighbors": {
                "field": "featureVec",
                "vec": {
                    "values": vec
                },
                "model": "lsh",
                "similarity": "l2",
                "candidates": 100
            }
        }
    }
    return es.search(index=INDEX, body=body)


def search_by_image_by_link(model,pca,link, number_of_query):
    res = request.urlopen(link).read()
    image = Image.open(BytesIO(res)).resize((224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    feature = model.predict(image, verbose=0)[0]
    feature = feature / np.linalg.norm(feature)
    vec = pca.transform(feature.reshape(1, -1))[0].tolist()
    body = {
        "size": number_of_query,
        "query": {
            "elastiknn_nearest_neighbors": {
                "field": "featureVec",
                "vec": {
                    "values": vec
                },
                "model": "lsh",
                "similarity": "l2",
                "candidates": 100
            }
        }
    }
    return es.search(index=INDEX, body=body)