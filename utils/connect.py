import os
from dotenv import load_dotenv
from flask_pymongo import pymongo
from gridfs import GridFSBucket
import googlemaps

load_dotenv()
CONNECTION_STRING = os.getenv("MONGODB_STRING_CLOUD")
GOOGLEMAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
LOAD_BALANCER_URL = os.getenv("HAPROXY_URL")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('gearstalk')
fs = GridFSBucket(db)
gmaps = googlemaps.Client(key=GOOGLEMAPS_KEY)

stopwords = ['Blazer','Burkha','Chudidar','Long-pants','Saree','Bags','Kurta','Skirt','Strip-dress','Sunglasses','Trousers','shirt']