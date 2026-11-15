# Sagar Coaching Centre - All Exam Notification & Video Platform
## Complete Master Architecture & Roadmap

---

## 1. प्रोजेक्ट का उद्देश्य (Project Vision)
**सागर कोचिंग सेंटर (Sagar Coaching Centre)** के लिए एक ऐसा ऑटोमेटेड और 100% भरोसेमंद सिस्टम बनाना जो:
1. भारत के प्रमुख प्रवेश और प्रतियोगी परीक्षाओं के आधिकारिक नोटिफिकेशन्स (Form Date, Admit Card, Result, Syllabus) को ट्रैक करे।
2. बिना किसी फेक या भ्रामक जानकारी (Zero Fake News) के केवल सरकारी/आधिकारिक स्रोतों से डेटा लाए।
3. कोचिंग सेंटर के YouTube वीडियो, क्लासेज और गाइडेंस को एक जगह छात्रों तक पहुँचाए।
4. छात्रों को WhatsApp, Telegram और वेबसाइट/ऐप पर तुरंत अलर्ट भेजे।

---

## 2. किस-किस परीक्षा (Exams) को कवर करना है?

### Category A: स्कूली व स्कॉलरशिप प्रवेश परीक्षाएं (Primary Focus for Sagar Coaching)
| Exam Name | Target Class / Age | Official Portal / Domain | Key Alerts |
| :--- | :--- | :--- | :--- |
| **NMMS** (National Means-cum-Merit Scholarship) | Class 8 | State SCERT Portals (e.g., scert.bihar.gov.in, entdata.co.in) | Form Date, Admit Card, Answer Key, District-wise Result |
| **Navodaya (JNVST)** | Class 6 & Class 9 | `navodaya.gov.in`, `cbseitms.nic.in` | Online Registration, Correction Window, Admit Card, Merit List |
| **Sainik School (AISSEE)** | Class 6 & Class 9 | `exams.nta.ac.in/AISSEE`, `nta.ac.in` | Application Window, City Slip, Admit Card, Result, Counseling |
| **Rashtriya Military School (RMS)** | Class 6 & Class 9 | `rashtriyamilitaryschools.edu.in` | CET Notification, Admit Card, Interview Dates |
| **CHS BHU (SET / EVS)** | Class 9 & Class 11 | `bhuonline.in`, `bhu.ac.in` | Entrance Test Form, School Admission List |
| **PM Yashasvi Scholarship** | Class 9 & Class 11 | `yet.nta.ac.in` | Eligibility, Application, Merit list |
| **State Board Exams** (Bihar Board, UP Board, etc.) | Class 10 & 12 | Official State Board Websites (`biharboardonline.bihar.gov.in`) | Model Papers, Timetable, Scrutiny, Result |

### Category B: आगे की प्रतियोगी परीक्षाएं (Optional / Secondary Expansion)
* **Defense / Paramilitary:** Agniveer (Army, Airforce, Navy), ITBP, CISF, CRPF Tradesman.
* **General SSC & Railway:** SSC GD, SSC MTS, RRB Group D, ALP.
* **State Police / Constable:** Bihar Police, UP Police, etc.
* **Polytechnic & ITI:** State PE / ITICAT Entrance.

---

## 3. गलत जानकारी और ब्लॉक होने से कैसे बचें? (Anti-Blocking & Accuracy)

### A. गलत जानकारी (Fake Info) से बचने का पक्का फॉर्मूला:
1. **White-listed Official Domains Only:**
   * केवल `.gov.in`, `.nic.in`, `.ac.in` या मान्यता प्राप्त आधिकारिक बोर्ड वेबसाइट्स को ही सोर्स बनाया जाएगा।
   * किसी भी प्राइवेट ब्लॉग (जैसे SarkariResult, JobRasta, etc.) से डायरेक्ट डेटा कभी नहीं लिया जाएगा, क्योंकि कई बार वहाँ तारीखें अनुमानित (tentative) या गलत होती हैं।
2. **Official PDF Hash & Link Verification:**
   * जब तक आधिकारिक नोटिस PDF नहीं मिलता, तब तक नोटिफिकेशन "Verified" मार्क नहीं होगा।
   * सिस्टम PDF डाउनलोड करके उसकी डेट और हेडर चेक करेगा।
3. **AI + Human Verification (Hybrid Safety):**
   * नया नोटिफिकेशन आते ही AI सिर्फ ड्राफ्ट बनाएगा।
   * सागर कोचिंग के एडमिन पैनल पर 1-क्लिक "Approve & Broadcast" बटन होगा ताकि कोई भी संदिग्ध चीज छात्रों तक सीधे न जाए।

### B. ब्लॉक होने से कैसे बचें (Anti-Scraping / Anti-Blocking Strategy):
1. **RSS Feeds & Sitemap First:**
   * सरकारी साइट्स (जैसे NTA, Navodaya) पर अक्सर RSS या नोटिस बोर्ड टेबल होती है।
   * पूरा पेज बार-बार लोड करने के बजाय सिर्फ नोटिस बोर्ड के पहले 5 लिंक चेक करेंगे।
2. **Polite Scraping (Rate Limiting & Delay):**
   * हर 15 से 30 मिनट में एक बार चेक करें (लगातार हर सेकंड हिट न करें)।
   * Requests के बीच 5 से 10 सेकंड का रैंडम गैप (Jitter)।
3. **ETag & `If-Modified-Since` Headers:**
   * वेबसाइट को सिर्फ तब फेच करें जब उस पर कोई बदलाव हुआ हो। अगर पेज नहीं बदला, तो सर्वर `304 Not Modified` देगा — जिससे आपका IP कभी ब्लॉक नहीं होगा और डेटा भी बचेगा।
4. **Rotating User-Agents & Clean Headers:**
   * बिल्कुल सामान्य ब्राउज़र (Chrome/Edge on Windows/Android) जैसे हेडर्स भेजें।
   * Bot की तरह बर्ताव न करें।

---

## 4. क्या Database (DB) चाहिए?

### **हाँ, Database 100% अनिवार्य है!**
बिना डेटाबेस के काम नहीं चलेगा, क्योंकि:
1. **Duplicate Prevention:** पहले से भेजा गया नोटिफिकेशन बार-बार छात्रों को न जाए (Hash / Notification ID स्टोर करने के लिए)।
2. **Notification History:** छात्रों को पुरानी नोटिस, कट-ऑफ और पिछले साल के रिजल्ट देखने के लिए।
3. **Videos & Coaching Content:** यूट्यूब वीडियो लिंक्स, थंबनेल और कैटेगरी (Maths, Reasoning, Science, News) को स्टोर करने के लिए।
4. **Subscribers List:** WhatsApp / Telegram / Web Push के टोकन्स स्टोर करने के लिए।

### **सर्वश्रेष्ठ DB सुझाव: Supabase (PostgreSQL - Cloud)**
* **लागत:** ₹0 (100% Free Tier उपलब्ध है - 500MB स्टोरेज, 50,000 मंथली एक्टिव यूजर्स)।
* **फायदा:** इन-बिल्ट ऑथेंटिकेशन, इंस्टेंट REST APIs, और रियल-टाइम नोटिफिकेशन्स।

---

## 5. क्या AI (आर्टिफिशियल इंटेलिजेंस) चाहिए?

### **हाँ, AI बहुत मददगार और गेम-चेंजर साबित होगा:**
1. **सरकारी नोटिस PDF की समरी (Auto-Summarizer):**
   * सरकारी सर्कुलर 10 से 50 पेज के होते हैं जिसे छात्र नहीं समझ पाते।
   * AI (Gemini Flash API) 2 सेकंड में मुख्य बातें निकालेगा:
     * *फॉर्म कब से कब तक भरा जाएगा?*
     * *फीस कितनी है?*
     * *उम्र सीमा (Age Limit) और पात्रता क्या है?*
     * *परीक्षा की तारीख क्या है?*
2. **सोशल मीडिया व यूट्यूब पोस्ट जनरेटर:**
   * एक क्लिक में WhatsApp/Telegram पर भेजने लायक हिंदी मैसेज तैयार करना।
   * यूट्यूब वीडियो का सटीक Title, Description, और Tags खुद बनाना।
3. **Fake Notice Detection:**
   * सोशल मीडिया पर वायरल फर्जी सर्कुलर की भाषा और फॉन्ट विसंगतियों को पहचानना।

---

## 6. सागर कोचिंग सेंटर वीडियो इंटीग्रेशन (YouTube & Classes)

1. **Auto Video Sync:**
   * सागर कोचिंग सेंटर के YouTube चैनल की RSS Feed या YouTube Data API से कनेक्ट।
   * जैसे ही चैनल पर नया वीडियो अपलोड होगा, पोर्टल पर अपने आप अपडेट हो जाएगा।
2. **Exam-wise Video Categorization:**
   * NMMS स्पेशल क्लास वीडियो।
   * नवोदय/सैनिक स्कूल रीजनिंग व मैथ ट्रिक्स।
   * फॉर्म भरने का स्टेप-बाय-स्टेप लाइव वीडियो गाइड।
3. **Video + Notification Binding:**
   * उदाहरण: जब "NMMS Admit Card जारी" का नोटिस आए, तो उसके ठीक नीचे सागर सर का वीडियो ("एडमिट कार्ड कैसे डाउनलोड करें और एग्जाम में क्या लेकर जाएं") एम्बेड दिखेगा।

---

## 7. पूरा सिस्टम आर्किटेक्चर (System Architecture)

```
┌────────────────────────────────────────────────────────┐
│     1. Official Sources (gov.in / nic.in / NTA)        │
└──────────────────────────┬─────────────────────────────┘
                           │ (Periodic Polite Check / Scraper)
                           ▼
┌────────────────────────────────────────────────────────┐
│     2. Background Worker (Node.js / Python Scraper)    │
│        - ETag / Last-Modified Check (No IP Block)      │
│        - PDF / Circular Link Grabber                   │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│     3. AI Engine (Gemini Flash API)                    │
│        - Extract Dates, Eligibility, Direct Links       │
│        - Generate Hindi Summary & WhatsApp Alerts      │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│     4. Database & Backend (Supabase PostgreSQL)        │
│        - Store Cleaned Notifications                   │
│        - Store Sagar Coaching Center Videos            │
└──────────────┬──────────────────────────┬──────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ 5. Student Web/Mobile Portal │ │ 6. Alert Broadcasting Channels│
│    (Next.js / React on       │ │    - Telegram Channel / Bot  │
│     Vercel or Cloudflare)    │ │    - WhatsApp Channel / Group │
│    - Videos + Live Alerts    │ │    - Web Push Notifications   │
└──────────────────────────────┘ └──────────────────────────────┘
```

---

## 8. होस्टिंग (Hosting) कैसे और कहाँ होगी? (न्यूनतम/जीरो खर्च)

| Component | Technology | Best Hosting Option | Cost |
| :--- | :--- | :--- | :--- |
| **Frontend Portal** | Next.js / Vite React + TailwindCSS | **Vercel** या **Cloudflare Pages** | **₹0 (Free)** |
| **Database** | PostgreSQL | **Supabase** | **₹0 (Free)** |
| **Automated Scraper** | Python (Playwright / Scrapling) or Node.js | **GitHub Actions Cron** (हर 30 मिनट) या **Render Background Worker** | **₹0 (Free)** |
| **AI Integration** | Gemini 1.5 / 2.0 Flash API | Google AI Studio API Key | **Free Tier (Free requests)** |
| **Alerts Engine** | Telegram Bot API & Web Push | Serverless Functions | **₹0 (Free)** |

---

## 9. विकास के चरण (Implementation Steps)

1. **Step 1: Database Setup**
   * Supabase पर टेबल्स बनाना (`exams`, `notifications`, `videos`, `subscribers`).
2. **Step 2: Scraper Engine**
   * सबसे पहले NMMS (State SCERT), Navodaya और Sainik School के लिए 100% वर्किंग स्क्रैपर तैयार करना।
3. **Step 3: AI Parser Engine**
   * सरकारी नोटिस से मुख्य तारीखें और हिंदी सारांश निकालने के लिए Gemini प्रॉम्प्ट और पाइपलाइन बनाना।
4. **Step 4: Sagar Coaching Admin & Student Portal**
   * क्लीन और मोबाइल-फ्रेंडली वेब पोर्टल जहाँ छात्र नोटिस पढ़ सकें और वीडियो देख सकें।
   * एडमिन पैनल जहाँ से नए वीडियो और नोटिस 1-क्लिक में पोस्ट हों।
5. **Step 5: Alert Integration & Deployment**
   * Telegram बॉट और पुश नोटिफिकेशन्स सेटअप।
   * Vercel और GitHub Actions पर ऑटोमेशन लाइव होस्ट करना।
