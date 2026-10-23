#!/usr/bin/env python3
"""
Applies the 5 user requests:
1. Sleek Editorial visual design cleanup (remove glows/blobs, matte white/dark styling, lime strictly on primary buttons and action points).
2. Hero portrait replaced with landscape image (assets/images/haris-hero-landscape.png), and last picture (About) replaced with portrait image (assets/images/haris-portrait-about.jpg).
3. Show 12 videos per page in the display (itemsPerPage: 12, visibleCount: 12).
4. Remove section 3 (Two Worlds. One Voice. / sports-gateways).
5. Remove section 4 (Commercial Sectors strip in sponsor section).
"""

import re

# 1. Read files
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

print("Original sizes: index.html =", len(html), "styles.css =", len(css), "app.js =", len(app_js))

# ==============================================================================
# TASK 4: Remove Section 3 (Coverage Pillars: Two Worlds. One Voice.)
# ==============================================================================
pillars_marker = '<!-- =======================================================================\n         5. SPORT CATEGORIES & MAIN MATCH PLAYLISTS'
idx_p_start = html.find(pillars_marker)
if idx_p_start != -1:
    idx_p_sec = html.find('id="sports-gateways"', idx_p_start)
    idx_p_end = html.find('</section>', idx_p_sec) + len('</section>')
    html = html[:idx_p_start] + html[idx_p_end:]
    print("✓ Successfully removed Section 3 (Two Worlds. One Voice.) from index.html")
else:
    print("Notice: sports-gateways marker not found")

# ==============================================================================
# TASK 5: Remove Section 4 (Commercial Sectors Strip in Sponsor section)
# ==============================================================================
strip_marker = '<!-- Commercial Sectors Strip -->'
idx_s_start = html.find(strip_marker)
if idx_s_start != -1:
    idx_s_dock = html.find('<!-- Luxury Action Dock -->', idx_s_start)
    # end of the strip div
    idx_s_end = html.rfind('</div>', idx_s_start, idx_s_dock) + len('</div>')
    html = html[:idx_s_start] + html[idx_s_end:]
    print("✓ Successfully removed Section 4 (Commercial Sectors strip) from index.html")
else:
    print("Notice: Commercial Sectors strip marker not found")

# ==============================================================================
# TASK 2: Replace Hero visual with Landscape image & About photo with Portrait image
# ==============================================================================
# Hero: Replace from '<!-- Right: Editorial Portrait of Haris Nenmara -->' to '<!-- Floating identity card -->'
hero_img_marker = '<!-- Right: Editorial Portrait of Haris Nenmara -->'
idx_h_start = html.find(hero_img_marker)
if idx_h_start != -1:
    idx_h_end = html.find('<!-- Floating identity card -->', idx_h_start)
    new_hero_visual = """<!-- Right: Cinematic Studio Visual of Haris Nenmara -->
        <div class="hero-portrait-wrapper">
          <div class="portrait-editorial-frame">
            <img 
              src="assets/images/haris-hero-landscape.png" 
              alt="Haris Nenmara — Final Third Sports Host &amp; Analyst" 
              class="portrait-editorial-img"
              width="1024" 
              height="576"
              loading="eager"
            />
          </div>
          """
    html = html[:idx_h_start] + new_hero_visual + html[idx_h_end:]
    print("✓ Successfully replaced Hero image with landscape picture (Reference 2)")
else:
    print("Notice: Hero portrait marker not found")

# About: Replace about image
about_img_marker = '<!-- Authentic Portrait of Haris Nenmara -->'
idx_a_start = html.find(about_img_marker)
if idx_a_start != -1:
    idx_a_end = html.find('<!-- About Details & Editorial Philosophy -->', idx_a_start)
    new_about_img = """<!-- Authentic Portrait of Haris Nenmara -->
          <div class="about-portrait-wrap">
            <img 
              src="assets/images/haris-portrait-about.jpg" 
              alt="Haris Nenmara — Creator &amp; Host of Final Third" 
              class="about-portrait-img" 
              width="682" 
              height="1024"
              loading="lazy"
            />
            <span class="about-badge">CREATOR &amp; HOST</span>
          </div>

          """
    html = html[:idx_a_start] + new_about_img + html[idx_a_end:]
    print("✓ Successfully replaced About image with portrait picture (Reference 1)")
else:
    print("Notice: About portrait marker not found")

# ==============================================================================
# TASK 3: Show only 12 videos in display
# ==============================================================================
html = html.replace('itemsPerPage: 20,           // 20 videos per page (user requested)', 'itemsPerPage: 12,           // 12 videos per page (user requested)')
html = html.replace('visibleCount: 20,           // 20 videos on 1st page', 'visibleCount: 12,           // 12 videos on 1st page')

app_js = app_js.replace('itemsPerPage: 20,           // 20 videos per page (user requested)', 'itemsPerPage: 12,           // 12 videos per page (user requested)')
app_js = app_js.replace('visibleCount: 20,           // 20 videos on 1st page', 'visibleCount: 12,           // 12 videos on 1st page')
print("✓ Successfully updated display video count to 12 videos per page")

# ==============================================================================
# TASK 1: Apply "Sleek Editorial" Styling (CSS cleanup in styles.css and index.html)
# ==============================================================================
# Define the sleek editorial CSS updates

editorial_css_additions = """
/* ==========================================================================
   SLEEK EDITORIAL DESIGN SYSTEM OVERRIDES (HARMONIZED MATTE PALETTE)
   ========================================================================== */

/* Typography & Titles: Crisp Pure Editorial White */
.section-title {
  color: #FFFFFF !important;
  text-shadow: none !important;
}

.highlight {
  color: #FFFFFF !important;
  text-shadow: none !important;
}

.lime {
  color: #FFFFFF !important;
  text-shadow: none !important;
}

/* Eyebrows: Sophisticated Neutral with Tiny Lime Dot */
.eyebrow {
  color: #888888 !important;
  font-size: 0.75rem !important;
  letter-spacing: 0.12em !important;
}

.eyebrow::before {
  background-color: var(--neon-lime) !important;
  border-radius: 50% !important;
  width: 6px !important;
  height: 6px !important;
}

/* Hero Section: Remove Glowing Blobs & Fit Landscape Frame */
.hero-section {
  background: #080808 !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.portrait-glow-ring,
.portrait-lime-accent {
  display: none !important;
}

.portrait-editorial-frame {
  max-width: 520px !important;
  aspect-ratio: 16 / 9 !important;
  border-radius: 16px !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9) !important;
  background: #0d0d0d !important;
}

.portrait-editorial-img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center 25% !important;
}

.portrait-floating-card {
  background: rgba(18, 18, 18, 0.92) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8) !important;
  bottom: -12px !important;
  right: 18px !important;
}

.stat-item .stat-value {
  color: #FFFFFF !important;
  text-shadow: none !important;
}

.badge-tag {
  background-color: #141414 !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #D4D4D4 !important;
}

/* Video Grid & Cards: Clean Matte Surfaces */
.video-card {
  background: #121212 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: none !important;
}

.video-card:hover {
  border-color: rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8) !important;
}

/* Filter Tabs: Inactive Neutral, Active Lime */
.sport-tab {
  background-color: #141414 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #A3A3A3 !important;
}

.sport-tab:hover {
  color: #FFFFFF !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
}

.sport-tab.active {
  background-color: var(--neon-lime) !important;
  color: #080808 !important;
  border-color: var(--neon-lime) !important;
}

/* Shorts Section: Matte Dark, Clean Badges */
.shorts-section {
  background: #0b0b0b !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.shorts-icon-pill {
  box-shadow: none !important;
}

.short-card {
  background: #141414 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.short-card:hover {
  border-color: rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.9) !important;
}

/* Sponsor Section: Remove Neon Glows */
.sponsor-banner-section {
  background: #080808 !important;
  border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.sponsor-banner-section::before,
.sponsor-banner-card::before,
.sponsor-banner-card::after {
  display: none !important;
}

.sponsor-banner-card {
  background: #111111 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8) !important;
}

.sponsor-stat-item {
  background: #161616 !important;
  border: 1px solid rgba(255, 255, 255, 0.06) !important;
}

.sponsor-stat-value {
  color: #FFFFFF !important;
  text-shadow: none !important;
}

.sponsor-package-card {
  background: #161616 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: none !important;
}

.sponsor-package-card:hover {
  border-color: rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8) !important;
}

.sponsor-package-card.featured {
  background: #181818 !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
}

.sponsor-dock {
  background: #161616 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* About Section */
.about-portrait-wrap {
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8) !important;
  border-radius: 16px !important;
}

.about-badge {
  background: rgba(18, 18, 18, 0.88) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  color: #FFFFFF !important;
}

/* Contact Section */
.contact-form-box {
  background: #111111 !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8) !important;
}

/* Primary Action Buttons: Maintain Brand Lime */
.btn-primary {
  background-color: var(--neon-lime) !important;
  color: #080808 !important;
  border-color: var(--neon-lime) !important;
  box-shadow: 0 4px 18px rgba(158, 226, 11, 0.25) !important;
}

.btn-primary:hover {
  background-color: #aef016 !important;
  border-color: #aef016 !important;
  box-shadow: 0 8px 24px rgba(158, 226, 11, 0.4) !important;
}

.btn-outline {
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #E0E0E0 !important;
}

.btn-outline:hover {
  border-color: rgba(255, 255, 255, 0.5) !important;
  color: #FFFFFF !important;
  background-color: rgba(255, 255, 255, 0.05) !important;
}
"""

# Append / Inject editorial_css_additions to styles.css
if "SLEEK EDITORIAL DESIGN SYSTEM OVERRIDES" not in css:
    css = css + "\n" + editorial_css_additions

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Inject into index.html <style> block right before </style>
if "SLEEK EDITORIAL DESIGN SYSTEM OVERRIDES" not in html:
    idx_style_end = html.find('</style>')
    if idx_style_end != -1:
        html = html[:idx_style_end] + editorial_css_additions + '\n  ' + html[idx_style_end:]
        print("✓ Successfully injected Sleek Editorial CSS overrides into index.html <style>")

# Update contact badge inline styles in index.html to match
contact_lime_pill = 'background: rgba(158,226,11,0.1); padding: 5px 12px; border-radius: 999px; border: 1px solid rgba(158,226,11,0.3);'
contact_matte_pill = 'background: #1a1a1a; padding: 5px 12px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.1); color: #FFFFFF;'
html = html.replace(contact_lime_pill, contact_matte_pill)

# Save updated files
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('assets/js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Finished applying all 5 updates!")
