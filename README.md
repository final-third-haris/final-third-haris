# FINAL THIRD — Premium Sports Media Website
Featuring **Haris Nenmara**

Official website for **FINAL THIRD**, the premier Malayalam sports broadcasting and journalism brand covering in-depth football analysis and cricket stories beyond the scoreboard.

---

## ⚡ Brand System
* **Brand Name:** FINAL THIRD
* **Host / Personality:** Haris Nenmara
* **Primary Accent Color:** `#9EE20B` (Official Neon Lime)
* **Background:** `#080808` (Pitch Black)
* **Surface:** `#151515` (Charcoal)
* **Typeface:** **Anek Malayalam** (Supports both native Malayalam script and Latin characters with perfect rendering across macOS, Windows, iOS, and Android).

---

## 📁 Project Architecture
```
final-third/
├── index.html                  # Core production HTML, SEO meta tags, Open Graph & Schema.org JSON-LD
├── sitemap.xml                 # XML Sitemap with Google Video extension
├── robots.txt                  # Search engine crawler directives
├── assets/
│   ├── images/
│   │   ├── final-third-logo-lime.png    # Official logo recolored to #9EE20B
│   │   ├── final-third-logo-white.png   # Secondary logo variant
│   │   ├── haris-nenmara.jpg            # Authentic portrait of Haris Nenmara
│   │   └── stadium-bg.svg               # Tactical stadium markings and floodlight glow
│   ├── css/
│   │   └── styles.css                   # Responsive styles, dark mode, cinema lightbox
│   └── js/
│       ├── config.js                    # Centralized brand, playlists, and video catalogue
│       └── app.js                       # Video modal playback, search, filter tabs & forms
└── README.md                   # Documentation & maintainer guide
```

---

## 🚀 How to Run Locally

### Option 1: Python HTTP Server (Recommended)
From inside this directory:
```bash
python3 -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

### Option 2: Direct File Open
You can also directly double-click or open `index.html` in any modern web browser.

---

## 🛠️ Maintainer Guide: Updating Content & Playlists

To add new videos, change playlists, or update contact info, you only need to edit **`assets/js/config.js`**:
* **Update Featured Story:** Change `featuredVideoId` to any YouTube video ID.
* **Add New Videos:** Append a new object into `FINAL_THIRD_CONFIG.videos`:
  ```javascript
  {
    id: "YOUTUBE_VIDEO_ID",
    title: "Video title in Malayalam",
    sport: "football", // or "cricket"
    playlistId: "kbfc-isl",
    playlistTitle: "Kerala Blasters & Indian Football",
    published: "Just now",
    views: "50K views",
    summary: "Brief tactical recap..."
  }
  ```
* **Update Contact Details:** Change phone, WhatsApp, or email directly in `FINAL_THIRD_CONFIG.contact`.

---

## 🌐 Deploying to Production
You can deploy this website in less than 60 seconds with 100% free hosting:
1. **Cloudflare Pages:** Connect repository or run `npx wrangler pages deploy .`
2. **Vercel:** Run `vercel` or drag-and-drop the `final-third` folder into the Vercel dashboard.
3. **Netlify:** Drag-and-drop this folder into [app.netlify.com/drop](https://app.netlify.com/drop).
4. **GitHub Pages:** Push this folder to a GitHub repository and enable Pages under Settings.
