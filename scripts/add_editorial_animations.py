#!/usr/bin/env python3
"""
Adds high-performance editorial animations to styles.css, app.js, and index.html:
1. Native IntersectionObserver Scroll Reveal (fade-and-rise on scroll)
2. Interactive Stat Numbers Counter (smooth easing on viewport entry)
3. Tactile button press feedback (:active scale)
4. Floating badge subtle animation and live beacon pulse
5. Frosted glass header elevation on scroll
"""

# 1. Read files
with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('assets/js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

animation_css = """
/* ==========================================================================
   EDITORIAL ANIMATIONS & MICRO-INTERACTIONS
   ========================================================================== */

/* 1. Fluid Scroll Reveal (60fps GPU-Accelerated) */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.reveal-on-scroll.revealed {
  opacity: 1;
  transform: translateY(0);
}

/* 2. Tactile Button Click Interaction */
.btn:active {
  transform: scale(0.97) !important;
  transition: transform 0.08s ease !important;
}

/* 3. Live Broadcast Beacon Pulse */
.live-indicator-dot {
  position: relative;
}

.live-indicator-dot::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid var(--neon-lime);
  animation: beaconPulse 2.4s cubic-bezier(0.24, 0, 0.38, 1) infinite;
}

@keyframes beaconPulse {
  0% { transform: scale(0.8); opacity: 0.9; }
  60% { transform: scale(2.2); opacity: 0; }
  100% { transform: scale(2.2); opacity: 0; }
}

/* 4. Subtle Floating Glass Badge on Hero Visual */
@keyframes subtleFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.portrait-floating-card {
  animation: subtleFloat 6s ease-in-out infinite;
}

/* 5. Sticky Header Frosted Elevation Transition */
.site-header {
  transition: background-color 0.3s ease, backdrop-filter 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.site-header.scrolled {
  background: rgba(8, 8, 8, 0.9) !important;
  backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
}

@media (prefers-reduced-motion: reduce) {
  .reveal-on-scroll {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
  .portrait-floating-card,
  .live-indicator-dot::after {
    animation: none !important;
  }
}
"""

animation_js = """
  // =========================================================================
  // EDITORIAL SCROLL REVEALS & STATS COUNTER ANIMATIONS
  // =========================================================================
  function initEditorialAnimations() {
    // 1. Header scroll elevation
    const siteHeader = document.querySelector('.site-header');
    if (siteHeader) {
      const handleScroll = () => {
        if (window.scrollY > 40) {
          siteHeader.classList.add('scrolled');
        } else {
          siteHeader.classList.remove('scrolled');
        }
      };
      window.addEventListener('scroll', handleScroll, { passive: true });
      handleScroll();
    }

    // 2. Scroll Reveal Observer
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, {
        root: null,
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
      });

      const targets = document.querySelectorAll(
        '.section-header, .video-card, .short-card, .about-grid, .sponsor-banner-card, .contact-form-box'
      );
      targets.forEach(t => {
        t.classList.add('reveal-on-scroll');
        revealObserver.observe(t);
      });
    }

    // 3. Animated Stats Counter
    const statElements = document.querySelectorAll('.stat-item .stat-value, .sponsor-stat-value');
    if (statElements.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const fullText = el.textContent.trim();
            const match = fullText.match(/^([\\d.,]+)(.*)$/);
            if (match) {
              const targetVal = parseFloat(match[1].replace(/,/g, ''));
              const suffix = match[2];
              const duration = 1200;
              const startTime = performance.now();

              const frame = (now) => {
                const elapsed = now - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(targetVal * ease);
                el.textContent = current.toLocaleString() + suffix;
                if (progress < 1) {
                  requestAnimationFrame(frame);
                } else {
                  el.textContent = fullText;
                }
              };
              requestAnimationFrame(frame);
            }
            observer.unobserve(el);
          }
        });
      }, { threshold: 0.5 });

      statElements.forEach(el => counterObserver.observe(el));
    }
  }
"""

# Append CSS to styles.css
if "EDITORIAL ANIMATIONS & MICRO-INTERACTIONS" not in css:
    css = css + "\n" + animation_css
    with open('assets/css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("✓ Added animation CSS to styles.css")

# Append CSS to index.html <style>
if "EDITORIAL ANIMATIONS & MICRO-INTERACTIONS" not in html:
    idx_s_end = html.find('</style>')
    if idx_s_end != -1:
        html = html[:idx_s_end] + animation_css + '\n  ' + html[idx_s_end:]
        print("✓ Added animation CSS to index.html")

# Inject JS into app.js
if "initEditorialAnimations()" not in app_js:
    target_call = "renderShorts();"
    idx_call = app_js.rfind(target_call)
    if idx_call != -1:
        insert_pos = idx_call + len(target_call)
        app_js = app_js[:insert_pos] + "\n  initEditorialAnimations();" + app_js[insert_pos:]
        # Also append the function body right before the last closing of DOMContentLoaded
        idx_end_listener = app_js.rfind("});")
        app_js = app_js[:idx_end_listener] + "\n" + animation_js + "\n" + app_js[idx_end_listener:]
        with open('assets/js/app.js', 'w', encoding='utf-8') as f:
            f.write(app_js)
        print("✓ Added animation JS logic to app.js")

# Inject JS into index.html <script>
if "initEditorialAnimations()" not in html:
    idx_h_call = html.rfind("renderShorts();")
    if idx_h_call != -1:
        insert_h_pos = idx_h_call + len("renderShorts();")
        html = html[:insert_h_pos] + "\n  initEditorialAnimations();" + html[insert_h_pos:]
        idx_h_end_listener = html.rfind("});\n  </script>")
        if idx_h_end_listener == -1:
            idx_h_end_listener = html.rfind("});")
        html = html[:idx_h_end_listener] + "\n" + animation_js + "\n" + html[idx_h_end_listener:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Added animation JS logic to index.html")

print("Animation integration complete!")
