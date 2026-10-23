#!/usr/bin/env python3
"""
Updates the hero image in index.html to assets/images/haris-hero-seamless.png
and refines the seamless hero CSS for the new 1024x958 front-facing portrait.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update image src in index.html
old_img_str = """            <img 
              src="assets/images/haris-hero-landscape.png" 
              alt="Haris Nenmara — Final Third Sports Host &amp; Analyst" 
              class="portrait-editorial-img"
              width="1024" 
              height="576"
              loading="eager"
            />"""

new_img_str = """            <img 
              src="assets/images/haris-hero-seamless.png" 
              alt="Haris Nenmara — Final Third Sports Host &amp; Analyst" 
              class="portrait-editorial-img"
              width="1024" 
              height="958"
              loading="eager"
            />"""

if old_img_str in html:
    html = html.replace(old_img_str, new_img_str)
    print("✓ Replaced hero image tag with haris-hero-seamless.png in index.html")
else:
    # try regex replacement
    import re
    html = re.sub(
        r'<img\s+src=\"assets/images/haris-hero-landscape\.png\"[^>]*class=\"portrait-editorial-img\"[^>]*>',
        '<img src="assets/images/haris-hero-seamless.png" alt="Haris Nenmara — Final Third Sports Host &amp; Analyst" class="portrait-editorial-img" width="1024" height="958" loading="eager" />',
        html
    )
    print("✓ Replaced hero image tag via regex in index.html")

# 2. Refined Seamless CSS
updated_seamless_css = """/* ==========================================================================
   SEAMLESS HERO VISUAL (LARGE, BORDERLESS & FEATHERED STUDIO INTEGRATION)
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
  transform: scale(1.05) !important;
  transform-origin: center center !important;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.9)) !important;
  transition: transform var(--transition-smooth) !important;
}

.portrait-editorial-frame:hover .portrait-editorial-img {
  transform: scale(1.08) !important;
}

.portrait-floating-card {
  position: absolute !important;
  bottom: 20px !important;
  right: 10% !important;
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
    idx_start = css.find(marker)
    css = css[:idx_start] + updated_seamless_css
    print("✓ Updated seamless hero CSS in styles.css")

if marker in html:
    idx_h_start = html.find(marker)
    idx_h_end = html.find("</style>", idx_h_start)
    html = html[:idx_h_start] + updated_seamless_css + "\n  " + html[idx_h_end:]
    print("✓ Updated seamless hero CSS in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Finished updating hero visual to seamless matching background!")
