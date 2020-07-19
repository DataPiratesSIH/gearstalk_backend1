import os
import time
import itertools
import json
import requests
from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import jwt_required
from utils.connect import client, db, fs
from bson import ObjectId
from bson.json_util import dumps

report = Blueprint("report", __name__)

'''-----------------------------------
            report-crud
-----------------------------------'''

@report.route('/getreport/<oid>', methods=['GET'])
# @jwt_required
def getReport(oid):
    if oid == None:
        return jsonify({"success": False, "message": "No Object Id in param."}), 400
    if "report" not in db.list_collection_names():
        return jsonify([]), 200
    else:
        reports = list(db.report.find({"userId": oid}))
        return dumps(reports), 200

@report.route('/addreport', methods=['POST'])
# @jwt_required
def addReport():
    report = json.loads(request.data)
    if report == None:
        return jsonify({"success": False, "message": "No data found in request."}), 400
    # try:
    res = db.report.insert_one(report)
    oid = res.inserted_id

    ## Oid received. Generate PDF Report from oid

    return jsonify({"success": True, "report_link": "https:datapiratessih.github.io"}), 200
    # except Exception as e:
    #     return jsonify({"success": False, "message": "No data found in request."}), 400

@report.route('/generatereport/<oid>', methods=['GET'])
# @jwt_required
def generateReport(oid):
    if oid == None:
        return jsonify({"success": False, "message": "No Object Id in param."}), 400

    oid = ObjectId(oid)

    ## Oid received. Generate PDF Report from oid
        
    return jsonify({"success": True, "report_link": "https:datapiratessih.github.io"}), 200

@report.route('/deletereport/<oid>', methods=['DELETE'])
# @jwt_required
def deleteReport(oid):
    if oid == None:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
    else:
        if "report" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection report."}), 404
        else:
            result = db.report.delete_one({"_id": ObjectId(oid)})
            if (result.deleted_count) > 0:
                return jsonify({"success": True, "message": "Report successfully deleted."}), 200
            else: 
                return jsonify({"success": False, "message": "Report with provided id doesn't exist."}), 404