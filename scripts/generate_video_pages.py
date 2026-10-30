#!/usr/bin/env python3
"""
Final Third — Dedicated Video SEO Pages & Category Hubs Generator
Generates:
1. 20 dedicated, accessible SEO video pages (14 Football, 6 Cricket)
2. Football category hub (/football/index.html) with 14 clickable video cards
3. Cricket category hub (/cricket/index.html) with 6 clickable video cards
4. Google Video XML Sitemap (sitemap.xml)
"""

import os
import json
import re

DOMAIN = "https://www.finalthird-haris.com"

_pipeline_file = os.path.join(os.path.dirname(__file__), "../data/content_pipeline.json")
if os.path.exists(_pipeline_file):
    with open(_pipeline_file, "r", encoding="utf-8") as _pf:
        _pipe_data = json.load(_pf)
    VIDEOS = list(_pipe_data.values())
else:
    VIDEOS = []

# Generate common navigation header
def render_navbar(active_page=""):
    football_active = ' active' if active_page == 'football' else ''
    cricket_active = ' active' if active_page == 'cricket' else ''
    home_active = ' active' if active_page == 'home' else ''
    fb_count = len([v for v in VIDEOS if v.get("sport") == "football"])
    cr_count = len([v for v in VIDEOS if v.get("sport") == "cricket"])
    
    return f"""  <header class="site-header">
    <div class="nav-container">
      <a href="/" class="brand-link" aria-label="Final Third Home">
        <picture>
          <source srcset="/assets/images/final-third-logo.webp" type="image/webp">
          <img src="/assets/images/final-third-logo.png" alt="Final Third Logo" class="brand-logo" width="160" height="36">
        </picture>
        <span class="brand-name">FINAL THIRD</span>
      </a>

      <!-- Desktop Navigation Links -->
      <nav class="main-nav" aria-label="Main Navigation">
        <ul class="nav-list">
          <li><a href="/" class="nav-link{home_active}">Home</a></li>
          <li><a href="/football/" class="nav-link{football_active}">⚽ Football Hub</a></li>
          <li><a href="/cricket/" class="nav-link{cricket_active}">🏏 Cricket Hub</a></li>
          <li><a href="/#videos" class="nav-link">Full Catalog (300+)</a></li>
          <li><a href="/#about" class="nav-link">About Haris</a></li>
          <li><a href="/#contact" class="nav-link">Contact</a></li>
        </ul>
      </nav>

      <!-- Action Buttons -->
      <div class="nav-actions">
        <a href="https://www.youtube.com/@FinalThird_HarisNenmara" target="_blank" rel="noopener noreferrer" class="btn btn-subscribe" aria-label="Subscribe on YouTube">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
          </svg>
          SUBSCRIBE
        </a>
        <button class="mobile-toggle" id="mobileMenuToggle" aria-label="Toggle Navigation Menu" aria-expanded="false">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16m-7 6h7" />
          </svg>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Drawer -->
  <div class="mobile-drawer" id="mobileDrawer" aria-hidden="true">
    <div class="drawer-content">
      <ul class="drawer-list">
        <li><a href="/" class="drawer-link{home_active}">Home</a></li>
        <li><a href="/football/" class="drawer-link{football_active}">⚽ Football Category Hub ({fb_count} Videos)</a></li>
        <li><a href="/cricket/" class="drawer-link{cricket_active}">🏏 Cricket Category Hub ({cr_count} Videos)</a></li>
        <li><a href="/#videos" class="drawer-link">Full Video Catalog (300+)</a></li>
        <li><a href="/#about" class="drawer-link">About Haris Nenmara</a></li>
        <li><a href="/privacy.html" class="drawer-link">Privacy Policy</a></li>
        <li><a href="/#contact" class="drawer-link">Contact &amp; Sponsorships</a></li>
      </ul>
      <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #2a2a2a;">
        <a href="https://www.youtube.com/@FinalThird_HarisNenmara" target="_blank" rel="noopener noreferrer" class="btn btn-subscribe" style="width: 100%; justify-content: center;">
          SUBSCRIBE ON YOUTUBE ↗
        </a>
      </div>
    </div>
  </div>"""

# Render individual video page
def render_page(video):
    vid = video["id"]
    slug = video["slug"]
    sport = video["sport"]
    sport_name = "Football" if sport == "football" else "Cricket"
    sport_hub_url = f"/{sport}/"
    url = f"{DOMAIN}/{sport}/{slug}/"
    thumb_hq = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    thumb_max = f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    
    # Verification Badge & Headings
    cov_type = video.get("coverage", "complete" if video.get("transcript_available") else "missing")
    if cov_type == "complete" or (video.get("transcript_available") and cov_type != "partial"):
        badge_html = '''<div class="verification-badge verified"><span class="badge-icon">✓</span> Grounded in Verified Complete Broadcast Transcript</div>'''
        section_h2 = "Verified Match Analysis &amp; Breakdown | മലയാളം അവലോകനം"
        takeaways_title = "Key Tactical Takeaways &amp; Discussion Points"
    elif cov_type == "partial":
        badge_html = '''<div class="verification-badge partial"><span class="badge-icon">ℹ</span> Grounded in Broadcast Excerpt (Full Transcript Pending)</div>'''
        section_h2 = "Match Analysis Excerpt &amp; Overview | മലയാളം അവലോകനം"
        takeaways_title = "Key Discussion Points &amp; Video Takeaways"
    else:
        badge_html = '''<div class="verification-badge awaiting"><span class="badge-icon">⏳</span> Awaiting Broadcast Transcript Verification</div>'''
        section_h2 = "Video Overview &amp; Match Analysis | മലയാളം അവലോകനം"
        takeaways_title = "Key Discussion Points &amp; Video Details"
    
    # 4 Related videos from the same sport
    same_sport_videos = [v for v in VIDEOS if v["sport"] == sport and v["id"] != vid]
    related = same_sport_videos[:4]
    if len(related) < 4:
        other_videos = [v for v in VIDEOS if v["id"] != vid and v not in related]
        related += other_videos[:4 - len(related)]
    
    related_cards_html = ""
    for r in related:
        r_url = f"/{r['sport']}/{r['slug']}/"
        related_cards_html += f"""
        <article class="related-card" onclick="window.location.href='{r_url}'" style="cursor: pointer;">
          <a href="{r_url}" class="related-thumb-link" aria-label="{r['title']}">
            <img src="https://i.ytimg.com/vi/{r['id']}/hqdefault.jpg" alt="{r['title']}" width="320" height="180" loading="lazy" decoding="async">
            <span class="related-sport-pill">{r['sport'].upper()}</span>
          </a>
          <div class="related-info">
            <span class="related-meta">{r['playlist']} · {r['views']}</span>
            <h4 class="related-title"><a href="{r_url}">{r['title']}</a></h4>
            <a href="{r_url}" class="related-action-link">Read Breakdown ↗</a>
          </div>
        </article>"""

    takeaways_html = "".join([f"<li>{t}</li>" for t in video["takeaways"]])
    tags_html = "".join([f'<span class="tag-pill">#{t}</span>' for t in video["tags"]])

    html = f"""<!DOCTYPE html>
<html lang="en" xml:lang="ml" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{video['seo_title']}</title>
  <meta name="description" content="{video['meta_desc']}">
  <meta name="author" content="Haris Nenmara (ഹാരിസ് നെന്മാറ)">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">

  <!-- Favicon -->
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">

  <!-- Open Graph -->
  <meta property="og:site_name" content="Final Third with Haris Nenmara">
  <meta property="og:type" content="video.other">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{video['seo_title']}">
  <meta property="og:description" content="{video['meta_desc']}">
  <meta property="og:image" content="{thumb_max}">
  <meta property="og:image:alt" content="{video['title']}">
  <meta property="og:locale" content="ml_IN">
  <meta property="og:locale:alternate" content="en_IN">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{video['seo_title']}">
  <meta name="twitter:description" content="{video['meta_desc']}">
  <meta name="twitter:image" content="{thumb_max}">

  <!-- Tracking -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-KFC9JGQJ');</script>

  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5399554232098923" crossorigin="anonymous"></script>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "VideoObject",
        "@id": "{url}#video",
        "name": {json.dumps(video['title'], ensure_ascii=False)},
        "description": {json.dumps(video['meta_desc'], ensure_ascii=False)},
        "thumbnailUrl": [
          "{thumb_max}",
          "{thumb_hq}"
        ],
        "uploadDate": "{video['published_iso']}",
        "embedUrl": "https://www.youtube.com/embed/{vid}",
        "contentUrl": "https://www.youtube.com/watch?v={vid}",
        "inLanguage": "ml",
        "creator": {{
          "@type": "Person",
          "@id": "{DOMAIN}/#person",
          "name": "Haris Nenmara",
          "alternateName": "ഹാരിസ് നെന്മാറ",
          "jobTitle": "Sports Journalist & Analyst"
        }},
        "publisher": {{
          "@type": "SportsOrganization",
          "@id": "{DOMAIN}/#organization",
          "name": "Final Third",
          "url": "{DOMAIN}/"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{DOMAIN}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{sport_name} Analysis",
            "item": "{DOMAIN}{sport_hub_url}"
          }},
          {{
            "@type": "ListItem",
            "position": 3,
            "name": {json.dumps(video['title'], ensure_ascii=False)},
            "item": "{url}"
          }}
        ]
      }},
      {{
        "@type": "WebPage",
        "@id": "{url}#webpage",
        "url": "{url}",
        "name": {json.dumps(video['seo_title'], ensure_ascii=False)},
        "isPartOf": {{
          "@id": "{DOMAIN}/#website"
        }},
        "primaryImageOfPage": "{thumb_max}"
      }}
    ]
  }}
  </script>

  <style>
    :root {{
      --neon-lime: #9EE20B;
      --neon-lime-hover: #b4f51e;
      --pitch-black: #080808;
      --charcoal: #151515;
      --charcoal-light: #202020;
      --charcoal-border: #2a2a2a;
      --off-white: #F5F5F0;
      --muted-grey: #a0a0a0;
      --dark-grey: #666666;
      --font-primary: 'Anek Malayalam', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--pitch-black);
      color: var(--off-white);
      font-family: var(--font-primary);
      line-height: 1.7;
      font-size: 1rem;
      -webkit-font-smoothing: antialiased;
    }}

    a {{ color: var(--neon-lime); text-decoration: none; transition: color 0.2s ease; }}
    a:hover {{ color: var(--neon-lime-hover); text-decoration: underline; }}

    /* Header & Navigation */
    .site-header {{
      border-bottom: 1px solid var(--charcoal-border);
      background-color: rgba(8, 8, 8, 0.95);
      backdrop-filter: blur(10px);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0.875rem 1.5rem;
    }}
    .nav-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand-link {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: var(--off-white);
      font-weight: 800;
      font-size: 1.125rem;
      letter-spacing: -0.02em;
    }}
    .brand-logo {{ height: 36px; width: auto; display: block; }}
    .brand-name {{ font-weight: 800; color: var(--off-white); letter-spacing: -0.02em; }}
    .main-nav {{ display: flex; align-items: center; }}
    .nav-list {{ display: flex; align-items: center; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; transition: color 0.2s; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}
    .nav-actions {{ display: flex; align-items: center; gap: 1rem; }}
    .btn-subscribe {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background: var(--neon-lime);
      color: #000;
      font-weight: 800;
      font-size: 0.8125rem;
      border-radius: 6px;
      text-decoration: none;
      transition: background-color 0.2s;
    }}
    .btn-subscribe:hover {{ background: var(--neon-lime-hover); text-decoration: none; }}
    .mobile-toggle {{
      display: none;
      background: none;
      border: none;
      color: var(--off-white);
      cursor: pointer;
    }}
    .mobile-drawer {{
      display: none;
      background: var(--charcoal);
      border-bottom: 1px solid var(--charcoal-border);
      padding: 1.5rem;
    }}
    .mobile-drawer.open {{ display: block; }}
    .drawer-list {{ list-style: none; display: flex; flex-direction: column; gap: 1rem; }}
    .drawer-link {{ color: var(--off-white); font-weight: 600; font-size: 1rem; text-decoration: none; }}
    .drawer-link.active {{ color: var(--neon-lime); }}

    /* Breadcrumbs Bar */
    .breadcrumb-bar {{
      max-width: 1140px;
      margin: 1.25rem auto 0;
      padding: 0 1.5rem;
      font-size: 0.8125rem;
      color: var(--dark-grey);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
    }}
    .breadcrumb-bar a {{ color: var(--muted-grey); }}
    .breadcrumb-bar a:hover {{ color: var(--neon-lime); }}
    .breadcrumb-sep {{ color: var(--dark-grey); font-weight: 700; }}
    .breadcrumb-current {{
      color: var(--off-white);
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 500px;
    }}

    /* Back Link Bar */
    .back-link-bar {{
      max-width: 1140px;
      margin: 0.75rem auto 0;
      padding: 0 1.5rem;
    }}
    .back-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--neon-lime);
      text-decoration: none;
      transition: transform 0.2s;
    }}
    .back-link:hover {{ text-decoration: underline; transform: translateX(-3px); }}

    /* Layout */
    .page-layout {{
      max-width: 1140px;
      margin: 1rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 2.5rem;
    }}

    /* Video Hero Box */
    .video-hero {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 2rem;
    }}
    .video-aspect-frame {{
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      background: #000;
    }}
    .video-aspect-frame iframe {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: 0;
    }}
    .video-meta-bar {{
      padding: 1.5rem;
      border-bottom: 1px solid var(--charcoal-border);
    }}
    .meta-pills {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.75rem;
      flex-wrap: wrap;
    }}
    .sport-pill {{
      background-color: var(--neon-lime);
      color: #000;
      font-size: 0.75rem;
      font-weight: 800;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
      letter-spacing: 0.05em;
    }}
    .playlist-pill {{
      background-color: var(--charcoal-light);
      border: 1px solid var(--charcoal-border);
      color: var(--muted-grey);
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
    }}
    .views-pill {{
      color: var(--muted-grey);
      font-size: 0.8125rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .article-h1 {{
      font-size: 1.75rem;
      font-weight: 800;
      line-height: 1.35;
      color: var(--off-white);
      margin-bottom: 1rem;
    }}
    .cta-row {{
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-top: 1.25rem;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.625rem 1.25rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.875rem;
      text-decoration: none;
      transition: all 0.2s ease;
    }}
    .btn-primary {{
      background-color: var(--neon-lime);
      color: #000;
    }}
    .btn-primary:hover {{
      background-color: var(--neon-lime-hover);
      text-decoration: none;
      transform: translateY(-1px);
    }}
    .btn-outline {{
      background: transparent;
      border: 1px solid var(--charcoal-border);
      color: var(--off-white);
    }}
    .btn-outline:hover {{
      border-color: var(--neon-lime);
      color: var(--neon-lime);
      text-decoration: none;
    }}

    /* Verification Badge */
    .verification-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.02em;
      margin-bottom: 1.25rem;
    }}
    .verification-badge.verified {{
      background: rgba(158, 226, 11, 0.12);
      border: 1px solid rgba(158, 226, 11, 0.35);
      color: var(--neon-lime);
    }}
    .verification-badge.partial {{
      background: rgba(59, 130, 246, 0.12);
      border: 1px solid rgba(59, 130, 246, 0.35);
      color: #60a5fa;
    }}
    .verification-badge.awaiting {{
      background: rgba(229, 169, 60, 0.12);
      border: 1px solid rgba(229, 169, 60, 0.35);
      color: #E5A93C;
    }}

    /* Editorial Section */
    .editorial-content {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 2rem;
      margin-bottom: 2rem;
    }}
    .editorial-content h2 {{
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--neon-lime);
      margin-bottom: 1rem;
      letter-spacing: -0.01em;
    }}
    .editorial-content p {{
      color: #d8d8d8;
      font-size: 1.0625rem;
      margin-bottom: 1.25rem;
      line-height: 1.8;
    }}
    .takeaways-box {{
      background-color: rgba(158, 226, 11, 0.05);
      border-left: 3px solid var(--neon-lime);
      padding: 1.25rem 1.5rem;
      border-radius: 0 8px 8px 0;
      margin: 1.5rem 0;
    }}
    .takeaways-box h3 {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
      margin-bottom: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .takeaways-box ul {{ list-style-type: none; }}
    .takeaways-box ul li {{
      position: relative;
      padding-left: 1.5rem;
      margin-bottom: 0.5rem;
      font-size: 0.9375rem;
      color: #e5e5e5;
    }}
    .takeaways-box ul li::before {{
      content: "✔";
      position: absolute;
      left: 0;
      color: var(--neon-lime);
      font-weight: 800;
    }}
    .tags-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1.5rem;
      padding-top: 1rem;
      border-top: 1px solid var(--charcoal-border);
    }}
    .tag-pill {{
      background: var(--charcoal-light);
      border: 1px solid var(--charcoal-border);
      color: var(--muted-grey);
      font-size: 0.75rem;
      padding: 0.25rem 0.6rem;
      border-radius: 4px;
    }}

    /* Author Card */
    .author-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      display: flex;
      gap: 1.25rem;
      align-items: center;
      margin-bottom: 2rem;
    }}
    .author-img {{
      width: 72px;
      height: 72px;
      border-radius: 50%;
      border: 2px solid var(--neon-lime);
      object-fit: cover;
      flex-shrink: 0;
    }}
    .author-info h4 {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
    }}
    .author-role {{ font-size: 0.8125rem; color: var(--neon-lime); margin-bottom: 0.25rem; }}
    .author-bio {{ font-size: 0.875rem; color: var(--muted-grey); line-height: 1.5; }}

    /* Sidebar */
    .sidebar-widget {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }}
    .widget-title {{
      font-size: 1rem;
      font-weight: 800;
      color: var(--off-white);
      margin-bottom: 1.25rem;
      border-bottom: 1px solid var(--charcoal-border);
      padding-bottom: 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .related-card {{
      margin-bottom: 1.25rem;
      display: flex;
      gap: 0.875rem;
      padding: 8px;
      border-radius: 8px;
      transition: background 0.2s, transform 0.2s;
    }}
    .related-card:hover {{
      background: rgba(255, 255, 255, 0.04);
      transform: translateX(2px);
    }}
    .related-thumb-link {{
      position: relative;
      width: 120px;
      height: 68px;
      flex-shrink: 0;
      border-radius: 6px;
      overflow: hidden;
      background: #000;
      display: block;
    }}
    .related-thumb-link img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .related-sport-pill {{
      position: absolute;
      top: 4px;
      left: 4px;
      background: rgba(0, 0, 0, 0.85);
      color: var(--neon-lime);
      font-size: 0.625rem;
      font-weight: 800;
      padding: 1px 4px;
      border-radius: 2px;
    }}
    .related-info {{ flex: 1; min-width: 0; }}
    .related-meta {{ font-size: 0.6875rem; color: var(--dark-grey); display: block; }}
    .related-title {{
      font-size: 0.8125rem;
      font-weight: 600;
      line-height: 1.35;
      margin-top: 0.2rem;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .related-title a {{ color: var(--off-white); }}
    .related-title a:hover {{ color: var(--neon-lime); text-decoration: none; }}
    .related-action-link {{
      font-size: 0.6875rem;
      font-weight: 700;
      color: var(--neon-lime);
      display: inline-block;
      margin-top: 4px;
    }}

    .catalog-cta-card {{
      background: linear-gradient(135deg, #151515 0%, #222222 100%);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      padding: 1.5rem;
      text-align: center;
    }}
    .catalog-cta-card h3 {{
      font-size: 1.125rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
      color: var(--off-white);
    }}
    .catalog-cta-card p {{
      font-size: 0.875rem;
      color: var(--muted-grey);
      margin-bottom: 1.25rem;
    }}

    /* Footer */
    .site-footer {{
      border-top: 1px solid var(--charcoal-border);
      background: var(--pitch-black);
      padding: 2.5rem 1.5rem;
      color: var(--dark-grey);
      font-size: 0.875rem;
    }}
    .footer-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .footer-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .footer-links a {{ color: var(--muted-grey); }}
    .footer-links a:hover {{ color: var(--neon-lime); }}

    @media (max-width: 900px) {{
      .page-layout {{ grid-template-columns: 1fr; }}
      .article-h1 {{ font-size: 1.5rem; }}
      .main-nav {{ display: none; }}
      .mobile-toggle {{ display: block; }}
      .breadcrumb-current {{ max-width: 250px; }}
    }}
  </style>
</head>
<body>

  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KFC9JGQJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {render_navbar(active_page=sport)}

  <!-- Breadcrumbs -->
  <nav class="breadcrumb-bar" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span class="breadcrumb-sep">&gt;</span>
    <a href="{sport_hub_url}">{sport_name}</a>
    <span class="breadcrumb-sep">&gt;</span>
    <span class="breadcrumb-current">{video['title']}</span>
  </nav>

  <!-- Back Link -->
  <div class="back-link-bar">
    <a href="{sport_hub_url}" class="back-link">
      &larr; Back to {sport_name} Match Analysis Hub
    </a>
  </div>

  <!-- Main Content Layout -->
  <main class="page-layout">
    <article>
      <!-- Video Player Hero Box -->
      <section class="video-hero">
        <div class="video-aspect-frame">
          <iframe 
            src="https://www.youtube.com/embed/{vid}?rel=0" 
            title="{video['title']}" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
            allowfullscreen 
            loading="lazy"
          ></iframe>
        </div>

        <div class="video-meta-bar">
          <div class="meta-pills">
            <span class="sport-pill">{video['sport'].upper()}</span>
            <span class="playlist-pill">{video['playlist']}</span>
            <span class="views-pill">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              {video['views']}
            </span>
            <span style="font-size: 0.8125rem; color: var(--dark-grey);">· {video['read_time']}</span>
          </div>

          <h1 class="article-h1" lang="ml">{video['title']}</h1>

          <div class="cta-row">
            <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener noreferrer" class="btn btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" aria-hidden="true">
                <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"/>
              </svg>
              Watch on YouTube ↗
            </a>
            <a href="{sport_hub_url}" class="btn btn-outline">
              &larr; Back to {sport_name}
            </a>
          </div>
        </div>
      </section>

      <!-- Tactical Editorial Breakdown -->
      <section class="editorial-content">
        {badge_html}
        <h2>{section_h2}</h2>
        <p lang="ml">{video['p1_ml']}</p>
        <p>{video['p2_en']}</p>

        <!-- Key Takeaways Box -->
        <div class="takeaways-box">
          <h3>{takeaways_title}</h3>
          <ul>{takeaways_html}</ul>
        </div>

        <div class="tags-row">
          {tags_html}
        </div>

        <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--charcoal-border);">
          <a href="{sport_hub_url}" class="btn btn-outline">
            &larr; Back to All {sport_name} Videos
          </a>
        </div>
      </section>

      <!-- Author Attribution Card -->
      <section class="author-card">
        <picture>
          <source srcset="/assets/images/haris-opt.webp" type="image/webp">
          <img src="/assets/images/haris-hero-portrait.png" alt="Haris Nenmara" class="author-img" width="72" height="72" loading="lazy">
        </picture>
        <div class="author-info">
          <h4>Analyzed by Haris Nenmara (ഹാരിസ് നെന്മാറ)</h4>
          <p class="author-role">Sports Journalist &amp; Tactical Analyst · Final Third</p>
          <p class="author-bio">Covering European football tactical systems, Kerala Blasters matchday dynamics in the ISL, and international cricket analysis in Malayalam.</p>
        </div>
      </section>
    </article>

    <!-- Sidebar Widget -->
    <aside>
      <div class="sidebar-widget">
        <h3 class="widget-title">
          <span>Related {video['sport'].capitalize()} Stories</span>
          <span style="font-size: 0.75rem; color: var(--neon-lime); font-weight: 700;">FINAL THIRD</span>
        </h3>
        {related_cards_html}
      </div>

      <div class="catalog-cta-card">
        <h3>300+ Video Analysis Archive</h3>
        <p>Explore our complete searchable catalog of football and cricket tactical breakdowns, player stories, and match debriefs.</p>
        <a href="/#videos" class="btn btn-primary" style="width: 100%; justify-content: center;">Browse Full Catalog →</a>
      </div>
    </aside>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="footer-container">
      <p>&copy; 2026 FINAL THIRD with Haris Nenmara. All rights reserved.</p>
      <ul class="footer-links">
        <li><a href="/">Home</a></li>
        <li><a href="/football/">Football Hub</a></li>
        <li><a href="/cricket/">Cricket Hub</a></li>
        <li><a href="/privacy.html">Privacy Policy</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </div>
  </footer>

  <script>
    // Mobile Drawer Toggle
    const mobileBtn = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    if (mobileBtn && mobileDrawer) {{
      mobileBtn.addEventListener('click', function() {{
        const isOpen = mobileDrawer.classList.toggle('open');
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }});
    }}
  </script>

</body>
</html>
"""
    return html

# Render category hub listing page
def render_category_hub(sport):
    sport_name = "Football" if sport == "football" else "Cricket"
    other_sport = "cricket" if sport == "football" else "football"
    other_sport_name = "Cricket" if sport == "football" else "Football"
    sport_ml = "ഫുട്ബോൾ അവലോകനങ്ങൾ" if sport == "football" else "ക്രിക്കറ്റ് അവലോകനങ്ങൾ"
    meta_desc = (
        "Kerala's premier Malayalam football tactical analysis platform by Haris Nenmara. In-depth match debriefs, El Clasico, European leagues, and Kerala Blasters ISL breakdowns."
        if sport == "football" else
        "Malayalam cricket match analysis, tactical breakdowns, and player stories by Haris Nenmara. In-depth coverage of Sanju Samson, Jasprit Bumrah, Team India T20s, and World Cup moments."
    )

    vids = [v for v in VIDEOS if v["sport"] == sport]
    
    cards_html = ""
    for v in vids:
        page_url = f"/{sport}/{v['slug']}/"
        cov = v.get("coverage", "complete" if v.get("transcript_available") else "missing")
        if cov == "complete" or (v.get("transcript_available") and cov != "partial"):
            tag_cls = "hub-card-verified-tag"
            tag_lbl = "✓ Verified Transcript"
        elif cov == "partial":
            tag_cls = "hub-card-partial-tag"
            tag_lbl = "ℹ Excerpt Grounded"
        else:
            tag_cls = "hub-card-awaiting-tag"
            tag_lbl = "⏳ Awaiting Transcript"

        cards_html += f"""
        <article class="hub-card" onclick="window.location.href='{page_url}'" style="cursor: pointer;">
          <a href="{page_url}" class="hub-card-thumb-link" aria-label="{v['title']}">
            <img src="https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg" alt="{v['title']}" width="480" height="270" loading="lazy" decoding="async">
            <span class="hub-card-badge">{v['playlist']}</span>
            <span class="hub-card-views">{v['views']}</span>
            <div class="hub-play-overlay" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            </div>
          </a>
          <div class="hub-card-body">
            <div class="hub-card-meta">
              <span class="hub-card-time">{v['published_iso'][:10]}</span>
              <span class="hub-card-dot">·</span>
              <span class="hub-card-read">{v['read_time']}</span>
              <span class="hub-card-dot">·</span>
              <span class="{tag_cls}">{tag_lbl}</span>
            </div>
            <h2 class="hub-card-title"><a href="{page_url}">{v['title']}</a></h2>
            <p class="hub-card-snippet">{v['meta_desc']}</p>
            <div class="hub-card-footer">
              <a href="{page_url}" class="hub-card-btn">
                Read Tactical Breakdown &amp; Watch Video ↗
              </a>
            </div>
          </div>
        </article>"""

    hub_url = f"{DOMAIN}/{sport}/"

    html = f"""<!DOCTYPE html>
<html lang="en" xml:lang="ml" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sport_name} Match Analysis &amp; Tactical Debriefs | Final Third with Haris Nenmara</title>
  <meta name="description" content="{meta_desc}">
  <meta name="author" content="Haris Nenmara (ഹാരിസ് നെന്മാറ)">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{hub_url}">

  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">

  <!-- Open Graph -->
  <meta property="og:site_name" content="Final Third with Haris Nenmara">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{hub_url}">
  <meta property="og:title" content="{sport_name} Tactical Analysis | Final Third">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{DOMAIN}/assets/images/og-image.jpg">

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{sport_name} Tactical Analysis | Final Third">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{DOMAIN}/assets/images/og-image.jpg">

  <!-- Tracking -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-KFC9JGQJ');</script>

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5399554232098923" crossorigin="anonymous"></script>

  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "{hub_url}#collection",
        "url": "{hub_url}",
        "name": "{sport_name} Match Analysis | Final Third",
        "description": {json.dumps(meta_desc, ensure_ascii=False)},
        "isPartOf": {{
          "@id": "{DOMAIN}/#website"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "{hub_url}#breadcrumb",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "{DOMAIN}/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "{sport_name} Analysis",
            "item": "{hub_url}"
          }}
        ]
      }}
    ]
  }}
  </script>

  <style>
    :root {{
      --neon-lime: #9EE20B;
      --neon-lime-hover: #b4f51e;
      --pitch-black: #080808;
      --charcoal: #151515;
      --charcoal-light: #202020;
      --charcoal-border: #2a2a2a;
      --off-white: #F5F5F0;
      --muted-grey: #a0a0a0;
      --dark-grey: #666666;
      --font-primary: 'Anek Malayalam', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--pitch-black);
      color: var(--off-white);
      font-family: var(--font-primary);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }}
    a {{ color: var(--neon-lime); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* Header & Navigation */
    .site-header {{
      border-bottom: 1px solid var(--charcoal-border);
      background: rgba(8, 8, 8, 0.95);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 0.875rem 1.5rem;
      backdrop-filter: blur(10px);
    }}
    .nav-container {{ max-width: 1140px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }}
    .brand-link {{ display: flex; align-items: center; gap: 0.75rem; color: var(--off-white); font-weight: 800; font-size: 1.125rem; }}
    .brand-logo {{ height: 36px; width: auto; display: block; }}
    .brand-name {{ font-weight: 800; color: var(--off-white); }}
    .main-nav {{ display: flex; align-items: center; }}
    .nav-list {{ display: flex; align-items: center; gap: 1.5rem; list-style: none; }}
    .nav-link {{ color: var(--muted-grey); font-weight: 600; font-size: 0.875rem; transition: color 0.2s; }}
    .nav-link:hover, .nav-link.active {{ color: var(--neon-lime); text-decoration: none; }}
    .nav-actions {{ display: flex; align-items: center; gap: 1rem; }}
    .btn-subscribe {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 1rem;
      background: var(--neon-lime);
      color: #000;
      font-weight: 800;
      font-size: 0.8125rem;
      border-radius: 6px;
      text-decoration: none;
      transition: background-color 0.2s;
    }}
    .btn-subscribe:hover {{ background: var(--neon-lime-hover); text-decoration: none; }}
    .mobile-toggle {{
      display: none;
      background: none;
      border: none;
      color: var(--off-white);
      cursor: pointer;
    }}
    .mobile-drawer {{
      display: none;
      background: var(--charcoal);
      border-bottom: 1px solid var(--charcoal-border);
      padding: 1.5rem;
    }}
    .mobile-drawer.open {{ display: block; }}
    .drawer-list {{ list-style: none; display: flex; flex-direction: column; gap: 1rem; }}
    .drawer-link {{ color: var(--off-white); font-weight: 600; font-size: 1rem; text-decoration: none; }}
    .drawer-link.active {{ color: var(--neon-lime); }}

    /* Hub Hero */
    .hub-hero {{
      max-width: 1140px;
      margin: 1.5rem auto 0;
      padding: 2rem 1.5rem;
      border-bottom: 1px solid var(--charcoal-border);
    }}
    .hub-eyebrow {{
      color: var(--neon-lime);
      font-size: 0.8125rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 0.5rem;
    }}
    .hub-title {{
      font-size: 2.25rem;
      font-weight: 800;
      color: var(--off-white);
      line-height: 1.2;
      margin-bottom: 0.75rem;
    }}
    .hub-lead {{
      font-size: 1.0625rem;
      color: var(--muted-grey);
      max-width: 820px;
      line-height: 1.7;
      margin-bottom: 1.5rem;
    }}

    /* Sport Switcher Chips */
    .hub-switcher {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .switch-chip {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 999px;
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--off-white);
      text-decoration: none;
      transition: all 0.2s;
    }}
    .switch-chip:hover, .switch-chip.active {{
      background: rgba(158, 226, 11, 0.12);
      border-color: var(--neon-lime);
      color: var(--neon-lime);
      text-decoration: none;
    }}
    .switch-count {{
      background: rgba(255, 255, 255, 0.1);
      padding: 2px 6px;
      border-radius: 999px;
      font-size: 0.6875rem;
    }}
    .switch-chip.active .switch-count {{
      background: var(--neon-lime);
      color: #000;
    }}

    /* Hub Grid */
    .hub-grid {{
      max-width: 1140px;
      margin: 2rem auto 5rem;
      padding: 0 1.5rem;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(330px, 1fr));
      gap: 1.75rem;
    }}

    .hub-card {{
      background: var(--charcoal);
      border: 1px solid var(--charcoal-border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    }}
    .hub-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(158, 226, 11, 0.5);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6);
    }}

    .hub-card-thumb-link {{
      position: relative;
      width: 100%;
      padding-top: 56.25%;
      display: block;
      background: #000;
      overflow: hidden;
    }}
    .hub-card-thumb-link img {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
    }}
    .hub-card:hover .hub-card-thumb-link img {{
      transform: scale(1.03);
    }}
    .hub-card-badge {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(0, 0, 0, 0.85);
      color: var(--neon-lime);
      font-size: 0.6875rem;
      font-weight: 800;
      padding: 3px 6px;
      border-radius: 4px;
      z-index: 2;
    }}
    .hub-card-views {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.85);
      color: #fff;
      font-size: 0.6875rem;
      font-weight: 600;
      padding: 3px 6px;
      border-radius: 4px;
      z-index: 2;
    }}
    .hub-play-overlay {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 48px;
      height: 48px;
      background: rgba(0, 0, 0, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--neon-lime);
      opacity: 0.85;
      transition: all 0.2s;
      z-index: 2;
    }}
    .hub-card:hover .hub-play-overlay {{
      background: var(--neon-lime);
      color: #000;
      opacity: 1;
      transform: translate(-50%, -50%) scale(1.1);
    }}

    .hub-card-body {{ padding: 1.25rem; flex: 1; display: flex; flex-direction: column; }}
    .hub-card-meta {{
      font-size: 0.75rem;
      color: var(--dark-grey);
      margin-bottom: 0.4rem;
      display: flex;
      gap: 6px;
      align-items: center;
    }}
    .hub-card-dot {{ color: var(--dark-grey); }}
    .hub-card-read {{ color: var(--neon-lime); font-weight: 600; }}
    .hub-card-verified-tag {{ color: var(--neon-lime); font-size: 0.6875rem; font-weight: 700; display: inline-flex; align-items: center; gap: 3px; }}
    .hub-card-partial-tag {{ color: #60a5fa; font-size: 0.6875rem; font-weight: 700; display: inline-flex; align-items: center; gap: 3px; }}
    .hub-card-awaiting-tag {{ color: #E5A93C; font-size: 0.6875rem; font-weight: 700; display: inline-flex; align-items: center; gap: 3px; }}
    .hub-card-title {{
      font-size: 1.0625rem;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 0.625rem;
    }}
    .hub-card-title a {{ color: var(--off-white); }}
    .hub-card-title a:hover {{ color: var(--neon-lime); text-decoration: none; }}
    .hub-card-snippet {{
      font-size: 0.8125rem;
      color: var(--muted-grey);
      line-height: 1.55;
      margin-bottom: 1.25rem;
      flex: 1;
    }}
    .hub-card-footer {{
      margin-top: auto;
      padding-top: 0.75rem;
      border-top: 1px solid var(--charcoal-border);
    }}
    .hub-card-btn {{
      font-size: 0.8125rem;
      font-weight: 700;
      color: var(--neon-lime);
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: opacity 0.2s;
    }}
    .hub-card-btn:hover {{
      text-decoration: underline;
      opacity: 0.85;
    }}

    .site-footer {{
      border-top: 1px solid var(--charcoal-border);
      background: var(--pitch-black);
      padding: 2.5rem 1.5rem;
      color: var(--dark-grey);
      font-size: 0.875rem;
    }}
    .footer-container {{
      max-width: 1140px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 1rem;
    }}
    .footer-links {{ display: flex; gap: 1.5rem; list-style: none; }}
    .footer-links a {{ color: var(--muted-grey); }}
    .footer-links a:hover {{ color: var(--neon-lime); }}

    @media (max-width: 900px) {{
      .main-nav {{ display: none; }}
      .mobile-toggle {{ display: block; }}
      .hub-grid {{ grid-template-columns: 1fr; }}
      .hub-title {{ font-size: 1.75rem; }}
    }}
  </style>
</head>
<body>

  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KFC9JGQJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  {render_navbar(active_page=sport)}

  <header class="hub-hero">
    <div class="hub-eyebrow">Category Listing · {sport_ml}</div>
    <h1 class="hub-title">{sport_name} Match Analysis &amp; Tactical Debriefs</h1>
    <p class="hub-lead">{meta_desc}</p>
    <div class="hub-switcher">
      <span style="font-size: 0.8125rem; color: var(--muted-grey); font-weight: 600;">Explore Categories:</span>
      <a href="/football/" class="switch-chip{' active' if sport == 'football' else ''}">
        ⚽ Football Analysis <span class="switch-count">{len([v for v in VIDEOS if v.get('sport') == 'football'])}</span>
      </a>
      <a href="/cricket/" class="switch-chip{' active' if sport == 'cricket' else ''}">
        🏏 Cricket Analysis <span class="switch-count">{len([v for v in VIDEOS if v.get('sport') == 'cricket'])}</span>
      </a>
      <a href="/#videos" class="switch-chip">
        📺 Full 300+ Archive <span class="switch-count">All</span>
      </a>
    </div>
  </header>

  <main class="hub-grid">
    {cards_html}
  </main>

  <footer class="site-footer">
    <div class="footer-container">
      <p>&copy; 2026 FINAL THIRD with Haris Nenmara. All rights reserved.</p>
      <ul class="footer-links">
        <li><a href="/">Home</a></li>
        <li><a href="/football/">Football Hub</a></li>
        <li><a href="/cricket/">Cricket Hub</a></li>
        <li><a href="/privacy.html">Privacy Policy</a></li>
        <li><a href="/#contact">Contact</a></li>
      </ul>
    </div>
  </footer>

  <script>
    // Mobile Drawer Toggle
    const mobileBtn = document.getElementById('mobileMenuToggle');
    const mobileDrawer = document.getElementById('mobileDrawer');
    if (mobileBtn && mobileDrawer) {{
      mobileBtn.addEventListener('click', function() {{
        const isOpen = mobileDrawer.classList.toggle('open');
        mobileBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }});
    }}
  </script>

</body>
</html>
"""
    return html

def generate_all():
    global VIDEOS
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pipeline_file = os.path.join(base_dir, "data/content_pipeline.json")
    if os.path.exists(pipeline_file):
        with open(pipeline_file, "r", encoding="utf-8") as pf:
            pipe_data = json.load(pf)
        # Dynamically filter to include all published, excerpt, or active pipeline articles
        # (Excludes records strictly in awaiting_captions retry queue without published content)
        VIDEOS = [v for v in pipe_data.values() if v.get("status") in ("published", "published_partial", "excerpt", "awaiting_transcript")]

    print("=" * 60)
    print("Final Third — Generating Dedicated Video Pages & Hubs")
    print(f"Total eligible dedicated SEO pages: {len(VIDEOS)}")
    print("=" * 60)

    # 1. Create Football & Cricket Hub Directories
    for sport in ["football", "cricket"]:
        sport_dir = os.path.join(base_dir, sport)
        os.makedirs(sport_dir, exist_ok=True)
        hub_html = render_category_hub(sport)
        with open(os.path.join(sport_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(hub_html)
        print(f"✓ Created /{sport}/ hub index.html")

    # 2. Create the Dedicated Video Pages
    created_pages = []
    for v in VIDEOS:
        page_dir = os.path.join(base_dir, v["sport"], v["slug"])
        os.makedirs(page_dir, exist_ok=True)
        page_html = render_page(v)
        file_path = os.path.join(page_dir, "index.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(page_html)
        created_pages.append(f"/{v['sport']}/{v['slug']}/")
        print(f"  ⚡ [{v['sport'].upper()}] /{v['sport']}/{v['slug']}/")

    print(f"\n✓ Successfully created {len(created_pages)} dedicated video pages!")

    # 3. Generate Updated sitemap.xml with Video Extensions
    sitemap_path = os.path.join(base_dir, "sitemap.xml")
    sitemap_entries = [
        f"""  <url>
    <loc>{DOMAIN}/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/football/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/cricket/</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>""",
        f"""  <url>
    <loc>{DOMAIN}/privacy.html</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>"""
    ]

    for v in VIDEOS:
        vid_url = f"{DOMAIN}/{v['sport']}/{v['slug']}/"
        thumb_url = f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"
        clean_title = v["title"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        clean_desc = v["meta_desc"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        
        sitemap_entries.append(f"""  <url>
    <loc>{vid_url}</loc>
    <lastmod>2026-10-30</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <video:video>
      <video:thumbnail_loc>{thumb_url}</video:thumbnail_loc>
      <video:title>{clean_title}</video:title>
      <video:description>{clean_desc}</video:description>
      <video:player_loc>https://www.youtube.com/embed/{v['id']}</video:player_loc>
      <video:publication_date>{v['published_iso']}</video:publication_date>
      <video:family_friendly>yes</video:family_friendly>
    </video:video>
  </url>""")

    full_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
{chr(10).join(sitemap_entries)}
</urlset>
"""
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(full_sitemap)
    print(f"✓ Successfully generated sitemap.xml with {len(sitemap_entries)} entries (including {len(VIDEOS)} video extensions)!")

if __name__ == "__main__":
    generate_all()
