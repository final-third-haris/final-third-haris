#!/usr/bin/env python3
"""
Final Third — Automated Daily YouTube Synchronization
Part of the production automation pipeline.

Workflow:
1. Queries Haris Nenmara's YouTube Channel (@FinalThird_HarisNenmara, UClD0Kli5qi5JE2tI1ReHLLQ)
   via YouTube Data API v3 (if YOUTUBE_API_KEY configured) or official YouTube RSS.
2. Identifies new video uploads.
3. Classifies sport (Football vs Cricket) via intelligent playlist & keyword analysis.
4. Attempts to retrieve the Malayalam caption track using YouTubeCaptionClient:
   - Official YouTube Data API OAuth captions.download if authorized.
   - Local transcript file fallback in transcripts/{video_id}.srt.
5. If transcript is present:
   - Cleans timestamps/subtitles.
   - Generates grounded Malayalam summary, English summary, takeaways, and verified tags.
   - Sets status to 'needs_review' (or 'published' if --auto-approve is passed).
6. If transcript is absent:
   - Sets status to 'awaiting_transcript'.
   - Generates strictly neutral metadata description (no invented tactical claims).
7. Creates the new dedicated SEO video page at /{sport}/{slug}/.
8. Updates category listing hubs (/football/ and /cricket/).
9. Updates sitemap.xml.
10. Idempotently updates index.html and assets/js/config.js (no duplicates).
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "scripts"))

from youtube_caption_client import YouTubeCaptionClient
import generate_video_pages

CHANNEL_ID = "UClD0Kli5qi5JE2tI1ReHLLQ"
RSS_FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
PIPELINE_PATH = os.path.join(base_dir, "data/content_pipeline.json")
INDEX_PATH = os.path.join(base_dir, "index.html")
CONFIG_JS_PATH = os.path.join(base_dir, "assets/js/config.js")

def slugify(text):
    text = text.lower()
    # Strip Malayalam and non-ascii for clean URL slugs
    clean = re.sub(r'[^\x00-\x7F]+', ' ', text)
    clean = re.sub(r'[^a-z0-9]+', '-', clean)
    clean = clean.strip('-')
    if not clean or len(clean) < 4:
        return "match-analysis-debrief"
    return clean[:60].rstrip('-')

def classify_sport(title, summary=""):
    # Strip channel boilerplate from summary so generic words don't contaminate
    cleaned_summary = re.sub(
        r"welcome to final third.*?subscribe and stay connected", 
        "", 
        summary or "", 
        flags=re.IGNORECASE | re.DOTALL
    )
    cleaned_summary = re.sub(
        r"final third.*?haris nenmara",
        "",
        cleaned_summary,
        flags=re.IGNORECASE | re.DOTALL
    )
    title_lower = title.lower()
    combined = (title + " " + cleaned_summary).lower()
    
    # 1. Football Keywords first (Barca, Real Madrid, Football, Ronaldo, Messi, Champions League, etc.)
    barca_kws = ["barcelona", "barca", "ബാഴ്സ", "flick", "yamal", "lamine", "camp nou", "pedri", "gavi", "clasico", "el clasico", "raphinha", "lewandowski"]
    real_madrid_kws = ["real madrid", "madrid", "റയൽ", "mbappe", "vinicius", "vini", "bellingham", "bernabeu", "ancelotti", "modric", "valverde", "leipzig"]
    kbfc_kws = ["kerala blasters", "blasters", "kbfc", "ബ്ലാസ്റ്റേഴ്സ്", "isl", "manjappada", "chhetri", "stahre", "sanan", "momo"]
    football_kws = ["football", "ഫുട്ബോൾ", "ronaldo", "റൊണാൾഡോ", "cristiano", "messi", "മെസി", "ballon d'or", "ballon d or", "champions league", "ucl", "la liga", "premier league", "serie a", "bundesliga", "psg", "roma", "galatasaray", "kane", "harry kane"]

    if any(k in title_lower for k in barca_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Barcelona"}
    if any(k in title_lower for k in real_madrid_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Real Madrid"}
    if any(k in title_lower for k in kbfc_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Kerala Blasters & Indian Football"}
    if any(k in title_lower for k in football_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "European & World Football"}

    # 2. Cricket Keywords
    cricket_kws = [
        "cricket", "ക്രിക്കറ്റ്", "sanju", "samson", "സഞ്ജു", "bumrah", "ബുംറ", 
        "bhuvneshwar", "bhuvi", "ഭുവി", "kohli", "rohit", "sharma", "abhishek", 
        "tilak varma", "varma", "suryavanshi", "dhoni", "ipl", "bcci", "ind vs", 
        "india vs", "new zealand", "kiwis", "srilanka", "england", "shami", "mohammed shami",
        "t20", "odi", "test match", "wicket", "chase"
    ]
    if any(k in combined for k in cricket_kws):
        return {
            "sport": "cricket",
            "sport_title": "Cricket Analysis",
            "playlist": "Indian Cricket Team"
        }
    
    # 3. Fallback check on combined
    if any(k in combined for k in barca_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Barcelona"}
    if any(k in combined for k in real_madrid_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Real Madrid"}
    if any(k in combined for k in kbfc_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Kerala Blasters & Indian Football"}
        
    return {
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "European & World Football"
    }

def fetch_channel_videos():
    """Fetch latest videos via YouTube Data API v3 (if key present) or official RSS feed"""
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    items = []
    
    if api_key:
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&maxResults=15&order=date&type=video&key={api_key}"
            req = urllib.request.Request(url, headers={"User-Agent": "FinalThird-Sync/1.0"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for it in data.get("items", []):
                    vid = it["id"]["videoId"]
                    snip = it["snippet"]
                    items.append({
                        "id": vid,
                        "title": snip.get("title", ""),
                        "published": snip.get("publishedAt", ""),
                        "summary": snip.get("description", "")
                    })
                if items:
                    print(f"✓ Retrieved {len(items)} videos via YouTube Data API v3.")
                    return items
        except Exception as e:
            print(f"[API Notice] YouTube API query failed ({e}), falling back to RSS feed.")

    # Fallback to RSS feed
    try:
        req = urllib.request.Request(RSS_FEED_URL, headers={"User-Agent": "Mozilla/5.0 (FinalThird-Sync/1.0)"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015",
                "media": "http://search.yahoo.com/mrss/"
            }
            
            for entry in root.findall("atom:entry", ns):
                vid_elem = entry.find("yt:videoId", ns)
                title_elem = entry.find("atom:title", ns)
                published_elem = entry.find("atom:published", ns)
                media_grp = entry.find("media:group", ns)
                desc_elem = media_grp.find("media:description", ns) if media_grp is not None else None
                
                if vid_elem is not None and title_elem is not None:
                    items.append({
                        "id": vid_elem.text.strip(),
                        "title": title_elem.text.strip(),
                        "published": published_elem.text.strip() if published_elem is not None else "",
                        "summary": desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                    })
            print(f"✓ Retrieved {len(items)} videos via YouTube RSS feed.")
    except Exception as e:
        print(f"[Error] Failed to fetch channel RSS feed: {e}")
        
    return items

def run_sync(dry_run=False, auto_approve=False):
    print("=" * 80)
    print("FINAL THIRD — DAILY YOUTUBE VIDEO & TRANSCRIPT SYNC")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    # 1. Load existing pipeline
    if not os.path.exists(PIPELINE_PATH):
        print(f"Error: Pipeline file {PIPELINE_PATH} not found.")
        return False
        
    with open(PIPELINE_PATH, "r", encoding="utf-8") as f:
        pipeline = json.load(f)
        
    print(f"Existing pipeline entries: {len(pipeline)}")
    
    # 2. Fetch channel uploads
    channel_videos = fetch_channel_videos()
    if not channel_videos:
        print("No videos retrieved. Exiting sync.")
        return True

    client = YouTubeCaptionClient(base_dir=base_dir)
    new_count = 0
    updated_count = 0

    for item in channel_videos:
        vid = item["id"]
        title = item["title"]
        summary = item["summary"]
        published = item["published"]
        
        # Skip YouTube Shorts
        if "#shorts" in title.lower() or "#shorts" in summary.lower():
            continue
            
        # Check if video already exists in pipeline
        if vid in pipeline:
            # Check if an existing awaiting video now has a transcript available
            existing = pipeline[vid]
            if not existing.get("transcript_available"):
                t_text, t_src = client.get_transcript(vid)
                if t_text:
                    print(f"⚡ [TRANSCRIPT FOUND] Previously awaiting video {vid} now has transcript ({t_src})!")
                    if not dry_run:
                        existing["transcript_available"] = True
                        existing["transcript_source"] = t_src
                        existing["status"] = "published" if auto_approve else "needs_review"
                        existing["human_approved"] = auto_approve
                        # Regenerate grounded content
                        grounded = client.process_video_content(existing)
                        existing["p1_ml"] = grounded["p1_ml"]
                        existing["p2_en"] = grounded["p2_en"]
                        existing["takeaways"] = grounded["takeaways"]
                        existing["tags"] = grounded["tags"]
                        updated_count += 1
            continue

        # NEW VIDEO DETECTED!
        new_count += 1
        sport_info = classify_sport(title, summary)
        sport = sport_info["sport"]
        sport_title = sport_info["sport_title"]
        playlist = sport_info["playlist"]
        slug = f"{slugify(title)}-{vid[:6].lower()}"
        
        print(f"\n★ NEW UPLOAD DETECTED: {vid}")
        print(f"  Title: {title}")
        print(f"  Sport: {sport.upper()} ({playlist})")
        print(f"  Slug: /{sport}/{slug}/")
        
        # Check transcript
        t_text, t_src = client.get_transcript(vid)
        has_t = bool(t_text)
        
        if has_t:
            print(f"  ✓ Transcript found via {t_src}!")
            status = "published" if auto_approve else "needs_review"
            human_appr = auto_approve
        else:
            print("  ⏳ No transcript found yet. Marking as awaiting_transcript.")
            status = "awaiting_transcript"
            human_appr = False
            
        video_record = {
            "id": vid,
            "title": title,
            "sport": sport,
            "sport_title": sport_title,
            "playlist": playlist,
            "slug": slug,
            "published_iso": published,
            "views": "1K+ views",
            "read_time": "3 min read",
            "seo_title": f"{title} | Final Third {sport_title}",
            "meta_desc": f"Analysis and match debrief by Haris Nenmara on '{title}'. Watch the full breakdown on Final Third."
        }
        
        grounded_data = client.process_video_content(video_record)
        video_record["p1_ml"] = grounded_data["p1_ml"]
        video_record["p2_en"] = grounded_data["p2_en"]
        video_record["takeaways"] = grounded_data["takeaways"]
        video_record["tags"] = grounded_data["tags"]
        video_record["status"] = status
        video_record["transcript_available"] = has_t
        video_record["transcript_source"] = t_src
        video_record["human_approved"] = human_appr
        video_record["notes"] = "Automatically indexed by daily sync."

        if not dry_run:
            pipeline[vid] = video_record

    print(f"\nSync summary: {new_count} new uploads, {updated_count} transcript updates.")

    if not dry_run and (new_count > 0 or updated_count > 0):
        # Save pipeline
        with open(PIPELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved updated pipeline to {PIPELINE_PATH}")
        
        # Rebuild all website pages, category hubs, and sitemap
        print("Rebuilding website pages, hubs, and sitemap...")
        generate_video_pages.generate_all()
        print("✓ All site pages, hubs, and sitemap updated.")
    elif dry_run:
        print("[DRY RUN] No files written.")
    else:
        print("✓ No changes required. Website is fully up-to-date.")

    return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    is_auto = "--auto-approve" in sys.argv
    run_sync(dry_run=is_dry, auto_approve=is_auto)
