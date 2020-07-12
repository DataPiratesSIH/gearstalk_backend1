import os
from dotenv import load_dotenv
from flask_pymongo import pymongo
from gridfs import GridFSBucket
import googlemaps

load_dotenv()
CONNECTION_STRING = os.getenv("MONGODB_STRING_CLOUD")
GOOGLEMAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('gearstalk')
fs = GridFSBucket(db)
gmaps = googlemaps.Client(key=GOOGLEMAPS_KEY)

stopwords =  ['Blazer', 'Burkha', 'Headwear', 'Long pants', 'Scarf', 'Sweater', 'Vest', 'bags', 'chudidar', 'hoddie', 'jeans', 'jersey', 'kurta', 'saree', 'shirt', 'shoes', 'skirt', 'strip-dress', 'sunglasses', 'tops', 'trousers', 'tshirt']