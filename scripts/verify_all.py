#!/usr/bin/env python3
"""
Comprehensive verification test suite for Final Third
"""
import os
import sys
import json
import re
import xml.etree.ElementTree as ET

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
errors = []

# 1. Test ads.txt
ads_path = os.path.join(base_dir, "ads.txt")
if not os.path.exists(ads_path):
    errors.append("ads.txt missing")
else:
    with open(ads_path) as f:
        content = f.read().strip()
    if "google.com, pub-5399554232098923, DIRECT, f08c47fec0942fa0" not in content:
        errors.append(f"ads.txt content unexpected: {content}")
    else:
        print("✓ ads.txt verified")

# 2. Test robots.txt
robots_path = os.path.join(base_dir, "robots.txt")
with open(robots_path) as f:
    robots_content = f.read()
if "https://www.finalthird-haris.com/sitemap.xml" not in robots_content:
    errors.append("robots.txt does not reference https://www.finalthird-haris.com/sitemap.xml")
else:
    print("✓ robots.txt verified")

# 3. Test sitemap.xml
sitemap_path = os.path.join(base_dir, "sitemap.xml")
try:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "video": "http://www.google.com/schemas/sitemap-video/1.1"
    }
    urls = root.findall("sm:url", ns)
    print(f"✓ sitemap.xml parsed successfully with {len(urls)} URLs")
    if len(urls) != 24:
        errors.append(f"Expected 24 URLs in sitemap, found {len(urls)}")
    
    video_count = 0
    for u in urls:
        loc = u.find("sm:loc", ns).text
        vid = u.find("video:video", ns)
        if vid is not None:
            video_count += 1
            t_loc = vid.find("video:thumbnail_loc", ns).text
            title = vid.find("video:title", ns).text
            desc = vid.find("video:description", ns).text
            p_loc = vid.find("video:player_loc", ns).text
            pub_date = vid.find("video:publication_date", ns).text
            if not t_loc or not title or not desc or not p_loc or not pub_date:
                errors.append(f"Incomplete video sitemap metadata for {loc}")
    print(f"✓ Found {video_count} video entries in sitemap.xml")
    if video_count != 20:
        errors.append(f"Expected 20 video entries, found {video_count}")
except Exception as e:
    errors.append(f"sitemap.xml error: {e}")

# 4. Check index.html 314 videos intact
index_path = os.path.join(base_dir, "index.html")
with open(index_path) as f:
    index_html = f.read()

m_vid = re.search(r"videos:\s*\[(.*?)\]\s*,\s*shorts:", index_html, re.DOTALL)
m_short = re.search(r"shorts:\s*\[(.*?)\]\s*,\s*playlists:", index_html, re.DOTALL)
if not m_short:
    m_short = re.search(r"shorts:\s*\[(.*?)\]\s*\n\};", index_html, re.DOTALL)

if m_vid and m_short:
    v_objs = re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_vid.group(1))
    s_objs = re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_short.group(1))
    total_videos = len(v_objs) + len(s_objs)
    print(f"✓ index.html has {len(v_objs)} main videos + {len(s_objs)} shorts = {total_videos} total items in FINAL_THIRD_CONFIG (expected 314)")
    if total_videos != 314:
        errors.append(f"Expected 314 total video items in FINAL_THIRD_CONFIG, found {total_videos}")
else:
    errors.append("Could not find videos or shorts array in index.html FINAL_THIRD_CONFIG")

# Check modal playback logic in index.html
if "openModal" not in index_html and "openVideoModal" not in index_html and "video-modal" not in index_html:
    errors.append("Modal video playback markup/script missing in index.html")
else:
    print("✓ Modal playback code verified in index.html")

# Check contact form and sponsors in index.html
if 'id="contact"' not in index_html:
    errors.append("Contact section missing in index.html")
else:
    print("✓ Contact section verified in index.html")
if 'id="sponsors"' not in index_html and 'sponsor' not in index_html:
    errors.append("Sponsor section missing in index.html")
else:
    print("✓ Sponsor section verified in index.html")

# 5. Check dedicated pages and hubs
pages_checked = 0
for sport in ["football", "cricket"]:
    sport_dir = os.path.join(base_dir, sport)
    hub_file = os.path.join(sport_dir, "index.html")
    if not os.path.exists(hub_file):
        errors.append(f"Hub missing: {hub_file}")
    else:
        with open(hub_file) as f:
            c = f.read()
        jsonld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
        for jm in jsonld_matches:
            try:
                j_obj = json.loads(jm.strip())
            except Exception as e:
                errors.append(f"Invalid JSON-LD in {hub_file}: {e}")
        print(f"✓ Verified hub /{sport}/")
    
    # Check each subfolder
    for item in os.listdir(sport_dir):
        item_path = os.path.join(sport_dir, item)
        if os.path.isdir(item_path):
            page_file = os.path.join(item_path, "index.html")
            if not os.path.exists(page_file):
                errors.append(f"Missing index.html in {item_path}")
                continue
            with open(page_file) as f:
                c = f.read()
            pages_checked += 1
            # Check JSON-LD
            jsonld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
            if not jsonld_matches:
                errors.append(f"No JSON-LD in {page_file}")
            for jm in jsonld_matches:
                try:
                    data = json.loads(jm.strip())
                    graph = data.get("@graph", [])
                    types = [node.get("@type") for node in graph]
                    if "VideoObject" not in types:
                        errors.append(f"Missing VideoObject in JSON-LD in {page_file}")
                    if "BreadcrumbList" not in types:
                        errors.append(f"Missing BreadcrumbList in JSON-LD in {page_file}")
                except Exception as e:
                    errors.append(f"Invalid JSON-LD in {page_file}: {e}")
            
            # Check AdSense
            if "ca-pub-5399554232098923" not in c:
                errors.append(f"AdSense script missing in {page_file}")
            # Check iframe
            if "youtube.com/embed/" not in c:
                errors.append(f"Iframe embed missing in {page_file}")
            # Check canonical
            expected_canonical = f"https://www.finalthird-haris.com/{sport}/{item}/"
            if f'<link rel="canonical" href="{expected_canonical}">' not in c:
                errors.append(f"Incorrect canonical in {page_file}")

print(f"✓ Verified {pages_checked} dedicated video pages (expected 20)")
if pages_checked != 20:
    errors.append(f"Expected 20 pages checked, got {pages_checked}")

# 6. Check privacy.html
privacy_path = os.path.join(base_dir, "privacy.html")
if not os.path.exists(privacy_path):
    errors.append("privacy.html missing")
else:
    with open(privacy_path) as f:
        pc = f.read()
    required_words = ["Meta Pixel", "907681935642413", "ca-pub-5399554232098923", "GDPR", "Phone"]
    for rw in required_words:
        if rw not in pc:
            errors.append(f"privacy.html missing disclosure: {rw}")
    print("✓ privacy.html all required disclosures verified")

# 7. Check vercel.json
vercel_path = os.path.join(base_dir, "vercel.json")
with open(vercel_path) as f:
    vj = json.load(f)
if "headers" not in vj or len(vj["headers"]) < 5:
    errors.append("vercel.json headers structure unexpected")
else:
    print(f"✓ vercel.json verified with {len(vj['headers'])} routing header rules")

if errors:
    print("\nFAILURES:")
    for err in errors:
        print("  - " + err)
    sys.exit(1)
else:
    print("\n============================================")
    print("ALL 7 VERIFICATION CATEGORIES PASSED (100%)!")
    print("============================================")
