import hashlib
import re
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

def generate_tech_dedup_hash(tool_id: str, version_tag: str, link: str = "", title: str = "") -> str:
    """
    Creates a unique hash per software version or news item so each update fires exactly once.
    """
    clean_id = tool_id.lower().strip()
    clean_version = version_tag.lower().strip()
    clean_link = link.split("?")[0].strip().lower() if link else ""
    raw = f"tech:{clean_id}:{clean_version}:{clean_link}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def is_tech_duplicate(dedup_hash: str, link: str = "", title: str = "") -> bool:
    db = get_db()
    # 1. Exact dedup_hash check
    if db.tech_notifications.find_one({"dedup_hash": dedup_hash}) is not None:
        return True

    # 2. Canonical Link check (prevents same URL from re-triggering with different parameters)
    if link:
        clean_link = link.split("?")[0].strip().lower()
        if clean_link:
            escaped_link = re.escape(clean_link)
            if db.tech_notifications.find_one({"link": {"$regex": f"^{escaped_link}"}}) is not None:
                return True

    # 3. CVE identifier check (e.g. CVE-2026-114938)
    if title:
        cve_match = re.search(r"cve-\d{4}-\d+", title.lower())
        if cve_match:
            cve_id = cve_match.group(0)
            if db.tech_notifications.find_one({"$or": [
                {"title": {"$regex": cve_id, "$options": "i"}},
                {"tool_name": {"$regex": cve_id, "$options": "i"}},
                {"link": {"$regex": cve_id, "$options": "i"}}
            ]}) is not None:
                return True

    return False

def save_tech_notification(doc: dict) -> bool:
    db = get_db()
    doc["created_at"] = datetime.utcnow()
    try:
        db.tech_notifications.insert_one(doc)
        return True
    except Exception as e:
        return False
