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




# import collections
# import pandas as pd


# start = time.time()
# data = db.unique_person.find({"video_id":"5f05d0f814e6a15bdc797d12"},{"labels":1, "colors":1,"_id":0})

# df = pd.DataFrame(data)
# new_data = df.labels


# data = np.array(data)
# new_data = data[:]['labels']+data[:]['colors']
# new_data = list(map(lambda t: map(lambda x: t['labels']+t['colors'] in t) in data))
# new_data = [ [x+','+y for x,y in zip(t['labels'],t['colors'])] for t in data]
# x = [_ for i in range(len(new_data)) for _ in new_data[i]]
# cc = collections.Counter(x)
# y = [ {"from": key.split(",")[0], "to": key.split(",")[1], "value": cc[key]} for key in cc]
# print(y,time.time()-start)

from collections import Counter

feature = db.features.find_one({ "video_id": "5f05d0f814e6a15bdc797d12"})
# frame_sec_array = []
# labels_array = []
# line_chart = []
# big_data = []
# big_data2 = []
# y_axis = []
# x_axis = []
# object_demo = feature["metadata"]
# for object_small in object_demo:
#         frame_sec = object_small["frame_sec"]
#         x_axis.append(frame_sec)
#         cnt = Counter()
#         key_array = []
#         value_array = []
#         dict_array = []
#         x = []
#         dict_new = {}
#         person = object_small["persons"]
#         person1 = json.loads(person)
#         y_axis.append(len(person1))
#         for i in person1:
#                 x.append(i["labels"])
#         merged = list(itertools.chain(*x))

#         for i in merged:
#                 cnt[i] += 1
#         new_cnt = dict(cnt)

#         for key, value in new_cnt.items():
#                 key_array.append(key)
#                 value_array.append(value)

#         for i in range(len(key_array)):
#                 res = {"labels": key_array[i], "count": value_array[i]}
#                 dict_new.update({key_array[i]: value_array[i]})
#                 # print(res)
#                 dict_array.append(res)
#         # # print(dict_array)
#         line_dict = {"date": frame_sec, "value": len(person1)}
#         dict_new2 = {"frame_sec": frame_sec, "Number of People": len(
#                 person1), "feature_label": dict_array}
#         big_data.append(dict_new2)
#         line_chart.append(line_dict)
#         big_data2.append(dict_new)



#line_chart
'''
feature = db.features.find_one({ "video_id": "5f05d0f814e6a15bdc797d12"})
Year = []
Unemployment_Rate = []
line_chart = { x['frame_sec'] : len(json.loads(x['persons'])) for x in feature['metadata']}

import matplotlib.pyplot as plt
import cv2
import io
   
Year = list(line_chart.keys())
Unemployment_Rate = list(line_chart.values())
print(Year,Unemployment_Rate)
  
plt.plot(Year, Unemployment_Rate)
plt.title('Timestamp Vs No. of persons')
plt.xlabel('No. of persons')
plt.ylabel('Timestamp')
plt.show()
'''
# buf = io.BytesIO()
# plt.savefig(buf, format="png", dpi=180)
# print(buf)
# cv2.imwrite("uwt.png",buf)





import time
import matplotlib.pyplot as plt
#heatMap
# '''
start = time.time()

data = db.unique_person.find({"video_id": "5f05d0f814e6a15bdc797d12"},{"labels":1, "colors":1,"_id":0})
new_data = [ [x+','+y for x,y in zip(t['labels'],t['colors'])] for t in data]
meta = [_ for i in range(len(new_data)) for _ in new_data[i]]
cc = Counter(meta)
colors = [ key.split(",")[1] for key in cc]

# features = { {[key.split(",")[0]][key.split(",")[1]] : cc[key]} for key in cc}

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

features=AutoVivification()
for key in cc:
        if key.split(",")[0] not in features.keys():
                for x in colors:
                        features[key.split(",")[0]][x] = 0
        features[key.split(",")[0]][key.split(",")[1]] = cc[key]
corr = [ list(val.values()) for val in features.values()]
print(list(features.keys()),list(features.values())[0].keys(),corr,time.time()-start)

end = time.time()
# print(end-start)

import seaborn as sns
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg

fig = plt.figure(figsize=(12,10), dpi= 80)
sns.heatmap(corr, xticklabels=list(list(features.values())[0].keys()), yticklabels=list(features.keys()), cmap='RdYlGn', center=0, annot=True)

# print(df.corr(), df.corr().columns, df.corr().columns)

# Decorations
plt.title('Relationship between Labels and resp. Colors', fontsize=14)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
png = BytesIO()
FigureCanvasAgg(fig).print_png(png)
plt.close(fig)
# print(png.getvalue())
print(time.time()-end)
# '''
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

