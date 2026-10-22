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
    itemsPerPage: 12,
    visibleCount: 12,
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

    videoGrid.innerHTML = visible.map(video => {
      const thumbUrl = `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`;
      const ytWatchUrl = `https://www.youtube.com/watch?v=${video.id}`;

      return `
        <article class="video-card" data-video-id="${video.id}">
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
    const video = FINAL_THIRD_CONFIG.videos.find(v => v.id === videoId) || {
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
  initPlaylistSelector();
  renderVideos();
});
