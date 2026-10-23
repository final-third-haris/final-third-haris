#!/usr/bin/env python3
"""
Updates the hero visual styling so Haris is large and the image blends 100% seamlessly
with the website background (no borders, no card box, feathered edges, and scale).
"""

with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

seamless_hero_css = """
/* ==========================================================================
   SEAMLESS HERO VISUAL (LARGE, BORDERLESS & FEATHERED STUDIO INTEGRATION)
   ========================================================================== */
.hero-grid {
  grid-template-columns: 1fr 1.15fr !important;
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
  max-width: 760px !important;
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
  max-width: 760px !important;
  height: auto !important;
  display: block !important;
  object-fit: contain !important;
  transform: scale(1.15) !important;
  transform-origin: 72% 52% !important;
  filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.9)) !important;
  -webkit-mask-image: radial-gradient(ellipse 80% 75% at 70% 50%, #000 50%, rgba(0,0,0,0.85) 65%, transparent 95%) !important;
  mask-image: radial-gradient(ellipse 80% 75% at 70% 50%, #000 50%, rgba(0,0,0,0.85) 65%, transparent 95%) !important;
  transition: transform var(--transition-smooth) !important;
}

.portrait-editorial-frame:hover .portrait-editorial-img {
  transform: scale(1.18) !important;
}

.portrait-floating-card {
  position: absolute !important;
  bottom: 12px !important;
  right: 14% !important;
  background: rgba(15, 15, 15, 0.85) !important;
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
  .portrait-editorial-img {
    transform: scale(1.05) !important;
    transform-origin: center center !important;
  }
  .portrait-floating-card {
    right: 5% !important;
    bottom: 5px !important;
  }
}
"""

# Append to styles.css
if "SEAMLESS HERO VISUAL" not in css:
    css = css + "\n" + seamless_hero_css
else:
    # replace existing block
    idx = css.find("/* ==========================================================================\n   SEAMLESS HERO VISUAL")
    css = css[:idx] + seamless_hero_css

with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Append to index.html <style>
if "SEAMLESS HERO VISUAL" not in html:
    idx_s = html.find('</style>')
    if idx_s != -1:
        html = html[:idx_s] + seamless_hero_css + '\n  ' + html[idx_s:]
else:
    idx = html.find("/* ==========================================================================\n   SEAMLESS HERO VISUAL")
    idx_end = html.find("</style>", idx)
    html = html[:idx] + seamless_hero_css + '\n  ' + html[idx_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✓ Applied seamless hero visual styles to styles.css and index.html!")
