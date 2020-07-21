import pandas as pd
import matplotlib.pyplot as plt
from pylab import title, figure, xlabel, ylabel, xticks, bar, legend, axis, savefig
from fpdf import FPDF
from collections import Counter
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient
import json
from itertools import chain
from flask import request
import time
import numpy as np
import ast
import cv2
import time
import seaborn as sns
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from bson import ObjectId


start = time.time()

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

client = MongoClient("mongodb+srv://admin:admin@cluster0-jnsfh.mongodb.net/test?retryWrites=true&w=majority")

db = client.get_database('gearstalk')
data = []

feature = db.features.find_one({ "video_id": "5f05d0f814e6a15bdc797d12"})
video = db.video.find({"_id" : ObjectId("5f05d0f814e6a15bdc797d12")})
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


image = []

# #Line Chart
line_chart_report = []
Year = []
Unemployment_Rate = []
table_data = [["Frame Sec", "Number of People"]]
line_chart = { x['frame_sec'] : len(json.loads(x['persons'])) for x in feature['metadata']}
Year = list(line_chart.keys())
Unemployment_Rate = list(line_chart.values())
fig = plt.figure(figsize=(12,10), dpi= 80)
plt.plot(Year, Unemployment_Rate)
plt.title('Timestamp Vs No. of persons')
plt.xlabel('Timestamp')
plt.ylabel('No. of persons')
# plt.savefig('plot.png')
line_buf = io.BytesIO()
plt.savefig(line_buf, format="png", dpi=180)
image.append(line_buf)
# print(png.getvalue())


# #HeatMap

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
# print(list(features.keys()),list(features.values())[0].keys(),corr,time.time()-start)
fig = plt.figure(figsize=(12,10), dpi= 80)
sns.heatmap(corr, xticklabels=list(list(features.values())[0].keys()), yticklabels=list(features.keys()), cmap='RdYlGn', center=0, annot=True)
# Decorations
plt.title('Relationship between Labels and resp. Colors', fontsize=14)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
# plt.show()
heatmap_buf = io.BytesIO()
plt.savefig(heatmap_buf, format="png", dpi=180)
image.append(heatmap_buf)


# #Pie Chart

pie_chart = Counter(list(chain(*[ list(chain(*[ x['labels'] for x in json.loads(metadata['persons'])])) for metadata in feature['metadata']])))
# print(list(pie_chart.values()))
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.axis('equal')
ax.pie(list(pie_chart.values()), labels = list(pie_chart.keys()),autopct='%1.2f%%')
pie_buf = io.BytesIO()
plt.savefig(pie_buf, format="png", dpi=180)
image.append(pie_buf)
# plt.show()




pdf=PDF()
pdf.alias_nb_pages()
pdf.add_page()
image_w = 100
image_h = 80
pdf.set_font('Times','B',14.0) 

pdf.cell(0, 30, txt="A Tabular and Graphical Report of number of people identified in the video", ln = 1, align = 'C')

image_w = 140
image_h = 140


df = pd.DataFrame(data,columns=['Question','Answer'])
# print(df)

for i in range(0, len(df)):
    pdf.cell(80, 18, '%s' % (df['Question'].iloc[i]), 1, 0, 'C')
    pdf.cell(110, 18, '%s' % (df['Answer'].iloc[i]), 1, 1, 'C')
    # pdf.cell(-90)

pdf.add_page()
pdf.cell(0, 30, txt="A Tabular and Graphical Report of number of people identified in the video", ln = 1, align = 'C')
pdf.image(image[0], x=35, y=60, w=image_w, h=image_h)
pdf.ln(1*image_h+15)
pdf.multi_cell(0,10, "A line graph is a graphical display of information that changes continuously over time. In this case the graph displays the number of people in the video at particular timestamps. ",0, 3 , 'L')
pdf.ln(30)
pdf.cell(0,10," Maximum Number of people in any frame of the video = {}".format(max(line_chart.values())) , 0, 1, "L")


pdf.add_page()
pdf.cell(0, 30, txt="A Tabular and Graphical Report of Realation between labels and colors in the video", ln = 1, align = 'C')
pdf.image(image[1], x=25, y=70, w=image_w + 40, h=image_h)
pdf.ln(1*image_h+15)
pdf.multi_cell(0,10,'The heat map is a data visualization technique that shows magnitude of a phenomenon as colour in two dimensions. This one in particular highlights the relationship between labels and their respective colours. The colours of respective clothing accessories like jeans,shirts,sweaters,etc range from various hues of grey,blue,brown and silver. Upon observation, we can conclude that the intensity of rosy brown jeans was the highest while dark grey scarfs and jeans were comparable as well.', 0, 1,'L')

pdf.add_page()
pdf.cell(0, 30, txt="A Tabular and Graphical Report of Realation between labels and colors in the video", ln = 1, align = 'C')
pdf.image(image[2], x=25, y=70, w=image_w + 40, h=image_h)
pdf.ln(1*image_h+15)
pdf.multi_cell(0,10,"This pie chart shows the result of a cctv surveillance camera, scanned frame by frame for clothing attributes. The video showcased a number of people wearing various clothing accessories. The different attributes identified are blazers, jeans, sweaters, scarfs, sarees, caps, shirts, jerseys, pants, etc. The pie chart above shows that majority people were wearing sweaters,scarfs and jeans; thereby hinting towards a possibility of cold climate.", 0, 1, 'L')


pdf.output('table-using-cell-borders.pdf','f')

print(time.time()-start)