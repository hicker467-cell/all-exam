# Sagar Coaching Centre: Target Websites, Screenshot Engine & Yearly Database Architecture

---

## 1. कुल कितने Exams और कितनी Websites हैं? (Total Count)

हमने 12वीं तक के सभी महत्वपूर्ण एग्जाम्स को 5 श्रेणियों में बांटा है:

| श्रेणी (Category) | कुल Exams | कुल Websites/Portals | मुख्य आकर्षण (Views Driver) |
| :--- | :---: | :---: | :--- |
| **1. टैलेंट सर्च & स्कॉलरशिप (Science/Maths/Scholarship)** | **9** | **7** | सर सी.वी. रमन, रामानुजन, NMMS (4 राज्य), PM यशस्वी, मेधासॉफ्ट |
| **2. स्कूल प्रवेश परीक्षाएं (Class 5/6/8/9 Admissions)** | **10** | **7** | नवोदय (6th & 9th), सैनिक स्कूल, मिलिट्री स्कूल, सिमुलतला, CHS BHU |
| **3. राज्य बोर्ड मैट्रिक व इंटर (10th & 12th Boards)** | **6** | **5** | बिहार बोर्ड (BSEB), UP बोर्ड, MP बोर्ड, राजस्थान बोर्ड |
| **4. वोकेशनल, डिप्लोमा & कॉलेज एंट्रेंस (10th/12th Pass)** | **5** | **3** | बिहार पॉलिटेक्निक (PE), ITICAT, UP JEECUP, CUET-UG, B.Sc नर्सिंग |
| **5. 12वीं पास तुरंत सरकारी नौकरी (Defence & Jobs)** | **6** | **4** | अग्निवीर (Army/Airforce), SSC GD/CHSL, बिहार/UP पुलिस, रेलवे |
| **कुल योग (Grand Total)** | **36 Exams** | **26 Official Websites** | *(कई बोर्ड्स जैसे BCECEB व NTA एक ही पोर्टल पर 3-4 एग्जाम्स चलाते हैं)* |

> 💡 **शुरुआती चरण (Phase 1 - तुरंत शुरू करने लायक):** 
> सबसे पहले शीर्ष **12 पोर्टल्स** (CV Raman, NMMS, Navodaya, Sainik School, Simultala, BSEB, Medhasoft, BCECEB) चालू होंगे, जहाँ से 80% ट्रैफिक आता है।

---

## 2. स्क्रीनशॉट इंजन (Automated Screenshot Capture Engine)

### क्या सिस्टम खुद ब्राउज़र खोलकर स्क्रीनशॉट ले सकता है?
**हाँ, 100% ले सकता है!** Playwright हेडलेस ब्राउज़र से यह बिल्कुल ऑटोमैटिक होगा:

1. **कैसे काम करेगा?**
   * जैसे ही कोई नया नोटिस आएगा, सिस्टम बैकग्राउंड में ब्राउज़र खोलेगा।
   * नोटिस का हेडर, तारीख और सर्कुलर वाला हिस्सा हाइलाइट करके एक साफ़ `.png` स्क्रीनशॉट ले लेगा।
   * यह स्क्रीनशॉट सीधे MongoDB में लिंक हो जाएगा और फोल्डर `screenshots/` में सुरक्षित रहेगा।
2. **यूट्यूब और कोचिंग के लिए इसके 3 बड़े फायदे:**
   * **YouTube Thumbnail:** सागर सर के वीडियो थंबनेल पर यही असली सरकारी स्क्रीनशॉट लगेगा (जिससे क्लिक 5 गुना बढ़ जाते हैं)।
   * **100% प्रमाण (Proof):** WhatsApp और Telegram पर नोटिस टेक्स्ट के साथ असली स्क्रीनशॉट जाएगा, जिससे छात्रों को 100% भरोसा होगा कि खबर सच्ची है।
   * **एडमिन 1-सेकंड प्रीव्यू:** आपको खुद साइट खोलकर चेक करने की ज़रूरत नहीं होगी; आप स्क्रीनशॉट देखकर ही समझ जाएंगे कि नोटिस किस बारे में है।

---

## 3. पुराने साल (Previous Year) की गलत न्यूज़ से बचने का पक्का नियम

सरकारी वेबसाइट्स पर अक्सर पिछले साल (2023, 2024) के पुराने लिंक होमपेज पर पड़े रहते हैं। इससे बचने के लिए हमने **Year Validation Filter** तैयार किया है:

### फ़िल्टर नियम (Year Safety Rules):
1. **Current Academic Session Check:**
   * सिस्टम का एक्टिव सेशन सेट रहेगा: `2025-2026` (या चालू वर्ष)।
2. **AI Year & Date Extraction:**
   * AI नोटिस के अंदर की तारीख (उदा. *"दिनांक 12/10/2023"* या *"सत्र 2023-24"*) पढ़ेगा।
   * अगर नोटिस में लिखा साल चालू सत्र से पुराना है, तो AI उसे तुरंत **`OLD_ARCHIVED_NOTICE`** मार्क करके डेटाबेस में इग्नोर कर देगा। कभी छात्रों को नहीं भेजेगा।
3. **अगले साल (Next Year) ऑटोमैटिक रोलओवर:**
   * डेटाबेस में हर रिकॉर्ड के साथ `academic_year` (उदा. `2025-26`) और `exam_year` (`2025`) अलग कॉलम में स्टोर होगा।
   * 2026 या 2027 आने पर सिस्टम खुद साल बढ़ा लेगा और पिछले साल का सारा डेटा इतिहास (Archive) में सुरक्षित रहेगा, ताकि छात्र पिछले साल का कट-ऑफ देख सकें।

---

## 4. MongoDB डेटाबेस स्कीमा (Database Schema Architecture)

डेटाबेस में कोई गड़बड़ी न हो, इसके लिए 3 मुख्य टेबल्स (Collections) होंगी:

```javascript
// 1. NOTIFICATIONS COLLECTION (notifications)
{
  "_id": ObjectId("..."),
  "exam_id": "bihar_cv_raman",            // एग्जाम का यूनिक कोड
  "exam_name": "Sir CV Raman Talent Search in Science",
  "category": "scholarship",              // scholarship / admission / board / job
  "target_class": ["6", "7", "8", "9", "10", "11", "12"],
  "state": "Bihar",
  
  // Year & Validity (गलत साल रोकने के लिए)
  "academic_year": "2025-2026",
  "exam_year": 2025,
  "is_current_session": true,
  
  // Notice Details
  "title": "CV Raman 2025 Admit Card Released",
  "title_hindi": "सर सी.वी. रमन विज्ञान परीक्षा 2025 का एडमिट कार्ड जारी",
  "summary_hindi": "कक्षा 6 से 12 तक के छात्र अपना एडमिट कार्ड नीचे दिए लिंक से डाउनलोड करें...",
  "event_type": "ADMIT_CARD",             // FORM / ADMIT_CARD / RESULT / ANSWER_KEY
  
  // Links & Proof
  "official_website": "https://state.bihar.gov.in/dst",
  "direct_pdf_url": "https://bcst.org.in/notices/admit_card_2025.pdf",
  "screenshot_path": "/screenshots/cv_raman_admit_2025.png",
  
  // Anti-Duplicate Hash (Unique Index)
  "dedup_hash": "sha256_bihar_cv_raman_2025_admit_card",
  
  // Sagar Coaching YouTube Growth Metadata
  "youtube_metadata": {
    "suggested_title": "CV Raman Exam 2025 Admit Card Kaise Download Kare | Direct Link | Sagar Sir",
    "suggested_tags": ["cv raman admit card 2025", "bcst patna", "sagar coaching", "science olympiad bihar"],
    "coaching_video_url": "https://youtube.com/watch?v=..." // जब सागर सर वीडियो अपलोड करें
  },
  
  "broadcast_status": {
    "telegram_sent": true,
    "whatsapp_sent": false,
    "website_live": true
  },
  
  "published_at": ISODate("2026-11-15T09:30:00Z"),
  "created_at": ISODate("2026-11-15T09:35:00Z")
}
```

```javascript
// 2. COACHING VIDEOS COLLECTION (coaching_videos)
{
  "_id": ObjectId("..."),
  "title": "NMMS Exam 2025 OMR Sheet Kaise Bhare | Sagar Sir",
  "youtube_id": "dQw4w9WgXcQ",
  "video_url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
  "thumbnail_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
  "related_exam": "nmms_bihar",
  "target_class": "8",
  "published_at": ISODate("...")
}
```
