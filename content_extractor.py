import io
import requests
import urllib3
import pymupdf
from bs4 import BeautifulSoup
from config import BROWSER_HEADERS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_content_from_link(url: str, timeout: int = 15) -> str:
    """
    Intelligently extracts readable text from either a PDF circular or an HTML article/page.
    Limits to ~2500 characters so AI receives concise, highly relevant information.
    """
    if not url or not url.startswith("http"):
        return ""
        
    try:
        resp = requests.get(
            url,
            headers=BROWSER_HEADERS,
            timeout=timeout,
            verify=False,
            allow_redirects=True
        )
        if resp.status_code != 200:
            return ""
            
        content_type = resp.headers.get("Content-Type", "").lower()
        
        # 1. If it's a PDF Document
        if "application/pdf" in content_type or url.lower().endswith(".pdf") or resp.content[:4] == b"%PDF":
            doc = pymupdf.open(stream=resp.content, filetype="pdf")
            extracted_text = []
            for page_num in range(min(len(doc), 3)): # read up to first 3 pages
                extracted_text.append(doc[page_num].get_text())
            full_text = "\n".join(extracted_text).strip()
            return full_text[:3000]
            
        # 2. If it's an HTML web page / article
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove noisy tags
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside"]):
            tag.decompose()
            
        # Prioritize main article or notice content
        main_container = soup.find(["article", "main"]) or soup.find(class_=lambda c: c and any(w in c.lower() for w in ["article", "content", "story", "detail", "notice"]))
        
        if main_container:
            text = main_container.get_text(separator=" ", strip=True)
        else:
            paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 20]
            text = " ".join(paragraphs) if paragraphs else soup.get_text(separator=" ", strip=True)
            
        # Clean excessive whitespace
        clean_text = " ".join(text.split())
        return clean_text[:3000]
        
    except Exception as e:
        print(f"Content extraction error on {url}: {e}")
        return ""
