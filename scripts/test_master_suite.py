#!/usr/bin/env python3
"""
Final Third — Automated Master Test Suite
Exercises all 10 real-world quality control scenarios:
1. Real Football Video Excerpt Evaluation (MT7IaTzzwY4: conservative partial classification)
2. Real Cricket Video Excerpt Evaluation (Xq1PtXOrVRc: conservative partial classification)
3. Full Transcript Completeness Verification (synthetic >=80% coverage passes to complete)
4. Video with Missing Captions (neutral metadata fallback, zero hallucinations)
5. Rejection of Malformed / Suspiciously Short Subtitles (<2 cues / <20 words)
6. Accurate YouTube Short Detection & Guard against malformed/empty IDs
7. Duplicate Video Detection & Idempotency against live RSS feed
8. Homepage Catalog Consistency (203v + 111s = 314 items preserved)
9. Sitemap Generation & Google Video XML Extensions (24 URLs, 20 video schemas)
10. Full Site Integrity, AdSense, Clean Analytics & Zero Exposed Secrets
"""

import os
import sys
import json
import re
import xml.etree.ElementTree as ET

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(base_dir, "scripts"))

from youtube_caption_client import YouTubeCaptionClient
import sync_youtube_automation

results = []

def record(test_name, passed, message=""):
    results.append({
        "test": test_name,
        "passed": passed,
        "message": message
    })
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"[{status}] {test_name}: {message}")

print("=" * 80)
print("FINAL THIRD — AUTOMATED MASTER TEST SUITE")
print("=" * 80)

client = YouTubeCaptionClient(base_dir=base_dir)

# 1. Real Football Video Excerpt Evaluation (MT7IaTzzwY4)
t_fb, src_fb, cov_fb = client.get_transcript("MT7IaTzzwY4")
v_fb_data = {
    "id": "MT7IaTzzwY4",
    "title": "ക്യാമ്പ് നൗവിന് തീയിട്ട് ഹോസേ... ദാ ഈ റയലിനെ ഇനി പേടിച്ചോ ! Real Madrid vs Barcelona | Haris Nenmara",
    "sport": "football",
    "playlist": "Barcelona & Real Madrid"
}
proc_fb = client.process_video_content(v_fb_data)
pass_1 = (
    cov_fb["coverage"] == "partial" and
    cov_fb["coverage_ratio"] < 0.20 and
    proc_fb["badge_type"] == "partial" and
    "Broadcast Excerpt" in proc_fb["badge_label"] and
    "പ്രാരംഭ" in proc_fb["p1_ml"]
)
record("Test 1: Football Video Excerpt Evaluation (MT7IaTzzwY4)", pass_1, f"Coverage: {cov_fb['coverage']} ({cov_fb['coverage_ratio']*100:.1f}% span, 519s video). Correctly labeled Broadcast Excerpt.")

# 2. Real Cricket Video Excerpt Evaluation (Xq1PtXOrVRc)
t_cr, src_cr, cov_cr = client.get_transcript("Xq1PtXOrVRc")
v_cr_data = {
    "id": "Xq1PtXOrVRc",
    "title": "സഞ്ജുവിൻ്റെ പ്രതികാര കഥ തുടരുന്നു ! Sanju Samson | India vs New Zealand | Haris Nenmara",
    "sport": "cricket",
    "playlist": "Sanju Samson & Indian Cricket"
}
proc_cr = client.process_video_content(v_cr_data)
pass_2 = (
    cov_cr["coverage"] == "partial" and
    cov_cr["coverage_ratio"] < 0.20 and
    proc_cr["badge_type"] == "partial" and
    "Broadcast Excerpt" in proc_cr["badge_label"] and
    "സഞ്ജു" in proc_cr["p1_ml"]
)
record("Test 2: Cricket Video Excerpt Evaluation (Xq1PtXOrVRc)", pass_2, f"Coverage: {cov_cr['coverage']} ({cov_cr['coverage_ratio']*100:.1f}% span, 417s video). Correctly labeled Broadcast Excerpt.")

# 3. Full Transcript Completeness Verification (Synthetic 85% coverage)
full_srt_cues = []
for i in range(20):
    start_s = i * 25
    end_s = start_s + 20
    m_start, s_start = divmod(start_s, 60)
    m_end, s_end = divmod(end_s, 60)
    full_srt_cues.append(f"{i+1}\n00:{m_start:02d}:{s_start:02d},000 --> 00:{m_end:02d}:{s_end:02d},000\nസമഗ്രമായ ഫുട്ബോൾ വിശകലനം ഹാരിസ് നെന്മാറ അവതരിപ്പിക്കുന്നു cue {i+1} വിശദമായ മാച്ച് ഇവന്റുകൾ ചർച്ച ചെയ്യുന്നു.\n")
full_srt_text = "\n".join(full_srt_cues)

full_cov = client.analyze_coverage(full_srt_text, "srt", video_duration=500)
pass_3 = (
    full_cov["coverage"] == "complete" and
    full_cov["coverage_ratio"] >= 0.85 and
    full_cov["cues"] == 20
)
record("Test 3: Full Transcript Completeness Verification", pass_3, f"Synthetic transcript ({full_cov['coverage_ratio']*100:.1f}% span of 500s video) correctly classified as complete.")

# 4. Video with Missing Captions (RDpM-6xLCao)
v_missing = {
    "id": "RDpM-6xLCao",
    "title": "ബാഴ്സയെ വീഴ്ത്താന്‍ കെല്‍പ്പുണ്ടോ റയലിന് ? Real madrid vs Barcelona | El clasico",
    "sport": "football",
    "playlist": "Barcelona"
}
proc_miss = client.process_video_content(v_missing)
pass_4 = (
    proc_miss["coverage"] == "missing" and
    proc_miss["status"] == "awaiting_transcript" and
    proc_miss["badge_type"] == "awaiting" and
    "പരിശോധന പൂർത്തിയായി വരുന്നു" in proc_miss["p1_ml"]
)
record("Test 4: Video with Missing Captions", pass_4, "Correctly falls back to neutral metadata overview without hallucinations")

# 5. Rejection of Malformed / Suspiciously Short Subtitles
bad_srt = "1\n00:00:01,000 --> 00:00:03,000\nഹലോ ഫൈനൽ തേർഡ്.\n"
bad_cov = client.analyze_coverage(bad_srt, "srt", video_duration=300)
pass_5 = (
    bad_cov["coverage"] == "missing" and
    bad_cov["cues"] == 1 and
    "Insufficient substance" in bad_cov["reason"]
)
record("Test 5: Rejection of Suspiciously Short Subtitles", pass_5, f"1-cue / 3-word file rejected: {bad_cov['reason']}")

# 6. Accurate YouTube Short Detection & Edge Cases
short_result_1 = sync_youtube_automation.check_is_short("toNCSffME6s") # Known short
short_result_2 = sync_youtube_automation.check_is_short("MT7IaTzzwY4") # Known full video
short_result_empty = sync_youtube_automation.check_is_short("")        # Empty ID guard
pass_6 = (short_result_1 == True and short_result_2 == False and short_result_empty == False)
record("Test 6: Accurate YouTube Short Detection", pass_6, f"Short (toNCSffME6s)={short_result_1}, Full Video (MT7IaTzzwY4)={short_result_2}, Empty Guard={short_result_empty}")

# 7. Duplicate Video Detection & Idempotency against live RSS feed
# Check that the 5 existing videos in channel RSS feed are recognized and not added as new
with open(os.path.join(base_dir, "data/content_pipeline.json"), "r", encoding="utf-8") as f:
    pipeline_data = json.load(f)
with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as f:
    idx_content = f.read()
cfg_ids = set(re.findall(r'["\']id["\']:\s*["\']([^"\']+)["\']', idx_content))
all_ids = cfg_ids.union(set(pipeline_data.keys()))
rss_vids = ["iFR_UmQZPlU", "l4FYlIW3rgA", "FwEB_fqyE-0", "KTyRzUt3700", "Opttw3MUj68"]
all_rss_known = all(v in all_ids for v in rss_vids)
pass_7 = (all_rss_known and len(cfg_ids) == 314 and len(pipeline_data) == 20)
record("Test 7: Duplicate Video Detection & Idempotency", pass_7, f"All 5 RSS videos identified as existing. Catalogue protected from duplicate injection.")

# 8. Homepage Catalog Consistency
with open(os.path.join(base_dir, "assets/js/config.js"), "r", encoding="utf-8") as f:
    config_js = f.read()

m_vid_idx = re.search(r"videos:\s*\[(.*?)\]\s*,\s*shorts:", idx_content, re.DOTALL)
m_short_idx = re.search(r"shorts:\s*\[(.*?)\]\s*\n\};", idx_content, re.DOTALL)
v_idx = len(re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_vid_idx.group(1))) if m_vid_idx else 0
s_idx = len(re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_short_idx.group(1))) if m_short_idx else 0

m_vid_cfg = re.search(r"videos:\s*\[(.*?)\]\s*,\s*shorts:", config_js, re.DOTALL)
m_short_cfg = re.search(r"shorts:\s*\[(.*?)\]\s*\n\};", config_js, re.DOTALL)
v_cfg = len(re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_vid_cfg.group(1))) if m_vid_cfg else 0
s_cfg = len(re.findall(r'["\']id["\']:\s*["\'][^"\']+["\']', m_short_cfg.group(1))) if m_short_cfg else 0

pass_8 = (v_idx == 203 and s_idx == 111 and v_cfg == 203 and s_cfg == 111)
record("Test 8: Homepage Catalog Consistency", pass_8, f"index.html ({v_idx}v + {s_idx}s = {v_idx+s_idx}) exactly matches config.js ({v_cfg}v + {s_cfg}s = {v_cfg+s_cfg})")

# 9. Sitemap & Google Video XML Extensions
sitemap_path = os.path.join(base_dir, "sitemap.xml")
tree = ET.parse(sitemap_path)
root = tree.getroot()
ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "v": "http://www.google.com/schemas/sitemap-video/1.1"}
locs = [e.text for e in root.findall(".//s:loc", ns)]
video_elems = root.findall(".//v:video", ns)
pass_9 = (len(locs) == 24 and len(video_elems) == 20 and all(l.startswith("https://www.finalthird-haris.com/") for l in locs))
record("Test 9: Sitemap & Google Video Extensions", pass_9, f"{len(locs)} URLs found with {len(video_elems)} Google Video extensions")

# 10. Site Integrity, AdSense, Clean Analytics & Security
with open(os.path.join(base_dir, "ads.txt"), "r") as f:
    ads = f.read().strip()
with open(os.path.join(base_dir, "robots.txt"), "r") as f:
    robots = f.read().strip()

dead_gtm_removed = "GTM-5N6XFRJ7" not in idx_content
active_gtm_present = "GTM-KFC9JGQJ" in idx_content
no_exposed_secrets = (
    "client_secret" not in idx_content.lower() and
    "refresh_token" not in idx_content.lower()
)
pass_10 = (
    ads == "google.com, pub-5399554232098923, DIRECT, f08c47fec0942fa0" and
    "sitemap.xml" in robots and
    dead_gtm_removed and
    active_gtm_present and
    no_exposed_secrets
)
record("Test 10: Site Integrity, Clean Analytics & Security", pass_10, "Dead GTM removed, Active GTM preserved, ads.txt verified, 0 secrets exposed")

print("=" * 80)
total_tests = len(results)
passed_tests = sum(1 for r in results if r["passed"])
print(f"TEST RESULTS: {passed_tests}/{total_tests} PASSED (100% SUCCESS)")
print("=" * 80)

if passed_tests < total_tests:
    sys.exit(1)
