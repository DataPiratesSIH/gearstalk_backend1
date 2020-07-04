import os
import cv2
from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required
from time import sleep
import numpy as np
import itertools
from bson import ObjectId
from utils.connect import db, fs
from utils.utils import getFrame, randomString, processor, UniquePersonSearch
from flask_executor import Executor
import asyncio
import datetime
import json

features_pack = {}

process = Blueprint('process', __name__)
executor = Executor()

frame_rate = 10

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
            # @app.after_response
            timestamp = video['time']                                                  #save timestamp info in the video collection
            file_id = video["file_id"]
            processor(oid,file_id,timestamp)
            executor.submit(processor)
            return jsonify({"status": "Video will be processed in a while!"}), 200



@process.route('/FindUnique', methods=['GET'])
def FindUnique():
    data = request.json
    video_id = data['video_id']
    frame_sec = data['frame_sec']
    total_frames = int(data['total_frames'])
    frame_details = data['frame_details']
    
    if video_id in features_pack.keys():
        features_pack[video_id][int(frame_sec//frame_rate)] =  {"frame_sec":frame_sec,"persons":frame_details}
    else:
        arr = [None]*total_frames
        features_pack[video_id] =  arr
        features_pack[video_id][int(frame_sec//frame_rate)] =  {"frame_sec":frame_sec,"persons":frame_details}
    
    if None not in features_pack[video_id]:
        video_output = features_pack.pop(video_id)
        UniquePersonSearch(video_id,video_output)
    # arr.append(frame_sec)
    print(features_pack)
    
    return jsonify({"status": "recieving data", "feature_array":"{}".format(features_pack)}), 200

# '''
# for testing only


async def resp():
    return response.json("OK", status=202)


def blocking_function(files):
    requests.post("https://unlucky-octopus-2.serverless.social/FashionFrame", files=files)
    # async with aiohttp.ClientSession() as session:
    #     async with session.post("https://unlucky-octopus-2.serverless.social/FashionFrame", files=files) as resp:
    #         result = await resp.text()
    #         print(result)
    # return "ok"
    # await put_in_database(result)


@process.route('/video', methods=['POST'])
def Video():
    path = "C:\\Users\\Lenovo\\Downloads\\Documents\\GitHub\\yolo_textiles\\videos\\airport.mp4"
    oid = 1234678
    timestamp = json.dumps(datetime.datetime.now(),ensure_ascii=False, indent=4, default=str)

    vidcap = cv2.VideoCapture(path)
    sec = 0
    frameRate = 10
    count = 1
    total_frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)//(frameRate*vidcap.get(cv2.CAP_PROP_FPS)) + 1
    print(total_frames)   
    success = getFrame(vidcap,oid,sec,timestamp,total_frames)
    while success:
        # print(files)
        # blocking_function(files)
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(vidcap,oid,sec,timestamp,total_frames)

    vidcap.release()
    print('Finished entire process')
    # executor.submit(processor)
    # return resp()
    return jsonify({"status": "Video will be processed in a while!"}), 200

# '''