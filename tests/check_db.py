from database import get_db

db = get_db()
docs = list(db.notifications.find())
print(f"Total Notices Saved in MongoDB: {len(docs)}")
for i, d in enumerate(docs, 1):
    print(f"{i}. [{d.get('exam_id')}] {d.get('title')[:60]}... | Dates: {d.get('dates')}")
