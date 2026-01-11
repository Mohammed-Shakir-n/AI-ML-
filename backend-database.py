from pymongo import MongoClient
import datetime

def log_to_mongodb(mongo_uri, user_query, ai_response, is_unsafe, logs):
    """Logs interaction details to MongoDB Atlas."""
    if not mongo_uri:
        return
    try:
        client = MongoClient(mongo_uri)
        db = client["yoga_app_db"]
        collection = db["interaction_logs"]
        
        document = {
            "timestamp": datetime.datetime.utcnow(),
            "user_query": user_query,
            "ai_response": ai_response,
            "is_unsafe": is_unsafe,
            "retrieved_chunks": logs,
        }
        collection.insert_one(document)
        client.close()
    except Exception as e:
        print(f"MongoDB Error: {e}")