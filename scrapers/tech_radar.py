import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import email.utils
from bs4 import BeautifulSoup
from config import BROWSER_HEADERS

# Strict Freshness Window: Ignore any release older than 7 days
MAX_FRESHNESS_DAYS = 7

GITHUB_CORE_REPOS = [
    {"name": "Node.js", "repo": "nodejs/node", "official_download": "https://nodejs.org/en/download"},
    {"name": "VS Code", "repo": "microsoft/vscode", "official_download": "https://code.visualstudio.com/Download"},
    {"name": "Git for Windows", "repo": "git-for-windows/git", "official_download": "https://git-scm.com/download/win"},
    {"name": "Ollama (Local AI)", "repo": "ollama/ollama", "official_download": "https://ollama.com/download"},
    {"name": "Docker Desktop", "repo": "docker/docker-ce", "official_download": "https://www.docker.com/products/docker-desktop/"},
    {"name": "Go (Golang)", "repo": "golang/go", "official_download": "https://go.dev/dl/"}
]

def format_freshness_badge(dt_utc: datetime) -> tuple[bool, str, int]:
    """
    Calculates age and formats a clear status badge.
    Returns: (is_fresh_enough, badge_string, age_in_days)
    """
    now = datetime.now(timezone.utc)
    diff = now - dt_utc
    age_in_hours = int(diff.total_seconds() // 3600)
    age_in_days = diff.days

    if age_in_days > MAX_FRESHNESS_DAYS:
        return False, f"🔴 {age_in_days} days old (OUTDATED)", age_in_days

    if age_in_days == 0:
        if age_in_hours <= 1:
            badge = "🟢 JUST NOW (< 1 hour ago) - ⚡ DAY ZERO!"
        else:
            badge = f"🟢 TODAY ({age_in_hours} hours ago) - ⚡ DAY ZERO!"
    elif age_in_days == 1:
        badge = "🟡 YESTERDAY (1 day ago) - 🔥 FRESH"
    else:
        badge = f"🟡 {age_in_days} Days Ago ({dt_utc.strftime('%d %b %Y')})"

    return True, badge, age_in_days

def check_python_official():
    """
    Directly checks python.org for the newest Python 3 release and its official date.
    """
    items = []
    url = "https://www.python.org/downloads/"
    try:
        resp = requests.get(url, headers=BROWSER_HEADERS, timeout=6)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            # Look for latest release rows
            for row in soup.find_all("span", class_="release-number")[:2]:
                parent = row.parent
                date_span = parent.find("span", class_="release-date")
                version_str = row.text.strip() # e.g. "Python 3.15.2"
                date_str = date_span.text.strip() if date_span else ""
                
                # Parse date like "Oct. 25, 2026" or "Nov. 15, 2026"
                try:
                    clean_date = date_str.replace(".", "")
                    dt = datetime.strptime(clean_date, "%b %d, %Y").replace(tzinfo=timezone.utc)
                    is_fresh, badge, days = format_freshness_badge(dt)
                    if is_fresh:
                        items.append({
                            "tool_id": f"python_{version_str.replace(' ', '_').lower()}",
                            "tool_name": version_str,
                            "version_tag": version_str,
                            "title": f"{version_str} Released",
                            "link": "https://www.python.org/downloads/",
                            "release_notes_url": "https://www.python.org/downloads/",
                            "content_snippet": f"Official Python release {version_str} on {date_str}.",
                            "update_type": "Software Version Release",
                            "release_badge": badge,
                            "age_days": days
                        })
                except Exception:
                    pass
    except Exception as e:
        print(f"Error checking Python official: {e}")
    return items

def check_github_releases():
    """
    Checks GitHub for the latest releases and filters by published date.
    """
    items = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for tool in GITHUB_CORE_REPOS:
        repo = tool["repo"]
        name = tool["name"]
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        try:
            resp = requests.get(url, headers=headers, timeout=4)
            if resp.status_code == 200:
                data = resp.json()
                tag = data.get("tag_name", "")
                pub_date_str = data.get("published_at", "")
                
                if not pub_date_str:
                    continue
                    
                dt = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                is_fresh, badge, days = format_freshness_badge(dt)
                
                # Strict Filter: Ignore if older than 7 days
                if not is_fresh:
                    print(f"⏩ Skipping {name} {tag} - too old ({days} days old)")
                    continue
                
                body = data.get("body", "") or ""
                html_url = data.get("html_url", "")
                
                items.append({
                    "tool_id": f"gh_{repo.replace('/', '_')}",
                    "tool_name": name,
                    "version_tag": tag,
                    "title": f"{name} {tag} Released",
                    "link": tool["official_download"],
                    "release_notes_url": html_url,
                    "content_snippet": body[:1500],
                    "update_type": "Software Version Release",
                    "release_badge": badge,
                    "age_days": days
                })
        except Exception as e:
            print(f"Error checking GitHub release for {name}: {e}")
            
    return items

def check_trending_tech_news():
    """
    Fetches trending tech, AI launches, and critical developer security bugs.
    Ensures articles are strictly from the current year and within the last 7 days.
    """
    items = []
    keywords = [
        "ai", "llm", "deepseek", "claude", "chatgpt", "openai", "model",
        "python", "windows 11", "vscode", "release", "released", "launch",
        "open source", "free tool", "editor", "terminal", "database", "ollama",
        "vulnerability", "cve-", "exploit", "zero-day", "0-day", "critical bug",
        "rce", "remote code execution", "security patch", "php bug"
    ]
    
    rss_urls = [
        "https://hnrss.org/newest?q=released+OR+launch",
        "https://hnrss.org/frontpage?points=100",
        "https://hnrss.org/newest?q=vulnerability+OR+exploit+OR+CVE"
    ]
    
    for rss_url in rss_urls:
        try:
            resp = requests.get(rss_url, headers=BROWSER_HEADERS, timeout=6)
            if resp.status_code != 200:
                continue
                
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:10]:
                title = item.find("title").text or ""
                link = item.find("link").text or ""
                pub_date = item.find("pubDate")
                pub_str = pub_date.text if pub_date is not None else ""
                
                # Check pub date freshness
                if pub_str:
                    try:
                        dt = email.utils.parsedate_to_datetime(pub_str)
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        is_fresh, badge, days = format_freshness_badge(dt)
                        if not is_fresh:
                            continue
                    except Exception:
                        badge = "🟡 RECENT"
                        days = 0
                else:
                    badge = "🟡 RECENT"
                    days = 0
                
                title_lower = title.lower()
                if any(kw in title_lower for kw in keywords):
                    items.append({
                        "tool_id": f"news_{abs(hash(title))}",
                        "tool_name": title,
                        "version_tag": "Trending",
                        "title": title,
                        "link": link,
                        "release_notes_url": link,
                        "content_snippet": "",
                        "update_type": "Critical Bug / Security Patch" if any(w in title_lower for w in ["vulnerability", "cve", "exploit", "bug", "rce"]) else "Trending AI / Tech News",
                        "release_badge": badge,
                        "age_days": days
                    })
        except Exception as e:
            print(f"Error fetching tech RSS from {rss_url}: {e}")
            
    return items

def scrape_all_tech():
    """
    Master function combining Python official, GitHub releases, and trending AI / security bugs.
    """
    python_items = check_python_official()
    releases = check_github_releases()
    news = check_trending_tech_news()
    return python_items + releases + news
