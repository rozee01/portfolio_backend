from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["PortfolioChatbot"]
conversations = db["convo_hist"]

def get_history(thread_id):
    doc = conversations.find_one({"thread_id": thread_id})
    return doc["history"] if doc else []

def save_message(thread_id, role, content):
    conversations.update_one(
        {"thread_id": thread_id},
        {"$push": {"history": {"role": role, "content": content}}},
        upsert=True
    )

def reset_history(thread_id):
    conversations.update_one(
        {"thread_id": thread_id},
        {"$set": {"history": []}},
        upsert=True
    )