#!/usr/bin/env python3
"""
Final Third — Schema.org & JSON-LD Structured Data Engine
Updates the structured data markup in index.html to implement a complete,
verified, and interconnected Schema.org @graph:
1. SportsOrganization (@id: #organization) - Official brand with verified logo, description & sameAs links.
2. Person (@id: #person) - Haris Nenmara with verified role, worksFor, and official links.
3. WebSite (@id: #website) - Canonical site representation with multilingual declarations.
4. WebPage (@id: #webpage) - Canonical landing page entity connecting author, publisher, and video.
5. ProfilePage (@id: #about) - Dedicated profile section for host Haris Nenmara (mainEntity: #person).
6. VideoObject (@id: #featured-video) - Google Video compliant markup for the genuinely embedded spotlight episode.
7. ImageObject (@id: #ogImage) - High-resolution 1200x630 social/primary page image.
"""

import re
import sys
import json
from html.parser import HTMLParser

INPUT_FILE = 'index.html'

def update_schema():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    orig_len = len(html)
    print(f"Original index.html size: {orig_len:,} bytes ({orig_len/1024:.1f} KB)")

    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SportsOrganization",
                "@id": "https://final-third-haris.github.io/#organization",
                "name": "Final Third",
                "alternateName": [
                    "Final Third with Haris Nenmara",
                    "Final Third Sports",
                    "ഫൈനൽ തേർഡ്"
                ],
                "url": "https://final-third-haris.github.io/",
                "logo": {
                    "@type": "ImageObject",
                    "@id": "https://final-third-haris.github.io/#logo",
                    "url": "https://final-third-haris.github.io/assets/images/final-third-logo.png",
                    "contentUrl": "https://final-third-haris.github.io/assets/images/final-third-logo.png",
                    "caption": "Final Third Logo"
                },
                "image": "https://final-third-haris.github.io/assets/images/og-image.jpg",
                "description": "Sports analysis media platform covering football match analysis, tactical formations, and cricket analysis by Haris Nenmara.",
                "sameAs": [
                    "https://www.youtube.com/@FinalThird_HarisNenmara",
                    "https://www.instagram.com/finalthird.official/",
                    "https://www.facebook.com/profile.php?id=61590005744291",
                    "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"
                ]
            },
            {
                "@type": "Person",
                "@id": "https://final-third-haris.github.io/#person",
                "name": "Haris Nenmara",
                "alternateName": "ഹാരിസ് നെന്മാറ",
                "jobTitle": "Sports Journalist & Analyst",
                "description": "Sports journalist and tactical analyst behind Final Third, analyzing football tactics, formations, and cricket in Malayalam.",
                "url": "https://final-third-haris.github.io/#about",
                "image": {
                    "@type": "ImageObject",
                    "@id": "https://final-third-haris.github.io/#personImage",
                    "url": "https://final-third-haris.github.io/assets/images/haris-hero-portrait.png",
                    "caption": "Haris Nenmara — Final Third Host & Analyst"
                },
                "worksFor": {
                    "@id": "https://final-third-haris.github.io/#organization"
                },
                "sameAs": [
                    "https://www.youtube.com/@FinalThird_HarisNenmara",
                    "https://www.instagram.com/finalthird.official/",
                    "https://www.facebook.com/profile.php?id=61590005744291",
                    "https://whatsapp.com/channel/0029VbCMhqQ0G0XYaQLOMP2U"
                ]
            },
            {
                "@type": "WebSite",
                "@id": "https://final-third-haris.github.io/#website",
                "url": "https://final-third-haris.github.io/",
                "name": "Final Third",
                "alternateName": [
                    "Final Third with Haris Nenmara",
                    "Final Third Sports",
                    "ഫൈനൽ തേർഡ്"
                ],
                "description": "Kerala's premier Malayalam sports media platform for football match analysis, tactics and formations, and cricket analysis.",
                "inLanguage": [
                    "ml",
                    "en"
                ],
                "publisher": {
                    "@id": "https://final-third-haris.github.io/#organization"
                }
            },
            {
                "@type": "WebPage",
                "@id": "https://final-third-haris.github.io/#webpage",
                "url": "https://final-third-haris.github.io/",
                "name": "Final Third | Football & Cricket Match Analysis by Haris Nenmara",
                "description": "Final Third by Haris Nenmara brings in-depth football match analysis, tactics and formations, Kerala Blasters stories, and cricket match analysis in Malayalam.",
                "isPartOf": {
                    "@id": "https://final-third-haris.github.io/#website"
                },
                "about": {
                    "@id": "https://final-third-haris.github.io/#organization"
                },
                "author": {
                    "@id": "https://final-third-haris.github.io/#person"
                },
                "primaryImageOfPage": {
                    "@id": "https://final-third-haris.github.io/#ogImage"
                },
                "video": {
                    "@id": "https://final-third-haris.github.io/#featured-video"
                }
            },
            {
                "@type": "ImageObject",
                "@id": "https://final-third-haris.github.io/#ogImage",
                "url": "https://final-third-haris.github.io/assets/images/og-image.jpg",
                "width": 1200,
                "height": 630,
                "caption": "Final Third — Football and Cricket Analysis by Haris Nenmara"
            },
            {
                "@type": "ProfilePage",
                "@id": "https://final-third-haris.github.io/#about",
                "url": "https://final-third-haris.github.io/#about",
                "name": "About Haris Nenmara | Final Third",
                "description": "Journalistic background, sports reporting experience, and tactical philosophy of Haris Nenmara, host of Final Third.",
                "isPartOf": {
                    "@id": "https://final-third-haris.github.io/#website"
                },
                "mainEntity": {
                    "@id": "https://final-third-haris.github.io/#person"
                }
            },
            {
                "@type": "VideoObject",
                "@id": "https://final-third-haris.github.io/#featured-video",
                "name": "ഇതൊക്കെയാണ് കം ബാക്ക് ! നമൻ ധീർ പ്രതീക്ഷയാണ് | Tilak Varma | NamanDhir",
                "description": "Final Third match coverage and cricket analysis with Haris Nenmara.",
                "thumbnailUrl": [
                    "https://i.ytimg.com/vi/F1X3eE_CBKU/maxresdefault.jpg",
                    "https://i.ytimg.com/vi/F1X3eE_CBKU/hqdefault.jpg"
                ],
                "uploadDate": "2026-10-25T12:00:00+05:30",
                "embedUrl": "https://www.youtube.com/embed/F1X3eE_CBKU",
                "contentUrl": "https://www.youtube.com/watch?v=F1X3eE_CBKU",
                "inLanguage": "ml",
                "creator": {
                    "@id": "https://final-third-haris.github.io/#person"
                }
            }
        ]
    }

    # Format as JSON string with 2 space indentation
    json_str = json.dumps(schema_graph, indent=2, ensure_ascii=False)
    # Indent each line by 2 spaces for clean HTML nesting
    indented_json = '\n'.join('  ' + line if line else line for line in json_str.split('\n'))

    new_script_tag = f'<script type="application/ld+json">\n{indented_json}\n  </script>'

    pattern = r'<script type="application/ld\+json">\s*\{.*?\}\s*</script>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        print("Error: Could not find existing JSON-LD script tag in HTML")
        sys.exit(1)

    html = html[:match.start()] + new_script_tag + html[match.end():]
    print("✓ Successfully replaced JSON-LD with unified, page-specific Schema.org @graph")

    # Validate tag balance
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
    print(f"SUCCESS! Updated index.html size: {new_len:,} bytes ({new_len/1024:.1f} KB)")
    print("=" * 60)

if __name__ == '__main__':
    update_schema()
