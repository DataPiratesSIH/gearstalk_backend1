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

process = Blueprint('process', __name__)
executor = Executor()

@process.route('/processvideo/<oid>', methods=['GET'])
@jwt_required
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



'''
for testing only

@process.route('/video', methods=['POST'])
def Video():
    # print('inside')
    # data = request.form
    # video = request.files['vidcap']
    # print(video)
    # image_cv = video.read()
    
    
    # np_image = np.frombuffer(image_cv, dtype=np.uint8)                                      # convert string data to numpy array
    
    # video_name = cv2.imdecode(np_image, flags=1)                                                   # convert numpy array to image
    # print(video_name)

    # def processor():

    path = "C:\\Users\\Lenovo\\Downloads\\Documents\\GitHub\\yolo_textiles\\videos\\airport.mp4"
    oid = 123467
    timestamp = "19/06/20" 

    vidcap = cv2.VideoCapture(path)
    sec = 0

    frameRate = 0.5                         
    # urls = itertools.cycle(['postman','vscode','ecplise'])
    success = getFrame(vidcap,oid,sec,timestamp)
    while success:
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(vidcap,oid,sec,timestamp)

    vidcap.release()

    #-----------------------------------
                    #end
    #-----------------------------------

    print("Processing Done. Now Removing Video.")
    # if os.path.exists(video_name):
    #     os.remove(video_name)

    print('Finished entire process')
    # executor.submit(processor)
    return jsonify({"status": "Video will be processed in a while!"}), 200

'''