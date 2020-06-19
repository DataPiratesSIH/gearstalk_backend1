import os
import time
import json,requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.connect import client, db, fs
from utils.geocode import address_resolver
from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
from bson.json_util import dumps
from utils.utils import getFirstFrame, allowed_file, randomString

video = Blueprint("video", __name__)

record = ['None', 'Today', 'This Week', 'This Month', 'This Year']
duration = ['None', 'Short (<4 minutes)', 'Medium (>4 minutes and <20 minutes)', 'Long (>20 minutes)']
sort = ['Relevance', 'Upload Date', 'Duration']
typeOf = ['None', 'Processed', 'Unprocessed']

def sameWeek(dateString):
    d1 = datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.today()
    return d1.isocalendar()[1] == d2.isocalendar()[1] \
            and d1.year == d2.year

def sameMonth(dateString):
    d1 = datetime.strptime(dateString,'%Y-%m-%d')
    d2 = datetime.today()
    print(d1.month, d2.month)
    return d1.month == d2.month \
            and d1.year == d2.year


def filterNone(filter):
    if filter['record'] == record[0] and filter['duration'] == duration[0] and filter['sort'] == sort[0] and filter['type'] == typeOf[0]:
        return None
    else:
        return True

def filterByRecord(recordVal, videos):
    if recordVal == record[0]:
        return videos
    elif recordVal == record[1]:
        items = []
        today = str(datetime.today().date())
        for v in videos:
            if v['date'] == today:
                items.append(v)
        return items
    elif recordVal == record[2]:
        items = []
        for v in videos:
            if sameWeek(v['date']):
                items.append(v)
        return items
    elif recordVal == record[3]:
        items = []
        for v in videos:
            if sameMonth(v['date']):
                items.append(v)
        return items
    elif recordVal == record[4]:
        items = []
        for v in videos:
            if datetime.strptime(v['date'],'%Y-%m-%d').year == datetime.today().year:
                items.append(v)
        return items
    else:
        return videos

def filterByDuration(durationVal, videos):
    if durationVal == duration[0]:
        return videos
    elif durationVal == duration[1]:
        items = []
        for v in videos:
            if int(v['duration'][0:2]) * 60 + int(v['duration'][3:5]) < 4:
                items.append(v)
        return items
    elif durationVal == duration[2]:
        items = []
        for v in videos:
            if int(v['duration'][0:2]) * 60 + int(v['duration'][3:5]) > 4 \
             and int(v['duration'][0:2]) * 60 + int(v['duration'][3:5]) < 20:
                items.append(v)
        return items
    elif durationVal == duration[3]:
        items = []
        for v in videos:
            if int(v['duration'][0:2]) * 60 + int(v['duration'][3:5]) > 20:
                items.append(v)
        return items
    else:
        return videos

def filterByType(typeVal, videos):
    if typeVal == typeOf[0]:
        return videos
    elif typeVal == typeOf[1]:
        items = []
        for v in videos:
            if v['processed'] == True:
                items.append(v)
        return items
    elif typeVal == typeOf[1]:
        items = []
        for v in videos:
            if v['processed'] == False:
                items.append(v)
        return items
    else:
        return videos

def sortBy(sortVal, videos):
    if sortVal == sort[0]:
        return videos
    elif sortVal == sort[1]:
        videos.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
        for v in videos:
            print(v['date'])
        return videos
    elif sortVal == sort[2]:
        videos.sort(key=lambda x: int(x['duration'][0:2]) * 3600 + int(x['duration'][3:5]) * 60 + int(x['duration'][6:8]), reverse=True)
        return videos
    else:
        return videos


'''-----------------------------------
            video-crud
-----------------------------------'''

# Get all Video documents
@video.route('/getvideo', methods=['GET'])
@jwt_required
def getVideo():
    if "video" not in db.list_collection_names():
        return jsonify([]), 200
    else:
        videos = list(db.video.find({}))
        return dumps(videos), 200

# Get Video by id
@video.route('/getvideobyid/<oid>', methods=['GET'])
@jwt_required
def getVideoById(oid):
    if oid == None:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
    else:
        if "video" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection video."}), 404
        else:
            video = db.video.find_one({ "_id": ObjectId(oid)})
            return dumps(video), 200

# Returns videos for a search query
@video.route('/search', methods=['POST'])
@jwt_required
def getVideoSearch():
    data = json.loads(request.data)
    search = data.get("search")
    if "video" not in db.list_collection_names() or search == None or search == "":
        return jsonify([]), 200
    else:
        videos = list(db.video.find({}))
        items = []
        for v in videos:
            if search.lower() in v['name'].lower():
                items.append(v)

        return dumps(items), 200

@video.route('/filter', methods=['POST'])
@jwt_required
def getVideoFilter():
    data = json.loads(request.data)
    filter = data.get("filter")
    print(filter)
    if "video" not in db.list_collection_names() or filter == None:
        return jsonify([]), 200
    elif filterNone(filter) == None:
        videos = list(db.video.find({}))
        return dumps(videos), 200
    else:
        videos = list(db.video.find({}))
        videos = filterByRecord(filter['record'], videos)
        videos = filterByDuration(filter['duration'], videos)
        videos = filterByType(filter['type'], videos)
        videos = sortBy(filter['sort'], videos)
        return dumps(videos), 200

# Upload a video to the database
@video.route('/addvideo', methods=['POST'])
@jwt_required
def addVideo():
    file = request.files['video']
    timestamp = request.form.get("time")
    location = request.form.get("location")
    process = request.form.get("process")
    name = file.filename
    name = os.path.splitext(name)[0]
    if process == "true":
        process = True
    else:
        process = False
    if file and allowed_file(file.filename):    
        if file.filename == None:
            filename = "Unknown_video"
        else:
            filename = secure_filename(file.filename)

    tmz_str = ' GMT+0530 (India Standard Time)'
    if timestamp.endswith(tmz_str):
        timestamp = timestamp.replace(tmz_str, '')

    date_time_obj = None
    try:
        date_time_obj = datetime.strptime(timestamp, '%a %b %d %Y %H:%M:%S')
    except Exception as e:
        pass
    if date_time_obj == None:
        return jsonify({
            "success": False,
            "message": "Timestamp is invalid. Please try again!"
        }), 403
        
    oid = fs.upload_from_stream(filename, file)
    video_name = 'saves/' + randomString() + '.mp4'
    f = open(video_name, 'wb+')
    fs.download_to_stream(oid, f)
    f.close()
    try:
        metadata = getFirstFrame(video_name)
        thumbnail = metadata[0]
        duration = time.strftime("%H:%M:%S", time.gmtime(metadata[1]))
    except Exception as e:
        print(e)
        if os.path.exists(video_name):
            os.remove(video_name)
        return jsonify({"success": False, "message": "Failed to process video"}), 500

    thumbnail_oid = fs.upload_from_stream(str(oid), thumbnail)
    # To check if image is saved
    # f_img = open('saves/frame2.jpg','wb+')
    # fs.download_to_stream(thumbnail_oid, f_img)
    # f_img.close()

    # insert video details
    db.video.insert_one({
        "name": name,
        "date": str(date_time_obj.date()),
        "time": str(date_time_obj.time()),
        "location_id": location,
        "file_id": str(oid),
        "thumbnail_id": str(thumbnail_oid),
        "duration": duration,
        "processed": False
    })

    if os.path.exists(video_name):
        os.remove(video_name)

    return jsonify({
        "success": True, 
        "message": "Video successfully uploaded"
    }), 200

'''
# Update Video by id
@video.route('/updatevideo', methods=['POST'])
def updateVideo():
    file = request.files['video']
    if file.filename == None:
        filename = "Unknown.video"
    else:
        filename = str(file.filename)
    oid = fs.upload_from_stream(filename, file)
    f = open('saves/test.mp4','wb+')
    fs.download_to_stream(oid, f)
    f.close()
    try:
        thumbnail = getFirstFrame('saves/test.mp4')
    except Exception as e:
        return jsonify({"success": False, "message": "Failed to process video"}), 500

    thumbnail_oid = fs.upload_from_stream(str(oid), thumbnail)
    return jsonify({
        "success": True, 
        "message": "Video successfully uploaded",
        "video": str(oid),
        "thumbnail": str(thumbnail_oid)
    }), 200

'''

# Update Video Location
@video.route('/updatevideolocation', methods=['PATCH'])
@jwt_required
def updateVideoLocation():
    data = json.loads(request.data)
    video_id = data.get("video_id")
    location_id = data.get("location_id")
    if video_id == None or location_id == None:
        return jsonify({"success": False, "message": "Fields are empty."}), 401
    try:
        location = db.cctv.find_one({ "_id": ObjectId(location_id)})
    except Exception as e:
        print(e)
        return jsonify({"success": False, "message": "Camera not found in database."}), 401
    result = db.video.update_one({"_id": ObjectId(video_id)}, { "$set": { "location_id": str(location["_id"]) } })
    if result.matched_count == 0:
        return jsonify({"success": False, "message": "ObjectId cannot be found."}), 404
    elif result.modified_count == 0:
        video = db.video.find_one({ "_id": ObjectId(video_id)})
        return dumps(video), 201
    else:
        video = db.video.find_one({ "_id": ObjectId(video_id)})
        return dumps(video), 200
    
# Update Video Timestamp
@video.route('/updatevideotimestamp', methods=['PATCH'])
@jwt_required
def updateVideoTimestamp():
    data = json.loads(request.data)
    video_id = data.get("video_id")
    timestamp = data.get("time")
    if video_id == None or timestamp == None:
        return jsonify({"success": False, "message": "Fields are empty."}), 401
    tmz_str = ' GMT+0530 (India Standard Time)'
    if timestamp.endswith(tmz_str):
        timestamp = timestamp.replace(tmz_str, '')
    date_time_obj = None
    try:
        date_time_obj = datetime.strptime(timestamp, '%a %b %d %Y %H:%M:%S')
    except Exception as e:
        print(e)
        pass
    if date_time_obj == None:
        return jsonify({
            "success": False,
            "message": "Timestamp is invalid. Please try again!"
        }), 403
    result = db.video.update_one(
            {"_id": ObjectId(video_id)}, 
            { "$set": { 
                "date": str(date_time_obj.date()),
                "time": str(date_time_obj.time()) 
            } })
    if result.matched_count == 0:
        return jsonify({"success": False, "message": "ObjectId cannot be found."}), 404
    elif result.modified_count == 0:
        video = db.video.find_one({ "_id": ObjectId(video_id)})
        return dumps(video), 201
    else:
        video = db.video.find_one({ "_id": ObjectId(video_id)})
        return dumps(video), 200

# Delete Video by id
@video.route('/deletevideo/<oid>', methods=['DELETE'])
@jwt_required
def deleteVideo(oid):
    if oid == None:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
    else:
        if "video" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection video."}), 404
        else:
            video = db.video.find_one({ "_id": ObjectId(oid)})
            try:
                fs.delete(ObjectId(video["file_id"]))
                fs.delete(ObjectId(video["thumbnail_id"]))
            except Exception as e:
                print(e)
                return jsonify({"success": False, "message": "Delete operation failed."}), 404
            result = db.video.delete_one({"_id": ObjectId(oid)})
            if (result.deleted_count) > 0:
                return jsonify({"success": True, "message": "Video successfully deleted."}), 200
            else: 
                return jsonify({"success": False, "message": "Video with provided id doesn't exist."}), 404


