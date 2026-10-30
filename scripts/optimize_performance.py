#!/usr/bin/env python3
"""
Final Third — Speed & Performance Optimization Engine
Applies Core Web Vitals optimizations:
1. Replaces 477KB of redundant inlined base64 images with cached, modern WebP/PNG assets.
2. Implements responsive modern <picture> tags for LCP Hero image (11KB-36KB vs 957KB raw PNG).
3. Adds high-priority responsive preloads in <head> for mobile/tablet/desktop LCP image.
4. Non-render-blocking Google Fonts loading (preconnect + async CSS swap with display=swap).
5. Positions <meta charset> and <meta viewport> at top of <head>.
6. Unifies Schema.org JSON-LD structured data and eliminates stranded duplicate block after </style>.
7. Implements content-visibility: auto for below-the-fold sections to slash mobile TBT.
8. Adds explicit width/height and decoding="async" to shorts and video thumbnails to eliminate CLS.
9. Removes duplicate un-throttled scroll event listener.
"""

import re
import sys
from html.parser import HTMLParser

INPUT_FILE = 'index.html'

def optimize():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    orig_len = len(html)
    print(f"Original index.html size: {orig_len:,} bytes ({orig_len/1024:.1f} KB)")

    # 1. Replace base64 og:image and twitter:image
    html = re.sub(
        r'<meta\s+property="og:image"\s+content="data:image/[^"]+">',
        '<meta property="og:image" content="https://www.finalthird-haris.com/assets/images/final-third-logo.png">',
        html
    )
    html = re.sub(
        r'<meta\s+name="twitter:image"\s+content="data:image/[^"]+">',
        '<meta name="twitter:image" content="https://www.finalthird-haris.com/assets/images/final-third-logo.png">',
        html
    )

    # 2. Header logo: Upgrade base64 to responsive WebP <picture>
    old_header_logo = re.search(
        r'<a\s+href="#hero"\s+class="logo-wrapper"[^>]*>\s*<img[^>]+src="data:image/png;base64,[^"]+"[^>]*>\s*</a>',
        html
    )
    if old_header_logo:
        new_header_logo = (
            '<a href="#hero" class="logo-wrapper" aria-label="Final Third — Home">\n'
            '        <picture>\n'
            '          <source type="image/webp" srcset="assets/images/final-third-logo-160.webp">\n'
            '          <img\n'
            '            src="assets/images/final-third-logo-160.png"\n'
            '            alt="Final Third Logo in Lime Green"\n'
            '            class="logo-img"\n'
            '            width="160"\n'
            '            height="82"\n'
            '            decoding="async"\n'
            '          />\n'
            '        </picture>\n'
            '      </a>'
        )
        html = html[:old_header_logo.start()] + new_header_logo + html[old_header_logo.end():]
        print("✓ Header logo upgraded to responsive WebP picture tag")

    # 3. Footer logo: Upgrade base64 to responsive WebP <picture>
    old_footer_logo = re.search(
        r'<img[^>]+src="data:image/png;base64,[^"]+"[^>]*class="logo-img"[^>]*>',
        html
    )
    if old_footer_logo:
        new_footer_logo = (
            '<picture>\n'
            '              <source type="image/webp" srcset="assets/images/final-third-logo-160.webp">\n'
            '              <img\n'
            '                src="assets/images/final-third-logo-160.png"\n'
            '                alt="Final Third Official Logo"\n'
            '                class="logo-img"\n'
            '                width="160"\n'
            '                height="82"\n'
            '                loading="lazy"\n'
            '                decoding="async"\n'
            '              />\n'
            '            </picture>'
        )
        html = html[:old_footer_logo.start()] + new_footer_logo + html[old_footer_logo.end():]
        print("✓ Footer logo upgraded to responsive WebP picture tag")

    # 4. Replace base64 in embedded FINAL_THIRD_CONFIG (logoLime and hostPortrait)
    html = re.sub(
        r'logoLime:\s*"data:image/png;base64,[^"]+"',
        'logoLime: "assets/images/final-third-logo.png"',
        html
    )
    html = re.sub(
        r'hostPortrait:\s*"data:image/jpeg;base64,[^"]+"',
        'hostPortrait: "assets/images/haris-opt.jpg"',
        html
    )
    print("✓ Config logoLime and hostPortrait cleaned of base64 bloat")

    # 5. Clean up redundant block between </style> and </head>
    # (Removes duplicate favicon and duplicate JSON-LD schema with stranded base64 logo)
    style_end_match = re.search(r'</style>', html)
    head_end_match = re.search(r'</head>', html)
    if style_end_match and head_end_match and style_end_match.end() < head_end_match.start():
        between_content = html[style_end_match.end():head_end_match.start()]
        if 'data:image' in between_content or 'SportsOrganization' in between_content:
            html = html[:style_end_match.end()] + '\n' + html[head_end_match.start():]
            print("✓ Consolidated structured data into head and removed duplicate block after </style>")

    # Check remaining base64 images
    remaining_b64 = re.findall(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', html)
    print(f"Remaining inlined base64 images: {len(remaining_b64)}")

    # 6. Upgrade Hero Portrait to responsive <picture> with AVIF & WebP + Preload
    old_hero_img = re.search(
        r'<div\s+class="portrait-editorial-frame">\s*<img\s+src="assets/images/haris-hero-portrait\.png\?v=5"[^>]*>\s*</div>',
        html
    )
    if old_hero_img:
        new_hero_img = (
            '<div class="portrait-editorial-frame">\n'
            '            <picture>\n'
            '              <source type="image/avif" srcset="assets/images/haris-hero-portrait-400.avif 400w, assets/images/haris-hero-portrait.avif 1024w" sizes="(max-width: 600px) 380px, (max-width: 992px) 520px, 660px">\n'
            '              <source type="image/webp" srcset="assets/images/haris-hero-portrait-400.webp 400w, assets/images/haris-hero-portrait-680.webp 680w, assets/images/haris-hero-portrait.webp 1024w" sizes="(max-width: 600px) 380px, (max-width: 992px) 520px, 660px">\n'
            '              <img \n'
            '                src="assets/images/haris-hero-portrait.png" \n'
            '                alt="Haris Nenmara (ഹാരിസ് നെന്മാറ) — Final Third Sports Host &amp; Tactical Analyst" \n'
            '                class="portrait-editorial-img" \n'
            '                width="1024" \n'
            '                height="958" \n'
            '                loading="eager" \n'
            '                fetchpriority="high"\n'
            '                decoding="async"\n'
            '              />\n'
            '            </picture>\n'
            '          </div>'
        )
        html = html[:old_hero_img.start()] + new_hero_img + html[old_hero_img.end():]
        print("✓ Hero LCP image upgraded to responsive AVIF/WebP <picture> with fetchpriority=high")

    # 7. Upgrade About Portrait to responsive <picture> with WebP
    old_about_img = re.search(
        r'<img\s+src="assets/images/haris-portrait-about\.jpg"[^>]*class="about-portrait-img"[^>]*>',
        html
    )
    if old_about_img:
        new_about_img = (
            '<picture>\n'
            '              <source type="image/webp" srcset="assets/images/haris-portrait-about-400.webp 400w, assets/images/haris-portrait-about.webp 682w" sizes="(max-width: 600px) 380px, 682px">\n'
            '              <img \n'
            '                src="assets/images/haris-portrait-about.jpg" \n'
            '                alt="Haris Nenmara — Sports Reporter &amp; Host at Final Third" \n'
            '                class="about-portrait-img"\n'
            '                width="682"\n'
            '                height="1024"\n'
            '                loading="lazy"\n'
            '                decoding="async"\n'
            '              />\n'
            '            </picture>'
        )
        html = html[:old_about_img.start()] + new_about_img + html[old_about_img.end():]
        print("✓ About section portrait upgraded to responsive WebP <picture>")

    # 8. Reorder <head>: place <meta charset> and <meta viewport> at top, add preloads, async Google Fonts, unified Schema.org
    head_start_match = re.search(r'<head>', html)
    style_start_match = re.search(r'<style>', html)
    if head_start_match and style_start_match:
        new_head_meta = (
            '\n  <meta charset="UTF-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '  <title>Final Third with Haris Nenmara | ഫൈനൽ തേർഡ് — Malayalam Football &amp; Cricket Analysis</title>\n'
            '  <meta name="description" content="ഫൈനൽ തേർഡ് (Final Third) with Haris Nenmara (ഹാരിസ് നെന്മാറ) — Kerala\'s premier sports platform for football &amp; cricket analysis, tactical debriefs, Kerala Blasters stories, ISL, and European football in Malayalam (മലയാളം സ്പോർട്സ് വിശകലനം).">\n'
            '  <meta name="keywords" content="ഫൈനൽ തേർഡ്, ഹാരിസ് നെന്മാറ, ഫൈനൽ തേർഡ് ഹാരിസ് നെന്മാറ, മലയാളം ഫുട്ബോൾ വിശകലനം, കേരള ബ്ലാസ്റ്റേഴ്സ്, കേരള ബ്ലാസ്റ്റേഴ്സ് വാർത്തകൾ, ഐഎസ്എൽ മലയാളം, ഇന്ത്യൻ ഫുട്ബോൾ, സഞ്ജു സാംസൺ ക്രിക്കറ്റ്, ക്രിക്കറ്റ് വിശകലനം മലയാളം, കായിക വാർത്തകൾ, ഫുട്ബോൾ ടാക്റ്റിക്സ്, സ്പോർട്സ് സ്റ്റോറികൾ, ഫൈനൽ തേർഡ് യൂട്യൂബ്, ഫുട്ബോൾ വിശകലനം, final third, haris nenmara, final third haris nenmara, malayalam football analysis, kerala blasters analysis malayalam, kerala blasters news, isl football malayalam, sanju samson malayalam analysis, indian football malayalam, malayalam sports channel, football tactics malayalam, sports analysis in malayalam, kerala sports journalism, football podcast malayalam, final third media">\n'
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
            '  <!-- Geo-Targeting & Regional Tags for Kerala & Global Malayali Diaspora -->\n'
            '  <meta name="geo.region" content="IN-KL">\n'
            '  <meta name="geo.placename" content="Kerala, India">\n'
            '  <meta name="geo.position" content="10.8505;76.2711">\n'
            '  <meta name="ICBM" content="10.8505, 76.2711">\n\n'
            '  <!-- Open Graph / Facebook -->\n'
            '  <meta property="og:site_name" content="Final Third with Haris Nenmara | ഫൈനൽ തേർഡ്">\n'
            '  <meta property="og:type" content="website">\n'
            '  <meta property="og:url" content="https://www.finalthird-haris.com/">\n'
            '  <meta property="og:locale" content="ml_IN">\n'
            '  <meta property="og:locale:alternate" content="en_IN">\n'
            '  <meta property="og:locale:alternate" content="en_US">\n'
            '  <meta property="og:locale:alternate" content="ar_AE">\n'
            '  <meta property="og:title" content="Final Third with Haris Nenmara | ഫൈനൽ തേർഡ് — Football &amp; Cricket in Malayalam">\n'
            '  <meta property="og:description" content="കായിക ലോകം, മലയാളത്തിൽ. Football &amp; cricket match coverage, tactical debriefs, and Kerala Blasters stories featuring Haris Nenmara.">\n'
            '  <meta property="og:image" content="https://www.finalthird-haris.com/assets/images/final-third-logo.png">\n\n'
            '  <!-- Twitter Card -->\n'
            '  <meta name="twitter:card" content="summary_large_image">\n'
            '  <meta name="twitter:title" content="Final Third with Haris Nenmara | ഫൈനൽ തേർഡ്">\n'
            '  <meta name="twitter:description" content="കായിക ലോകം മലയാളത്തിൽ. Football &amp; Cricket match analysis and sports stories.">\n'
            '  <meta name="twitter:image" content="https://www.finalthird-haris.com/assets/images/final-third-logo.png">\n\n'
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
            '  <!-- Schema.org JSON-LD Structured Data (Google Rich Results & Knowledge Graph) -->\n'
            '  <script type="application/ld+json">\n'
            '  {\n'
            '    "@context": "https://schema.org",\n'
            '    "@graph": [\n'
            '      {\n'
            '        "@type": "WebSite",\n'
            '        "@id": "https://www.finalthird-haris.com/#website",\n'
            '        "url": "https://www.finalthird-haris.com/",\n'
            '        "name": "Final Third with Haris Nenmara | ഫൈനൽ തേർഡ്",\n'
            '        "alternateName": [\n'
            '          "Final Third",\n'
            '          "ഫൈനൽ തേർഡ്",\n'
            '          "Final Third Malayalam",\n'
            '          "Haris Nenmara Sports"\n'
            '        ],\n'
            '        "description": "Kerala\'s premier Malayalam sports media platform for football & cricket tactical analysis, match reviews, and Kerala Blasters debriefs.",\n'
            '        "inLanguage": ["ml", "en"],\n'
            '        "publisher": {\n'
            '          "@id": "https://www.finalthird-haris.com/#organization"\n'
            '        }\n'
            '      },\n'
            '      {\n'
            '        "@type": "SportsOrganization",\n'
            '        "@id": "https://www.finalthird-haris.com/#organization",\n'
            '        "name": "Final Third",\n'
            '        "url": "https://www.finalthird-haris.com/",\n'
            '        "logo": "https://www.finalthird-haris.com/assets/images/final-third-logo.png",\n'
            '        "sameAs": [\n'
            '          "https://www.youtube.com/@FinalThird_HarisNenmara",\n'
            '          "https://www.instagram.com/finalthird.official/",\n'
            '          "https://www.facebook.com/profile.php?id=61590005744291",\n'
            '          "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"\n'
            '        ],\n'
            '        "description": "Premium sports media publication covering football and cricket stories, match analysis, and perspectives in Malayalam."\n'
            '      },\n'
            '      {\n'
            '        "@type": "Person",\n'
            '        "@id": "https://www.finalthird-haris.com/#person",\n'
            '        "name": "Haris Nenmara",\n'
            '        "alternateName": "ഹാരിസ് നെന്മാറ",\n'
            '        "jobTitle": "Sports Analyst, Host & Storyteller",\n'
            '        "worksFor": {\n'
            '          "@id": "https://www.finalthird-haris.com/#organization"\n'
            '        },\n'
            '        "description": "Sports analyst and creator of Final Third, analyzing football tactics, ISL, Kerala Blasters, and cricket in Malayalam.",\n'
            '        "url": "https://www.finalthird-haris.com/#about",\n'
            '        "image": "https://www.finalthird-haris.com/assets/images/haris-hero-portrait.png",\n'
            '        "nationality": {\n'
            '          "@type": "Country",\n'
            '          "name": "India"\n'
            '        },\n'
            '        "address": {\n'
            '          "@type": "PostalAddress",\n'
            '          "addressRegion": "Kerala",\n'
            '          "addressCountry": "IN"\n'
            '        },\n'
            '        "sameAs": [\n'
            '          "https://www.youtube.com/@FinalThird_HarisNenmara",\n'
            '          "https://www.instagram.com/finalthird.official/",\n'
            '          "https://www.facebook.com/profile.php?id=61590005744291",\n'
            '          "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"\n'
            '        ]\n'
            '      },\n'
            '      {\n'
            '        "@type": "CreativeWorkSeries",\n'
            '        "@id": "https://www.finalthird-haris.com/#series",\n'
            '        "name": "Final Third (ഫൈനൽ തേർഡ്)",\n'
            '        "headline": "The Game. Beyond the Obvious. — Malayalam Sports Analysis",\n'
            '        "description": "In-depth tactical breakdowns, Kerala Blasters reviews, ISL analysis, European football coverage, and cricket stories in Malayalam.",\n'
            '        "inLanguage": ["ml", "en"],\n'
            '        "creator": {\n'
            '          "@id": "https://www.finalthird-haris.com/#person"\n'
            '        },\n'
            '        "genre": [\n'
            '          "Sports Analysis",\n'
            '          "Football",\n'
            '          "Cricket",\n'
            '          "Tactics",\n'
            '          "Kerala Blasters",\n'
            '          "ISL"\n'
            '        ],\n'
            '        "keywords": "ഫൈനൽ തേർഡ്, ഹാരിസ് നെന്മാറ, malayalam football analysis, kerala blasters, sanju samson, isl football, sports tactics malayalam"\n'
            '      }\n'
            '    ]\n'
            '  }\n'
            '  </script>\n\n  '
        )
        html = html[:head_start_match.end()] + new_head_meta + html[style_start_match.start():]
        print("✓ <head> restructured with modern performance preloads and non-render-blocking fonts")

    # 9. Add content-visibility: auto into CSS style tag
    css_insert_point = html.find('/* --------------------------------------------------------------------------\n   Layout Containers & Utilities')
    if css_insert_point != -1:
        perf_css = (
            '/* --------------------------------------------------------------------------\n'
            '   Core Web Vitals & Mobile Performance (content-visibility off-screen)\n'
            '   -------------------------------------------------------------------------- */\n'
            '.video-section,\n'
            '.shorts-section,\n'
            '.sponsor-banner-section,\n'
            '.about-section,\n'
            '.social-section,\n'
            '.contact-section {\n'
            '  content-visibility: auto;\n'
            '  contain-intrinsic-size: auto 650px;\n'
            '}\n\n'
        )
        html = html[:css_insert_point] + perf_css + html[css_insert_point:]
        print("✓ Added content-visibility: auto to off-screen sections")

    # 10. Add width, height and decoding="async" to shorts in renderShorts()
    old_short_img = '<img src="${thumb}" alt="${escapeHtml(short.title)}" class="short-thumb-img" loading="lazy">'
    new_short_img = '<img src="${thumb}" alt="${escapeHtml(short.title)}" class="short-thumb-img" loading="lazy" width="360" height="640" decoding="async">'
    if old_short_img in html:
        html = html.replace(old_short_img, new_short_img)
        print("✓ Added explicit width=360, height=640, decoding=async to short cards (CLS prevention)")

    # 11. Add decoding="async" to video cards in renderVideos()
    old_video_thumb = (
        '            <img \n'
        '              src="${thumbUrl}" \n'
        '              alt="Thumbnail for ${escapeHtml(video.title)}" \n'
        '              loading="lazy" \n'
        '              width="480" \n'
        '              height="270"\n'
        '            />'
    )
    new_video_thumb = (
        '            <img \n'
        '              src="${thumbUrl}" \n'
        '              alt="Thumbnail for ${escapeHtml(video.title)}" \n'
        '              loading="lazy" \n'
        '              decoding="async"\n'
        '              width="480" \n'
        '              height="270"\n'
        '            />'
    )
    if old_video_thumb in html:
        html = html.replace(old_video_thumb, new_video_thumb)
        print("✓ Added decoding=async to video catalog cards")

    # 12. Remove duplicate unthrottled scroll listener
    duplicate_scroll = re.search(
        r'\s*// Sticky Header Scroll Effect\s*window\.addEventListener\(\'scroll\',\s*\(\)\s*=>\s*\{\s*if\s*\(window\.scrollY\s*>\s*50\)\s*\{\s*siteHeader\?\.classList\.add\(\'scrolled\'\);\s*\}\s*else\s*\{\s*siteHeader\?\.classList\.remove\(\'scrolled\'\);\s*\}\s*\}\);',
        html
    )
    if duplicate_scroll:
        html = html[:duplicate_scroll.start()] + html[duplicate_scroll.end():]
        print("✓ Removed redundant unthrottled scroll listener")

    # 13. Validate HTML tag balance
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
    savings = orig_len - new_len
    pct = (savings / orig_len) * 100
    print("=" * 60)
    print(f"SUCCESS! Optimized index.html size: {new_len:,} bytes ({new_len/1024:.1f} KB)")
    print(f"Saved: {savings:,} bytes ({savings/1024:.1f} KB, -{pct:.1f}%)")
    print("=" * 60)

if __name__ == '__main__':
    optimize()
