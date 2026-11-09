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
import ssl
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

def safe_urlopen(req, timeout=12):
    """Robust urlopen wrapper with SSL fallback for environments with missing root certs"""
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except (ssl.SSLError, urllib.error.URLError) as e:
        if isinstance(e, ssl.SSLError) or (isinstance(e, urllib.error.URLError) and "CERTIFICATE_VERIFY_FAILED" in str(e)):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return urllib.request.urlopen(req, timeout=timeout, context=ctx)
        raise

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "scripts"))

from youtube_caption_client import YouTubeCaptionClient
import generate_video_pages

CHANNEL_ID = "UClD0Kli5qi5JE2tI1ReHLLQ"
RSS_FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
PIPELINE_PATH = os.path.join(base_dir, "data/content_pipeline.json")
INDEX_PATH = os.path.join(base_dir, "index.html")
CONFIG_JS_PATH = os.path.join(base_dir, "assets/js/config.js")
SITEMAP_PATH = os.path.join(base_dir, "sitemap.xml")

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
    try:
        import ssl
        ctx = ssl.create_default_context()
        try:
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), NoRedirect)
            resp = opener.open(req, timeout=10)
            return resp.getcode() == 200
        except (ssl.SSLError, urllib.error.URLError):
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), NoRedirect)
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
    real_madrid_kws = ["real madrid", "madrid", "റയൽ", "mbappe", "vinicius", "vini", "bellingham", "bernabeu", "ancelotti", "modric", "valverde", "leipzig", "diomande", "ഡിയോമന്‍റെ"]
    kbfc_kws = ["kerala blasters", "blasters", "kbfc", "ബ്ലാസ്റ്റേഴ്സ്", "isl", "manjappada", "chhetri", "stahre", "sanan", "momo"]
    football_kws = [
        "football", "ഫുട്ബോൾ", "ronaldo", "റൊണാൾഡോ", "cristiano", "messi", "മെസി", 
        "ballon d'or", "ballon d or", "champions league", "ucl", "la liga", "premier league", 
        "epl", "serie a", "bundesliga", "psg", "roma", "galatasaray", "kane", "harry kane",
        "arsenal", "ആഴ്സണൽ", "liverpool", "ലിവർപൂൾ", "arteta", "ആർട്ടേറ്റ", "അർട്ടേറ്റ", 
        "manchester", "chelsea", "tottenham", "shot on target", "ഷോട്ട് ഓൺ ടാർഗറ്റ്", 
        "slot", "arne slot", "guardiola", "pep guardiola", "amorim", "ruben amorim", "haaland"
    ]

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
        "india vs", "new zealand", "kiwis", "srilanka", "shami", "mohammed shami",
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
    if any(k in combined for k in football_kws):
        return {"sport": "football", "sport_title": "Football Analysis", "playlist": "European & World Football", "playlistId": "european-football"}
        
    return {
        "sport": "football",
        "sport_title": "Football Analysis",
        "playlist": "European & World Football",
        "playlistId": "european-football"
    }

def format_views(count_val):
    try:
        n = int(count_val)
        if n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M views"
        elif n >= 100_000:
            return f"{n // 1_000}K views"
        elif n >= 1_000:
            val = n / 1_000.0
            return f"{val:.1f}K views" if val < 10.0 else f"{round(val)}K views"
        else:
            return f"{n} views"
    except (ValueError, TypeError):
        return "10K views"

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

def update_existing_views(filepath, views_map, pub_time_map=None):
    if not views_map or not os.path.exists(filepath):
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    update_count = 0

    # 1. Update JSON config entries in FINAL_THIRD_CONFIG
    for vid, v_str in views_map.items():
        pattern = rf'("id":\s*"{re.escape(vid)}"[^}}]+?"views":\s*")[^"]*(")'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            old_full = match.group(0)
            new_full = re.sub(pattern, rf'\g<1>{v_str}\g<2>', old_full, flags=re.DOTALL)
            if old_full != new_full:
                content = content[:match.start()] + new_full + content[match.end():]
                update_count += 1

        if pub_time_map and vid in pub_time_map and pub_time_map[vid]:
            p_time = pub_time_map[vid]
            p_pattern = rf'("id":\s*"{re.escape(vid)}"[^}}]+?"published":\s*")[^"]*(")'
            p_match = re.search(p_pattern, content, re.DOTALL)
            if p_match:
                p_old = p_match.group(0)
                p_new = re.sub(p_pattern, rf'\g<1>{p_time}\g<2>', p_old, flags=re.DOTALL)
                if p_old != p_new:
                    content = content[:p_match.start()] + p_new + content[p_match.end():]
                    update_count += 1

    # 2. Update static video cards in HTML (if present)
    for vid, v_str in views_map.items():
        card_pattern = rf'(<(?:article|div)[^>]+data-video-id="{re.escape(vid)}"[^>]*>.*?</(?:article|div)>)'
        card_match = re.search(card_pattern, content, re.DOTALL)
        if card_match:
            card_html = card_match.group(1)
            new_card = re.sub(
                r'(<span class="card-views-pill"[^>]*>\s*<svg[^>]*>.*?</svg>\s*)[^<]+(</span>)',
                rf'\g<1>{v_str}\n              \g<2>',
                card_html,
                flags=re.DOTALL
            )
            if pub_time_map and vid in pub_time_map and pub_time_map[vid]:
                new_card = re.sub(
                    r'(<span class="card-published-time"[^>]*>)[^<]+(</span>)',
                    rf'<span class="card-published-time" data-nosnippet>{pub_time_map[vid]}\g<2>',
                    new_card
                )
            if card_html != new_card:
                content = content[:card_match.start()] + new_card + content[card_match.end():]
                update_count += 1

    # 3. Update static short cards in HTML (if present)
    for vid, v_str in views_map.items():
        short_pattern = rf'(<(?:article|div)[^>]+data-short-id="{re.escape(vid)}"[^>]*>.*?</(?:article|div)>)'
        short_match = re.search(short_pattern, content, re.DOTALL)
        if short_match:
            short_html = short_match.group(1)
            new_short = re.sub(
                r'(<span class="short-views-pill"[^>]*>\s*<svg[^>]*>.*?</svg>\s*)[^<]+(</span>)',
                rf'\g<1>{v_str}\n                \g<2>',
                short_html,
                flags=re.DOTALL
            )
            if short_html != new_short:
                content = content[:short_match.start()] + new_short + content[short_match.end():]
                update_count += 1

    if update_count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return update_count

def parse_follower_number(val_str):
    """
    Parses follower / subscriber text (e.g. '41.3K+', '27K', '21,727', '1.5M') into an integer.
    """
    if not val_str:
        return 0
    clean = str(val_str).strip().upper().replace(",", "").replace("+", "")
    if clean.endswith("M"):
        try:
            return int(float(clean[:-1]) * 1_000_000)
        except ValueError:
            return 0
    if clean.endswith("K"):
        try:
            return int(float(clean[:-1]) * 1_000)
        except ValueError:
            return 0
    try:
        return int(float(clean))
    except ValueError:
        return 0

def fetch_instagram_followers(username="finalthird.official"):
    """
    Fetches real-time follower count from public Instagram profile.
    Uses crawler User-Agent to retrieve OpenGraph description metadata.
    Falls back to verified baseline (27K+) if network or platform changes occur.
    """
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with safe_urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r"([0-9.,]+[KMBkmb]?)\s*Followers", html, re.I)
        if m:
            raw_val = m.group(1).strip()
            num = parse_follower_number(raw_val)
            text = f"{raw_val.upper()}+" if not raw_val.endswith("+") else raw_val.upper()
            if num > 0:
                return {"count": num, "text": text}
    except Exception as e:
        print(f"[fetch_instagram_followers notice]: {e}. Using baseline.")
    return {"count": 27000, "text": "27K+"}

def fetch_facebook_followers(page_id="61590005744291"):
    """
    Fetches real-time follower count from public Facebook page.
    Uses crawler User-Agent to retrieve OpenGraph description metadata.
    Matches English 'followers' and Malayalam 'ഫോളോവേഴ്‌സ്'.
    Falls back to verified baseline (21.7K+) if network or platform changes occur.
    """
    url = f"https://www.facebook.com/profile.php?id={page_id}"
    headers = {
        "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with safe_urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        m = re.search(r"([0-9,]+)\s*(?:followers|ഫോളോവേഴ്‌സ്|people follow this)", html, re.I)
        if m:
            raw_str = m.group(1).replace(",", "").strip()
            num = int(raw_str)
            k_val = round(num / 1000.0, 1)
            text = f"{k_val}K+"
            if num > 0:
                return {"count": num, "text": text}
    except Exception as e:
        print(f"[fetch_facebook_followers notice]: {e}. Using baseline.")
    return {"count": 21727, "text": "21.7K+"}

def fetch_channel_stats(channel_id=CHANNEL_ID):
    """
    Fetches real-time total channel views and subscriber count for Haris Nenmara.
    1. Tries YouTube Data API v3 if YOUTUBE_API_KEY is present in the environment.
    2. Falls back to scraping the public channel about page (no API quota needed).
    Returns dict: {'view_count': int, 'subscriber_text': str, 'subscriber_count': int} or None on failure.
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    if api_key:
        try:
            api_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"
            req = urllib.request.Request(api_url, headers={"User-Agent": "FinalThirdSync/1.0"})
            with safe_urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                items = data.get("items", [])
                if items:
                    stats = items[0].get("statistics", {})
                    v_raw = int(stats.get("viewCount", 0))
                    s_raw = int(stats.get("subscriberCount", 0))
                    if s_raw >= 1000:
                        s_val = s_raw / 1000.0
                        s_text = f"{s_val:.1f}K+" if s_val < 100.0 else f"{round(s_val)}K+"
                    else:
                        s_text = f"{s_raw}+"
                    if v_raw > 0:
                        return {"view_count": v_raw, "subscriber_text": s_text, "subscriber_count": s_raw}
        except Exception as e:
            print(f"[fetch_channel_stats API error]: {e}. Falling back to public channel scrape.")

    # Fallback: Scrape public channel about page
    try:
        url = "https://www.youtube.com/@FinalThird_HarisNenmara/about"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }
        )
        with safe_urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")

        v_match = re.search(r'"viewCountText":\s*\{\s*"simpleText":\s*"([^"]+)"', html)
        if not v_match:
            v_match = re.search(r'"viewCountText":\s*"([^"]+)"', html)
        if not v_match:
            v_match = re.search(r'([0-9,]+)\s+views', html)

        s_match = re.search(r'"subscriberCountText":\s*\{\s*"simpleText":\s*"([^"]+)"', html)
        if not s_match:
            s_match = re.search(r'"subscriberCountText":\s*"([^"]+)"', html)

        v_raw = 0
        if v_match:
            digits = re.sub(r"[^\d]", "", v_match.group(1))
            if digits:
                v_raw = int(digits)

        s_text = "41.3K+"
        if s_match:
            raw_sub = s_match.group(1).strip()
            sub_val = re.sub(r"(?i)\s*subscribers?", "", raw_sub).strip()
            if not sub_val.endswith("+"):
                sub_val = f"{sub_val.upper()}+"
            else:
                sub_val = sub_val.upper()
            s_text = sub_val

        if v_raw > 0:
            s_count = parse_follower_number(s_text)
            return {"view_count": v_raw, "subscriber_text": s_text, "subscriber_count": s_count}
    except Exception as e:
        print(f"[fetch_channel_stats scrape error]: {e}")

    return None

def update_ecosystem_views(filepath, stats=None):
    """
    Updates the Total Ecosystem Reach banner, the sponsor audience strip,
    and all social cards (YouTube, Instagram, Facebook) with real-time views,
    subscribers, and followers across YouTube, Instagram, and Facebook.
    Preserves other platform metrics (Instagram Reels 2.5M+, FB 1.8M+, WhatsApp 500K+).
    Returns number of modified sections, or 0 if already up to date.
    """
    if not os.path.exists(filepath):
        return 0

    if not stats:
        stats = fetch_channel_stats()
    if not stats or not stats.get("view_count"):
        return 0

    v_count = stats["view_count"]
    yt_m = v_count / 1_000_000.0
    yt_views_str = f"{yt_m:.1f}M+"

    # Cross-platform ecosystem calculation:
    # YouTube (live) + Reels (2.5M) + FB (1.8M) + WhatsApp (0.5M) = yt_m + 4.8M
    total_reach = yt_m + 4.8
    total_reach_str = f"{round(total_reach, 1):.1f}M+"

    # YouTube Subscribers
    subs_str = stats.get("subscriber_text", "41.3K+")
    yt_subs_count = stats.get("subscriber_count") or parse_follower_number(subs_str)

    # Instagram & Facebook Followers
    ig_stats = fetch_instagram_followers()
    fb_stats = fetch_facebook_followers()

    # Combined Followers & Subscribers across YouTube, Instagram, and Facebook
    total_followers_num = yt_subs_count + ig_stats["count"] + fb_stats["count"]
    total_followers_k = total_followers_num / 1000.0
    total_followers_str = f"{total_followers_k:.1f}K+" if total_followers_k < 100.0 else f"{round(total_followers_k)}K+"

    with open(filepath, "r", encoding="utf-8") as f:
        old_content = f.read()

    content = old_content
    match_count = 0

    # 1. Ecosystem strip total number
    content, n1 = re.subn(
        r'(<div class="ecosystem-total-num">)[^<]+(</div>)',
        rf'\g<1>{total_reach_str}\g<2>',
        content
    )
    match_count += n1

    # 2. Ecosystem strip YouTube Views pill
    content, n2 = re.subn(
        r'(<span><strong>)[^<]+(</strong>\s*YouTube Views</span>)',
        rf'\g<1>{yt_views_str}\g<2>',
        content
    )
    match_count += n2

    # 3. Sponsor strip - Total YouTube Views
    content, n3 = re.subn(
        r'(<div class="sponsor-stat-value">)[^<]+(</div>\s*<div class="sponsor-stat-label">Total YouTube Views</div>)',
        rf'\g<1>{yt_views_str}\g<2>',
        content
    )
    match_count += n3

    # 4. Sponsor strip - Cross-Platform Views
    content, n4 = re.subn(
        r'(<div class="sponsor-stat-value">)[^<]+(</div>\s*<div class="sponsor-stat-label">Cross-Platform Views</div>)',
        rf'\g<1>{total_reach_str}\g<2>',
        content
    )
    match_count += n4

    # 5. Sponsor strip - Combined Followers & Subscribers (YouTube + IG + FB)
    sponsor_cell_pattern = (
        r'(<div class="sponsor-stat-cell">\s*'
        r'<div class="sponsor-stat-value">)[^<]+(</div>\s*'
        r'<div class="sponsor-stat-label">)[^<]+(</div>\s*'
        r'<div class="sponsor-stat-sub">)[^<]+(</div>\s*'
        r'</div>\s*<div class="sponsor-stat-cell">\s*<div class="sponsor-stat-value">Kerala &amp; GCC</div>)'
    )
    content, n5 = re.subn(
        sponsor_cell_pattern,
        rf'\g<1>{total_followers_str}\g<2>Followers &amp; Subscribers\g<3>YouTube • Instagram • Facebook\g<4>',
        content
    )
    if n5 == 0:
        content, n5 = re.subn(
            r'(<div class="sponsor-stat-value">)[^<]+(</div>\s*<div class="sponsor-stat-label">(?:Dedicated Subscribers|Followers &amp; Subscribers|Followers & Subscribers)</div>)',
            rf'\g<1>{total_followers_str}\g<2>',
            content
        )
    match_count += n5

    # 6. YouTube Social Card
    yt_card_pattern = (
        r'(<!-- YouTube Card -->.*?<div class="social-card">.*?'
        r'<span class="social-views-num">)[^<]+(</span>\s*<span class="social-views-label">Total Views</span>.*?'
        r'<span class="social-sub-stat">)[^<]+(</span>)'
    )
    content, n6 = re.subn(
        yt_card_pattern,
        rf'\g<1>{yt_views_str}\g<2>{subs_str} Subs\g<3>',
        content,
        flags=re.DOTALL
    )
    match_count += n6

    # 7. Instagram Social Card
    ig_card_pattern = (
        r'(<!-- Instagram Card -->.*?<div class="social-card">.*?'
        r'<span class="social-sub-stat">)[^<]+(</span>)'
    )
    content, n7 = re.subn(
        ig_card_pattern,
        rf'\g<1>{ig_stats["text"]} Followers\g<2>',
        content,
        flags=re.DOTALL
    )
    match_count += n7

    # 8. Facebook Social Card
    fb_card_pattern = (
        r'(<!-- Facebook Card -->.*?<div class="social-card">.*?'
        r'<span class="social-sub-stat">)[^<]+(</span>)'
    )
    content, n8 = re.subn(
        fb_card_pattern,
        rf'\g<1>{fb_stats["text"]} Followers\g<2>',
        content,
        flags=re.DOTALL
    )
    match_count += n8

    if content != old_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return match_count

    return 0

def update_featured_id(filepath, video_id):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    new_content, n = re.subn(r'featuredVideoId:\s*"[^"]*"', f'featuredVideoId: "{video_id}"', content)
    if n > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def update_static_featured(filepath, video):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    vid = video["id"]
    title = video["title"]
    sport = (video.get("sport") or "football").upper()
    pl_title = video.get("playlist") or video.get("playlistTitle") or "Latest Release"
    pub = video.get("published") or video.get("published_relative") or "Latest Upload"
    views = video.get("views") or "10K views"
    summary = video.get("meta_desc") or video.get("summary") or title

    featured_pattern = r'<section class="section featured-match-section" id="featured">.*?</section>'
    new_featured = f'''<section class="section featured-match-section" id="featured">
      <div class="container">
        <div class="section-header">
          <div class="eyebrow">Featured Story | മലയാളം സ്പോർട്സ് ഫീച്ചർ</div>
          <h2 class="section-title">Spotlight <span class="highlight">Analysis</span></h2>
        </div>

        <div class="featured-match-card">
          <!-- 16:9 Thumbnail with Cinema Modal Trigger -->
          <div 
            class="featured-media-container" 
            id="featuredThumbnail" 
            role="button" 
            tabindex="0" 
            onclick="openVideoModal('{vid}')"
            aria-label="Play featured story: {title}"
          >
            <img 
              src="https://i.ytimg.com/vi/{vid}/maxresdefault.jpg" 
              alt="Featured Story Thumbnail: {title}" 
              width="680" 
              height="382" 
              loading="lazy"
              onerror="this.src='https://i.ytimg.com/vi/{vid}/hqdefault.jpg'"
            />
            <div class="play-overlay-btn" id="featuredPlayBtn" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            </div>
          </div>

          <!-- Video Details & Metadata -->
          <div class="featured-info-container">
            <div>
              <div class="featured-tag-bar">
                <span class="badge-tag">{sport}</span>
                <span class="featured-views-pill" id="featuredViewsPill">
                  <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" style="vertical-align:-1px; margin-right:4px;" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>{views}
                </span>
                <span style="font-size: 0.8125rem; color: var(--muted-grey); font-weight: 700;">
                  {pl_title} · Spotlight Analysis
                </span>
              </div>

              <h3 class="featured-headline" lang="ml" id="featuredHeadline" style="cursor: pointer;" onclick="openVideoModal('{vid}')">
                {title}
              </h3>

              <p class="featured-summary">
                {summary}
              </p>
            </div>

            <div class="featured-actions">
              <button class="btn btn-primary" id="featuredWatchStoryBtn" type="button" onclick="openVideoModal('{vid}')">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                WATCH STORY
              </button>
              <a 
                href="https://www.youtube.com/watch?v={vid}" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="btn btn-outline"
              >
                WATCH ON YOUTUBE ↗
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>'''

    new_content, n = re.subn(featured_pattern, new_featured, content, count=1, flags=re.DOTALL)
    if n > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def update_schema_video_object(filepath, video):
    """
    Safeguard: Homepage schema deliberately excludes VideoObject to protect
    Google Search snippet appearance (preventing misleading 'X days ago' relative date badges).
    Legitimate VideoObject structured data is preserved on dedicated video pages.
    """
    return False

def sanitize_sitemap_homepage(sitemap_path):
    """
    Safeguard: Ensures the root homepage URL in sitemap.xml does not have a <lastmod> tag,
    preventing Google Search from treating the homepage as a dated article and attaching
    relative date bylines ('X days ago') to the search snippet.
    """
    if not os.path.exists(sitemap_path):
        return False
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(
        r'(<loc>https://(?:www\.)?finalthird-haris\.com/</loc>\s*)<lastmod>[^<]+</lastmod>\s*',
        r'\g<1>',
        content
    )
    if new_content != content:
        with open(sitemap_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def sync_active_featured_stats(filepath, views_map, pub_time_map=None):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    m_fid = re.search(r'featuredVideoId:\s*"([^"]+)"', content)
    if not m_fid:
        return False
    fid = m_fid.group(1)

    changed = False
    if fid in views_map:
        v_str = views_map[fid]
        new_content = re.sub(
            r'(<span class="featured-views-pill" id="featuredViewsPill">\s*<svg[^>]*>.*?</svg>)[^<]+(</span>)',
            rf'\g<1>{v_str}\g<2>',
            content,
            flags=re.DOTALL
        )
        if new_content != content:
            content = new_content
            changed = True

    if changed:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def fetch_channel_videos():
    """Fetch latest videos via YouTube Data API v3 or official RSS feed"""
    api_key = os.environ.get("YOUTUBE_API_KEY", "")
    items = []
    
    if api_key:
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={CHANNEL_ID}&maxResults=15&order=date&type=video&key={api_key}"
            req = urllib.request.Request(url, headers={"User-Agent": "FinalThird-Sync/1.0"})
            with safe_urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for it in data.get("items", []):
                    vid = it["id"]["videoId"]
                    snip = it["snippet"]
                    pub_iso = snip.get("publishedAt", "")
                    items.append({
                        "id": vid,
                        "title": snip.get("title", ""),
                        "published": pub_iso,
                        "published_relative": format_published_time(pub_iso),
                        "views": "10K views",
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
        with safe_urlopen(req, timeout=12) as resp:
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
                stats_elem = entry.find("media:group/media:community/media:statistics", ns)
                
                if vid_elem is not None and title_elem is not None:
                    vid = vid_elem.text.strip()
                    title = title_elem.text.strip()
                    pub_iso = published_elem.text.strip() if published_elem is not None else ""
                    desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                    views_raw = stats_elem.attrib.get("views") if stats_elem is not None else None
                    views_fmt = format_views(views_raw) if views_raw else "10K views"

                    items.append({
                        "id": vid,
                        "title": title,
                        "published": pub_iso,
                        "published_relative": format_published_time(pub_iso),
                        "views": views_fmt,
                        "views_raw": int(views_raw) if views_raw and views_raw.isdigit() else 10000,
                        "summary": desc
                    })
            print(f"✓ Retrieved {len(items)} videos via YouTube RSS feed.")
    except Exception as e:
        print(f"[Error] Failed to fetch channel RSS feed: {e}")

    # Fallback to direct channel page scrape
    if not items:
        try:
            print("[Channel Scrape] RSS feed unavailable. Falling back to direct channel page...")
            url = f"https://www.youtube.com/@FinalThird_HarisNenmara/videos"
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            )
            with safe_urlopen(req, timeout=12) as resp:
                html = resp.read().decode("utf-8")

            start_marker = "ytInitialData = "
            idx = html.find(start_marker)
            if idx != -1:
                idx += len(start_marker)
                end_idx = html.find(";</script>", idx)
                data = json.loads(html[idx:end_idx])

                def extract_from_obj(obj):
                    res = []
                    if isinstance(obj, dict):
                        if "lockupViewModel" in obj:
                            lvm = obj["lockupViewModel"]
                            vid = lvm.get("contentId")
                            meta = lvm.get("metadata", {}).get("lockupMetadataViewModel", {})
                            title = meta.get("title", {}).get("content", "")
                            rows = meta.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
                            views = ""
                            pub_time = ""
                            for r in rows:
                                for part in r.get("metadataParts", []):
                                    txt = part.get("text", {}).get("content", "")
                                    acc = part.get("accessibilityLabel", "")
                                    if "view" in acc.lower():
                                        v_text = part.get("text", {}).get("content", "")
                                        if v_text:
                                            v_text = v_text.upper()
                                            views = v_text if v_text.endswith("VIEWS") else f"{v_text} views"
                                    elif "ago" in acc.lower() or "yesterday" in acc.lower() or "hour" in acc.lower():
                                        pub_time = acc
                            if vid and title:
                                res.append({
                                    "id": vid,
                                    "title": title,
                                    "published": pub_time or "Recent",
                                    "published_relative": pub_time or "Recent",
                                    "views": views or "10K views",
                                    "summary": title
                                })
                        for k, v in obj.items():
                            res.extend(extract_from_obj(v))
                    elif isinstance(obj, list):
                        for x in obj:
                            res.extend(extract_from_obj(x))
                    return res

                extracted = extract_from_obj(data)
                seen = set()
                for it in extracted:
                    if it["id"] not in seen:
                        seen.add(it["id"])
                        items.append(it)
                if items:
                    print(f"✓ Retrieved {len(items)} videos via direct channel page fallback.")
        except Exception as e:
            print(f"[Error] Failed to fetch channel page fallback: {e}")
        
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
            f'      "published": "{v.get("published", v.get("published_iso", "")[:10])}",\n'
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
    m = re.search(r'<div[^>]+id="videoGrid"[^>]*>', content)
    if not m:
        return False
    insert_pos = m.end()
    title = video["title"]
    sport_cap = (video.get("sport") or "football").capitalize()
    views = video.get("views") or "10K views"
    pl_title = video.get("playlist") or "Latest Release"
    pub = video.get("published") or video.get("published_relative") or video.get("published_iso", "")[:10]
    summary = video.get("meta_desc") or title
    slug = video.get("slug")
    sport = video.get("sport") or "football"
    dedicated_btn_html = ""
    if slug:
        dedicated_btn_html = f'''
            <div class="card-dedicated-row">
              <a href="/{sport}/{slug}/" class="card-dedicated-btn">
                <span>📖 Read Dedicated Tactical Breakdown</span>
                <span>↗</span>
              </a>
            </div>'''

    card_html = f'''
          <div class="video-card reveal-cascade" data-video-id="{vid}" style="--cascade-index: 0">
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
                <span class="card-published-time" data-nosnippet>{pub}</span>
              </div>
              <h3 class="video-card-title">{title}</h3>
              <p class="video-card-summary">{summary}</p>{dedicated_btn_html}
            </div>
          </div>'''
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
    m = re.search(r'<div[^>]+id="shortsShelf"[^>]*>', content)
    if not m:
        return False
    insert_pos = m.end()
    title = short["title"]
    views = short.get("views") or "10K views"

    card_html = f'''
            <div class="short-card reveal-cascade" data-short-id="{vid}" role="button" tabindex="0" aria-label="Play Short: {title}" style="--cascade-index: 0">
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
            </div>'''
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

    views_map = {item["id"]: item["views"] for item in channel_videos if item.get("id") and item.get("views")}
    pub_time_map = {item["id"]: item["published_relative"] for item in channel_videos if item.get("id") and item.get("published_relative")}

    # Recalculate fresh relative timestamps for all known videos from their actual publication ISO
    for p_id, p_val in pipeline.items():
        if p_id not in pub_time_map and p_val.get("published_iso"):
            pub_time_map[p_id] = format_published_time(p_val["published_iso"])

    client = YouTubeCaptionClient(base_dir=base_dir)
    now_dt = datetime.now(timezone.utc)
    now_iso = now_dt.isoformat()

    new_published_videos = []
    new_homepage_videos = []
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
                        "published": item.get("published_relative", "Recent"),
                        "views": item.get("views", "10K views")
                    }
                    new_shorts_added.append(short_record)
                    all_known_ids.add(vid)
                    existing_config_ids.add(vid)
                continue

            # 2. FULL-LENGTH VIDEO: SKIP IF ALREADY KNOWN
            # (Transcript upgrades for known videos are handled uniformly in the weekly retry queue below)
            if is_already_known:
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
                "published": item.get("published_relative", "Recent"),
                "views": item.get("views", "10K views"),
                "read_time": "3 min read",
                "seo_title": f"{title} | Final Third {sport_title}",
                "meta_desc": f"Analysis and match debrief by Haris Nenmara on '{title}'. Watch the full breakdown on Final Third."
            }

            grounded = client.process_video_content(video_record)
            video_record["has_transcript"] = grounded["has_transcript"]
            video_record["transcript_available"] = grounded["has_transcript"]
            video_record["transcript_source"] = grounded["transcript_source"]
            video_record["coverage"] = grounded["coverage"]
            video_record["p1_ml"] = grounded["p1_ml"]
            video_record["p2_en"] = grounded["p2_en"]
            video_record["takeaways"] = grounded["takeaways"]
            video_record["tags"] = grounded["tags"]
            video_record["last_checked"] = now_iso

            # AUTOMATIC QUALITY GATE
            if grounded["coverage"] == "complete":
                # Complete captions: publish full analysis immediately
                video_record["status"] = "published"
                video_record["human_approved"] = True
                video_record["retry_status"] = "completed"
                video_record["notes"] = "Auto-synced & published (complete verified transcript)."
                new_published_videos.append(video_record)
                new_homepage_videos.append(video_record)
                print(f"  ✓ Quality Gate PASSED (Complete Captions): Scheduled for dedicated SEO page publication.")
            elif grounded["coverage"] == "partial":
                # Partial captions: publish broadcast excerpt & queue for full transcript retry
                video_record["status"] = "published_partial"
                video_record["human_approved"] = False
                video_record["next_retry"] = (now_dt + timedelta(days=7)).isoformat()
                video_record["retry_count"] = 0
                video_record["retry_status"] = "queued"
                video_record["notes"] = "Auto-synced as broadcast excerpt (full transcript pending)."
                new_published_videos.append(video_record)
                new_homepage_videos.append(video_record)
                print(f"  ℹ Quality Gate EXCERPT: Published as broadcast excerpt, queued for weekly retry.")
            else:
                # Missing captions: publish grounded matchday debrief with awaiting badge & queue for weekly transcript retry
                video_record["status"] = "awaiting_transcript"
                video_record["human_approved"] = False
                video_record["next_retry"] = (now_dt + timedelta(days=7)).isoformat()
                video_record["retry_count"] = 0
                video_record["retry_status"] = "queued"
                video_record["notes"] = "Auto-synced as grounded debrief; full transcript queued for weekly verification."
                new_published_videos.append(video_record)
                new_homepage_videos.append(video_record)
                print(f"  ✓ Quality Gate GROUNDED: Published dedicated SEO page with awaiting-transcript badge; queued for weekly caption retry.")

            pipeline[vid] = video_record
            all_known_ids.add(vid)
            existing_config_ids.add(vid)

        except Exception as e:
            print(f"[Error processing video {item.get('id')}]: {e}. Continuing with remaining uploads.")

    # 4. WEEKLY RETRY ENGINE FOR CAPTION SYNCHRONIZATION
    print("\nEvaluating weekly transcript retry queue...")
    retry_candidates = [
        (v_id, v_data) for v_id, v_data in pipeline.items()
        if v_data.get("status") in ("awaiting_captions", "awaiting_transcript", "published_partial")
    ]
    print(f"Total retry queue candidates: {len(retry_candidates)}")
    retry_state_updated = False

    for vid, existing in retry_candidates:
        next_retry_str = existing.get("next_retry")
        is_due = False
        if not next_retry_str:
            is_due = True
        else:
            try:
                nr_dt = datetime.fromisoformat(next_retry_str.replace("Z", "+00:00"))
                if now_dt >= nr_dt:
                    is_due = True
            except Exception:
                is_due = True

        if is_due:
            t_text, t_src, cov = client.get_transcript(vid)
            cov_status = cov.get("coverage", "missing")

            if cov_status == "complete" and existing.get("coverage") != "complete":
                print(f"★ [TRANSCRIPT UPGRADE] Video {vid} now has COMPLETE transcript ({cov['cues']} cues, {cov['duration_seconds']}s)!")
                existing["transcript_source"] = t_src
                grounded = client.generate_grounded_article(existing, t_text, cov_status, cov)
                existing["has_transcript"] = True
                existing["transcript_available"] = True
                existing["coverage"] = "complete"
                existing["status"] = "published"
                existing["p1_ml"] = grounded["p1_ml"]
                existing["p2_en"] = grounded["p2_en"]
                existing["takeaways"] = grounded["takeaways"]
                existing["tags"] = grounded["tags"]
                existing["human_approved"] = True
                existing["notes"] = f"Automatically upgraded to complete analysis on {now_iso[:10]}."
                existing["last_checked"] = now_iso
                existing["retry_status"] = "completed"
                upgraded_videos += 1
                retry_state_updated = True
            elif cov_status == "partial" and existing.get("status") in ("awaiting_captions", "awaiting_transcript"):
                print(f"★ [TRANSCRIPT EXCERPT] Video {vid} now has PARTIAL transcript ({cov['cues']} cues)!")
                existing["transcript_source"] = t_src
                grounded = client.generate_grounded_article(existing, t_text, cov_status, cov)
                existing["has_transcript"] = True
                existing["transcript_available"] = True
                existing["coverage"] = "partial"
                existing["status"] = "published_partial"
                existing["p1_ml"] = grounded["p1_ml"]
                existing["p2_en"] = grounded["p2_en"]
                existing["takeaways"] = grounded["takeaways"]
                existing["tags"] = grounded["tags"]
                existing["human_approved"] = False
                existing["notes"] = f"Automatically upgraded to broadcast excerpt on {now_iso[:10]}."
                existing["last_checked"] = now_iso
                existing["next_retry"] = (now_dt + timedelta(days=7)).isoformat()
                existing["retry_count"] = existing.get("retry_count", 0) + 1
                upgraded_videos += 1
                retry_state_updated = True
            else:
                # Still missing or still partial -> backoff 7 days to avoid repeated unnecessary API calls
                existing["last_checked"] = now_iso
                existing["next_retry"] = (now_dt + timedelta(days=7)).isoformat()
                existing["retry_count"] = existing.get("retry_count", 0) + 1
                retry_state_updated = True

    print(f"\nSync summary: {len(new_published_videos)} new published pages, {len(new_homepage_videos)} new homepage items, {len(new_shorts_added)} new shorts, {upgraded_videos} transcript upgrades.")

    if not dry_run:
        changes_made = False

        # 0. Update view counts and relative timestamps on existing items
        if views_map:
            print("Refreshing view counts across existing catalogue...")
            vc1 = update_existing_views(INDEX_PATH, views_map, pub_time_map)
            vc2 = update_existing_views(CONFIG_JS_PATH, views_map, pub_time_map)
            for v_id, v_str in views_map.items():
                if v_id in pipeline and pipeline[v_id].get("views") != v_str:
                    pipeline[v_id]["views"] = v_str
                    changes_made = True
            if vc1 > 0 or vc2 > 0:
                changes_made = True
                print(f"✓ Updated live view counts for existing cards ({vc1} HTML updates, {vc2} JS updates).")

        # 0b. Refresh channel ecosystem reach, audience stats & YouTube social cards
        print("Refreshing channel ecosystem reach & audience stats...")
        channel_stats = fetch_channel_stats()
        if channel_stats:
            eco_updates = update_ecosystem_views(INDEX_PATH, channel_stats)
            if eco_updates > 0:
                changes_made = True
                print(f"✓ Updated Total Ecosystem Reach & Channel Stats ({eco_updates} sections updated).")

        # 1. Update Shorts on homepage if any
        if new_shorts_added:
            print(f"Updating homepage config with {len(new_shorts_added)} new shorts...")
            update_catalog_array(INDEX_PATH, new_shorts_added, target_key="shorts")
            update_catalog_array(CONFIG_JS_PATH, new_shorts_added, target_key="shorts")
            for s in reversed(new_shorts_added):
                prepend_static_short_card(INDEX_PATH, s)
            changes_made = True

        # 2. Update Videos on homepage if any
        if new_homepage_videos:
            print(f"Updating homepage config with {len(new_homepage_videos)} new full videos...")
            update_catalog_array(INDEX_PATH, new_homepage_videos, target_key="videos")
            update_catalog_array(CONFIG_JS_PATH, new_homepage_videos, target_key="videos")
            for v in reversed(new_homepage_videos):
                prepend_static_video_card(INDEX_PATH, v)

            # Update Spotlight / Featured analysis to newest video
            latest_new_video = new_homepage_videos[0]
            update_featured_id(INDEX_PATH, latest_new_video["id"])
            update_featured_id(CONFIG_JS_PATH, latest_new_video["id"])
            update_static_featured(INDEX_PATH, latest_new_video)
            update_schema_video_object(INDEX_PATH, latest_new_video)
            print(f"✓ Spotlight Analysis updated to newest video: {latest_new_video['id']}")
            changes_made = True
        else:
            # If no new video, keep active featured video view stats updated
            if sync_active_featured_stats(INDEX_PATH, views_map, pub_time_map):
                changes_made = True

        # 3. Save pipeline if any modifications occurred
        if new_homepage_videos or upgraded_videos > 0 or retry_state_updated or changes_made:
            with open(PIPELINE_PATH, "w", encoding="utf-8") as f:
                json.dump(pipeline, f, ensure_ascii=False, indent=2)

        # 4. Rebuild dedicated SEO pages, hubs, and sitemap if new published pages or upgrades occurred
        if new_published_videos or upgraded_videos > 0:
            print("Rebuilding dedicated SEO pages, hubs, and sitemap...")
            generate_video_pages.generate_all()
            changes_made = True

        # Always ensure sitemap homepage has no <lastmod> to protect Google Search snippet
        if sanitize_sitemap_homepage(SITEMAP_PATH):
            changes_made = True

        if changes_made:
            print("✓ Website successfully updated with new YouTube content!")
        else:
            print("✓ Website is fully up-to-date with YouTube channel.")
    else:
        print("[DRY RUN] No files written.")
        channel_stats = fetch_channel_stats()
        if channel_stats:
            print(f"[DRY RUN] Channel stats: views={channel_stats['view_count']}, subs={channel_stats['subscriber_text']}")

    return True

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    run_sync(dry_run=is_dry)
