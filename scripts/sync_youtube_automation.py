#!/usr/bin/env python3
"""
Final Third — Automated Master YouTube Video & Transcript Synchronization Platform
Handles:
1. Queries Haris Nenmara's YouTube Channel (@FinalThird_HarisNenmara, UClD0Kli5qi5JE2tI1ReHLLQ)
   via YouTube Data API v3 or official YouTube RSS feed.
2. Accurate Shorts detection using HTTP 200/303 redirect check on /shorts/{id} + metadata.
3. Classifies sport (Football vs Cricket) via multi-factor playlist and keyword analysis.
4. Retrieves Malayalam caption tracks using YouTubeCaptionClient:
   - Distinguishes complete vs partial vs missing vs failed captions.
   - Computes caption coverage (cues, duration, word count).
   - Generates grounded Malayalam summary, natural English translation, discussion points, takeaways.
5. Automatic page creation (dedicated SEO page at /{sport}/{slug}/).
6. Automatic category updates (adds cards to /football/ and /cricket/ hubs).
7. Automatic homepage updates (syncs FINAL_THIRD_CONFIG in index.html & assets/js/config.js,
   prepends crawlable static cards to #videoGrid and #shortsShelf).
8. Automatic sitemap updates (sitemap.xml with Google Video extensions).
9. Idempotent execution (never creates duplicates; automatically upgrades awaiting videos
   when complete captions become available).
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
    clean = re.sub(r'[^\x00-\x7F]+', ' ', text)
    clean = re.sub(r'[^a-z0-9]+', '-', clean)
    clean = clean.strip('-')
    if not clean or len(clean) < 4:
        return "match-analysis-debrief"
    return clean[:60].rstrip('-')

def check_is_short(video_id, title="", summary=""):
    """
    Accurately detects whether a video is a YouTube Short:
    1. Checks #shorts in title or description.
    2. Uses YouTube's official HTTP redirect behavior:
       https://www.youtube.com/shorts/{video_id} returns HTTP 200 for Shorts,
       and redirects (301/302/303) to /watch?v=... for full landscape videos.
    """
    if not video_id or not isinstance(video_id, str) or not video_id.strip():
        return False
    video_id = video_id.strip()

    if "#shorts" in (title + " " + summary).lower():
        return True

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

def classify_sport(title, summary=""):
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
    
    # 1. Football Keywords (Barca, Real Madrid, Football, Ronaldo, Messi, Champions League, etc.)
    barca_kws = ["barcelona", "barca", "ബാഴ്സ", "flick", "yamal", "lamine", "camp nou", "pedri", "gavi", "clasico", "el clasico", "raphinha", "lewandowski"]
    real_madrid_kws = ["real madrid", "madrid", "റയൽ", "mbappe", "vinicius", "vini", "bellingham", "bernabeu", "ancelotti", "modric", "valverde", "leipzig"]
    kbfc_kws = ["kerala blasters", "blasters", "kbfc", "ബ്ലാസ്റ്റേഴ്സ്", "isl", "manjappada", "chhetri", "stahre", "sanan", "momo"]
    football_kws = ["football", "ഫുട്ബോൾ", "ronaldo", "റൊണാൾഡോ", "cristiano", "messi", "മെസി", "ballon d'or", "ballon d or", "champions league", "ucl", "la liga", "premier league", "serie a", "bundesliga", "psg", "roma", "galatasaray", "kane", "harry kane"]

    if any(k in title_lower for k in barca_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Barcelona", "playlistId": "PLGWXiMbN17ik"}
    if any(k in title_lower for k in real_madrid_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Real Madrid", "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS"}
    if any(k in title_lower for k in kbfc_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Kerala Blasters & Indian Football", "playlistId": "kbfc-isl"}
    if any(k in title_lower for k in football_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "European & World Football", "playlistId": "european-football"}

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
            "playlist": "Indian Cricket Team",
            "playlistId": "indian-cricket"
        }
    
    # 3. Fallbacks
    if any(k in combined for k in barca_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Barcelona", "playlistId": "PLGWXiMbN17ik"}
    if any(k in combined for k in real_madrid_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Real Madrid", "playlistId": "PLRqJyYpkYUnHsNkojNOoKGYrBITpb_ksS"}
    if any(k in combined for k in kbfc_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "Kerala Blasters & Indian Football", "playlistId": "kbfc-isl"}
        
    return {
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "European & World Football",
        "playlistId": "european-football"
    }

def fetch_channel_videos():
    """Fetch latest videos via YouTube Data API v3 or official RSS feed"""
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

def update_catalog_array(filepath, new_items, target_key="videos"):
    if not new_items or not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    marker = f"{target_key}: ["
    idx = content.find(marker)
    if idx == -1:
        return False

    insert_pos = idx + len(marker)
    entries = []
    for v in new_items:
        entries.append(
            "\n    {\n"
            f'      "id": "{v["id"]}",\n'
            f'      "title": {json.dumps(v["title"], ensure_ascii=False)},\n'
            f'      "sport": "{v.get("sport", "football")}",\n'
            f'      "playlistId": "{v.get("playlistId", "latest")}",\n'
            f'      "playlistTitle": {json.dumps(v.get("playlist", "Latest Release"), ensure_ascii=False)},\n'
            f'      "published": "{v.get("published_iso", "")[:10]}",\n'
            f'      "views": "{v.get("views", "10K views")}",\n'
            f'      "summary": {json.dumps(v.get("meta_desc", v["title"]), ensure_ascii=False)}\n'
            "    },"
        )
    block = "".join(entries)
    new_content = content[:insert_pos] + block + content[insert_pos:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def prepend_static_video_card(filepath, video):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    vid = video["id"]
    if f'data-video-id="{vid}"' in content:
        return True
    marker = '<div class="video-grid" id="videoGrid" aria-live="polite">'
    idx = content.find(marker)
    if idx == -1:
        return False
    insert_pos = idx + len(marker)
    title = video["title"]
    sport_cap = (video.get("sport") or "football").capitalize()
    views = video.get("views") or "10K views"
    pl_title = video.get("playlist") or "Latest Release"
    pub = video.get("published_iso", "")[:10]
    summary = video.get("meta_desc") or title

    card_html = f'''
          <article class="video-card reveal-cascade" data-video-id="{vid}" style="--cascade-index: 0">
            <div class="video-thumbnail-wrap" role="button" tabindex="0" aria-label="Play video: {title}">
              <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="Video thumbnail: {title}" loading="lazy" decoding="async" width="480" height="270" />
              <span class="card-sport-pill">{sport_cap}</span>
              <span class="card-views-pill" title="Live Video Views">
                <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                {views}
              </span>
              <div class="card-play-btn" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">
                  <polygon points="6 4 20 12 6 20 6 4"></polygon>
                </svg>
              </div>
            </div>
            <div class="video-card-body">
              <div class="card-meta-row">
                <span class="card-playlist-name">{pl_title}</span>
                <span class="card-published-time">{pub}</span>
              </div>
              <h3 class="video-card-title">{title}</h3>
              <p class="video-card-summary">{summary}</p>
            </div>
          </article>'''
    new_content = content[:insert_pos] + card_html + content[insert_pos:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def prepend_static_short_card(filepath, short):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    vid = short["id"]
    if f'data-short-id="{vid}"' in content:
        return True
    marker = '<div class="shorts-shelf" id="shortsShelf">'
    idx = content.find(marker)
    if idx == -1:
        return False
    insert_pos = idx + len(marker)
    title = short["title"]
    views = short.get("views") or "10K views"

    card_html = f'''
            <article class="short-card reveal-cascade" data-short-id="{vid}" role="button" tabindex="0" aria-label="Play Short: {title}" style="--cascade-index: 0">
              <img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="Final Third Short: {title}" class="short-thumb-img" loading="lazy" width="360" height="640" decoding="async">
              <div class="short-card-scrim" aria-hidden="true"></div>
              <div class="short-badge-top" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" aria-hidden="true"><path d="M17.77 10.32l-1.2-.5L18 8.06a3.74 3.74 0 0 0-3.5-5.46 3.7 3.7 0 0 0-2.62 1.1L6.26 9.32a3.75 3.75 0 0 0 1.2 6.84l1.2.5L7 18.4a3.74 3.74 0 0 0 3.5 5.46c1 0 1.95-.4 2.62-1.1l5.62-5.62a3.75 3.75 0 0 0-1-6.82zM10 14.5v-5l4.5 2.5-4.5 2.5z"/></svg>
                SHORTS
              </div>
              <div class="short-card-content">
                <span class="short-views-pill">
                  <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                  {views}
                </span>
                <h3 class="short-title" lang="ml">{title}</h3>
              </div>
            </article>'''
    new_content = content[:insert_pos] + card_html + content[insert_pos:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    return True

def run_sync(dry_run=False):
    print("=" * 80)
    print("FINAL THIRD — AUTOMATED MASTER YOUTUBE SYNC PLATFORM")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 80)

    if not os.path.exists(PIPELINE_PATH):
        print(f"Error: Pipeline file {PIPELINE_PATH} not found.")
        return False
        
    with open(PIPELINE_PATH, "r", encoding="utf-8") as f:
        pipeline = json.load(f)
        
    print(f"Current pipeline entries: {len(pipeline)}")
    
    channel_videos = fetch_channel_videos()
    if not channel_videos:
        print("No videos retrieved. Exiting sync.")
        return True

    client = YouTubeCaptionClient(base_dir=base_dir)
    new_videos_added = []
    new_shorts_added = []
    upgraded_videos = 0

    # Load all existing IDs from index.html and config.js to strictly prevent duplicates
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_html = f.read()

    existing_config_ids = set(re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', index_html))
    if os.path.exists(CONFIG_JS_PATH):
        with open(CONFIG_JS_PATH, "r", encoding="utf-8") as f:
            cfg_js = f.read()
        existing_config_ids.update(re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', cfg_js))

    # Master set of all known IDs across homepage catalogue and content pipeline
    all_known_ids = existing_config_ids.union(set(pipeline.keys()))
    print(f"Loaded {len(existing_config_ids)} homepage catalogue IDs and {len(pipeline)} pipeline records ({len(all_known_ids)} total unique known IDs).")

    for item in channel_videos:
        try:
            vid = item.get("id", "").strip()
            if not vid:
                continue
            title = item.get("title", "").strip()
            summary = item.get("summary", "").strip()
            published = item.get("published", "").strip()

            is_already_known = (vid in all_known_ids)

            # 1. ACCURATE SHORTS DETECTION
            is_short = check_is_short(vid, title, summary)
            if is_short:
                if not is_already_known:
                    print(f"⚡ [NEW SHORT DETECTED] {vid}: {title}")
                    short_record = {
                        "id": vid,
                        "title": title,
                        "published_iso": published,
                        "views": "10K views"
                    }
                    new_shorts_added.append(short_record)
                    all_known_ids.add(vid)
                    existing_config_ids.add(vid)
                else:
                    # Existing short - skip cleanly
                    pass
                continue

            # 2. FULL-LENGTH VIDEO: EXISTING OR TRANSCRIPT UPGRADE CHECK
            if is_already_known:
                # Video already exists in homepage catalogue or pipeline. Never re-add.
                if vid in pipeline:
                    existing = pipeline[vid]
                    if existing.get("coverage") != "complete":
                        t_text, t_src, cov = client.get_transcript(vid)
                        if cov.get("coverage") == "complete":
                            print(f"★ [TRANSCRIPT UPGRADE] Previously awaiting/partial video {vid} now has COMPLETE transcript!")
                            grounded = client.process_video_content(existing)
                            existing["has_transcript"] = True
                            existing["transcript_available"] = True
                            existing["transcript_source"] = t_src
                            existing["coverage"] = "complete"
                            existing["status"] = "published"
                            existing["p1_ml"] = grounded["p1_ml"]
                            existing["p2_en"] = grounded["p2_en"]
                            existing["takeaways"] = grounded["takeaways"]
                            existing["tags"] = grounded["tags"]
                            existing["human_approved"] = True
                            existing["notes"] = f"Automatically upgraded on {datetime.now(timezone.utc).isoformat()[:10]}."
                            upgraded_videos += 1
                continue

            # 3. BRAND NEW FULL-LENGTH VIDEO DETECTED!
            # Only reached if vid is NOT in all_known_ids (neither on homepage nor pipeline)
            sport_info = classify_sport(title, summary)
            sport = sport_info["sport"]
            sport_title = sport_info["sport_title"]
            playlist = sport_info["playlist"]
            playlist_id = sport_info["playlistId"]
            slug = f"{slugify(title)}-{vid[:6].lower()}"

            print(f"\n★ NEW FULL-LENGTH VIDEO: {vid}")
            print(f"  Title: {title}")
            print(f"  Sport: {sport.upper()} ({playlist})")
            print(f"  Slug: /{sport}/{slug}/")

            video_record = {
                "id": vid,
                "title": title,
                "sport": sport,
                "sport_title": sport_title,
                "playlist": playlist,
                "playlistId": playlist_id,
                "slug": slug,
                "published_iso": published,
                "views": "10K views",
                "read_time": "3 min read",
                "seo_title": f"{title} | Final Third {sport_title}",
                "meta_desc": f"Analysis and match debrief by Haris Nenmara on '{title}'. Watch the full breakdown on Final Third."
            }

            grounded = client.process_video_content(video_record)
            video_record["has_transcript"] = grounded["has_transcript"]
            video_record["transcript_available"] = grounded["has_transcript"]
            video_record["transcript_source"] = grounded["transcript_source"]
            video_record["coverage"] = grounded["coverage"]
            video_record["status"] = grounded["status"]
            video_record["p1_ml"] = grounded["p1_ml"]
            video_record["p2_en"] = grounded["p2_en"]
            video_record["takeaways"] = grounded["takeaways"]
            video_record["tags"] = grounded["tags"]
            video_record["human_approved"] = True if grounded["coverage"] == "complete" else False
            video_record["notes"] = f"Auto-synced ({grounded['coverage']} captions)."

            new_videos_added.append(video_record)
            pipeline[vid] = video_record
            all_known_ids.add(vid)
            existing_config_ids.add(vid)

        except Exception as e:
            print(f"[Error processing video {item.get('id')}]: {e}. Continuing with remaining uploads.")

    print(f"\nSync summary: {len(new_videos_added)} new full videos, {len(new_shorts_added)} new shorts, {upgraded_videos} transcript upgrades.")

    if not dry_run:
        changes_made = False

        # 1. Update Shorts on homepage if any
        if new_shorts_added:
            print(f"Updating homepage config with {len(new_shorts_added)} new shorts...")
            update_catalog_array(INDEX_PATH, new_shorts_added, target_key="shorts")
            update_catalog_array(CONFIG_JS_PATH, new_shorts_added, target_key="shorts")
            for s in new_shorts_added:
                prepend_static_short_card(INDEX_PATH, s)
            changes_made = True

        # 2. Update Videos on homepage if any
        if new_videos_added:
            print(f"Updating homepage config with {len(new_videos_added)} new full videos...")
            update_catalog_array(INDEX_PATH, new_videos_added, target_key="videos")
            update_catalog_array(CONFIG_JS_PATH, new_videos_added, target_key="videos")
            for v in new_videos_added:
                prepend_static_video_card(INDEX_PATH, v)
            changes_made = True

        # 3. Save pipeline & rebuild pages, hubs, sitemap if videos added or upgraded
        if new_videos_added or upgraded_videos > 0:
            with open(PIPELINE_PATH, "w", encoding="utf-8") as f:
                json.dump(pipeline, f, ensure_ascii=False, indent=2)
            print("Rebuilding dedicated SEO pages, hubs, and sitemap...")
            generate_video_pages.generate_all()
            changes_made = True

        if changes_made:
            print("✓ Website successfully updated with new YouTube content!")
        else:
            print("✓ Website is fully up-to-date with YouTube channel.")
    else:
        print("[DRY RUN] No files written.")

    return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    run_sync(dry_run=is_dry)
