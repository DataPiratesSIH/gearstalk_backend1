from collections import Counter
from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json
import itertools
from flask import request
from matplotlib import pyplot as plt
import numpy as np

client = MongoClient("mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('gearstalk')
video_sample = "5f05d0f814e6a15bdc797d12"
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

def index2():
    frame_sec_array = []
    labels_array = []
    big_data = []
    big_data2 = []
    y_axis = []
    x_axis = []
    x_pie = []
    y_pie = []
    for doc in db.features.find():
        if(doc["video_id"]==video_sample):
            object_demo = doc["metadata"]
            for object_small in object_demo:
                frame_sec = object_small["frame_sec"]
                x_axis.append(frame_sec)
                cnt = Counter()
                key_array = []
                value_array = []
                dict_array = []
                x = []
                dict_new = {}
                person = object_small["persons"]
                person1 = json.loads(person)
                y_axis.append(len(person1))
                for i in person1:
                    x.append(i["labels"])                
                merged = list(itertools.chain(*x))

                for i in merged:
                    cnt[i] += 1
                new_cnt = dict(cnt)
                
                for key, value in new_cnt.items() :
                    key_array.append(key)
                    value_array.append(value)

                for i in range(len(key_array)):
                    res = {"labels": key_array[i], "count": value_array[i]} 
                    dict_new.update({key_array[i] : value_array[i]})
                    # print(res)
                    dict_array.append(res)
                # # print(dict_array)
                dict_new2 = {"frame_sec": frame_sec, "Number of People":len(person1), "feature_label": dict_array}
                big_data.append(dict_new2)
                big_data2.append(dict_new)

    # for i in big_data:
    #     print(i)
    # for i in x_axis:
    #     print(i)
    # print(x_axis)
    # print(y_axis)
    counter = Counter() 
    for d in big_data2:  
        counter.update(d) 
      
    result = dict(counter) 
    # print(result)
    for key,value in result.items():
        # res = {"category" : key, "value1": value}
        # labels_array.append(res)
        x_pie.append(key)
        y_pie.append(value)

    print(x_pie)
    print(y_pie)
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.axis('equal')
    # langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    # students = [23,17,35,29,12]
    ax.pie(y_pie, labels = x_pie,autopct='%1.2f%%')
    plt.show()

index2()

