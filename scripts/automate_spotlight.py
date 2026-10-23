#!/usr/bin/env python3
"""
Automates Spotlight Analysis so it ALWAYS automatically features the latest video:
1. Adds renderSpotlightVideo() to app.js and index.html (client-side dynamic automation).
2. Updates sync_youtube_videos.py so automated cron jobs update featuredVideoId on new releases.
3. Updates static HTML in index.html to pre-render the latest video (Xq1PtXOrVRc - Sanju Samson).
4. Updates featuredVideoId in assets/js/config.js.
"""

import re
import json

# ==============================================================================
# 1. Update assets/js/config.js and index.html config
# ==============================================================================
with open('assets/js/config.js', 'r', encoding='utf-8') as f:
    config_js = f.read()

config_js = re.sub(r'featuredVideoId:\s*"[^"]*"', 'featuredVideoId: "Xq1PtXOrVRc"', config_js)
with open('assets/js/config.js', 'w', encoding='utf-8') as f:
    f.write(config_js)
print("✓ Updated featuredVideoId in assets/js/config.js to Xq1PtXOrVRc")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'featuredVideoId:\s*"[^"]*"', 'featuredVideoId: "Xq1PtXOrVRc"', html)

# ==============================================================================
# 2. Update static HTML of featured-match-card in index.html
# ==============================================================================
latest_title = "സഞ്ജുവിൻ്റെ പ്രതികാര കഥ തുടരുന്നു ! Sanju Samson"
latest_id = "Xq1PtXOrVRc"
latest_sport = "CRICKET"
latest_meta = "Cricket Stories &amp; Analysis · Latest Upload · Just now"
latest_summary = "സഞ്ജുവിൻ്റെ പ്രതികാര കഥ തുടരുന്നു ! Sanju Samson"

# Replace thumbnail container
html = re.sub(
    r'onclick="openVideoModal\(\'Opttw3MUj68\'\)"',
    f'onclick="openVideoModal(\'{latest_id}\')"',
    html
)
html = re.sub(
    r'https://i\.ytimg\.com/vi/Opttw3MUj68/maxresdefault\.jpg',
    f'https://i.ytimg.com/vi/{latest_id}/maxresdefault.jpg',
    html
)
html = re.sub(
    r'https://i\.ytimg\.com/vi/Opttw3MUj68/hqdefault\.jpg',
    f'https://i.ytimg.com/vi/{latest_id}/hqdefault.jpg',
    html
)
html = html.replace(
    'alt="Featured Story Thumbnail: Mohammed Shami and Bhuvneshwar Kumar pace analysis"',
    f'alt="Featured Story Thumbnail: {latest_title}"'
)
html = html.replace(
    'aria-label="Play featured story: ഭുവി വന്നു; ഷമി വരില്ലേ ? Mohammed Shami"',
    f'aria-label="Play featured story: {latest_title}"'
)
html = html.replace(
    'Team India &amp; Pace Attack · Latest Upload · 13h ago',
    latest_meta
)
html = html.replace(
    'ഭുവി വന്നു; ഷമി വരില്ലേ ? Mohammed Shami',
    latest_title
)
html = html.replace(
    'Tactical breakdown and pace bowling analysis on Bhuvneshwar Kumar and Mohammed Shami\'s potential comeback into Team India\'s attack.',
    latest_summary
)
html = html.replace(
    'href="https://www.youtube.com/watch?v=Opttw3MUj68"',
    f'href="https://www.youtube.com/watch?v={latest_id}"'
)
print("✓ Updated static HTML in index.html to pre-render the latest video")

# ==============================================================================
# 3. Add renderSpotlightVideo() to app.js and index.html
# ==============================================================================
spotlight_renderer_js = """
  // =========================================================================
  // DYNAMIC SPOTLIGHT ANALYSIS (ALWAYS AUTOMATICALLY USES LATEST VIDEO)
  // =========================================================================
  function renderSpotlightVideo() {
    if (typeof FINAL_THIRD_CONFIG === 'undefined' || !FINAL_THIRD_CONFIG.videos || FINAL_THIRD_CONFIG.videos.length === 0) return;

    // Always automatically pick the newest full-length episode (index 0)
    const latest = FINAL_THIRD_CONFIG.videos[0];
    FINAL_THIRD_CONFIG.featuredVideoId = latest.id;

    const thumbContainer = document.getElementById('featuredThumbnail');
    const headline = document.getElementById('featuredHeadline');
    const summary = document.querySelector('.featured-summary');
    const sportBadge = document.querySelector('.featured-tag-bar .badge-tag');
    const metaSpan = document.querySelector('.featured-tag-bar span:last-child');
    const watchStoryBtn = document.getElementById('featuredWatchStoryBtn');
    const watchYtBtn = document.querySelector('.featured-actions a.btn-outline');

    if (thumbContainer) {
      thumbContainer.onclick = () => openVideoModal(latest.id);
      thumbContainer.setAttribute('aria-label', `Play featured story: ${latest.title}`);
      const img = thumbContainer.querySelector('img');
      if (img) {
        img.src = `https://i.ytimg.com/vi/${latest.id}/maxresdefault.jpg`;
        img.alt = `Spotlight Analysis Thumbnail: ${latest.title}`;
        img.onerror = function() {
          this.src = `https://i.ytimg.com/vi/${latest.id}/hqdefault.jpg`;
        };
      }
    }

    if (headline) {
      headline.textContent = latest.title;
      headline.onclick = () => openVideoModal(latest.id);
    }

    if (summary) {
      summary.textContent = latest.summary || latest.title;
    }

    if (sportBadge) {
      sportBadge.textContent = (latest.sport || 'Sports').toUpperCase();
    }

    if (metaSpan) {
      const plTitle = latest.playlistTitle || 'Latest Release';
      const pubTime = latest.published || 'Latest';
      metaSpan.textContent = `${plTitle} · Latest Upload · ${pubTime}`;
    }

    if (watchStoryBtn) {
      watchStoryBtn.onclick = () => openVideoModal(latest.id);
    }

    if (watchYtBtn) {
      watchYtBtn.href = `https://www.youtube.com/watch?v=${latest.id}`;
    }
  }
"""

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

if "renderSpotlightVideo()" not in app_js:
    # Insert function before the closing of DOMContentLoaded
    idx_end = app_js.rfind("initEditorialAnimations();")
    if idx_end != -1:
        insert_pos = idx_end + len("initEditorialAnimations();")
        app_js = app_js[:insert_pos] + "\n  renderSpotlightVideo();" + app_js[insert_pos:]
        
    idx_end_listener = app_js.rfind("});")
    app_js = app_js[:idx_end_listener] + "\n" + spotlight_renderer_js + "\n" + app_js[idx_end_listener:]
    with open('assets/js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    print("✓ Added renderSpotlightVideo() to assets/js/app.js")

if "renderSpotlightVideo()" not in html:
    idx_h_end = html.rfind("initEditorialAnimations();")
    if idx_h_end != -1:
        insert_h_pos = idx_h_end + len("initEditorialAnimations();")
        html = html[:insert_h_pos] + "\n  renderSpotlightVideo();" + html[insert_h_pos:]
        
    idx_h_listener = html.rfind("});\n  </script>")
    if idx_h_listener == -1:
        idx_h_listener = html.rfind("});")
    html = html[:idx_h_listener] + "\n" + spotlight_renderer_js + "\n" + html[idx_h_listener:]
    print("✓ Added renderSpotlightVideo() to index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ==============================================================================
# 4. Update scripts/sync_youtube_videos.py to automate featuredVideoId
# ==============================================================================
with open('scripts/sync_youtube_videos.py', 'r', encoding='utf-8') as f:
    sync_code = f.read()

helper_fn = """def update_featured_id(filepath, video_id):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'featuredVideoId:\\s*"[^"]*"', f'featuredVideoId: "{video_id}"', content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
"""

if "def update_featured_id" not in sync_code:
    idx_fn = sync_code.find("def update_file")
    sync_code = sync_code[:idx_fn] + helper_fn + "\n" + sync_code[idx_fn:]

hook = """    if ok1 and ok2:
        if new_full_videos:
            newest_id = new_full_videos[0]["id"]
            update_featured_id("index.html", newest_id)
            update_featured_id("assets/js/config.js", newest_id)
            print(f"★ Automatically set Spotlight Analysis to latest release: [{newest_id}]")
"""

old_hook = """    if ok1 and ok2:
        print(f"✓ Successfully routed {len(new_full_videos)} episode(s) and {len(new_shorts)} short(s) to index.html and config.js!")"""

if "update_featured_id(\"index.html\"" not in sync_code and old_hook in sync_code:
    sync_code = sync_code.replace(
        old_hook,
        hook + "\n        " + 'print(f"✓ Successfully routed {len(new_full_videos)} episode(s) and {len(new_shorts)} short(s) to index.html and config.js!")'
    )
    with open('scripts/sync_youtube_videos.py', 'w', encoding='utf-8') as f:
        f.write(sync_code)
    print("✓ Updated scripts/sync_youtube_videos.py to automatically keep Spotlight Analysis current")

print("All Spotlight Analysis automation completed successfully!")
