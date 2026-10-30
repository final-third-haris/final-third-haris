# Final Third — YouTube Caption Integration & Daily Automation Setup

This document outlines the architecture, security, and setup instructions for the automated daily synchronization and Malayalam caption processing pipeline on **Final Third** ([https://www.finalthird-haris.com/](https://www.finalthird-haris.com/)).

---

## 1. System Architecture & Caption Grounding Protocol

Haris Nenmara uploads authentic Malayalam subtitles/captions with his YouTube videos. These captions serve as the **primary source of truth** for all website descriptions, tactical takeaways, and match analysis.

### Factual Integrity & Automation Principles:
1. **Never Invent Details:** If a tactical point, player formation, coach strategy, or match incident is absent from the broadcast transcript, it will never be fabricated.
2. **Transcript Coverage Evaluation:**
   - **Complete Captions (>= 8 cues, >= 130 words, >= 60s):** Automatically generates a natural Malayalam summary, accurate English translation, discussion points, takeaways, and verified tags. Status: `published` (`✓ Grounded in Verified Complete Broadcast Transcript`).
   - **Partial Captions (Excerpts):** Generates summary limited strictly to the spoken excerpt, clearly labeled as `published_partial` (`ℹ Grounded in Broadcast Excerpt`).
   - **Missing or Failed Captions:** Publishes a clean, neutral metadata overview without pretending it is transcript-based. Transparent status: `awaiting_transcript` (`⏳ Awaiting Broadcast Transcript Verification`). Retries automatically on future daily runs.
3. **No Manual Work Required:** The pipeline is 100% autonomous. New uploads are detected, categorized, summarized, and published to production automatically without requiring manual approval.
4. **Accurate Shorts Detection:** Uses YouTube's official HTTP redirect behavior on `https://www.youtube.com/shorts/{id}` (HTTP 200 = Short, HTTP 303 = Full Video) plus duration and hashtag validation to ensure Shorts go to the Shorts shelf and never become full-length SEO article pages.
5. **Unified Catalog Sync:** When a new video or short is processed, it is automatically added to both `FINAL_THIRD_CONFIG` in `index.html` and `assets/js/config.js` and prepended to the homepage grids.
6. **Optional Admin CLI:** While the system is fully automated, the local CLI tool (`scripts/content_review.py`) remains available for inspecting, importing local subtitle files, or manually editing records.

---

## 2. YouTube Data API v3 & OAuth 2.0 Requirements

### Why OAuth is Required:
The YouTube Data API endpoint `captions.list` can be queried with an API key, but `captions.download` **strictly requires OAuth 2.0 authorization** with the channel owner's account and the scope:
```
https://www.googleapis.com/auth/youtube.force-ssl
```
This protects private caption tracks and ensures only the authorized channel owner can export raw subtitle files.

---

## 3. Step-by-Step Google Cloud Setup

### Step 3.1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown at the top and select **New Project**.
3. Name it **Final Third Automation** and click **Create**.

### Step 3.2: Enable YouTube Data API v3
1. In the Google Cloud Console, navigate to **APIs & Services > Library**.
2. Search for **YouTube Data API v3**.
3. Click on it and select **Enable**.

### Step 3.3: Configure the OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**.
2. Select User Type **External** and click **Create**.
3. Fill in:
   - **App name:** Final Third Caption Sync
   - **User support email:** Your Google email address
   - **Developer contact information:** Your email address
4. Click **Save and Continue**.
5. Under **Scopes**, click **Add or Remove Scopes**, add `https://www.googleapis.com/auth/youtube.force-ssl`, and click **Update**.
6. Under **Test users**, click **Add Users** and enter the Google Account email associated with the `@FinalThird_HarisNenmara` YouTube channel.
7. Click **Save and Continue**.

### Step 3.4: Create OAuth 2.0 Client ID Credentials
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Application type: Select **Desktop app** (or **Web application** with Authorized redirect URIs set to `http://localhost:8080`).
4. Name: `Final Third Automation Client`.
5. Click **Create**.
6. Copy your **Client ID** and **Client Secret**.

---

## 4. One-Click OAuth Token Generation

We have included a dedicated interactive helper script in the repository:

```bash
python3 scripts/get_youtube_oauth_token.py
```

### What happens when you run this script:
1. It prompts you for your `Client ID` and `Client Secret`.
2. It automatically opens your browser to Google's consent screen.
3. Sign in with Haris Nenmara's channel Google account and grant access.
4. The local script catches the redirect callback on `http://localhost:8080`.
5. It prints your long-lived **Refresh Token** directly in your terminal.

---

## 5. Configuring GitHub Repository Secrets

To enable the daily GitHub Actions workflow:

1. Open your GitHub repository in your browser: `https://github.com/final-third-haris/final-third-haris`.
2. Go to **Settings > Secrets and variables > Actions**.
3. Click **New repository secret** for each of the following:

| Secret Name | Value Description |
|---|---|
| `YOUTUBE_CLIENT_ID` | Your Google Cloud OAuth Client ID |
| `YOUTUBE_CLIENT_SECRET` | Your Google Cloud OAuth Client Secret |
| `YOUTUBE_REFRESH_TOKEN` | The refresh token generated in Step 4 |
| `YOUTUBE_API_KEY` | *(Optional)* Google Cloud YouTube API Key |

> **Security Note:** These secrets are stored encrypted inside GitHub and are only accessible inside server-side GitHub Actions runners. They are **never** exposed in frontend JavaScript, HTML, or client-side assets.

---

## 6. Automated Daily Execution & Vercel Auto-Deployment

The workflow is defined in `.github/workflows/daily_youtube_sync.yml`.

### How It Works:
1. **Schedule:** Runs automatically every day at `06:00 UTC` (11:30 AM IST). Can also be triggered manually anytime via the GitHub Actions tab (`Run workflow`).
2. **Channel Polling:** Detects new videos on `@FinalThird_HarisNenmara`.
3. **Sport Classification:** Categorizes new uploads into Football or Cricket using playlist and keyword matching.
4. **Caption Retrieval:** Downloads Malayalam subtitles via authorized YouTube Data API, strips timestamps, and generates grounded summaries.
5. **Page Generation:** Generates dedicated SEO pages, updates category hubs (`/football/` and `/cricket/`), and updates `sitemap.xml`.
6. **Vercel Deployment:** Commits changes back to `main`, which automatically triggers Vercel's zero-downtime production deployment.

---

## 7. Editorial CLI & Manual Transcript Review

If you prefer to manually import transcripts or approve drafts before publication:

### Check Status of All Videos:
```bash
python3 scripts/content_review.py list
```

### Import a Local `.srt` or `.vtt` Subtitle File:
```bash
python3 scripts/content_review.py import-transcript <VIDEO_ID> path/to/transcript.srt
```

### Approve a Video for Publication:
```bash
python3 scripts/content_review.py approve <VIDEO_ID>
```

### Rebuild Website Pages After Updates:
```bash
python3 scripts/content_review.py build
```
