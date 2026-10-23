/**
 * FINAL THIRD — Main Client Application Logic
 * Powers video catalog rendering, modal cinema playback, filtering, search, and contact interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Application State
  const state = {
    currentSport: 'all',        // 'all' | 'football' | 'cricket'
    currentPlaylist: 'all',     // 'all' | playlistId
    searchQuery: '',
    itemsPerPage: 12,           // 12 videos per page (user requested)
    visibleCount: 12,           // 12 videos on 1st page
    activeModalVideoId: null
  };

  // DOM Elements
  const videoGrid = document.getElementById('videoGrid');
  const emptyState = document.getElementById('emptyState');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const sportTabs = document.querySelectorAll('.filter-tab-btn');
  const playlistSelect = document.getElementById('playlistSelect');
  const searchInput = document.getElementById('videoSearchInput');
  const videoModal = document.getElementById('videoModal');
  const modalPlayerFrame = document.getElementById('modalPlayerFrame');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalVideoTitle = document.getElementById('modalVideoTitle');
  const modalSportBadge = document.getElementById('modalSportBadge');
  const modalPlaylistBadge = document.getElementById('modalPlaylistBadge');
  const modalMetaText = document.getElementById('modalMetaText');
  const modalWatchYtBtn = document.getElementById('modalWatchYtBtn');
  const featuredWatchStoryBtn = document.getElementById('featuredWatchStoryBtn');
  const siteHeader = document.querySelector('.site-header');
  const menuToggle = document.getElementById('menuToggle');
  const mobileNavDrawer = document.getElementById('mobileNavDrawer');
  const contactForm = document.getElementById('contactForm');
  const formFeedback = document.getElementById('formFeedback');

  // Populate Playlist Selector options from config
  function initPlaylistSelector() {
    if (!playlistSelect) return;
    playlistSelect.innerHTML = '<option value="all">All Playlists & Series</option>';

    const allPlaylists = [
      ...FINAL_THIRD_CONFIG.playlists.football,
      ...FINAL_THIRD_CONFIG.playlists.cricket
    ];

    allPlaylists.forEach(pl => {
      const opt = document.createElement('option');
      opt.value = pl.id;
      opt.textContent = `${pl.title} (${pl.sport.toUpperCase()})`;
      playlistSelect.appendChild(opt);
    });
  }

  // Filter video catalogue
  function getFilteredVideos() {
    return FINAL_THIRD_CONFIG.videos.filter(v => {
      // Sport filter
      if (state.currentSport !== 'all' && v.sport !== state.currentSport) {
        return false;
      }
      // Playlist filter
      if (state.currentPlaylist !== 'all' && v.playlistId !== state.currentPlaylist) {
        return false;
      }
      // Search query (matches Malayalam & English text)
      if (state.searchQuery.trim() !== '') {
        const query = state.searchQuery.toLowerCase();
        const matchTitle = v.title.toLowerCase().includes(query);
        const matchSummary = (v.summary || '').toLowerCase().includes(query);
        const matchPlaylist = (v.playlistTitle || '').toLowerCase().includes(query);
        if (!matchTitle && !matchSummary && !matchPlaylist) {
          return false;
        }
      }
      return true;
    });
  }

  // Render Video Grid
  function renderVideos() {
    if (!videoGrid) return;
    const filtered = getFilteredVideos();
    const visible = filtered.slice(0, state.visibleCount);

    if (visible.length === 0) {
      videoGrid.innerHTML = '';
      if (emptyState) emptyState.style.display = 'block';
      if (loadMoreBtn) loadMoreBtn.style.display = 'none';
      return;
    }

    if (emptyState) emptyState.style.display = 'none';

    videoGrid.innerHTML = visible.map((video, idx) => {
      const thumbUrl = `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`;
      const ytWatchUrl = `https://www.youtube.com/watch?v=${video.id}`;

      return `
        <article class="video-card reveal-cascade" data-video-id="${video.id}" style="--cascade-index: ${idx % 4}">
          <div class="video-thumbnail-wrap" role="button" tabindex="0" aria-label="Play video: ${escapeHtml(video.title)}">
            <img 
              src="${thumbUrl}" 
              alt="Thumbnail for ${escapeHtml(video.title)}" 
              loading="lazy" 
              width="480" 
              height="270"
            />
            <span class="card-sport-pill">${video.sport}</span>
            <div class="card-play-icon" aria-hidden="true">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            </div>
          </div>
          <div class="video-card-body">
            <div class="video-card-meta">
              <span class="playlist-name">${escapeHtml(video.playlistTitle)}</span>
              <span class="tactical-stamp"><span class="stamp-dot">●</span> ${escapeHtml(video.sport || 'SPORTS').toUpperCase()}</span>
              <span>${video.published}</span>
            </div>
            <h3 class="video-card-title" role="button" tabindex="0">${escapeHtml(video.title)}</h3>
            <p class="video-card-summary">${escapeHtml(video.summary || '')}</p>
            <div class="video-card-footer">
              <button class="card-action-link" type="button" data-video-id="${video.id}">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3" fill="currentColor"></polygon>
                </svg>
                Watch on Website
              </button>
              <a href="${ytWatchUrl}" target="_blank" rel="noopener noreferrer" class="card-external-yt" title="Watch directly on YouTube">
                YouTube ↗
              </a>
            </div>
          </div>
        </article>
      `;
    }).join('');

    if (window._revealObserver) {
      videoGrid.querySelectorAll('.reveal-cascade:not(.revealed)').forEach(el => window._revealObserver.observe(el));
    }

    initCard3DTilt();

    // Update Load More button visibility
    if (loadMoreBtn) {
      if (state.visibleCount < filtered.length) {
        loadMoreBtn.style.display = 'inline-flex';
        loadMoreBtn.textContent = `LOAD MORE (${filtered.length - state.visibleCount} REMAINING)`;
      } else {
        loadMoreBtn.style.display = 'none';
      }
    }

    // Attach click listeners to cards and buttons
    attachCardListeners();
  }

  // Open Video Lightbox Player
  function openVideoModal(videoId) {
    if (!videoId) videoId = FINAL_THIRD_CONFIG.featuredVideoId;
    const video = (FINAL_THIRD_CONFIG.videos && FINAL_THIRD_CONFIG.videos.find(v => v.id === videoId)) ||
      (FINAL_THIRD_CONFIG.shorts && FINAL_THIRD_CONFIG.shorts.find(s => s.id === videoId)) || {
      id: videoId,
      title: "Featured Story | Final Third",
      sport: "football",
      playlistTitle: "Featured Story",
      published: "Latest",
      views: ""
    };

    state.activeModalVideoId = videoId;

    const fileNotice = document.getElementById('fileProtocolNotice');
    if (fileNotice) {
      fileNotice.style.display = (window.location.protocol === 'file:') ? 'block' : 'none';
    }

    if (modalPlayerFrame) {
      modalPlayerFrame.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&enablejsapi=1`;
    }
    if (modalVideoTitle) modalVideoTitle.textContent = video.title;
    if (modalSportBadge) modalSportBadge.textContent = (video.sport || 'story').toUpperCase();
    if (modalPlaylistBadge) modalPlaylistBadge.textContent = video.playlistTitle || '';
    if (modalMetaText) modalMetaText.textContent = `${video.published || ''} ${video.views ? '· ' + video.views : ''}`;
    if (modalWatchYtBtn) modalWatchYtBtn.href = `https://www.youtube.com/watch?v=${videoId}`;
    const fallbackLink = document.getElementById('fallbackYtLink');
    if (fallbackLink) fallbackLink.href = `https://www.youtube.com/watch?v=${videoId}`;

    if (videoModal) {
      videoModal.classList.add('active');
      document.body.style.overflow = 'hidden';
      modalCloseBtn?.focus();
    }
  }

  // Expose globally so inline onclick or any caller works 100%
  window.openVideoModal = openVideoModal;

  // Close Video Lightbox Player
  function closeVideoModal() {
    if (!videoModal) return;
    videoModal.classList.remove('active');
    document.body.style.overflow = '';
    state.activeModalVideoId = null;

    // Reset iframe to stop audio playback
    if (modalPlayerFrame) {
      modalPlayerFrame.src = '';
    }
  }
  window.closeVideoModal = closeVideoModal;

  // Attach card click handlers
  function attachCardListeners() {
    document.querySelectorAll('.video-card').forEach(card => {
      const videoId = card.getAttribute('data-video-id');
      const thumb = card.querySelector('.video-thumbnail-wrap');
      const title = card.querySelector('.video-card-title');
      const actionBtn = card.querySelector('.card-action-link');

      const triggerModal = (e) => {
        if (e) e.preventDefault();
        openVideoModal(videoId);
      };

      thumb?.addEventListener('click', triggerModal);
      title?.addEventListener('click', triggerModal);
      actionBtn?.addEventListener('click', triggerModal);

      // Keyboard accessibility for cards
      thumb?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerModal();
        }
      });
      title?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          triggerModal();
        }
      });
    });
  }

  // Featured Story Modal Trigger
  const featuredPlayBtn = document.getElementById('featuredPlayBtn');
  const featuredThumbnail = document.getElementById('featuredThumbnail');
  const launchFeatured = (e) => {
    if (e) e.preventDefault();
    openVideoModal(FINAL_THIRD_CONFIG.featuredVideoId);
  };
  if (featuredPlayBtn) featuredPlayBtn.addEventListener('click', launchFeatured);
  if (featuredThumbnail) featuredThumbnail.addEventListener('click', launchFeatured);
  if (featuredWatchStoryBtn) featuredWatchStoryBtn.addEventListener('click', launchFeatured);

  // Tab Filtering
  sportTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      sportTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      state.currentSport = tab.getAttribute('data-sport') || 'all';
      state.visibleCount = state.itemsPerPage;
      renderVideos();
    });
  });

  // Playlist Selector Change
  if (playlistSelect) {
    playlistSelect.addEventListener('change', (e) => {
      state.currentPlaylist = e.target.value;
      state.visibleCount = state.itemsPerPage;
      renderVideos();
    });
  }

  // Real-time Search input
  if (searchInput) {
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        state.searchQuery = e.target.value;
        state.visibleCount = state.itemsPerPage;
        renderVideos();
      }, 200);
    });
  }

  // Load More Button
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
      state.visibleCount += state.itemsPerPage;
      renderVideos();
    });
  }

  // Modal Close Events
  modalCloseBtn?.addEventListener('click', closeVideoModal);

  videoModal?.addEventListener('click', (e) => {
    if (e.target === videoModal) {
      closeVideoModal();
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && videoModal?.classList.contains('active')) {
      closeVideoModal();
    }
  });

  // Sticky Header Scroll Effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      siteHeader?.classList.add('scrolled');
    } else {
      siteHeader?.classList.remove('scrolled');
    }
  });

  // Mobile Menu Toggle
  menuToggle?.addEventListener('click', () => {
    const isOpen = mobileNavDrawer?.classList.contains('open');
    if (isOpen) {
      mobileNavDrawer?.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    } else {
      mobileNavDrawer?.classList.add('open');
      menuToggle.setAttribute('aria-expanded', 'true');
    }
  });

  // Close Mobile Menu on link click
  document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileNavDrawer?.classList.remove('open');
      menuToggle?.setAttribute('aria-expanded', 'false');
    });
  });

  // Contact Form Mode Switcher (Dark Native Form vs Google Form)
  const tabNativeForm = document.getElementById('tabNativeForm');
  const tabGoogleForm = document.getElementById('tabGoogleForm');
  const nativeFormContainer = document.getElementById('nativeFormContainer');
  const googleFormContainer = document.getElementById('googleFormContainer');

  tabNativeForm?.addEventListener('click', () => {
    tabNativeForm.classList.add('active');
    tabGoogleForm?.classList.remove('active');
    if (nativeFormContainer) nativeFormContainer.style.display = 'block';
    if (googleFormContainer) googleFormContainer.style.display = 'none';
  });

  tabGoogleForm?.addEventListener('click', () => {
    tabGoogleForm.classList.add('active');
    tabNativeForm?.classList.remove('active');
    if (nativeFormContainer) nativeFormContainer.style.display = 'none';
    if (googleFormContainer) googleFormContainer.style.display = 'block';
    if (typeof gtag === 'function') {
      gtag('event', 'view_google_form_tab', {
        event_category: 'Lead Generation',
        event_label: 'Google Form Tab'
      });
    }
  });

  // Contact Form Submission (Direct Email Dispatch + GA4/GTM Lead Tracking + WhatsApp Fallback)
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('contactName')?.value.trim();
      const email = document.getElementById('contactEmail')?.value.trim();
      const phone = document.getElementById('contactPhone')?.value.trim();
      const purpose = document.getElementById('contactPurpose')?.value.trim() || 'General Inquiry';
      const brand = document.getElementById('contactBrand')?.value.trim() || 'N/A';
      const message = document.getElementById('contactMessage')?.value.trim();
      const submitBtn = document.getElementById('contactSubmitBtn');

      if (!name || !email || !phone || !purpose || !message) {
        showFormFeedback('error', 'Please fill in all required fields (Name, Email, WhatsApp Number, Purpose, Message).');
        return;
      }

      // Email format check
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        showFormFeedback('error', 'Please enter a valid email address.');
        return;
      }

      // 1. Google Analytics 4 Lead Conversion Tracking
      if (typeof gtag === 'function') {
        gtag('event', 'generate_lead', {
          event_category: 'Contact Form',
          event_label: purpose,
          lead_name: name,
          lead_email: email
        });
      }

      // 2. Google Tag Manager dataLayer Event Tracking
      if (window.dataLayer) {
        window.dataLayer.push({
          event: 'generate_lead',
          leadPurpose: purpose,
          trafficReferrer: document.referrer || 'direct'
        });
      }

      const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '<span>SEND INQUIRY ↗</span>';
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>SENDING INQUIRY...</span>';
      }

      try {
        // Direct zero-friction dispatch to Haris Nenmara via FormSubmit AJAX
        const response = await fetch('https://formsubmit.co/ajax/mailtofinalthird@gmail.com', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            _subject: `New Inquiry from Final Third Site: ${name} [${purpose}]`,
            Name: name,
            Email: email,
            WhatsApp_Phone: phone,
            Inquiry_Purpose: purpose,
            Brand_Turf_Name: brand,
            Proposal_Message: message,
            Traffic_Source: document.referrer || 'Direct Site Visit'
          })
        });

        showFormFeedback('success', `✅ Thank you, ${name}! Your inquiry has been sent directly to Haris Nenmara (mailtofinalthird@gmail.com). We will review your details and respond within 24 to 48 hours.`);
        renderDirectContactFallbacks(name, email, phone, purpose, message);
        contactForm.reset();

      } catch (err) {
        console.warn('Direct email dispatch notification:', err);
        showFormFeedback('success', `Thank you, ${name}! Your inquiry has been prepared. Click below to deliver your message instantly to Haris Nenmara via WhatsApp or Email:`);
        renderDirectContactFallbacks(name, email, phone, purpose, message);
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHtml;
        }
      }
    });
  }

  function renderDirectContactFallbacks(name, email, phone, subject, message) {
    const waMsg = encodeURIComponent(`Hi Haris (Final Third),\n\nName: ${name}\nEmail: ${email}\nPhone: ${phone || 'N/A'}\nSubject: ${subject}\n\nMessage:\n${message}`);
    const fallbackContainer = document.createElement('div');
    fallbackContainer.style.marginTop = '16px';
    fallbackContainer.style.display = 'flex';
    fallbackContainer.style.gap = '12px';
    fallbackContainer.style.flexWrap = 'wrap';
    fallbackContainer.innerHTML = `
      <a href="https://wa.me/918129059309?text=${waMsg}" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="padding: 10px 18px; font-size: 0.85rem;">
        Send via WhatsApp ↗
      </a>
      <a href="mailto:mailtofinalthird@gmail.com?subject=${encodeURIComponent(subject)}&body=${waMsg}" class="btn btn-outline" style="padding: 10px 18px; font-size: 0.85rem;">
        Send via Email ↗
      </a>
    `;
    formFeedback.appendChild(fallbackContainer);
  }

  function showFormFeedback(type, htmlText) {
    if (!formFeedback) return;
    formFeedback.className = `form-feedback ${type}`;
    formFeedback.innerHTML = htmlText;
    formFeedback.style.display = 'block';
  }

  // Track Google Form clicks into GA4 & GTM
  ['channelGoogleFormLink', 'openGoogleFormExternalBtn'].forEach(btnId => {
    document.getElementById(btnId)?.addEventListener('click', () => {
      if (typeof gtag === 'function') {
        gtag('event', 'click_google_form', {
          event_category: 'Lead Generation',
          event_label: 'Official Google Form External'
        });
      }
      if (window.dataLayer) {
        window.dataLayer.push({
          event: 'click_google_form',
          form_url: 'https://forms.gle/ysMKP3Njy3WVpz986'
        });
      }
    });
  });

  // Smooth scroll for Back to Top
  document.getElementById('backToTopBtn')?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Helper function to sanitize HTML output
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Initialize
  
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

    shortsShelf.innerHTML = visibleShorts.map((short, idx) => {
      const thumb = `https://i.ytimg.com/vi/${short.id}/hqdefault.jpg`;
      const sportLabel = (short.sport || 'Sports').toUpperCase();

      return `
        <article class="short-card reveal-cascade" data-short-id="${short.id}" role="button" tabindex="0" aria-label="Play Short: ${escapeHtml(short.title)}" style="--cascade-index: ${idx % 4}">
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

    if (window._revealObserver) {
      shortsShelf.querySelectorAll('.reveal-cascade:not(.revealed)').forEach(el => window._revealObserver.observe(el));
    }

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

  initPlaylistSelector();
  renderVideos();
  renderShorts();
  initEditorialAnimations();
  renderSpotlightVideo();
  initCard3DTilt();
  initCustomCursor();
  initPlaybook();


  // =========================================================================
  // EDITORIAL SCROLL REVEALS, PARALLAX & SCROLLSPY (OPTION B SUITE)
  // =========================================================================
  function initEditorialAnimations() {
    // 1. Header scroll elevation, Progress Bar & Ambient Space Motes Parallax
    const siteHeader = document.querySelector('.site-header');
    const progressBar = document.getElementById('scrollProgressBar');
    const spaceMotesLayer = document.getElementById('spaceMotesLayer');

    const updateScrollState = () => {
      const scrollY = window.scrollY || document.documentElement.scrollTop;
      if (siteHeader) {
        if (scrollY > 40) {
          siteHeader.classList.add('scrolled');
        } else {
          siteHeader.classList.remove('scrolled');
        }
      }

      if (progressBar && !window.CSS?.supports?.('animation-timeline', 'scroll()')) {
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;
        progressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
      }

      if (spaceMotesLayer && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        const bgOffset = (scrollY * 0.12) % 400;
        spaceMotesLayer.style.transform = `translate3d(0, -${bgOffset}px, 0)`;
      }
    };

    let scrollTicking = false;
    window.addEventListener('scroll', () => {
      if (!scrollTicking) {
        window.requestAnimationFrame(() => {
          updateScrollState();
          scrollTicking = false;
        });
        scrollTicking = true;
      }
    }, { passive: true });
    updateScrollState();

    // 2. Scroll Reveal & Staggered Cascade Observer
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
      const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            observer.unobserve(entry.target);
          }
        });
      }, {
        root: null,
        threshold: 0.08,
        rootMargin: '0px 0px -40px 0px'
      });

      window._revealObserver = revealObserver;

      const targets = document.querySelectorAll(
        '.section-header, .featured-match-card, .video-card, .short-card, .about-grid, .sponsor-banner-card, .contact-form-box'
      );
      targets.forEach(t => {
        if (!t.classList.contains('reveal-cascade')) {
          t.classList.add('reveal-on-scroll');
        }
        revealObserver.observe(t);
      });
    }

    // 3. Cinematic Hero Depth, Dissolve & Multi-Plane Parallax (Passive, GPU-accelerated)
    const heroWrapper = document.querySelector('.hero-portrait-wrapper');
    const heroFloatingCard = document.querySelector('.portrait-floating-card');
    const heroContent = document.querySelector('.hero-content');
    const heroSection = document.getElementById('hero');

    if (heroWrapper && heroSection && window.innerWidth > 768 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      let heroTicking = false;
      const updateHeroParallax = () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop;
        const heroHeight = heroSection.offsetHeight;
        if (scrollY <= heroHeight) {
          const transY = scrollY * 0.10;
          const transCardY = scrollY * 0.22;
          const portraitScale = Math.max(0.96, 1 - (scrollY * 0.00008));
          heroWrapper.style.transform = `translate3d(0, ${transY}px, 0) scale(${portraitScale})`;
          if (heroFloatingCard) {
            heroFloatingCard.style.transform = `translate3d(0, ${transCardY}px, 0)`;
          }
          if (heroContent) {
            const contentY = scrollY * 0.14;
            const contentOpacity = Math.max(0.15, 1 - (scrollY / (heroHeight * 0.85)));
            heroContent.style.transform = `translate3d(0, ${contentY}px, 0)`;
            heroContent.style.opacity = contentOpacity;
          }
        }
        heroTicking = false;
      };

      window.addEventListener('scroll', () => {
        if (!heroTicking) {
          window.requestAnimationFrame(updateHeroParallax);
          heroTicking = true;
        }
      }, { passive: true });
    }

    // 4. Scrollspy Active Navigation Indicator
    const sections = document.querySelectorAll('section[id], header#hero');
    const navLinks = document.querySelectorAll('.nav-link');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

    if ('IntersectionObserver' in window && sections.length) {
      const scrollspyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            const targetHref = `#${id}`;

            navLinks.forEach(link => {
              if (link.getAttribute('href') === targetHref) {
                link.classList.add('active');
              } else {
                link.classList.remove('active');
              }
            });

            mobileNavLinks.forEach(link => {
              if (link.getAttribute('href') === targetHref) {
                link.classList.add('active');
              } else {
                link.classList.remove('active');
              }
            });
          }
        });
      }, {
        root: null,
        rootMargin: '-25% 0px -60% 0px',
        threshold: 0
      });

      sections.forEach(sec => scrollspyObserver.observe(sec));
    }

    // 5. Animated Stats Counter
    const statElements = document.querySelectorAll('.stat-item .stat-value, .sponsor-stat-value');
    if (statElements.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
      const counterObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const fullText = el.textContent.trim();
            const match = fullText.match(/^([\d.,]+)(.*)$/);
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



  // =========================================================================
  // DYNAMIC SPOTLIGHT ANALYSIS (ALWAYS AUTOMATICALLY USES LATEST VIDEO)
  // =========================================================================
  function renderSpotlightVideo() {
    if (typeof FINAL_THIRD_CONFIG === 'undefined' || !FINAL_THIRD_CONFIG.videos || FINAL_THIRD_CONFIG.videos.length === 0) return;

    // Always automatically pick the newest full-length episode (index 0)
    const latest = FINAL_THIRD_CONFIG.videos[0];
    FINAL_THIRD_CONFIG.featuredVideoId = latest.id;

    const thumbContainer = document.getElementById('featuredThumbnail');
    const headline = document.getElementById('featuredHeadline');
    const summary = document.querySelector('.featured-summary');
    const sportBadge = document.querySelector('.featured-tag-bar .badge-tag');
    const metaSpan = document.querySelector('.featured-tag-bar span:last-child');
    const watchStoryBtn = document.getElementById('featuredWatchStoryBtn');
    const watchYtBtn = document.querySelector('.featured-actions a.btn-outline');

    if (thumbContainer) {
      thumbContainer.onclick = () => openVideoModal(latest.id);
      thumbContainer.setAttribute('aria-label', `Play featured story: ${latest.title}`);
      const img = thumbContainer.querySelector('img');
      if (img) {
        img.src = `https://i.ytimg.com/vi/${latest.id}/maxresdefault.jpg`;
        img.alt = `Spotlight Analysis Thumbnail: ${latest.title}`;
        img.onerror = function() {
          this.src = `https://i.ytimg.com/vi/${latest.id}/hqdefault.jpg`;
        };
      }
    }

    if (headline) {
      headline.textContent = latest.title;
      headline.onclick = () => openVideoModal(latest.id);
    }

    if (summary) {
      summary.textContent = latest.summary || latest.title;
    }

    if (sportBadge) {
      sportBadge.textContent = (latest.sport || 'Sports').toUpperCase();
    }

    if (metaSpan) {
      const plTitle = latest.playlistTitle || 'Latest Release';
      const pubTime = latest.published || 'Latest';
      metaSpan.textContent = `${plTitle} · Latest Upload · ${pubTime}`;
    }

    if (watchStoryBtn) {
      watchStoryBtn.onclick = () => openVideoModal(latest.id);
    }

    if (watchYtBtn) {
      watchYtBtn.href = `https://www.youtube.com/watch?v=${latest.id}`;
    }

    initCard3DTilt();
  }

  // =========================================================================
  // 3D CARD PERSPECTIVE TILT & DYNAMIC GLASS SHEEN
  // =========================================================================
  function initCard3DTilt() {
    if (window.matchMedia('(pointer: coarse)').matches || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const cards = document.querySelectorAll('.video-card, .featured-match-card, .playbook-card');
    cards.forEach(card => {
      if (card._tiltAttached) return;
      card._tiltAttached = true;

      let sheen = card.querySelector('.card-glass-sheen');
      if (!sheen) {
        sheen = document.createElement('div');
        sheen.className = 'card-glass-sheen';
        sheen.setAttribute('aria-hidden', 'true');
        card.appendChild(sheen);
      }

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -3.5;
        const rotateY = ((x - centerX) / centerX) * 3.5;

        card.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.01, 1.01, 1.01)`;
        sheen.style.background = `radial-gradient(circle at ${(x / rect.width * 100).toFixed(1)}% ${(y / rect.height * 100).toFixed(1)}%, rgba(255,255,255,0.08) 0%, transparent 60%)`;
        sheen.style.opacity = '1';
      }, { passive: true });

      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
        sheen.style.opacity = '0';
      });
    });
  }

  // =========================================================================
  // MAGNETIC CUSTOM CURSOR WITH CONTEXTUAL PILL STATES
  // =========================================================================
  function initCustomCursor() {
    if (window.matchMedia('(pointer: coarse)').matches || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const cursor = document.getElementById('customCursor');
    const cursorText = document.getElementById('cursorText');
    if (!cursor) return;

    let mouseX = -100, mouseY = -100;
    let curX = -100, curY = -100;
    let isMoving = false;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      if (!isMoving) {
        isMoving = true;
        cursor.style.opacity = '1';
      }
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
      isMoving = false;
    });

    function updateCursor() {
      curX += (mouseX - curX) * 0.22;
      curY += (mouseY - curY) * 0.22;
      cursor.style.transform = `translate3d(${curX}px, ${curY}px, 0)`;
      requestAnimationFrame(updateCursor);
    }
    requestAnimationFrame(updateCursor);

    document.addEventListener('mouseover', (e) => {
      const mediaTarget = e.target.closest('.video-card, .short-card, .featured-media-container, .playbook-pitch-wrap');
      const buttonTarget = e.target.closest('.btn, .nav-link, .mobile-nav-link, .filter-pill, .social-card, .playbook-tab');

      if (mediaTarget) {
        cursor.classList.add('cursor-media');
        cursor.classList.remove('cursor-hover');
        if (cursorText) {
          cursorText.textContent = mediaTarget.classList.contains('playbook-pitch-wrap') ? 'TACTICS' : 'WATCH';
        }
      } else if (buttonTarget) {
        cursor.classList.add('cursor-hover');
        cursor.classList.remove('cursor-media');
      } else {
        cursor.classList.remove('cursor-media', 'cursor-hover');
      }
    }, { passive: true });
  }

  // =========================================================================
  // SIGNATURE INTERACTIVE TACTICAL PLAYBOOK LAB
  // =========================================================================
  function initPlaybook() {
    const tabs = document.querySelectorAll('.playbook-tab');
    const arrowsGroup = document.getElementById('tacticalArrowsGroup');
    const playersGroup = document.getElementById('tacticalPlayersGroup');
    const badgeEl = document.getElementById('dossierBadge');
    const titleEl = document.getElementById('dossierTitle');
    const descEl = document.getElementById('dossierDesc');
    const objEl = document.getElementById('metricObjective');
    const zoneEl = document.getElementById('metricZone');
    const xgEl = document.getElementById('metricXg');
    const quoteEl = document.getElementById('dossierQuote');

    if (!tabs.length || !arrowsGroup || !playersGroup) return;

    const tactics = {
      overload: {
        badge: '[ ATTACKING PHASE // 4-3-3 ]',
        title: 'The Half-Space Overload',
        desc: "Manipulating the opponent's backline by pinning the fullback with the winger (#11) while the attacking midfielder (#8) surges into the channel.",
        obj: 'Create 2v1 qualitative superiority against fullback',
        zone: 'Left Half-Space (Zone 14 Edge)',
        xg: '+0.38 xG shot probability per sequence',
        quote: '"When the fullback commits to the touchline, that pocket between center-back and fullback is undefendable if timed at top speed."',
        players: [
          { num: '6', x: 250, y: 200, role: 'Pivot', team: 'home' },
          { num: '8', x: 440, y: 140, role: 'Half-Space Runner', team: 'home', highlight: true },
          { num: '11', x: 490, y: 65, role: 'Touchline Winger', team: 'home' },
          { num: '9', x: 480, y: 200, role: 'Target 9', team: 'home' },
          { num: '2', x: 450, y: 80, role: 'Opponent Fullback', team: 'opp' },
          { num: '4', x: 490, y: 160, role: 'Opponent Center-Back', team: 'opp' }
        ],
        arrows: [
          '<path d="M 265 190 Q 370 120 475 75" fill="none" stroke="var(--neon-lime)" stroke-width="2.5" stroke-dasharray="6,4" class="anim-pass"/>',
          '<path d="M 480 80 L 448 125" fill="none" stroke="var(--neon-lime)" stroke-width="2.5" stroke-dasharray="4,4" class="anim-pass"/>',
          '<path d="M 440 140 Q 480 140 520 160" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="2" marker-end="url(#arrowhead)" stroke-dasharray="4,4"/>',
          '<path d="M 520 160 L 510 195" fill="none" stroke="var(--neon-lime)" stroke-width="3" marker-end="url(#arrowhead)"/>'
        ]
      },
      press: {
        badge: '[ DEFENSIVE TRANSITION // HIGH-PRESS ]',
        title: 'The High-Press Funnel Trap',
        desc: 'Curving the pressing angle from the center forward to eliminate the switch of play, forcing the opponent goalkeeper or center-back into a trapped touchline duel.',
        obj: "Force turnover within 4 seconds in opponent's defensive third",
        zone: 'Touchline Press Trap (Attacking Right)',
        xg: 'High-value turnover resulting in immediate +0.45 xG counter',
        quote: '"A great press isn\'t about running tirelessly; it\'s about closing the angles so the ball carrier has only one bad pass available."',
        players: [
          { num: '9', x: 470, y: 220, role: 'Curving 9', team: 'home', highlight: true },
          { num: '7', x: 440, y: 310, role: 'Trigger Winger', team: 'home', highlight: true },
          { num: '10', x: 380, y: 190, role: 'Pivot Lock', team: 'home' },
          { num: 'GK', x: 560, y: 200, role: 'Opponent Keeper', team: 'opp' },
          { num: 'CB', x: 500, y: 260, role: 'Target CB', team: 'opp' },
          { num: 'LB', x: 450, y: 340, role: 'Trapped LB', team: 'opp' }
        ],
        arrows: [
          '<path d="M 545 205 L 515 250" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2" stroke-dasharray="4,4"/>',
          '<path d="M 450 170 Q 470 210 490 245" fill="none" stroke="var(--neon-lime)" stroke-width="3" marker-end="url(#arrowhead)"/>',
          '<path d="M 410 290 L 440 325" fill="none" stroke="var(--neon-lime)" stroke-width="3" marker-end="url(#arrowhead)"/>',
          '<circle cx="475" cy="300" r="30" fill="rgba(158,226,11,0.12)" stroke="var(--neon-lime)" stroke-width="1.5" stroke-dasharray="4,4"/>'
        ]
      },
      transition: {
        badge: '[ VERTICAL COUNTER // 3RD MAN RUN ]',
        title: 'The Direct Third-Man Combination',
        desc: 'Vertical punch pass into the dropping striker, drawing the center-back out of line, while the blind-side winger bursts through the vacant corridor.',
        obj: 'Break two defensive lines with maximum 3 touches',
        zone: 'Central Corridor to Blind-Side Box',
        xg: '+0.52 xG breakaway chance on goal',
        quote: '"The third man is always free because the defense is watching the passer and the receiver—never the runner arriving from deep."',
        players: [
          { num: '6', x: 230, y: 200, role: 'Deep Passer', team: 'home' },
          { num: '9', x: 400, y: 200, role: 'False 9 / Wall', team: 'home' },
          { num: '7', x: 490, y: 230, role: 'Blind-Side Sprinter', team: 'home', highlight: true },
          { num: 'CB', x: 440, y: 190, role: 'Pulled CB', team: 'opp' },
          { num: 'CB', x: 490, y: 160, role: 'Covering CB', team: 'opp' }
        ],
        arrows: [
          '<path d="M 245 200 L 385 200" fill="none" stroke="var(--neon-lime)" stroke-width="3" stroke-dasharray="5,3"/>',
          '<path d="M 405 205 L 435 240" fill="none" stroke="var(--neon-lime)" stroke-width="2.5" stroke-dasharray="3,3"/>',
          '<path d="M 360 280 Q 430 260 485 235" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5" marker-end="url(#arrowhead)"/>',
          '<path d="M 495 230 L 555 205" fill="none" stroke="var(--neon-lime)" stroke-width="3" marker-end="url(#arrowhead)"/>'
        ]
      }
    };

    function renderTactic(key) {
      const data = tactics[key];
      if (!data) return;

      badgeEl.textContent = data.badge;
      titleEl.textContent = data.title;
      descEl.textContent = data.desc;
      objEl.textContent = data.obj;
      zoneEl.textContent = data.zone;
      xgEl.textContent = data.xg;
      quoteEl.textContent = data.quote;

      let defs = document.getElementById('tacticalDefs');
      if (!defs) {
        defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        defs.id = 'tacticalDefs';
        defs.innerHTML = `
          <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" fill="#9EE20B" />
          </marker>
        `;
        arrowsGroup.parentNode.insertBefore(defs, arrowsGroup);
      }

      arrowsGroup.innerHTML = data.arrows.join('');

      playersGroup.innerHTML = data.players.map(p => {
        const isHome = p.team === 'home';
        const bgFill = isHome ? (p.highlight ? 'var(--neon-lime)' : '#1A1C20') : '#E63946';
        const textFill = isHome ? (p.highlight ? '#080808' : '#FFFFFF') : '#FFFFFF';
        const strokeColor = isHome ? (p.highlight ? 'none' : 'var(--neon-lime)') : '#FFFFFF';
        const halo = p.highlight ? `<circle cx="${p.x}" cy="${p.y}" r="22" fill="rgba(158,226,11,0.22)" class="player-halo"/>` : '';

        return `
          <g class="player-node">
            ${halo}
            <circle cx="${p.x}" cy="${p.y}" r="14" fill="${bgFill}" stroke="${strokeColor}" stroke-width="2" class="player-circle"/>
            <text x="${p.x}" y="${p.y + 4}" fill="${textFill}" font-size="10" font-weight="800" text-anchor="middle" font-family="sans-serif">${p.num}</text>
          </g>
        `;
      }).join('');
    }

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        const tacticKey = tab.getAttribute('data-tactic');
        renderTactic(tacticKey);
      });
    });

    renderTactic('overload');
  }


});
