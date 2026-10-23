#!/usr/bin/env python3
"""
Restores the original, uncompressed, crystal-clear studio photograph of Haris:
1. Points index.html to assets/images/haris-hero-original.jpg (zero pixel manipulation, natural skin tones, zero green tint).
2. Uses a non-destructive CSS edge vignette that only touches the outer margin so the dark studio background dissolves seamlessly into the website's #080808 background.
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update image src in index.html to the pristine original JPEG
html = re.sub(
    r'<img\s+src=\"assets/images/haris-hero-[^\"]+\"[^>]*class=\"portrait-editorial-img\"[^>]*>',
    '<img src="assets/images/haris-hero-original.jpg" alt="Haris Nenmara — Final Third Sports Host &amp; Analyst" class="portrait-editorial-img" width="1024" height="958" loading="eager" />',
    html
)
print("✓ Updated hero img src in index.html to pristine assets/images/haris-hero-original.jpg")

# 2. Refine the CSS to preserve 100% natural clarity and seamless background
clean_seamless_css = """/* ==========================================================================
   SEAMLESS HERO VISUAL (NATURAL STUDIO PORTRAIT & SEAMLESS BLEND)
   ========================================================================== */
.hero-grid {
  grid-template-columns: 1fr 1.05fr !important;
  gap: 20px !important;
  align-items: center !important;
}

.hero-portrait-wrapper {
  position: relative !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  width: 100% !important;
  overflow: visible !important;
}

.portrait-glow-ring,
.portrait-lime-accent {
  display: none !important;
}

.portrait-editorial-frame {
  position: relative !important;
  width: 100% !important;
  max-width: 660px !important;
  aspect-ratio: auto !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
  overflow: visible !important;
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}

.portrait-editorial-img {
  width: 100% !important;
  max-width: 660px !important;
  height: auto !important;
  display: block !important;
  object-fit: contain !important;
  image-rendering: auto !important;
  /* Seamless edge blend: only softens the outer 12% perimeter, leaving Haris 100% sharp and untouched */
  -webkit-mask-image: radial-gradient(ellipse 88% 85% at 50% 50%, black 72%, rgba(0,0,0,0.85) 84%, transparent 100%) !important;
  mask-image: radial-gradient(ellipse 88% 85% at 50% 50%, black 72%, rgba(0,0,0,0.85) 84%, transparent 100%) !important;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.9)) !important;
  transition: transform var(--transition-smooth) !important;
}

.portrait-editorial-frame:hover .portrait-editorial-img {
  transform: scale(1.02) !important;
}

.portrait-floating-card {
  position: absolute !important;
  bottom: 20px !important;
  right: 8% !important;
  background: rgba(15, 15, 15, 0.88) !important;
  backdrop-filter: blur(14px) !important;
  -webkit-backdrop-filter: blur(14px) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 12px !important;
  padding: 10px 18px !important;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8) !important;
  z-index: 5 !important;
}

@media (max-width: 1024px) {
  .hero-grid {
    grid-template-columns: 1fr !important;
    gap: 30px !important;
  }
  .portrait-editorial-frame {
    max-width: 480px !important;
  }
  .portrait-floating-card {
    right: 5% !important;
    bottom: 10px !important;
  }
}
"""

marker = "/* ==========================================================================\n   SEAMLESS HERO VISUAL"
if marker in css:
    idx_css = css.find(marker)
    css = css[:idx_css] + clean_seamless_css
    print("✓ Updated CSS in styles.css")

if marker in html:
    idx_h = html.find(marker)
    idx_h_end = html.find("</style>", idx_h)
    html = html[:idx_h] + clean_seamless_css + "\n  " + html[idx_h_end:]
    print("✓ Updated CSS in index.html <style>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Restoration complete!")
