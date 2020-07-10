import os
import cv2
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required
from time import sleep
import numpy as np
import itertools
from bson import ObjectId
from utils.connect import db, fs
from utils.utils import getFrame, randomString, processor
from flask_executor import Executor
from datetime import datetime
import json
import collections
import ast

features_pack = {}

process = Blueprint('process', __name__)
executor = Executor()

frame_rate = 2

'''------------------------------------------------
        Finding unique persons from the video
--------------------------------------------------'''

#find the unique person in video (traverse sequentially)
##find the similarity between 2 frames based on labels
##check the similarity betwen them using box sizes
#Save into db twice at 2 different locations (Whole video_output and unique_person)
def UniquePersonSearch(video_id, video_output):
    
    #Saving all the frames into the db
    db.features.insert_many(video_output)

    #converting to 3d-Array
    array3d=[]
    array3d = [collections.Counter([ str(feature['labels']+feature['colors'])  for feature in data['persons']]) for data in object_data]
    unique_person = []

    #Finding the Unique ones
    for i in range(len(array3d)-1):
        person = array3d[i]-array3d[i+1]
        if person:
            for k in person :
                unique_person.append({'last_seen': i*frame_rate,'labels': ast.literal_eval(k)})
    for k in array3d[len(array3d)-1]:
        unique_person.append({'last_seen': (i+1)*frame_rate,'labels': ast.literal_eval(k)})
    
    #Saving the unique persons into db
    db.unique_person.insert_many(unique_person)

    return "Your video is processed"




'''------------------------------------------------
    breaking video down to frames and processing
--------------------------------------------------'''

@process.route('/processvideo/<oid>', methods=['GET'])
# @jwt_required
def processVideo(oid):
    print(oid)
    if oid == None or len(oid) != 24:
        return jsonify({"success": False, "message": "No Object Id in param."}), 400
    elif "video" not in db.list_collection_names():
        return jsonify({"success": False, "message": "No Collection video."}), 404
    else:
        video = db.video.find_one({ "_id": ObjectId(oid)}) 
        if video['processed'] == True:
            return jsonify({"success": False, "message": "Video is already processed."}), 404
        elif video['processed'] == "processing":
            return jsonify({"success": False, "message": "Video is currently being processed."}), 404
        else:
            #save timestamp info in the video collection
            date = video['date']
            time = video['time']
            timestamp = json.dumps(datetime.strptime( date+time, '%Y-%m-%d%H:%M:%S'),ensure_ascii=False, indent=4, default=str)
            file_id = video["file_id"]
            processor(oid,file_id,timestamp)
            executor.submit(processor)
            # db.video.update({ "_id": ObjectId(oid) }, { "$set": { "processed" : "processing" }})
            return jsonify({"success": True, "message": "Video will be processed in a while!"}), 200



'''------------------------------------------------
    breaking video down to frames and processing
--------------------------------------------------'''

# @process.route('/processimage/<oid>', methods=['GET'])
# # @jwt_required
# def processVideo(oid):
#     print(oid)
#     if oid == None or len(oid) != 24:
#         return jsonify({"success": False, "message": "No Object Id in param."}), 400
#     elif "video" not in db.list_collection_names():
#         return jsonify({"success": False, "message": "No Collection video."}), 404
#     else:
#         video = db.video.find_one({ "_id": ObjectId(oid)}) 
#         if video['processed'] == True:
#             return jsonify({"success": False, "message": "Video is already processed."}), 404
#         elif video['processed'] == "processing":
#             return jsonify({"success": False, "message": "Video is currently being processed."}), 404
#         else:
#             #save timestamp info in the video collection
#             date = video['date']
#             time = video['time']
#             timestamp = json.dumps(datetime.strptime( date+time, '%Y-%m-%d%H:%M:%S'),ensure_ascii=False, indent=4, default=str)
#             file_id = video["file_id"]
#             processor(oid,file_id,timestamp)
#             executor.submit(processor)
#             # db.video.update({ "_id": ObjectId(oid) }, { "$set": { "processed" : "processing" }})
#             return jsonify({"success": True, "message": "Video will be processed in a while!"}), 200




'''------------------------------------------------
    Reciving video output in chunks from backend2
--------------------------------------------------'''

@process.route('/FindUnique', methods=['POST'])
def FindUnique():
    records = json.loads(request.data)
    video = db.video.find_one({ "_id": ObjectId(records['video_id'])})
    cctv = db.cctv.find_one({ "_id": ObjectId(video['location_id']) })
    print(records['unique_person'])
    if records['unique_person'] != []:
        for single_record in records['unique_person']:
            #not really sure abt the parameters
            single_record.update({'coord': {"latitude": cctv['latitude'], "longitude": cctv['longitude']}, 'location_type': cctv['location_type'], "street": cctv['street'], "city": cctv['city'], "county": cctv['county'], "country": cctv['country'], "state": cctv['state'], "sublocality": cctv['sublocality']})

        #saving unique_persons into db
        db.unique_person.insert_many(records['unique_person'])
        db.video.update({ "_id": ObjectId(records['video_id']) }, { "$set": { "processed" : True }})

    return jsonify({"success": True, "message": "Video is processed!"}), 200




# @process.route('/FindUnique', methods=['POST'])
# def FindUnique():
#     data = json.loads(request.data)
#     video_id = data['video_id']
#     frame_sec = data['frame_sec']
#     timestamp = data['timestamp']
#     total_frames = int(data['total_frames'])
#     frame_details = data['frame_details']
#     message = "Video Processing not over!!"
    
#     if video_id in features_pack.keys():
#         features_pack[video_id][int(frame_sec//frame_rate)] =  {"frame_sec":frame_sec,"persons":frame_details}
#     else:
#         arr = [None]*total_frames
#         features_pack[video_id] =  arr
#         features_pack[video_id][int(frame_sec//frame_rate)] =  {"frame_sec":frame_sec,"persons":frame_details}
    
#     if None not in features_pack[video_id]:
#         video_output = features_pack.pop(video_id)
#         message = UniquePersonSearch(video_id,video_output)

    
    # return jsonify({"status": message}), 200




'''------------------------------------------------
                for testing only
--------------------------------------------------'''

# '''
@process.route('/video', methods=['POST'])
def Video():
    path = "C:\\Users\\Lenovo\\Downloads\\Documents\\GitHub\\yolo_textiles\\videos\\airport.mp4"
    oid = 1234678
    timestamp = json.dumps(datetime.now(),ensure_ascii=False, indent=4, default=str)

    vidcap = cv2.VideoCapture(path)
    sec = 0
    count = 1
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)//(frame_rate*vidcap.get(cv2.CAP_PROP_FPS)) + 1
    print(total_frames)   
    success = getFrame(vidcap,oid,sec,timestamp,total_frames)
    while success:
        sec = sec + frame_rate
        sec = round(sec, 2)
        success = getFrame(vidcap,oid,sec,timestamp,total_frames)

    vidcap.release()
    print('Finished entire process')
    return jsonify({"status": "Video will be processed in a while!"}), 200

# '''