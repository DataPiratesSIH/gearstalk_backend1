from flask import Flask, render_template
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json
from flask import jsonify
from flask_cors import CORS
from flask import request
import itertools
from collections import Counter

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('gearstalk')

video_sample = "987654321"

@app.route('/',methods=['GET']) #method to get data from the database to the javascript of the line graph.
def index2():
    frame_sec_array = []
    labels_array = []
    line_chart = []
    big_data = []
    big_data2 = []
    y_axis = []
    x_axis = []
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
                line_dict = {"date": frame_sec, "value":len(person1)}
                dict_new2 = {"frame_sec": frame_sec, "Number of People":len(person1), "feature_label": dict_array}
                big_data.append(dict_new2)
                line_chart.append(line_dict)
                big_data2.append(dict_new)

    counter = Counter() 
    for d in big_data2:  
        counter.update(d) 
      
    result = dict(counter) 
    # print(result)
    for key,value in result.items():
        res = {"category" : key, "value1": value}
        labels_array.append(res)

    return jsonify(line_chart, big_data, labels_array)


if __name__ == '__main__':
    app.run(debug=True)

