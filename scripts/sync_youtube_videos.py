#!/usr/bin/env python3
"""
Final Third — Automated YouTube Video & Realtime Views Synchronizer
Fetches latest public videos from YouTube channel @FinalThird_HarisNenmara
using the official YouTube RSS feed (zero API keys required, zero rate limit).
Automatically routes full episodes to 'videos' and 9:16 vertical reels to 'shorts'
and keeps live view counts synchronized in both index.html and assets/js/config.js.
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

def classify_sport(title, summary=""):
    # Strip channel boilerplate from summary so generic words don't contaminate
    cleaned_summary = re.sub(
        r"welcome to final third.*?subscribe and stay connected", 
        "", 
        summary or "", 
        flags=re.IGNORECASE | re.DOTALL
    )
    title_lower = title.lower()
    combined_text = (title + " " + cleaned_summary).lower()

    # 1. Football Keywords (Prioritize specific football clubs, competitions & players)
    barca_kws = [
        "barcelona", "barca", "ബാഴ്സ", "clasico", "el clasico", "lamine", "yamal", 
        "raphinha", "flick", "hansi flick", "lewandowski", "camp nou", "pedri", "gavi"
    ]
    if any(k in title_lower for k in barca_kws):
        return {
            "sport": "football",
            "playlistId": "PLGWXiMbN17ik",
            "playlistTitle": "Barcelona"
        }

    real_madrid_kws = [
        "real madrid", "madrid", "റയൽ", "റയലിന്", "റയലേ", "mbappe", "bellingham", 
        "vinicius", "vini", "ancelotti", "bernabeu", "modric", "valverde", "leipzig"
    ]
    if any(k in title_lower for k in real_madrid_kws):
        return {
            "sport": "football",
            "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS",
            "playlistTitle": "Real Madrid"
        }

    kbfc_kws = [
        "kbfc", "blasters", "isl", "ബ്ലാസ്റ്റേഴ്സ്", "manjappada", "indian football", 
        "chhetri", "stahre", "kerala blasters"
    ]
    if any(k in title_lower for k in kbfc_kws):
        return {
            "sport": "football",
            "playlistId": "kbfc-isl",
            "playlistTitle": "Kerala Blasters & Indian Football"
        }

    general_football_kws = [
        "ucl", "champions league", "premier league", "la liga", "laliga", "serie a", 
        "bundesliga", "arsenal", "chelsea", "liverpool", "manchester", "man city", 
        "man utd", "bayern", "psg", "inter milan", "ac milan", "juventus", "atletico", 
        "football", "ഫുട്ബോൾ", "messi", "മെസി", "ronaldo", "റൊണാൾഡോ", "mourinho", 
        "മോറീന്യോ", "guardiola", "ballon d'or", "fifa", "world cup"
    ]
    if any(k in title_lower for k in general_football_kws):
        return {
            "sport": "football",
            "playlistId": "european-football",
            "playlistTitle": "European & World Football"
        }

    # 2. Cricket Keywords (Check title and cleaned summary)
    cricket_kws = [
        "cricket", "ക്രിക്കറ്റ്", "ipl", "ഐപിഎൽ", "bcci", "shami", "bumrah", "kohli", 
        "rohit", "dhoni", "sanju", "samson", "സഞ്ജു", "t20", "odi", "test match", 
        "pant", "hardik", "siraj", "സിറാജ്", "ashwin", "kl rahul", "suryakumar", "sky", 
        "സ്കൈ", "ind vs", "india vs", "australia", "england", "srilanka", "lanka", 
        "ലങ്ക", "pakistan", "babar", "gill", "jaiswal", "ജയ്സ്വാൾ", "century", 
        "സെഞ്ചുറി", "wicket", "flintoff", "gambhir", "dravid", "tilak", "naman dhir", "namandhir"
    ]
    if any(k in title_lower for k in cricket_kws) or any(k in combined_text for k in cricket_kws):
        return {
            "sport": "cricket",
            "playlistId": "cricket-insights",
            "playlistTitle": "Cricket Stories & Analysis"
        }

    # Fallback to football
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

def format_views(count_val):
    try:
        n = int(count_val)
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M views"
        elif n >= 10_000:
            return f"{n // 1_000}K views"
        elif n >= 1_000:
            return f"{n / 1_000:.1f}K views"
        else:
            return f"{n} views"
    except (ValueError, TypeError):
        return "10K views"

def fetch_latest_feed_videos():
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "FinalThirdSyncBot/1.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
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

            # Extract real-time view count directly from media:community/media:statistics
            stats_elem = entry.find("media:group/media:community/media:statistics", ns)
            views_raw = stats_elem.attrib.get("views") if stats_elem is not None else None
            views_formatted = format_views(views_raw) if views_raw else "10K views"

            meta = classify_sport(title, desc)
            videos.append({
                "id": vid,
                "title": title,
                "sport": meta["sport"],
                "playlistId": meta["playlistId"],
                "playlistTitle": meta["playlistTitle"],
                "published": format_published_time(published_iso),
                "views": views_formatted,
                "summary": title
            })

        if videos:
            return videos
    except Exception as e:
        print(f"Notice: RSS feed retrieval returned ({e}). Switching to direct channel parser fallback...")

    # Robust Fallback: Scrape public channel videos
    channel_url = "https://www.youtube.com/@FinalThird_HarisNenmara"
    req = urllib.request.Request(
        channel_url, 
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="ignore")

    videos = []
    seen = set()
    for m in re.finditer(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', html):
        vid = m.group(1)
        if vid in seen:
            continue
        seen.add(vid)
        snippet = html[m.start():m.start()+4000]
        t_match = re.search(r'\"lockupMetadataViewModel\":\{\"title\":\{\"content\":\"([^\"]+)\"', snippet)
        if t_match:
            title = t_match.group(1)
            # Decode unicode escapes like \u200d if present
            try:
                title = json.loads(f'"{title}"')
            except Exception:
                pass
            v_match = re.search(r'\"metadataParts\":\[\{\"text\":\{\"content\":\"([^\"]+)\"', snippet)
            views = v_match.group(1) + " views" if v_match else "10K views"
            p_match = re.search(r'\{\"text\":\{\"content\":\"([^\"]+ ago)\"\}', snippet)
            published = p_match.group(1) if p_match else "Recent"

            meta = classify_sport(title)
            videos.append({
                "id": vid,
                "title": title,
                "sport": meta["sport"],
                "playlistId": meta["playlistId"],
                "playlistTitle": meta["playlistTitle"],
                "published": published,
                "views": views,
                "summary": title
            })

    return videos

def update_featured_id(filepath, video_id):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'featuredVideoId:\s*"[^"]*"', f'featuredVideoId: "{video_id}"', content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def update_existing_views(filepath, views_map):
    if not views_map:
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    update_count = 0
    for vid, v_str in views_map.items():
        pattern = rf'("id":\s*"{re.escape(vid)}"[^}}]+?"views":\s*")[^"]*(")'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            old_full = match.group(0)
            new_full = re.sub(pattern, rf'\g<1>{v_str}\g<2>', old_full, flags=re.DOTALL)
            if old_full != new_full:
                content = content[:match.start()] + new_full + content[match.end():]
                update_count += 1

    if update_count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return update_count

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
    print("Final Third — Synchronizing YouTube Channel Videos & Realtime Views")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    try:
        feed_videos = fetch_latest_feed_videos()
        print(f"Fetched {len(feed_videos)} recent uploads with live views from YouTube RSS feed.")
    except Exception as e:
        print(f"Failed to fetch YouTube feed: {e}")
        sys.exit(1)

    # 1. Update live view counts for all videos found in the feed
    views_map = {v["id"]: v["views"] for v in feed_videos if v.get("views")}
    updated1 = update_existing_views("index.html", views_map)
    updated2 = update_existing_views("assets/js/config.js", views_map)
    if updated1 or updated2:
        print(f"★ Updated live view statistics for {max(updated1, updated2)} video(s) in repository.")

    # 2. Check for brand new video uploads
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    existing_ids = set(re.findall(r'"id":\s*"([a-zA-Z0-9_-]{11})"', html))
    print(f"Currently tracking {len(existing_ids)} unique video/short IDs in repository.")

    new_items = [v for v in feed_videos if v["id"] not in existing_ids]

    if not new_items:
        if updated1 or updated2:
            print("✓ Live view counts updated for existing videos!")
            with open("NEW_VIDEOS_FOUND.txt", "w") as f:
                f.write(str(max(updated1, updated2)))
        else:
            print("✓ All latest YouTube videos, shorts, and view counts are already up to date!")
        return

    print(f"★ Found {len(new_items)} NEW upload(s). Classifying into Full Episodes vs Shorts...")
    new_full_videos = []
    new_shorts = []

    for v in new_items:
        is_short = check_is_short(v["id"])
        if is_short:
            print(f"  ⚡ [SHORT] {v['id']} ({v['views']}) — {v['title']}")
            new_shorts.append(v)
        else:
            print(f"  🎬 [FULL EPISODE] {v['id']} ({v['views']}) — {v['title']}")
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
            f.write(str(len(new_items) + max(updated1, updated2)))
    else:
        print("Error updating files!")
        sys.exit(1)

if __name__ == "__main__":
    main()
