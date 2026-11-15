import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
print("Connecting to MongoDB Atlas...")
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=8000)
    db = client.get_database("all_exams_db")
    
    # Test index creation for Zero-Duplicate Guarantee
    db.notifications.create_index("dedup_hash", unique=True)
    
    # Count documents
    count = db.notifications.count_documents({})
    print(f"MongoDB Connected Successfully! Active DB: 'all_exams_db', Collections: {db.list_collection_names()}, Docs: {count}")
    
    # Test inserting and updating a heartbeat record
    db.system_status.update_one(
        {"service": "all_exam_bot"},
        {"$set": {"last_test": "SUCCESS", "status": "ONLINE"}},
        upsert=True
    )
    print("Heartbeat written successfully to MongoDB.")
except Exception as e:
    print("MongoDB Connection Error:", e)
