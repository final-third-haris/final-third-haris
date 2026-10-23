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
  initTacticalScrolly();


  // =========================================================================
  // EDITORIAL SCROLL REVEALS, PARALLAX & SCROLLSPY (OPTION B SUITE)
  // =========================================================================
  function initEditorialAnimations() {
    // 1. Header scroll elevation & Sleek Brand Scroll Progress Bar
    const siteHeader = document.querySelector('.site-header');
    const progressBar = document.getElementById('scrollProgressBar');

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

    // 3. Cinematic Hero Depth & Soft Parallax (Passive, GPU-accelerated)
    const heroWrapper = document.querySelector('.hero-portrait-wrapper');
    const heroFloatingCard = document.querySelector('.portrait-floating-card');
    const heroSection = document.getElementById('hero');

    if (heroWrapper && heroSection && window.innerWidth > 768 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      let heroTicking = false;
      const updateHeroParallax = () => {
        const scrollY = window.scrollY || document.documentElement.scrollTop;
        const heroHeight = heroSection.offsetHeight;
        if (scrollY <= heroHeight) {
          const transY = scrollY * 0.10;
          const transCardY = scrollY * 0.16;
          heroWrapper.style.transform = `translate3d(0, ${transY}px, 0)`;
          if (heroFloatingCard) {
            heroFloatingCard.style.transform = `translate3d(0, ${transCardY}px, 0)`;
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
  }

  // =========================================================================
  // TACTICAL FILM LAB: INTERACTIVE SCROLLYTELLING ANIMATION ENGINE
  // =========================================================================
  function initTacticalScrolly() {
    const scrollySection = document.getElementById('tactics');
    const pitchStage = document.getElementById('tacticalPitchStage');
    const hudPhaseLabel = document.getElementById('hudPhaseLabel');
    const hudTelemetryPill = document.getElementById('hudTelemetryPill');
    const phaseTabs = document.querySelectorAll('.phase-tab-btn');
    const scrollyCards = document.querySelectorAll('.scrolly-card');
    const playToggleBtn = document.getElementById('btnTacticalPlayToggle');
    const playToggleText = document.getElementById('tacticalPlayText');

    if (!scrollySection || !pitchStage) return;

    const phaseConfig = {
      '1': {
        label: 'PHASE 01 · PRESS BAITING',
        telemetry: 'ZONE: MIDDLE THIRD'
      },
      '2': {
        label: 'PHASE 02 · OVERLOAD CREATED',
        telemetry: '+1 NUMERICAL ADVANTAGE'
      },
      '3': {
        label: 'PHASE 03 · CUTBACK TRAJECTORY',
        telemetry: 'TARGET: PENALTY SPOT'
      },
      '4': {
        label: 'PHASE 04 · GOAL CONVERSION',
        telemetry: '0.76 xG · GOAL ACCREDITED'
      }
    };

    let activePhase = '1';
    let autoSimInterval = null;

    function setPhase(phase, syncScroll = false) {
      if (!phaseConfig[phase]) return;
      activePhase = phase;

      // 1. Update pitch stage dataset attribute (animates tokens, lines, and ball)
      pitchStage.setAttribute('data-phase', phase);

      // 2. Update HUD headers
      if (hudPhaseLabel) hudPhaseLabel.textContent = phaseConfig[phase].label;
      if (hudTelemetryPill) hudTelemetryPill.textContent = phaseConfig[phase].telemetry;

      // 3. Update tabs active state
      phaseTabs.forEach(tab => {
        const isCurrent = tab.getAttribute('data-phase-target') === phase;
        tab.classList.toggle('active', isCurrent);
        tab.setAttribute('aria-selected', isCurrent ? 'true' : 'false');
      });

      // 4. Update narrative cards active state
      scrollyCards.forEach(card => {
        const isCurrent = card.getAttribute('data-phase-card') === phase;
        card.classList.toggle('is-active', isCurrent);
      });

      // 5. Optionally smooth scroll target card into view if triggered via tab click
      if (syncScroll) {
        const targetCard = document.querySelector(`.scrolly-card[data-phase-card="${phase}"]`);
        if (targetCard) {
          const yOffset = -140;
          const y = targetCard.getBoundingClientRect().top + window.pageYOffset + yOffset;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      }
    }

    // A. IntersectionObserver for Natural Scroll-Driven Phase Sync
    if ('IntersectionObserver' in window) {
      const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const phase = entry.target.getAttribute('data-phase-card');
            if (phase && phase !== activePhase) {
              setPhase(phase, false);
            }
          }
        });
      }, {
        root: null,
        rootMargin: '-30% 0px -40% 0px',
        threshold: 0
      });

      scrollyCards.forEach(c => cardObserver.observe(c));
    }

    // B. Interactive Tab Click Handlers
    phaseTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetPhase = tab.getAttribute('data-phase-target');
        if (targetPhase) {
          stopAutoSimulation();
          setPhase(targetPhase, true);
        }
      });
    });

    // C. Auto Simulation Loop (Play/Pause)
    function startAutoSimulation() {
      if (autoSimInterval) return;
      if (playToggleBtn) {
        playToggleBtn.classList.add('playing');
        if (playToggleText) playToggleText.textContent = 'Pause Simulation';
      }
      autoSimInterval = setInterval(() => {
        const nextPhase = activePhase === '4' ? '1' : String(Number(activePhase) + 1);
        setPhase(nextPhase, false);
      }, 2600);
    }

    function stopAutoSimulation() {
      if (autoSimInterval) {
        clearInterval(autoSimInterval);
        autoSimInterval = null;
      }
      if (playToggleBtn) {
        playToggleBtn.classList.remove('playing');
        if (playToggleText) playToggleText.textContent = 'Auto Simulation';
      }
    }

    if (playToggleBtn) {
      playToggleBtn.addEventListener('click', () => {
        if (autoSimInterval) {
          stopAutoSimulation();
        } else {
          startAutoSimulation();
        }
      });
    }

    // Pause simulation if user manually scrolls the page
    window.addEventListener('scroll', () => {
      if (autoSimInterval) {
        stopAutoSimulation();
      }
    }, { passive: true });
  }

});
