import collections
# from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json
import itertools
from flask import request
import time
import numpy as np
import ast

client = MongoClient("mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('gearstalk')
# video_sample = "959424"
# frame_sec_array = []
# labels_array = []
# big_data = []
# x_axis = []
# y_axis = []

# # This is for Person's Labels and Colors 3D array

# object_data = [{'frame_sec': '1.0', 'persons': []},
#                 {'frame_sec': '1.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}, 
#                 {'frame_sec': '0.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "black"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.0', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}, 
#                 {'frame_sec': '0.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "black"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.0', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}, 
#                 {'frame_sec': '0.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "black"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.0', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}, 
#                 {'frame_sec': '0.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "black"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},{'frame_sec': '1.0', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]},
#                 {'frame_sec': '1.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "darkolivegreen"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}, 
#                 {'frame_sec': '0.5', 'persons': [{"box": [41, 71, 11, 30], "labels": ["Burkha"], "colors": ["black", "darkolivegreen"]}, {"box": [165, 72, 16, 42], "labels": ["saree", "Long pants"], "colors": ["darkslategray", "gray"]}, {"box": [253, 73, 15, 40], "labels": ["jeans"], "colors": ["darkslategray", "black"]}, {"box": [76, 73, 19, 60], "labels": ["Sweater", "Long pants"], "colors": ["darkslategray", "dimgray"]}, {"box": [111, 76, 15, 54], "labels": ["Long pants"], "colors": ["darkslategray", "lightgray"]}, {"box": [130, 74, 19, 59], "labels": ["Long pants"], "colors": ["lightgray", "darkslategray"]}, {"box": [193, 72, 22, 73], "labels": ["Sweater", "skirt"], "colors": ["darkkhaki", "black"]}, {"box": [15, 91, 42, 94], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}, {"box": [91, 90, 24, 87], "labels": ["Long pants"], "colors": ["silver", "darkslategray"]}, {"box": [0, 98, 15, 89], "labels": ["Sweater"], "colors": ["gray", "darkslategray"]}]}]

# # start = time.time()
# # array3d = []
# # for data in object_data:
# #     persons = data['persons']
# #     y=[]
# #     for feature in persons:
# #         y.append(feature['labels']+feature['colors'])
# #     array3d.append(y)

# # start2 = time.time()
# array3d=[]
# frame_rate = 0.5

# array3d = [collections.Counter([ str(feature['labels']+feature['colors'])  for feature in data['persons']]) for data in object_data]

# unique_person = []

# for i in range(len(array3d)-1):
#     person = array3d[i]-array3d[i+1]
#     if person:
#         for k in person :
#             unique_person.append({'last_seen': i*frame_rate,'labels': ast.literal_eval(k)})
# for k in array3d[len(array3d)-1]:
#     unique_person.append({'last_seen': (i+1)*frame_rate,'labels': ast.literal_eval(k)})

# print(unique_person)
# end = time.time()


# arr = [{'last_seen': 0, 'labels': ['jeans', 'Scarf'], 'colors': ['darkslategray', 'darkslategray']}, {'last_seen': 2, 'labels': ['Sweater', 'Scarf'], 'colors': ['darkslategray', 'darkslategray']}, {'last_seen': 2, 'labels': ['Blazer'], 'colors': ['darkslategray']}, {'last_seen': 2, 'labels': ['Sweater'], 'colors': ['darkslategray']}, {'last_seen': 4, 'labels': ['Sweater', 'skirt'], 'colors': ['rosybrown', 'darkslategray']}, {'last_seen': 4, 'labels': ['Blazer', 'Scarf'], 'colors': ['darkslategray','darkslategray']}, {'last_seen': 6, 'labels': ['Sweater'], 'colors': ['darkslategray']}, {'last_seen': 6, 'labels': ['Sweater'], 'colors': ['darkslategray']}, {'last_seen': 6, 'labels': ['jeans'], 'colors': ['darkslategray']}, {'last_seen': 10, 'labels': ['Sweater'], 'colors': ['darkslategray']}, {'last_seen': 12, 'labels': ['Sweater', 'skirt'], 'colors': ['darkslategray', 'darkslateblue']}, {'last_seen': 18, 'labels': ['Long pants'], 'colors': ['rosybrown']}, {'last_seen': 20, 'labels': ['Sweater', 'jeans'], 'colors': ['silver', 'dimgray']}, {'last_seen': 20, 'labels': ['Sweater', 'jeans'], 'colors': ['silver', 'dimgray']}, {'last_seen': 20, 'labels': ['jersey', 'jeans', 'Scarf'], 'colors': ['dimgray', 'gray', 'silver']}, {'last_seen': 22, 'labels': ['shirt', 'jeans'], 'colors': ['darkgray', 'dimgray']}, {'last_seen': 22, 'labels': ['Blazer'], 'colors': ['saddlebrown']}]

# start = time.time()
# for i in arr:
#     # multiassign(i['timestamp', 'location'], [time.time(), {"lat":352,"lng":7658}])
#     i.update({'timestamp':time.time(),'location': {"lat":352,"lng":7658}})
#     # i['timestamp'] = time.time()
#     # i['location'] = {"lat":352,"lng":7658}
# print(arr)
# print(time.time()-start)


# print(start2-start,end - start2) 
# for doc in db.features.find():
#     if(doc["video_id"]==video_sample):
#         big_data = []
#         object_demo = doc["metadata"]
#         print(object_demo)
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
        # print(big_data)

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




import collections
import pandas as pd


start = time.time()
data = db.unique_person.find({"video_id":"5f05d0f814e6a15bdc797d12"},{"labels":1, "colors":1,"_id":0})

# df = pd.DataFrame(data)
# new_data = df.labels


# data = np.array(data)
# new_data = data[:]['labels']+data[:]['colors']
# new_data = list(map(lambda t: map(lambda x: t['labels']+t['colors'] in t) in data))
new_data = [ [x+','+y for x,y in zip(t['labels'],t['colors'])] for t in data]
x = [_ for i in range(len(new_data)) for _ in new_data[i]]
cc = collections.Counter(x)
y = [ {"from": key.split(",")[0], "to": key.split(",")[1], "value": cc[key]} for key in cc]
print(y,time.time()-start)