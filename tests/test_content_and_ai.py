from content_extractor import extract_content_from_link
from ai_parser import analyze_notice

test_url = "https://www.livehindustan.com/career/isro-ursc-recruitment-2026-application-last-date-extended-driver-technician-posts-for-10th-iti-pass-201794708552750.html"

print("1. Extracting article content from LiveHindustan...")
text = extract_content_from_link(test_url)
print(f"Extracted Text Length: {len(text)} chars")
print(f"Sample Text: {text[:300]}...")

print("\n2. Sending Extracted Text to Groq AI (openai/gpt-oss-120b)...")
ai_res = analyze_notice("ISRO 10th-ITI Recruitment", text, "लाइव हिन्दुस्तान")
import json
print("\n3. AI Extracted Result:")
print(json.dumps(ai_res, indent=2, ensure_ascii=False))
