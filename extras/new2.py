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
import seaborn as sns
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from bson import ObjectId

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('logo512.png', 10, 8, 15)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Gearstalk Search Report', 0, 0, 'C')
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
dataframe = []

report = db.report.find_one({ "_id": ObjectId("5f16adfa5fe7342de7eeb348")})
# print(report['results'])
# print
for x in report['results']:
    instance = []
    # frame_sec = []
    # time = []
    # print(i['time']) 
    # print(x)
    if not x:
        print("List is empty")
    else:  
              
        # print(x)
        for i in x:
            # print(i)
            y = {}
            y.update({'Date':i['date']})
            y.update({'Time':i['time']})
            y.update({'City':i['city']})
            y.update({'SubLocality':i['sublocality']})
            y.update({'State':i['state']})
            y.update({'Country':i['country']})
            # y.update({'Labels':i['labels']])
            # y.update(['Colours':i['colors']])
            instance.append(y)
    data.append(instance)
# print(data)    
    # data.append(mini_data)
        # for i in mini_data:
        #     print(i)

# for i in data:
#     print(i)
# print(data)


pdf=PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times','B',14.0) 
# th = pdf.font_size
# epw = pdf.w - 2*pdf.l_margin
# col_width = epw/2
pdf.cell(0,20, "Report of User's Search Result", 0, 2, 'C')
for i in range(len(data)):
    if not i:
        pdf.cell(0,10,"The person "+str(i)+" is not found ", 0, 1, "L")
    else:
        pdf.cell(0,10,"The number of Persons found with the provided details of clothing attributes are " + str(len(data[i])), 0, 1, "L")
        # print("The number of Persons found with the provided details of clothing attributes are " + str(len(data[i])))
        # print(data[i])
        for row in range(len(data[i])):
            # Enter data in colums
            print(data[i][row]['Date'])
            pdf.cell(0,15, "Details of the Instance " + str(row)+ " of Person " + str(i)+ " are:", 0, 1 , 'L')
            # print(row['Date'])
            # print("The selected person was found on "+ row['Date']+" at " +row['Time']+ ". The Camera spotted the person at "+row['SubLocality']+ ", " +row['City']+ ", "+row['State']+ ", "+row['Country']+ ". The Person is found wearing the searched clothes.")
            pdf.multi_cell(0,10, "The selected person was found on "+ data[i][row]['Date']+" at " +data[i][row]['Time']+ ". The Camera spotted the person at "+data[i][row]['SubLocality']+ ", " +data[i][row]['City']+ ", "+data[i][row]['State']+ ", "+data[i][row]['Country']+ ". The Person is found wearing the searched clothes.",0, 3, "L")
            pdf.ln(28)
            # Notice the use of the function str to coerce any input to the 
            # string type. This is needed
            # since pyFPDF expects a string, not a number.
            # pdf.cell(col_width, 2*th, "Hello "+str(datum), border=1, align = 'C')
        
            # pdf.ln(2*th)
        if(i < len(data)-1):
            pdf.add_page()
pdf.output('table.pdf','F')

