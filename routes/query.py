import os
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required
from utils.connect import client, db, fs, stopwords
from bson.json_util import dumps
from datetime import datetime
import nltk
from nltk.tokenize import word_tokenize
from matplotlib import colors
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.colorlist import colours
import datefinder
import numpy as np

nltk.download('punkt')
nltk.download('wordnet')

query = Blueprint('query', __name__)
lemmatizer = WordNetLemmatizer()
all_colors = [color[3] for color in colours]                                #importing list of available colors




'''-----------------------------------
            query functions
-----------------------------------'''


def nlp_text(text):
    tokens = word_tokenize(text)
    prev = ""
    color_values = []
    features = []
    dates = ""
    dates = [str(x.date()) for x in datefinder.find_dates(text)]
    for token in tokens:
        lemmatizer.lemmatize(token)
        if token in all_colors:
            color_values.append(token)
        elif token in stopwords:
            features.append(token) 
    return features,list(set(color_values)),dates[0]






'''-----------------------------------
            query-routes
-----------------------------------'''


#returns the list of unique_persons with the best match
@query.route('/search', methods=['GET'])
# @jwt_required
def search():
    try:
        data = request.get_json()
        labels = [ x.lower() for x in data['labels']]
        colors = [ x.lower() for x in data['colors']]
        if len(labels) == 0 and len(colors) == 0:
            return jsonify({"status": False, "message": "Provide Labels or colors in the text!!", "person": []}), 200
        elif "features" not in db.list_collection_names():
            return jsonify({"success": False, "message": "Video is not yet processed!!"}), 404
        else:
            best_match = list(db.unique_person.find({"labels": { "$in": labels }, "colors": { "$in": colors}}).limit(8))
            print(best_match)
            return jsonify({"status": True, "message": "Top 8 best_matches!!", "person": dumps(best_match)}), 200
    except Exception as e:
        return f"An Error Occured: {e}"




#returns the list of unique_persons with the best match
@query.route('/text_search', methods=['GET'])
# @jwt_required
def text_search():
    try:
        data = request.get_json()
        text = data['text'].lower()
        labels,colors,date = nlp_text(text)
        if len(labels) == 0 and len(colors) == 0:
            return jsonify({"status": False, "message": "Provide Labels or colors in the text!!", "person": []}), 200
        elif "features" not in db.list_collection_names():
            return jsonify({"success": False, "message": "Video is not yet processed!!"}), 404
        else:
            best_match = list(db.unique_person.find({"labels": { "$in": labels }, "colors": { "$in": colors}}).limit(8))
            return jsonify({"status": True, "message": "Top 8 best_matches!!", "person": dumps(best_match)}), 200
    except Exception as e:
        return f"An Error Occured: {e}"




#returns metadata of the whole video 
@query.route('/metadata/<oid>', methods=['GET'])
# @jwt_required
def video_metadata(oid):
    try:
        print(oid)
        if oid == None or len(oid) != 24:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
        elif "features" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection features."}), 404
        else:
            features = db.features.find_one({ "video_id": oid})
            return jsonify({"status": True, "message": "Retriving video metadata!!", "metadata": dumps(features)}), 200
    except Exception as e:
        return f"An Error Occured: {e}"




#returns the list of unique_persons with the best match
# @query.route('/video/<oid>', methods=['GET'])
# # @jwt_required
# def video_search_person(oid):
#     try:
#         if oid == None or len(oid) != 24:
#             return jsonify({"success": False, "message": "No Object Id in param."}), 400
#         elif "features" not in db.list_collection_names():
#             return jsonify({"success": False, "message": "No Collection features."}), 404
#         else:
#             features = db.features.find_one({ "video_id": oid})
#             return jsonify({"status": True, "message": "Retriving video metadata!!", "metadata": dumps(features)}), 200
#     except Exception as e:
#         return f"An Error Occured: {e}"