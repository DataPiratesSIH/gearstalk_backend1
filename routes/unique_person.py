from collections import Counter
from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json
import itertools
from flask import request

client = MongoClient("mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('gearstalk')
video_sample = "987654321"
frame_sec_array = []
labels_array = []
big_data = []
x_axis = []
y_axis = []

# This is for Person's Labels and Colors 3D array

# for doc in db.features.find():
#     if(doc["video_id"]==video_sample):
#         big_data = []
#         object_demo = doc["metadata"]
#         for object_small in object_demo:
#             frame_array = []
#             x = []            
#             person = object_small["persons"]
#             person1 = json.loads(person)
#             for i in person1:
#                 y = []
#                 y.append(i["labels"])
#                 y.append(i["colors"])
#                 y_new = []
#                 for elem in y:
#                     y_new.extend(elem)
#                 # print(y_new)
#                 x.append(y_new)
#             # print(x) 
#             big_data.append(x)
#         print(big_data)

# This is for Person's Box 3D array

# for doc in db.features.find():
#     if(doc["video_id"]==video_sample):
#         big_data = []
#         object_demo = doc["metadata"]
#         for object_small in object_demo:
#             frame_array = []
#             x = []            
#             person = object_small["persons"]
#             person1 = json.loads(person)
#             for i in person1:
#                 y = []
#                 y.append(i["box"])
#                 # y.append(i["colors"])
#                 y_new = []
#                 for elem in y:
#                     y_new.extend(elem)
#                 # print(y_new)
#                 x.append(y_new)
#             # print(x) 
#             big_data.append(x)
#         print(big_data)