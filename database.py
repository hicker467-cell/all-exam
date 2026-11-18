import hashlib
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, DB_NAME

_client = None
_db = None

def get_db():
    global _client, _db
    if _db is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=8000)
        _db = _client.get_database(DB_NAME)
        # Unique index on dedup_hash for 100% duplicate prevention
        _db.notifications.create_index("dedup_hash", unique=True)
        _db.notifications.create_index("exam_id")
        _db.notifications.create_index("academic_year")
        # 30-day auto-cleanup TTL index
        _db.notifications.create_index("created_at", expireAfterSeconds=30 * 86400)
        # Unique index for Coding with Sudhir tech alerts
        _db.tech_notifications.create_index("dedup_hash", unique=True)
        # 30-day auto-cleanup TTL index
        _db.tech_notifications.create_index("created_at", expireAfterSeconds=30 * 86400)
    return _db

def generate_dedup_hash(exam_id: str, title: str, link: str, dates: dict = None) -> str:
    """
    Creates a canonical SHA-256 hash from cleaned exam_id, normalized title, core document url and key date.
    Removes tracking parameters (?v=, &id=) so URLs don't cause duplicate alerts.
    """
    clean_link = link.split("?")[0].strip().lower()
    clean_title = "".join(ch for ch in title.lower() if ch.isalnum() or ch.isspace()).strip()
    key_date = dates.get("form_last_date", "") if dates else ""
    raw = f"{exam_id}:{clean_title}:{clean_link}:{key_date}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def is_duplicate(dedup_hash: str) -> bool:
    db = get_db()
    return db.notifications.find_one({"dedup_hash": dedup_hash}) is not None

def save_notification(doc: dict) -> bool:
    db = get_db()
    doc["created_at"] = datetime.utcnow()
    try:
        db.notifications.insert_one(doc)
        return True
    except Exception as e:
        # Duplicate key error or write error
        return False

def generate_tech_dedup_hash(tool_id: str, version_tag: str) -> str:
    """
    Creates a unique hash per software version so each new release fires exactly once.
    """
    raw = f"tech:{tool_id.lower().strip()}:{version_tag.lower().strip()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def is_tech_duplicate(dedup_hash: str) -> bool:
    db = get_db()
    return db.tech_notifications.find_one({"dedup_hash": dedup_hash}) is not None

def save_tech_notification(doc: dict) -> bool:
    db = get_db()
    doc["created_at"] = datetime.utcnow()
    try:
        db.tech_notifications.insert_one(doc)
        return True
    except Exception as e:
        return False
