#!/usr/bin/env python3
"""
Adds the Final Third Shorts section to index.html, assets/css/styles.css, and assets/js/app.js.
"""

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS for shorts
shorts_css = """/* ==========================================================================
   FINAL THIRD SHORTS — VERTICAL REELS SHELF
   ========================================================================== */
.shorts-section {
  position: relative;
  padding: 80px 0;
  background: radial-gradient(circle at 50% 0%, rgba(255, 0, 0, 0.05) 0%, rgba(8, 8, 8, 0.98) 50%, #080808 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.shorts-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.shorts-icon-pill {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  background: #ff0000;
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 12px rgba(255, 0, 0, 0.5);
}

.shorts-shelf {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
  gap: 20px;
  margin-top: 28px;
}

.short-card {
  position: relative;
  background: #111111;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  aspect-ratio: 9 / 16;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.short-card:hover {
  transform: translateY(-6px) scale(1.02);
  border-color: var(--neon-lime);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.8), 0 0 25px rgba(158, 226, 11, 0.2);
}

.short-thumb-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.short-card:hover .short-thumb-img {
  transform: scale(1.06);
}

.short-card-scrim {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.2) 0%, transparent 40%, rgba(0, 0, 0, 0.6) 70%, rgba(0, 0, 0, 0.95) 100%);
  pointer-events: none;
}

.short-badge-top {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(0, 0, 0, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.6875rem;
  font-weight: 800;
  color: #FFFFFF;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  backdrop-filter: blur(6px);
}

.short-play-btn {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(158, 226, 11, 0.95);
  color: #080808;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.25s ease;
  z-index: 2;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
}

.short-card:hover .short-play-btn {
  opacity: 1;
  transform: translate(-50%, -50%) scale(1.05);
}

.short-info {
  position: relative;
  z-index: 2;
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.short-title {
  font-size: 0.9375rem;
  font-weight: 800;
  color: #FFFFFF;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
}

.short-meta {
  font-size: 0.75rem;
  color: var(--neon-lime);
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 768px) {
  .shorts-shelf {
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
  }
}

"""

marker_css = '/* ==========================================================================\n   SPONSOR / ADVERTISE WITH US'
idx_css = html.find(marker_css)
if idx_css != -1 and 'FINAL THIRD SHORTS' not in html:
    html = html[:idx_css] + shorts_css + html[idx_css:]
    print('Added shorts CSS to index.html!')

# Navigation: Add Shorts
old_nav_html = '<li><a href="#videos" class="nav-link">Videos</a></li>'
new_nav_html = '<li><a href="#videos" class="nav-link">Videos</a></li>\n          <li><a href="#shorts" class="nav-link">Shorts</a></li>'
if 'href="#shorts"' not in html:
    html = html.replace(old_nav_html, new_nav_html, 1)

old_mob_nav = '<li><a href="#videos" class="mobile-nav-link">Videos</a></li>'
new_mob_nav = '<li><a href="#videos" class="mobile-nav-link">Videos</a></li>\n      <li><a href="#shorts" class="mobile-nav-link">Shorts</a></li>'
if 'href="#shorts" class="mobile-nav-link"' not in html:
    html = html.replace(old_mob_nav, new_mob_nav, 1)

# HTML Section: Add #shorts right after #videos
shorts_sec_html = """

    <!-- =======================================================================
         4C. FINAL THIRD SHORTS (VERTICAL REELS SHELF)
         ======================================================================= -->
    <section class="shorts-section" id="shorts">
      <div class="container">
        <div class="section-header flex-row">
          <div>
            <div class="eyebrow shorts-eyebrow">
              <span class="shorts-icon-pill" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                  <path d="M17.77 10.32l-1.2-.5L18 8.06a3.74 3.74 0 0 0-3.5-5.46 3.7 3.7 0 0 0-2.62 1.1L6.26 9.32a3.75 3.75 0 0 0 1.2 6.84l1.2.5L7 18.4a3.74 3.74 0 0 0 3.5 5.46c1 0 1.95-.4 2.62-1.1l5.62-5.62a3.75 3.75 0 0 0-1-6.82zM10 14.5v-5l4.5 2.5-4.5 2.5z"/>
                </svg>
              </span>
              60-Second Reels
            </div>
            <h2 class="section-title">FINAL THIRD <span class="highlight">SHORTS.</span></h2>
            <p class="section-subtitle">
              Fast match reactions, tactical breakdowns, viral quotes, and quick-fire sports perspectives.
            </p>
          </div>
          <a href="https://www.youtube.com/@FinalThird_HarisNenmara/shorts" target="_blank" rel="noopener noreferrer" class="btn btn-outline">
            ALL SHORTS ON YOUTUBE ↗
          </a>
        </div>

        <!-- Shorts Shelf -->
        <div class="shorts-shelf-container">
          <div class="shorts-shelf" id="shortsShelf">
            <!-- Dynamically populated via config.js shorts array -->
          </div>
        </div>

        <!-- Load More Shorts Button -->
        <div style="text-align: center; margin-top: 36px;">
          <button id="loadMoreShortsBtn" class="btn btn-outline" type="button">
            LOAD MORE SHORTS
          </button>
        </div>

      </div>
    </section>
"""

marker_sec = '<!-- =======================================================================\n         4B. SPONSOR & ADVERTISE WITH FINAL THIRD'
idx_sec = html.find(marker_sec)
if idx_sec != -1 and 'id="shorts"' not in html:
    html = html[:idx_sec] + shorts_sec_html + '\n    ' + html[idx_sec:]
    print('Added #shorts section HTML to index.html!')

# JS Logic for Shorts
shorts_js = """
  // Shorts Shelf State & Renderer
  const shortsState = {
    visibleCount: 8,
    perPage: 8
  };

  const shortsShelf = document.getElementById('shortsShelf');
  const loadMoreShortsBtn = document.getElementById('loadMoreShortsBtn');

  function renderShorts() {
    if (!shortsShelf) return;
    const allShorts = (typeof FINAL_THIRD_CONFIG !== 'undefined' && FINAL_THIRD_CONFIG.shorts) ? FINAL_THIRD_CONFIG.shorts : [];
    const visibleShorts = allShorts.slice(0, shortsState.visibleCount);

    if (visibleShorts.length === 0) {
      const sec = document.getElementById('shorts');
      if (sec) sec.style.display = 'none';
      return;
    }

    shortsShelf.innerHTML = visibleShorts.map(short => {
      const thumb = `https://i.ytimg.com/vi/${short.id}/hqdefault.jpg`;
      const sportLabel = (short.sport || 'Sports').toUpperCase();

      return `
        <article class="short-card" data-short-id="${short.id}" role="button" tabindex="0" aria-label="Play Short: ${escapeHtml(short.title)}">
          <img src="${thumb}" alt="${escapeHtml(short.title)}" class="short-thumb-img" loading="lazy">
          <div class="short-card-scrim" aria-hidden="true"></div>
          
          <div class="short-badge-top">
            <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor">
              <path d="M17.77 10.32l-1.2-.5L18 8.06a3.74 3.74 0 0 0-3.5-5.46 3.7 3.7 0 0 0-2.62 1.1L6.26 9.32a3.75 3.75 0 0 0 1.2 6.84l1.2.5L7 18.4a3.74 3.74 0 0 0 3.5 5.46c1 0 1.95-.4 2.62-1.1l5.62-5.62a3.75 3.75 0 0 0-1-6.82zM10 14.5v-5l4.5 2.5-4.5 2.5z"/>
            </svg>
            ${sportLabel}
          </div>

          <div class="short-play-btn" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <polygon points="6 4 20 12 6 20 6 4"></polygon>
            </svg>
          </div>

          <div class="short-info">
            <h4 class="short-title">${escapeHtml(short.title)}</h4>
            <div class="short-meta">
              <span>⚡ Short</span>
              <span>•</span>
              <a href="https://www.youtube.com/shorts/${short.id}" target="_blank" rel="noopener noreferrer" style="color:var(--neon-lime); text-decoration:underline;" onclick="event.stopPropagation();">
                Open ↗
              </a>
            </div>
          </div>
        </article>
      `;
    }).join('');

    shortsShelf.querySelectorAll('.short-card').forEach(card => {
      const clickHandler = () => {
        const sid = card.getAttribute('data-short-id');
        openVideoModal(sid);
      };
      card.addEventListener('click', clickHandler);
      card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          clickHandler();
        }
      });
    });

    if (loadMoreShortsBtn) {
      if (shortsState.visibleCount >= allShorts.length) {
        loadMoreShortsBtn.style.display = 'none';
      } else {
        loadMoreShortsBtn.style.display = 'inline-block';
      }
    }
  }

  if (loadMoreShortsBtn) {
    loadMoreShortsBtn.addEventListener('click', () => {
      shortsState.visibleCount += shortsState.perPage;
      renderShorts();
    });
  }
"""

marker_init = 'initPlaylistSelector();\n  renderVideos();'
if marker_init in html and 'renderShorts();' not in html:
    html = html.replace(marker_init, shorts_js + '\n  initPlaylistSelector();\n  renderVideos();\n  renderShorts();')
    print('Added shorts JS logic to index.html!')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Also update assets/css/styles.css
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

idx_c = css.find(marker_css)
if idx_c != -1 and 'FINAL THIRD SHORTS' not in css:
    css = css[:idx_c] + shorts_css + css[idx_c:]
    with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Added shorts CSS to styles.css!')

# Also update assets/js/app.js
with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

if marker_init in app_js and 'renderShorts();' not in app_js:
    app_js = app_js.replace(marker_init, shorts_js + '\n  initPlaylistSelector();\n  renderVideos();\n  renderShorts();')
    with open('assets/js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    print('Added shorts JS logic to app.js!')

print('Successfully integrated Shorts section across all files!')
