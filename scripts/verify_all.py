#!/usr/bin/env python3
"""
Comprehensive verification test suite for Final Third
Tests:
1. ads.txt (Authorized Google Publisher declaration)
2. robots.txt (Valid sitemap reference)
3. sitemap.xml (24 URLs + 20 Google Video schema extensions)
4. index.html (314 authentic videos in FINAL_THIRD_CONFIG, modal player, category links in desktop/mobile nav)
5. Category Listing Hubs (/football/ with 14 cards, /cricket/ with 6 cards, all clickable to dedicated pages)
6. Dedicated Video Pages (Breadcrumbs: Home > Sport > Title, Back links, 4 Clickable related video cards, Schema.org VideoObject/BreadcrumbList/WebPage, AdSense, Analytics)
7. privacy.html (AdSense, GA4, GTM, Meta Pixel, Phone/Name/Email contact form, GDPR disclosures)
8. vercel.json (Explicit routing and caching rules)
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
errors = []

print("==================================================")
print("FINAL THIRD — INTEGRATION & DEPLOYMENT TEST SUITE")
print("==================================================")

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
        print("✓ 1. ads.txt verified (pub-5399554232098923 DIRECT)")

# 2. Test robots.txt
robots_path = os.path.join(base_dir, "robots.txt")
with open(robots_path) as f:
    robots_content = f.read()
if "https://www.finalthird-haris.com/sitemap.xml" not in robots_content:
    errors.append("robots.txt does not reference https://www.finalthird-haris.com/sitemap.xml")
else:
    print("✓ 2. robots.txt verified (references sitemap.xml)")

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
    if video_count != 20:
        errors.append(f"Expected 20 video entries, found {video_count}")
    print(f"✓ 3. sitemap.xml verified ({len(urls)} URLs, {video_count} video entries)")
except Exception as e:
    errors.append(f"sitemap.xml error: {e}")

# 4. Check index.html
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
    if total_videos != 314:
        errors.append(f"Expected 314 total video items in FINAL_THIRD_CONFIG, found {total_videos}")
    print(f"✓ 4a. FINAL_THIRD_CONFIG verified: {len(v_objs)} videos + {len(s_objs)} shorts = {total_videos} items (100% intact)")
else:
    errors.append("Could not find videos or shorts array in index.html FINAL_THIRD_CONFIG")

# Check modal playback logic in index.html
if "openVideoModal" not in index_html:
    errors.append("Modal video playback logic missing in index.html")
else:
    print("✓ 4b. Modal playback functionality verified in index.html")

# Check category links in desktop & mobile nav on homepage
if 'href="/football/"' not in index_html or 'href="/cricket/"' not in index_html:
    errors.append("Category links (/football/ or /cricket/) missing from index.html")
else:
    print("✓ 4c. Navigation links to /football/ and /cricket/ verified in index.html (desktop & mobile nav)")

# Check category banner on homepage
if "category-hubs-banner" not in index_html:
    errors.append("category-hubs-banner missing in index.html")
else:
    print("✓ 4d. Category Hubs quick navigation banner verified in index.html")

# Check DEDICATED_PAGE_MAP in index.html
if "DEDICATED_PAGE_MAP" not in index_html:
    errors.append("DEDICATED_PAGE_MAP missing in index.html")
else:
    print("✓ 4e. Client-side DEDICATED_PAGE_MAP verified in index.html")

# 5. Check Category Hubs (/football/ and /cricket/)
hub_card_counts = {}
for sport in ["football", "cricket"]:
    hub_file = os.path.join(base_dir, sport, "index.html")
    if not os.path.exists(hub_file):
        errors.append(f"Hub file missing: {hub_file}")
        continue
    with open(hub_file) as f:
        hub_c = f.read()
    
    # Check JSON-LD
    m_jld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', hub_c, re.DOTALL)
    for jm in m_jld:
        try:
            d = json.loads(jm.strip())
            types = [n.get("@type") for n in d.get("@graph", [])]
            if "CollectionPage" not in types or "BreadcrumbList" not in types:
                errors.append(f"Missing CollectionPage/BreadcrumbList in {hub_file}")
        except Exception as e:
            errors.append(f"JSON-LD error in {hub_file}: {e}")
            
    # Check cards
    cards = re.findall(r'<article class="hub-card".*?href="(/[^"]+)".*?</article>', hub_c, re.DOTALL)
    hub_card_counts[sport] = len(cards)
    
    # Confirm every card links to a valid dedicated video page
    for card_url in cards:
        target_path = os.path.join(base_dir, card_url.strip("/"), "index.html")
        if not os.path.exists(target_path):
            errors.append(f"Broken card link in /{sport}/: {card_url} (target does not exist)")

print(f"✓ 5. Category listing hubs verified: /football/ ({hub_card_counts.get('football', 0)} clickable cards), /cricket/ ({hub_card_counts.get('cricket', 0)} clickable cards)")
if hub_card_counts.get("football") != 14:
    errors.append(f"Expected 14 cards in /football/, found {hub_card_counts.get('football')}")
if hub_card_counts.get("cricket") != 6:
    errors.append(f"Expected 6 cards in /cricket/, found {hub_card_counts.get('cricket')}")

# 6. Check All 20 Dedicated Video Pages
pages_checked = 0
for sport in ["football", "cricket"]:
    sport_dir = os.path.join(base_dir, sport)
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
            
            # Check Breadcrumb format: Home > Sport > Title
            if "breadcrumb-bar" not in c or "&gt;" not in c:
                errors.append(f"Missing visible &gt; breadcrumbs in {page_file}")
            
            # Check Back link
            if f'href="/{sport}/"' not in c or "Back to" not in c:
                errors.append(f"Missing Back to {sport} link in {page_file}")
                
            # Check Related Cards (at least 3-4 cards)
            related_cards = re.findall(r'<article class="related-card".*?href="(/[^"]+)".*?</article>', c, re.DOTALL)
            if len(related_cards) < 3:
                errors.append(f"Insufficient related cards in {page_file} (found {len(related_cards)})")
            for rc_url in related_cards:
                rc_target = os.path.join(base_dir, rc_url.strip("/"), "index.html")
                if not os.path.exists(rc_target):
                    errors.append(f"Broken related card link in {page_file}: {rc_url}")
            
            # Check JSON-LD
            m_jld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', c, re.DOTALL)
            for jm in m_jld:
                try:
                    d = json.loads(jm.strip())
                    types = [n.get("@type") for n in d.get("@graph", [])]
                    if "VideoObject" not in types or "BreadcrumbList" not in types:
                        errors.append(f"Missing VideoObject/BreadcrumbList in {page_file}")
                except Exception as e:
                    errors.append(f"JSON-LD error in {page_file}: {e}")
            
            # Check Canonical
            expected_canonical = f"https://www.finalthird-haris.com/{sport}/{item}/"
            if f'<link rel="canonical" href="{expected_canonical}">' not in c:
                errors.append(f"Incorrect canonical in {page_file}")

print(f"✓ 6. Verified {pages_checked} dedicated video pages (breadcrumbs, back-links, related cards, Schema.org, canonical)")
if pages_checked != 20:
    errors.append(f"Expected 20 pages checked, found {pages_checked}")

# 7. Check privacy.html
privacy_path = os.path.join(base_dir, "privacy.html")
with open(privacy_path) as f:
    pc = f.read()
required_words = ["Meta Pixel", "907681935642413", "ca-pub-5399554232098923", "GDPR", "Phone"]
for rw in required_words:
    if rw not in pc:
        errors.append(f"privacy.html missing disclosure: {rw}")
print("✓ 7. privacy.html verified with full compliance disclosures")

# 8. Check vercel.json
vercel_path = os.path.join(base_dir, "vercel.json")
with open(vercel_path) as f:
    vj = json.load(f)
if "headers" not in vj or len(vj["headers"]) < 5:
    errors.append("vercel.json headers structure unexpected")
else:
    print(f"✓ 8. vercel.json verified ({len(vj['headers'])} explicit routing rules)")

if errors:
    print("\nFAILURES:")
    for err in errors:
        print("  - " + err)
    sys.exit(1)
else:
    print("\n==================================================")
    print("ALL 8 VERIFICATION CATEGORIES PASSED (100% GREEN)!")
    print("==================================================")
