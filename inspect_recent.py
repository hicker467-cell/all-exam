from database import get_db

db = get_db()
docs = list(db.notifications.find().sort("_id", -1).limit(10))
print(f"Total in notifications: {db.notifications.count_documents({})}")
for d in docs:
    print(f"- Title: {d.get('title')[:60]}")
    print(f"  Source: {d.get('source_name')} | Exam ID: {d.get('exam_id')}")
    print(f"  Dates: {d.get('dates')}")
    print(f"  Created At: {d.get('created_at')}\n")

print("\n--- TECH NOTIFICATIONS ---")
tech_docs = list(db.tech_notifications.find().sort("_id", -1).limit(5))
for t in tech_docs:
    print(f"- Tech Title: {t.get('title')}")
    print(f"  Badge: {t.get('release_badge')}")
    print(f"  Created At: {t.get('created_at')}\n")
