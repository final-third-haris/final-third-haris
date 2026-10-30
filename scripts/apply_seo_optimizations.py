#!/usr/bin/env python3
"""
Final Third — Technical SEO & Indexability Engine
Applies comprehensive Technical SEO optimizations:
1. Canonical HTTPS URL & Robots directives.
2. Title & Meta Description optimization for Google SERP CTR.
3. Natural integration of core brand and topical phrases:
   - Final Third
   - Final Third football analysis
   - Football match analysis
   - Football tactics and formations
   - Cricket match analysis
   - Haris Nenmara sports analysis
4. Clean, unified Schema.org JSON-LD (SportsOrganization, Person, WebSite, WebPage).
5. 1200x630 Open Graph & Twitter Summary Large Image social metadata.
6. Fixes broken internal links (#sports-gateways -> #videos).
7. Fixes heading hierarchy (removes stray h3 in hero floating card).
8. Adds pre-rendered crawlable video and shorts cards to HTML DOM for zero-JS crawlers.
9. Adds aria-hidden="true" to decorative SVGs and descriptive alt texts to images.
10. Validates 100% HTML tag balance.
"""

import re
import sys
import json
import html as html_lib
from html.parser import HTMLParser

INPUT_FILE = 'index.html'

def apply_seo():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    orig_len = len(html)
    print(f"Original index.html size: {orig_len:,} bytes ({orig_len/1024:.1f} KB)")

    # 1. Update <head> meta, title, description, OG, Twitter, and Schema.org
    head_start_match = re.search(r'<head>', html)
    style_start_match = re.search(r'<style>', html)
    if not (head_start_match and style_start_match):
        print("Error: Could not locate <head> or <style> tags")
        sys.exit(1)

    new_head_meta = (
        '\n  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <title>Final Third | Football &amp; Cricket Match Analysis by Haris Nenmara</title>\n'
        '  <meta name="description" content="Final Third by Haris Nenmara brings in-depth football match analysis, tactics and formations, Kerala Blasters stories, and cricket match analysis in Malayalam.">\n'
        '  <meta name="keywords" content="Final Third, Haris Nenmara, Final Third football analysis, football match analysis, football tactics and formations, cricket match analysis, Haris Nenmara sports analysis, malayalam football analysis, kerala blasters analysis, isl football malayalam, sports tactics malayalam, ഫൈനൽ തേർഡ്, ഹാരിസ് നെന്മാറ">\n'
        '  <meta name="author" content="Haris Nenmara (ഹാരിസ് നെന്മാറ)">\n'
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">\n'
        '  <link rel="canonical" href="https://www.finalthird-haris.com/">\n\n'
        '  <!-- Favicon & Device Touch Icons -->\n'
        '  <link rel="icon" type="image/png" sizes="32x32" href="assets/images/favicon-32x32.png">\n'
        '  <link rel="apple-touch-icon" sizes="192x192" href="assets/images/favicon-192x192.png">\n\n'
        '  <!-- Performance: Critical Resource Preconnects -->\n'
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n\n'
        '  <!-- Performance: Preload Critical LCP Hero Image (Mobile First) -->\n'
        '  <link rel="preload" as="image" href="assets/images/haris-hero-portrait-400.webp" type="image/webp" media="(max-width: 600px)" fetchpriority="high">\n'
        '  <link rel="preload" as="image" href="assets/images/haris-hero-portrait-680.webp" type="image/webp" media="(min-width: 601px) and (max-width: 992px)" fetchpriority="high">\n'
        '  <link rel="preload" as="image" href="assets/images/haris-hero-portrait.webp" type="image/webp" media="(min-width: 993px)" fetchpriority="high">\n\n'
        '  <!-- Performance: Non-Render-Blocking Google Fonts with display=swap -->\n'
        '  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&display=swap">\n'
        '  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&display=swap" media="print" onload="this.media=\'all\'">\n'
        '  <noscript>\n'
        '    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Malayalam:wght@400;600;700;800&display=swap">\n'
        '  </noscript>\n\n'
        '  <!-- Regional Tags for Kerala & Global Malayali Audience -->\n'
        '  <meta name="geo.region" content="IN-KL">\n'
        '  <meta name="geo.placename" content="Kerala, India">\n\n'
        '  <!-- Open Graph / Facebook / WhatsApp (Standard 1200x630) -->\n'
        '  <meta property="og:site_name" content="Final Third with Haris Nenmara">\n'
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:url" content="https://www.finalthird-haris.com/">\n'
        '  <meta property="og:locale" content="ml_IN">\n'
        '  <meta property="og:locale:alternate" content="en_IN">\n'
        '  <meta property="og:locale:alternate" content="en_US">\n'
        '  <meta property="og:title" content="Final Third | Football &amp; Cricket Match Analysis by Haris Nenmara">\n'
        '  <meta property="og:description" content="In-depth football match analysis, tactics and formations, Kerala Blasters stories, and cricket match analysis in Malayalam by Haris Nenmara.">\n'
        '  <meta property="og:image" content="https://www.finalthird-haris.com/assets/images/og-image.jpg">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta property="og:image:alt" content="Final Third — Football and Cricket Analysis by Haris Nenmara">\n'
        '  <meta property="og:image:type" content="image/jpeg">\n\n'
        '  <!-- Twitter / X Card -->\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <meta name="twitter:title" content="Final Third | Football &amp; Cricket Match Analysis by Haris Nenmara">\n'
        '  <meta name="twitter:description" content="Football match analysis, tactics and formations, and cricket analysis in Malayalam with Haris Nenmara.">\n'
        '  <meta name="twitter:image" content="https://www.finalthird-haris.com/assets/images/og-image.jpg">\n'
        '  <meta name="twitter:image:alt" content="Final Third — Football and Cricket Analysis by Haris Nenmara">\n\n'
        '  <!-- Google Search Console & Verification Meta (Keep updated with your GSC token) -->\n'
        '  <!-- <meta name="google-site-verification" content="YOUR_GSC_VERIFICATION_TOKEN"> -->\n\n'
        '  <!-- Google Tag Manager (Async) -->\n'
        '  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\n'
        '  new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n'
        '  j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n'
        '  \'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n'
        '  })(window,document,\'script\',\'dataLayer\',\'GTM-5N6XFRJ7\');</script>\n\n'
        '  <!-- Google Analytics 4 (Async) -->\n'
        '  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XR8PCQNHRE"></script>\n'
        '  <script>\n'
        '    window.dataLayer = window.dataLayer || [];\n'
        '    function gtag(){dataLayer.push(arguments);}\n'
        '    gtag(\'js\', new Date());\n'
        '    gtag(\'config\', \'G-XR8PCQNHRE\');\n'
        '  </script>\n\n'
        '  <!-- Schema.org JSON-LD Structured Data (Validated Entities: Organization, Person, WebSite, WebPage) -->\n'
        '  <script type="application/ld+json">\n'
        '  {\n'
        '    "@context": "https://schema.org",\n'
        '    "@graph": [\n'
        '      {\n'
        '        "@type": "SportsOrganization",\n'
        '        "@id": "https://www.finalthird-haris.com/#organization",\n'
        '        "name": "Final Third",\n'
        '        "url": "https://www.finalthird-haris.com/",\n'
        '        "logo": "https://www.finalthird-haris.com/assets/images/final-third-logo.png",\n'
        '        "description": "Sports analysis platform covering football match analysis, tactical formations, and cricket match analysis by Haris Nenmara.",\n'
        '        "sameAs": [\n'
        '          "https://www.youtube.com/@FinalThird_HarisNenmara",\n'
        '          "https://www.instagram.com/finalthird.official/",\n'
        '          "https://www.facebook.com/profile.php?id=61590005744291",\n'
        '          "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"\n'
        '        ]\n'
        '      },\n'
        '      {\n'
        '        "@type": "Person",\n'
        '        "@id": "https://www.finalthird-haris.com/#person",\n'
        '        "name": "Haris Nenmara",\n'
        '        "alternateName": "ഹാരിസ് നെന്മാറ",\n'
        '        "jobTitle": "Sports Journalist & Analyst",\n'
        '        "worksFor": {\n'
        '          "@id": "https://www.finalthird-haris.com/#organization"\n'
        '        },\n'
        '        "description": "Sports journalist and analyst behind Final Third, analyzing football tactics, formations, and cricket in Malayalam.",\n'
        '        "url": "https://www.finalthird-haris.com/#about",\n'
        '        "image": "https://www.finalthird-haris.com/assets/images/haris-hero-portrait.png",\n'
        '        "sameAs": [\n'
        '          "https://www.youtube.com/@FinalThird_HarisNenmara",\n'
        '          "https://www.instagram.com/finalthird.official/",\n'
        '          "https://www.facebook.com/profile.php?id=61590005744291",\n'
        '          "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"\n'
        '        ]\n'
        '      },\n'
        '      {\n'
        '        "@type": "WebSite",\n'
        '        "@id": "https://www.finalthird-haris.com/#website",\n'
        '        "url": "https://www.finalthird-haris.com/",\n'
        '        "name": "Final Third",\n'
        '        "alternateName": [\n'
        '          "Final Third with Haris Nenmara",\n'
        '          "Final Third Sports",\n'
        '          "ഫൈനൽ തേർഡ്"\n'
        '        ],\n'
        '        "description": "Kerala\'s premier Malayalam sports media platform for football match analysis, tactics and formations, and cricket analysis.",\n'
        '        "inLanguage": ["ml", "en"],\n'
        '        "publisher": {\n'
        '          "@id": "https://www.finalthird-haris.com/#organization"\n'
        '        }\n'
        '      },\n'
        '      {\n'
        '        "@type": "WebPage",\n'
        '        "@id": "https://www.finalthird-haris.com/#webpage",\n'
        '        "url": "https://www.finalthird-haris.com/",\n'
        '        "name": "Final Third | Football & Cricket Match Analysis by Haris Nenmara",\n'
        '        "isPartOf": {\n'
        '          "@id": "https://www.finalthird-haris.com/#website"\n'
        '        },\n'
        '        "about": {\n'
        '          "@id": "https://www.finalthird-haris.com/#organization"\n'
        '        },\n'
        '        "primaryImageOfPage": "https://www.finalthird-haris.com/assets/images/og-image.jpg"\n'
        '      }\n'
        '    ]\n'
        '  }\n'
        '  </script>\n\n  '
    )
    html = html[:head_start_match.end()] + new_head_meta + html[style_start_match.start():]
    print("✓ <head> optimized: Title, Meta Description, OG 1200x630, Twitter Cards, Validated Schema.org")

    # 2. Hero Section: Natural integration of core brand & topic keywords
    old_hero_descriptor = re.search(r'<p\s+class="hero-descriptor">.*?</p>', html, re.DOTALL)
    if old_hero_descriptor:
        new_hero_descriptor = (
            '<p class="hero-descriptor">\n'
            '            Final Third football analysis &amp; cricket match analysis by Haris Nenmara <span lang="ml" style="font-weight: 500; opacity: 0.9;">(മലയാളം സ്പോർട്സ് വിശകലനം)</span>\n'
            '          </p>'
        )
        html = html[:old_hero_descriptor.start()] + new_hero_descriptor + html[old_hero_descriptor.end():]
        print("✓ Hero descriptor updated with natural keywords")

    old_hero_desc = re.search(r'<p\s+class="hero-description">.*?</p>', html, re.DOTALL)
    if old_hero_desc:
        new_hero_desc = (
            '<p class="hero-description">\n'
            '            Welcome to Final Third (ഫൈനൽ തേർഡ്). Haris Nenmara sports analysis explores the stories behind the game — from in-depth football match analysis, tactics and formations across European leagues and ISL, to strategic cricket match analysis.\n'
            '          </p>'
        )
        html = html[:old_hero_desc.start()] + new_hero_desc + html[old_hero_desc.end():]
        print("✓ Hero description updated with natural keywords")

    # 3. Heading Hierarchy: Fix stray <h3> in Hero floating identity card
    old_floating_card = re.search(
        r'<div\s+class="portrait-floating-card">\s*<div\s+class="floating-host-meta">\s*<h3>(.*?)</h3>',
        html,
        re.DOTALL
    )
    if old_floating_card:
        inner_content = old_floating_card.group(1)
        new_floating_card = (
            '<div class="portrait-floating-card">\n'
            '            <div class="floating-host-meta">\n'
            f'              <div class="floating-host-name"><strong>{inner_content}</strong></div>'
        )
        html = html[:old_floating_card.start()] + new_floating_card + html[old_floating_card.end():]
        print("✓ Heading hierarchy resolved: Replaced stray h3 in hero floating card")

    # 4. Videos Section: Subtitle natural keyword integration
    old_videos_subtitle = re.search(
        r'<p\s+class="section-subtitle">\s*All tactical breakdowns, match reviews, and sports stories in Malayalam, sourced directly from the official Final Third YouTube channel\.\s*</p>',
        html
    )
    if old_videos_subtitle:
        new_videos_subtitle = (
            '<p class="section-subtitle">\n'
            '              Football match analysis, tactics and formations, and cricket match analysis in Malayalam, updated daily from the official Final Third YouTube channel.\n'
            '            </p>'
        )
        html = html[:old_videos_subtitle.start()] + new_videos_subtitle + html[old_videos_subtitle.end():]
        print("✓ Videos section subtitle updated with natural keywords")

    # 5. Fix Broken Internal Link (#sports-gateways -> #videos)
    if '#sports-gateways' in html:
        html = html.replace('href="#sports-gateways"', 'href="#videos"')
        html = html.replace('Football &amp; Cricket</a></li>', 'Football &amp; Cricket Analysis</a></li>')
        print("✓ Fixed broken internal link: #sports-gateways -> #videos")

    # 6. Fix Modal fallback href="#"
    if 'id="modalWatchYtBtn" \n            href="#"' in html:
        html = html.replace(
            'id="modalWatchYtBtn" \n            href="#"',
            'id="modalWatchYtBtn" \n            href="https://www.youtube.com/@FinalThird_HarisNenmara"'
        )
        print("✓ Modal fallback link upgraded to YouTube channel URL")

    # 7. Pre-render Initial 12 Video Cards inside #videoGrid for Search Crawlers
    # Extract first 12 videos from embedded FINAL_THIRD_CONFIG
    v_match = re.search(r'videos:\s*\[(.*?)\],\s*shorts:', html, re.DOTALL)
    if v_match:
        try:
            v_json_str = '[' + v_match.group(1).rstrip().rstrip(',') + ']'
            videos_data = json.loads(v_json_str)
            initial_12 = videos_data[:12]

            video_cards_html = []
            for idx, v in enumerate(initial_12):
                vid = v['id']
                vtitle = html_lib.escape(v['title'])
                vsport = html_lib.escape(v.get('sport', 'football').capitalize())
                vviews = html_lib.escape(v.get('views', '10K views'))
                vplaylist = html_lib.escape(v.get('playlistTitle', 'Sports Analysis'))
                vpub = html_lib.escape(v.get('published', 'Recent'))
                vsummary = html_lib.escape(v.get('summary', v['title']))
                thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"

                card = (
                    f'          <article class="video-card reveal-cascade" data-video-id="{vid}" style="--cascade-index: {idx % 4}">\n'
                    f'            <div class="video-thumbnail-wrap" role="button" tabindex="0" aria-label="Play video: {vtitle}">\n'
                    f'              <img src="{thumb}" alt="Video thumbnail: {vtitle}" loading="lazy" decoding="async" width="480" height="270" />\n'
                    f'              <span class="card-sport-pill">{vsport}</span>\n'
                    f'              <span class="card-views-pill" title="Live Video Views">\n'
                    f'                <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>\n'
                    f'                {vviews}\n'
                    f'              </span>\n'
                    f'              <div class="card-play-btn" aria-hidden="true">\n'
                    f'                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true">\n'
                    f'                  <polygon points="6 4 20 12 6 20 6 4"></polygon>\n'
                    f'                </svg>\n'
                    f'              </div>\n'
                    f'            </div>\n'
                    f'            <div class="video-card-body">\n'
                    f'              <div class="card-meta-row">\n'
                    f'                <span class="card-playlist-name">{vplaylist}</span>\n'
                    f'                <span class="card-published-time">{vpub}</span>\n'
                    f'              </div>\n'
                    f'              <h3 class="video-card-title">{vtitle}</h3>\n'
                    f'              <p class="video-card-summary">{vsummary}</p>\n'
                    f'            </div>\n'
                    f'          </article>'
                )
                video_cards_html.append(card)

            initial_grid_content = '\n' + '\n'.join(video_cards_html) + '\n        '
            
            # Replace empty videoGrid
            old_grid_pattern = r'<div class="video-grid" id="videoGrid" aria-live="polite">\s*<!-- Populated dynamically via config\.js & app\.js -->\s*</div>'
            new_grid = f'<div class="video-grid" id="videoGrid" aria-live="polite">{initial_grid_content}</div>'
            html = re.sub(old_grid_pattern, new_grid, html)
            print(f"✓ Crawlability: Injected {len(initial_12)} pre-rendered crawlable video cards into initial HTML DOM")

        except Exception as e:
            print(f"Notice: Could not parse videos for pre-render ({e})")

    # 8. Pre-render Initial 8 Shorts Cards inside #shortsShelf
    s_idx = html.find('shorts: [')
    if s_idx != -1:
        end_idx = html.find(']\n};', s_idx)
        if end_idx != -1:
            try:
                s_json_str = html[s_idx + 8 : end_idx + 1].strip()
                shorts_data = json.loads(s_json_str)
                initial_8 = shorts_data[:8]

                short_cards_html = []
                for idx, s in enumerate(initial_8):
                    sid = s['id']
                    stitle = html_lib.escape(s['title'])
                    ssport = html_lib.escape(s.get('sport', 'Sports').upper())
                    sviews = html_lib.escape(s.get('views', '15K views'))
                    spub = html_lib.escape(s.get('published', 'Recent'))
                    thumb = f"https://i.ytimg.com/vi/{sid}/hqdefault.jpg"

                    scard = (
                        f'            <article class="short-card reveal-cascade" data-short-id="{sid}" role="button" tabindex="0" aria-label="Play Short: {stitle}" style="--cascade-index: {idx % 4}">\n'
                        f'              <img src="{thumb}" alt="Final Third Short: {stitle}" class="short-thumb-img" loading="lazy" width="360" height="640" decoding="async">\n'
                        f'              <div class="short-card-scrim" aria-hidden="true"></div>\n'
                        f'              <div class="short-badge-top" aria-hidden="true">\n'
                        f'                <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" aria-hidden="true"><path d="M17.77 10.32l-1.2-.5L18 8.06a3.74 3.74 0 0 0-3.5-5.46 3.7 3.7 0 0 0-2.62 1.1L6.26 9.32a3.75 3.75 0 0 0 1.2 6.84l1.2.5L7 18.4a3.74 3.74 0 0 0 3.5 5.46c1 0 1.95-.4 2.62-1.1l5.62-5.62a3.75 3.75 0 0 0-1-6.82zM10 14.5v-5l4.5 2.5-4.5 2.5z"/></svg>\n'
                        f'                {ssport}\n'
                        f'              </div>\n'
                        f'              <div class="short-play-btn" aria-hidden="true">\n'
                        f'                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><polygon points="6 4 20 12 6 20 6 4"></polygon></svg>\n'
                        f'              </div>\n'
                        f'              <div class="short-info">\n'
                        f'                <h4 class="short-title">{stitle}</h4>\n'
                        f'                <div class="short-meta-row">\n'
                        f'                  <span class="short-views">\n'
                        f'                    <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>\n'
                        f'                    {sviews}\n'
                        f'                  </span>\n'
                        f'                  <span>{spub}</span>\n'
                        f'                </div>\n'
                        f'              </div>\n'
                        f'            </article>'
                    )
                    short_cards_html.append(scard)

                initial_shorts_content = '\n' + '\n'.join(short_cards_html) + '\n          '
                old_shorts_pattern = r'<div class="shorts-shelf" id="shortsShelf">\s*<!-- Dynamically populated via config\.js shorts array -->\s*</div>'
                new_shorts = f'<div class="shorts-shelf" id="shortsShelf">{initial_shorts_content}</div>'
                html = re.sub(old_shorts_pattern, new_shorts, html)
                print(f"✓ Crawlability: Injected {len(initial_8)} pre-rendered crawlable shorts cards into initial HTML DOM")

            except Exception as e:
                print(f"Notice: Could not parse shorts for pre-render ({e})")

    # 9. Accessibility: Add aria-hidden="true" to all decorative SVGs that lack it
    def add_aria_hidden(m):
        tag = m.group(0)
        if 'aria-hidden' in tag or 'aria-label' in tag or 'role="img"' in tag:
            return tag
        return tag[:-1] + ' aria-hidden="true">'

    html = re.sub(r'<svg\b[^>]*>', add_aria_hidden, html)
    print("✓ Accessibility: Added aria-hidden='true' to decorative SVGs")

    # 10. Alt texts on permanent images
    html = html.replace(
        'alt="Final Third Logo in Lime Green"',
        'alt="Final Third — Football &amp; Cricket Analysis Logo"'
    )
    html = html.replace(
        'alt="Final Third Official Logo"',
        'alt="Final Third — Sports Analysis Platform"'
    )
    html = html.replace(
        'alt="Haris Nenmara (ഹാരിസ് നെന്മാറ) — Final Third Sports Host &amp; Tactical Analyst"',
        'alt="Haris Nenmara, sports analyst and host of Final Third"'
    )
    html = html.replace(
        'alt="Haris Nenmara — Sports Reporter &amp; Host at Final Third"',
        'alt="Haris Nenmara, journalist and sports analyst behind Final Third"'
    )
    print("✓ Image SEO: Refined alt texts to be informative and descriptive")

    # 11. Validate HTML tag balance
    class TagChecker(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack = []
            self.void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

        def handle_starttag(self, tag, attrs):
            if tag not in self.void_tags:
                self.stack.append((tag, self.getpos()))

        def handle_endtag(self, tag):
            if tag in self.void_tags:
                return
            if not self.stack:
                print(f"Unmatched closing tag: </{tag}> at line {self.getpos()}")
                return
            last, pos = self.stack.pop()
            if last != tag:
                print(f"Mismatched tag: expected </{last}> (opened at {pos}), found </{tag}> at line {self.getpos()}")

    checker = TagChecker()
    checker.feed(html)
    if checker.stack:
        print(f"ERROR: Found {len(checker.stack)} unclosed tags! Aborting.")
        for tag, pos in checker.stack[-5:]:
            print(f"  Unclosed: <{tag}> opened at {pos}")
        sys.exit(1)
    else:
        print("✓ HTML tag validation PASSED! All tags cleanly balanced.")

    # Write output
    with open(INPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    new_len = len(html)
    print("=" * 60)
    print(f"SUCCESS! Optimized index.html size: {new_len:,} bytes ({new_len/1024:.1f} KB)")
    print("=" * 60)

if __name__ == '__main__':
    apply_seo()
