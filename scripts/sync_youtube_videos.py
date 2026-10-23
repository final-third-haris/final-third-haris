#!/usr/bin/env python3
"""
Final Third — Automated YouTube Video Synchronizer
Fetches latest public videos from YouTube channel @FinalThird_HarisNenmara
using the official YouTube RSS feed (zero API keys required, zero rate limit).
Automatically routes full episodes to 'videos' and 9:16 vertical reels to 'shorts'
in both index.html and assets/js/config.js.
"""

import sys
import ssl
import json
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

CHANNEL_ID = "UClD0Kli5qi5JE2tI1ReHLLQ"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

CRICKET_KEYWORDS = [
    "cricket", "ipl", "bcci", "shami", "bumrah", "kohli", "rohit", "dhoni",
    "sanju", "samson", "t20", "odi", "test match", "pant", "hardik", "siraj",
    "ashwin", "kl rahul", "suryakumar", "ind vs", "india vs", "australia", "england"
]

def classify_sport(title, summary=""):
    text = (title + " " + summary).lower()
    for kw in CRICKET_KEYWORDS:
        if kw in text:
            return {
                "sport": "cricket",
                "playlistId": "cricket-insights",
                "playlistTitle": "Cricket Stories & Analysis"
            }
    
    # Default to football
    if any(k in text for k in ["kbfc", "blasters", "isl", "kerala", "indian football"]):
        return {
            "sport": "football",
            "playlistId": "kbfc-isl",
            "playlistTitle": "Kerala Blasters & Indian Football"
        }
    
    return {
        "sport": "football",
        "playlistId": "european-football",
        "playlistTitle": "European & World Football"
    }

def check_is_short(video_id):
    """
    Checks if a YouTube video ID is a Short or a regular video.
    YouTube returns HTTP 200 for /shorts/<id>, or redirects (HTTP 303) for regular landscape videos.
    """
    url = f"https://www.youtube.com/shorts/{video_id}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        resp = opener.open(req, timeout=10)
        return resp.getcode() == 200
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 303, 307):
            return False
        return False
    except Exception:
        return False

def format_published_time(iso_str):
    try:
        pub_dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - pub_dt
        days = diff.days
        hours = diff.seconds // 3600

        if days == 0:
            if hours <= 1:
                return "Just now"
            return f"{hours} hours ago"
        elif days == 1:
            return "Yesterday"
        elif days < 7:
            return f"{days} days ago"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    except Exception:
        return "Recent"

def fetch_latest_feed_videos():
    ctx = ssl._create_unverified_context()
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "FinalThirdSyncBot/1.0"})
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/"
    }

    videos = []
    for entry in root.findall("atom:entry", ns):
        vid_elem = entry.find("yt:videoId", ns)
        title_elem = entry.find("atom:title", ns)
        pub_elem = entry.find("atom:published", ns)
        desc_elem = entry.find("media:group/media:description", ns)

        if vid_elem is None or vid_elem.text is None:
            continue
        if title_elem is None or title_elem.text is None:
            continue

        vid = vid_elem.text.strip()
        title = title_elem.text.strip()
        published_iso = pub_elem.text.strip() if (pub_elem is not None and pub_elem.text) else ""
        desc = desc_elem.text.strip() if (desc_elem is not None and desc_elem.text) else title

        meta = classify_sport(title, desc)
        videos.append({
            "id": vid,
            "title": title,
            "sport": meta["sport"],
            "playlistId": meta["playlistId"],
            "playlistTitle": meta["playlistTitle"],
            "published": format_published_time(published_iso),
            "views": "New",
            "summary": title
        })

    return videos

def update_featured_id(filepath, video_id):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'featuredVideoId:\s*"[^"]*"', f'featuredVideoId: "{video_id}"', content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def update_file(filepath, new_items, target_key="videos"):
    if not new_items:
        return True

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find target array (videos: [ or shorts: [)
    marker = f"{target_key}: ["
    idx = content.find(marker)
    if idx == -1:
        print(f"Error: Could not find '{marker}' in {filepath}")
        return False

    insert_pos = idx + len(marker)

    formatted_entries = []
    for v in new_items:
        formatted_entries.append(
            "  {\n"
            f'    "id": "{v["id"]}",\n'
            f'    "title": {json.dumps(v["title"], ensure_ascii=False)},\n'
            f'    "sport": "{v["sport"]}",\n'
            f'    "playlistId": "{v["playlistId"]}",\n'
            f'    "playlistTitle": {json.dumps(v["playlistTitle"], ensure_ascii=False)},\n'
            f'    "published": "{v["published"]}",\n'
            f'    "views": "{v["views"]}",\n'
            f'    "summary": {json.dumps(v["summary"], ensure_ascii=False)}\n'
            "  }"
        )

    insertion_text = "\n" + ",\n".join(formatted_entries) + ","
    new_content = content[:insert_pos] + insertion_text + content[insert_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True

def main():
    print("=" * 60)
    print("Final Third — Synchronizing YouTube Channel Videos & Shorts")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    try:
        feed_videos = fetch_latest_feed_videos()
        print(f"Fetched {len(feed_videos)} recent uploads from YouTube RSS feed.")
    except Exception as e:
        print(f"Failed to fetch YouTube feed: {e}")
        sys.exit(1)

    # Read existing video IDs from index.html
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    existing_ids = set(re.findall(r'"id":\s*"([a-zA-Z0-9_-]{11})"', html))
    print(f"Currently tracking {len(existing_ids)} unique video/short IDs in repository.")

    # Find videos from the feed that are not yet in the catalogue
    new_items = [v for v in feed_videos if v["id"] not in existing_ids]

    if not new_items:
        print("✓ All latest YouTube videos and shorts are already up to date! No changes needed.")
        return

    print(f"★ Found {len(new_items)} NEW upload(s). Classifying into Full Episodes vs Shorts...")
    new_full_videos = []
    new_shorts = []

    for v in new_items:
        is_short = check_is_short(v["id"])
        if is_short:
            print(f"  ⚡ [SHORT] {v['id']} — {v['title']}")
            new_shorts.append(v)
        else:
            print(f"  🎬 [FULL EPISODE] {v['id']} — {v['title']}")
            new_full_videos.append(v)

    # Update index.html and assets/js/config.js
    ok1 = update_file("index.html", new_full_videos, "videos") and update_file("index.html", new_shorts, "shorts")
    ok2 = update_file("assets/js/config.js", new_full_videos, "videos") and update_file("assets/js/config.js", new_shorts, "shorts")

    if ok1 and ok2:
        if new_full_videos:
            newest_id = new_full_videos[0]["id"]
            update_featured_id("index.html", newest_id)
            update_featured_id("assets/js/config.js", newest_id)
            print(f"★ Automatically set Spotlight Analysis to latest release: [{newest_id}]")

        print(f"✓ Successfully routed {len(new_full_videos)} episode(s) and {len(new_shorts)} short(s) to index.html and config.js!")
        with open("NEW_VIDEOS_FOUND.txt", "w") as f:
            f.write(str(len(new_items)))
    else:
        print("Error updating files!")
        sys.exit(1)

if __name__ == "__main__":
    main()
