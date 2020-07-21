import os
import time
import itertools
import json
import requests
from flask import Blueprint, request, jsonify, render_template, make_response
from flask_jwt_extended import jwt_required
from utils.connect import client, db, fs
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt
from fpdf import FPDF
from bson import ObjectId
import seaborn as sns
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from bson.json_util import dumps

report = Blueprint("report", __name__)


'''-----------------------------------
        support functions
-----------------------------------'''

"""Implementation of perl's autovivification feature.(Wrapper-Function)"""
class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class PDF(FPDF):
    def header(self):
        # Logo
        # self.image('logo512.png', 10, 8, 15)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Gearstalk Report', 0, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def image_to_buffer(plt_image):
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=180)
    return buf


def videoPDF_format(video,line_chart,linechart_buf,heatmap_buf,piechart_buf):
    pdf=PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    image_w,image_h = 100,80
    pdf.set_font('Times','B',14.0) 

    pdf.cell(0, 30, txt="A Tabular and Graphical Report of number of people identified in the video", ln = 1, align = 'C')

    image_w,image_h = 140,140
    
    data =[]
    for x in video:
        data.append(["Name of Video",x['name']])
        data.append(["Date",x['date']])
        data.append(["Time",x['time']])
        data.append(["Duration of the video",x['duration']])
        location = db.cctv.find({"_id" : ObjectId(x['location_id'])})
        for y in location:
            # data.append(["Address", y['formatted_address']])
            data.append(["Street",y['street']])
            data.append(["City", y['city']])
            data.append(["State", y['state']])
            data.append(["Country", y['country']])
            data.append(['Postal Code', y['postal_code']])
            data.append(["Latitude", y['latitude']])
            data.append(["Longitude", y['longitude']])


    df = pd.DataFrame(data,columns=['Question','Answer'])
    # print(df)

    for i in range(0, len(df)):
        pdf.cell(80, 18, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
        pdf.cell(110, 18, '%s' % (df['Answer'].iloc[i]), 1, 1, 'C')
        # pdf.cell(-90)

    pdf.add_page()
    pdf.cell(0, 30, txt="A Tabular and Graphical Report of number of people identified in the video", ln = 1, align = 'C')
    pdf.image(linechart_buf, x=35, y=60, w=image_w, h=image_h)
    pdf.ln(1*image_h+15)
    pdf.multi_cell(0,10, "A line graph is a graphical display of information that changes continuously over time. In this case the graph displays the number of people in the video at particular timestamps. ",0, 3 , 'L')
    pdf.ln(30)
    pdf.cell(0,10," Maximum Number of people in any frame of the video = {}".format(max(line_chart.values())) , 0, 1, "L")


    pdf.add_page()
    pdf.cell(0, 30, txt="A Tabular and Graphical Report of Realation between labels and colors in the video", ln = 1, align = 'C')
    pdf.image(heatmap_buf, x=25, y=70, w=image_w + 40, h=image_h)
    pdf.ln(1*image_h+15)
    pdf.multi_cell(0,10,'The heat map is a data visualization technique that shows magnitude of a phenomenon as colour in two dimensions. This one in particular highlights the relationship between labels and their respective colours. The colours of respective clothing accessories like jeans,shirts,sweaters,etc range from various hues of grey,blue,brown and silver. Upon observation, we can conclude that the intensity of rosy brown jeans was the highest while dark grey scarfs and jeans were comparable as well.', 0, 1,'L')

    pdf.add_page()
    pdf.cell(0, 30, txt="A Tabular and Graphical Report of Realation between labels and colors in the video", ln = 1, align = 'C')
    pdf.image(piechart_buf, x=25, y=70, w=image_w + 40, h=image_h)
    pdf.ln(1*image_h+15)
    pdf.multi_cell(0,10,"This pie chart shows the result of a cctv surveillance camera, scanned frame by frame for clothing attributes. The video showcased a number of people wearing various clothing accessories. The different attributes identified are blazers, jeans, sweaters, scarfs, sarees, caps, shirts, jerseys, pants, etc. The pie chart above shows that majority people were wearing sweaters,scarfs and jeans; thereby hinting towards a possibility of cold climate.", 0, 1, 'L')


    pdf.output('Video_Analysis_Report.pdf','f')

    # return 




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
    try:
        if oid == None or len(oid) != 24:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
        elif "unique_person" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection features."}), 404
        else:
            #query db
            feature = db.features.find_one({ "video_id": oid})
            data = db.unique_person.find({"video_id": oid},{"labels":1, "colors":1,"_id":0})
            video = db.video.find({"_id" : ObjectId(oid)})


            #line chart
            line_chart = { x['frame_sec'] : len(json.loads(x['persons'])) for x in feature['metadata']}
            #plotting
            plt.plot(list(line_chart.keys()), list(line_chart.values()))
            plt.title('TimeFrame Vs No. of persons')
            plt.xlabel('No. of persons')
            plt.ylabel('TimeFrame')
            linechart_buf = image_to_buffer(plt)


            #heat Map
            new_data = [ [x+','+y for x,y in zip(t['labels'],t['colors'])] for t in data]
            meta = [_ for i in range(len(new_data)) for _ in new_data[i]]
            cc = Counter(meta)
            colors = [ key.split(",")[1] for key in cc]
            features=AutoVivification()
            for key in cc:
                if key.split(",")[0] not in features.keys():
                        for x in colors:
                                features[key.split(",")[0]][x] = 0
                features[key.split(",")[0]][key.split(",")[1]] = cc[key]
            corr = [ list(val.values()) for val in features.values()]
            #plotting
            fig = plt.figure(figsize=(12,10), dpi= 80,facecolor=(1, 1, 1))
            sns.heatmap(corr, xticklabels=list(list(features.values())[0].keys()), yticklabels=list(features.keys()), cmap='RdYlGn', center=0, annot=True)
            plt.title('Relationship between Labels and resp. Colors', fontsize=14)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            heatmap_buf = image_to_buffer(plt)


            #pie chart
            pie_chart = Counter(list(chain(*[ list(chain(*[ x['labels'] for x in json.loads(metadata['persons'])])) for metadata in feature['metadata']])))
            #plotting
            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.axis('equal')
            ax.pie(list(pie_chart.values()), labels = list(pie_chart.keys()),autopct='%1.2f%%')
            piechart_buf = image_to_buffer(plt)

            #generate_pdf
            videoPDF_format(video,line_chart,linechart_buf,heatmap_buf,piechart_buf)
            
            return jsonify({"success": True, "report_link": "https:datapiratessih.github.io"}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
        



@video.route('/searchreport/<oid>', methods=['GET'])
def search_report(oid):
    try:
        if oid == None or len(oid) != 24:
            return jsonify({"success": False, "message": "No Object Id in param."}), 400
        elif "unique_person" not in db.list_collection_names():
            return jsonify({"success": False, "message": "No Collection features."}), 404
        else:
            line_chart = { x['frame_sec'] : len(json.loads(x['persons'])) for x in feature['metadata']}

            
            return jsonify({"status": True, "message": "Report Generated", "Attachment": response}), 200
    except Exception as e:
        return f"An Error Occured: {e}"



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