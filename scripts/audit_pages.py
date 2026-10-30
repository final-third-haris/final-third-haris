#!/usr/bin/env python3
import os
import sys
import json
import re
import urllib.request
import urllib.error

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

with open(os.path.join(base_dir, "index.html"), encoding="utf-8") as f:
    index_html = f.read()

m_vid = re.search(r'videos:\s*\[(.*?)\]\s*,\s*shorts:', index_html, re.DOTALL)
m_short = re.search(r'shorts:\s*\[(.*?)\]\s*\n\};', index_html, re.DOTALL)

config_videos = {}
def parse_entries(block):
    items = re.findall(r'\{\s*"id":\s*"([^"]+)",\s*"title":\s*"([^"]+)".*?"summary":\s*"([^"]*)"', block, re.DOTALL)
    for vid, title, summary in items:
        config_videos[vid] = {"title": title, "summary": summary}

if m_vid:
    parse_entries(m_vid.group(1))
if m_short:
    parse_entries(m_short.group(1))

sys.path.append(os.path.join(base_dir, "scripts"))
from generate_video_pages import VIDEOS

print(f"Total videos parsed in FINAL_THIRD_CONFIG: {len(config_videos)}")
print(f"Total pages created: {len(VIDEOS)}")

results = []

for i, v in enumerate(VIDEOS, 1):
    vid = v["id"]
    slug = v["slug"]
    sport = v["sport"]
    page_title = v["title"].strip()
    
    in_config = vid in config_videos
    config_entry = config_videos.get(vid, None)
    config_title = config_entry["title"].strip() if config_entry else "NOT IN CONFIG"
    
    # Call oEmbed
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    oembed_title = ""
    oembed_status = ""
    try:
        req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            oembed_title = data.get("title", "").strip()
            oembed_status = "200 OK"
    except urllib.error.HTTPError as e:
        oembed_status = f"HTTP {e.code}"
    except Exception as e:
        oembed_status = f"ERROR: {e}"
        
    # Check title match
    norm_p = re.sub(r'\s+', ' ', page_title).strip()
    norm_oe = re.sub(r'\s+', ' ', oembed_title).strip()
    
    if norm_p == norm_oe:
        match_str = "Yes"
    elif norm_p in norm_oe or norm_oe in norm_p:
        match_str = "Partial"
    else:
        match_str = "No"
        
    results.append({
        "num": i,
        "page": f"/{sport}/{slug}/",
        "id": vid,
        "in_config": "Yes" if in_config else "No",
        "oembed_status": oembed_status,
        "page_title": norm_p,
        "oembed_title": norm_oe,
        "config_title": config_title,
        "match": match_str,
        # Content breakdown for factual check:
        "p1_ml": v["p1_ml"],
        "p2_en": v["p2_en"],
        "takeaways": v["takeaways"],
        "tags": v["tags"]
    })

# Save JSON results for analysis
with open(os.path.join(base_dir, "scripts/audit_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nAudit completed and saved to scripts/audit_results.json")
