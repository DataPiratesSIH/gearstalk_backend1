import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.connect import client, db, fs, stopwords
from bson.json_util import dumps
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from matplotlib import colors
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

nltk.download('punkt')
nltk.download('wordnet')

query = Blueprint("query", __name__)
lemmatizer = WordNetLemmatizer()

COSINE_THRESHOLD = 0.85                         #set the threshold here

'''-----------------------------------
            query functions
-----------------------------------'''

def cosine_search(x,y):
    cos_sim = cosine_similarity(x, y)
    threshold_indices = np.nonzero(cos_sim[0] > COSINE_THRESHOLD)[0].tolist()                        
    return threshold_indices


def nlp_text(text):
    tokens = word_tokenize(text)
    prev = ""
    color_values = []
    features = []
    for token in tokens:
        lemmatizer.lemmatize(token)
        if len(token) > 1 and colors.is_color_like(token):
            if colors.is_color_like(prev + token):
                color_values.append(list(colors.to_rgba(prev + token)))
            else:
                color_values.append(list(colors.to_rgba(token)))
            prev = token
        elif token in stopwords:
            features.append(token) 
    return color_values,features


def class_ids(arr):
    ids_list = [0]*10000 
    for i in arr:
        index = stopwords[i]
        ids_list[stopwords.index(i)] = 1
    return ids_list


def searchFunction(metadata, features, colors):
    box=[]
    labels=[]
    colors=[]
    for i in metadata:
        for j in i['persons']:
            box.append(j['box'])
            labels.append(j['labels'])
            meta_colors.append(j['colors'])

    feature_indices = cosine_search(features, labels)
    feature_colors=[]
    for j in feature_indices:
        feature_colors.append(meta_colors[j])

    color_indices = cosine_search(colors, feature_colors)
    metadata_person = []
    for i in color_indices:
        metadata_person.append({"box": box[i],"labels": labels[i], "colors": color[i]})
    
    return metadata_person



'''-----------------------------------
            query-routes
-----------------------------------'''


#returns list of best matches from the metadata
@query.route('/textarea', methods=['POST'])
@jwt_required
def textarea():
    try:
        data = request.get_json()
        text = data['textarea']
        lat = data['lat']
        lng = data['lng']
        
        #extract features from the text
        colors, features = nlp_text(text)
        query = {
                "location" : 
                    {
                        "lat":lat,
                        "lng":lng
                    }
                }

        #extracting metadata
        cursor = dumps(db.features.find(query))
        metadata = cursor['metadata']

        #searchFunction
        metadata_person = searchFunction(metadata, features, colors)                          
    
        return jsonify({"closest_match": metadata_person}), 200
    except Exception as e:
        return f"An Error Occured: {e}"



#returns metadata of the whole video 
@query.route('/metadata', methods=['POST'])
@jwt_required
def video_search():
    try:
        data = request.get_json()
        video_id = data['video_id']
        cursor = dumps(db.features.find({"video_id" : video_id}))

        return jsonify({"metadata": cursor["metadata"]}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


#returns a list of best matches from the given video_id
@query.route('/metadata_search', methods=['POST'])
@jwt_required
def video_search():
    try:
        data = request.get_json()
        video_id = data['video_id']
        query = data['query']
        colors = data['colors']
        features = class_ids(query)

        #get the metadata for video_id
        cursor = dumps(db.features.find({"video_id" : video_id}))
        metadata = cursor["metadata"]

        #searchFunction
        metadata_person = searchFunction(metadata,features,colors)

        return jsonify({"closest_match": metadata_person}), 200
    except Exception as e:
        return f"An Error Occured: {e}"



#returns best match in a given interval of time
@query.route('/metadata_search', methods=['POST'])
@jwt_required
def time_search():
    try:
        data = request.get_json()
        query = data['query']
        colors = data['colors']
        features = class_ids(query)

    #     #get the metadata for video_id
    #     cursor = dumps(db.features.find({"video_id" : video_id}))
    #     metadata = cursor["metadata"]

    #     #searchFunction
    #     metadata_person = searchFunction(metadata,features,colors)

    #     return jsonify({"closest_match": metadata_person}), 200
    # except Exception as e:
    #     return f"An Error Occured: {e}"