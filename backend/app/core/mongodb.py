import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
client = MongoClient(MONGO_URI)
db = client.cv_matcher

def get_jobs_collection():
    return db.linkedin_jobs
