# CountWize Website

[![Netlify Status](https://api.netlify.com/api/v1/badges/placeholder/deploy-status)](https://app.netlify.com/)
![Version](https://img.shields.io/badge/version-3.0.0-green)
![License](https://img.shields.io/badge/license-proprietary-blue)

Professional crypto recovery services website. CountWize offers secure, efficient crypto recovery services to recover lost or stolen assets with precision, using advanced tracking and forensic analysis.

## 🎯 Overview

This is a static HTML/CSS/JavaScript website deployed on Netlify with serverless functions for backend integrations. Built on a Webflow foundation with a fully custom design system.

## ✨ Key Features

- **Enterprise Design System**: 100+ CSS design tokens for colors, typography, spacing, and elevation
- **Responsive Design**: Mobile-first approach, optimized for all devices (320px - 1920px)
- **Video Education**: Vimeo-hosted educational videos with smooth lesson switching
- **Contact Forms**: Multiple contact forms with real-time validation and Telegram notifications
- **Live Chat**: LiveChat integration for real-time customer support
- **SEO Optimized**: Schema.org structured data, Open Graph, canonical URLs
- **Security Hardened**: CSP, HSTS, X-Frame-Options, and more
- **Accessibility**: WCAG AAA compliance, skip links, ARIA labels, semantic HTML

## 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Design System** | Custom CSS with Webflow foundation |
| **Hosting** | Netlify (CDN, automatic deployments) |
| **Serverless** | Netlify Functions (Node.js) |
| **Video** | Vimeo embeds with custom player |
| **Analytics** | Google Analytics 4 + Google Ads |
| **Chat** | LiveChat integration |
| **Notifications** | Telegram Bot API |
| **Fonts** | Google Fonts (Be Vietnam Pro, Poppins) |

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Arvin-DeltaX/CountWize.git
cd CountWize

# Install dependencies (for Netlify functions)
npm install

# Start a local server (Python 3)
python3 -m http.server 8000

# Or with Node.js
npx serve .

# Visit http://localhost:8000
```

### Environment Variables (for serverless functions)

Create a `.env` file or set in Netlify dashboard:

```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Production Deployment

The site deploys automatically to Netlify when changes are pushed to the `main` branch. Serverless functions in `netlify/functions/` are deployed alongside the static site.

```bash
# Push to deploy (triggers Netlify CI/CD)
git push origin main
```

## 📁 Project Structure

```
CountWize/
├── 📄 HTML Pages (24 pages)
│   ├── index.html                    # Homepage
│   ├── about-us.html                 # About page
│   ├── contact-us.html               # Contact page
│   ├── recovery.html                 # Main recovery service
│   ├── recovery-questionnaire.html   # Recovery intake form
│   ├── success.html                  # Form submission success
│   ├── crypto-recovery.html          # Recovery information
│   ├── crypto-recovery-guide.html    # Recovery guide
│   ├── crypto-education.html         # Education hub
│   ├── crypto-insights.html          # Market insights
│   ├── crypto-tax.html               # Tax information
│   ├── faq-crypto-recovery.html      # FAQ (with schema)
│   ├── team.html                     # Team page
│   ├── news.html                     # News feed
│   ├── blog.html                     # Blog listing
│   ├── privacy-policy.html           # Privacy policy
│   ├── cookie-policy.html            # Cookie policy
│   ├── legal-page.html               # Legal information
│   ├── 401.html                      # Auth error page
│   └── 404.html                      # Not found page
│
├── 📁 blog/                          # Blog articles
│   ├── forex-scams.html
│   ├── how-do-you-check-if-a-website-is-legitimate.html
│   ├── how-does-a-crypto-recovery-phrase-work.html
│   └── how-to-avoid-losing-your-crypto-*.html
│
├── 📁 netlify/functions/             # Serverless functions
│   └── telegram.js                   # Telegram bot notification handler
│
├── 📁 css/
│   ├── main.css                      # Main stylesheet (17K+ lines)
│   ├── normalize.css                 # CSS reset
│   └── webflow.css                   # Webflow base styles
│
├── 📁 js/
│   └── webflow.js                    # Webflow interactions
│
├── 📁 images/                        # Image assets (176+ files)
│   ├── *.svg                         # Vector graphics
│   ├── *.webp                        # Optimized images
│   └── *.jpg                         # Photos
│
├── 📁 documents/
│   └── countwize-iso-27001-2111-1.pdf
│
├── 📄 Configuration
│   ├── netlify.toml                  # Netlify build, headers, redirects
│   ├── package.json                  # Node dependencies (dotenv)
│   ├── robots.txt                    # Search engine directives
│   ├── sitemap.xml                   # XML sitemap
│   └── llms.txt                      # LLM context file
│
└── 📄 Documentation
    ├── README.md                     # This file
    └── CHANGELOG.md                  # Version history
```

## 🎨 Design System

The website implements a comprehensive design system (see `css/main.css`):

### Color Palette

| Variable | Value | Usage |
|----------|-------|-------|
| `--color-primary-500` | `#07B96A` | Brand green |
| `--color-neutral-900` | `#090910` | Background |
| `--color-neutral-50` | `#fcfcfc` | Text |
| `--color-error-500` | `#ef4444` | Errors |
| `--color-success-500` | `#07B96A` | Success |

### Typography

- **Body**: Be Vietnam Pro (400, 500, 600, 700)
- **Headings**: Poppins (300, 400, 500, 600, 700)
- **Scale**: 12px - 80px

### Spacing

4px base unit with scale: 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128px

### Shadows

Green-tinted brand shadows with 5 elevation levels.

## 🔒 Security

### HTTP Headers (via Netlify)

| Header | Value |
|--------|-------|
| Strict-Transport-Security | 1 year, includeSubDomains, preload |
| Content-Security-Policy | Comprehensive policy |
| X-Frame-Options | SAMEORIGIN |
| X-Content-Type-Options | nosniff |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | Restricted API access |

### CSP Domains

```
script-src:  ajax.googleapis.com, googletagmanager.com, cdnjs.cloudflare.com, player.vimeo.com
frame-src:   player.vimeo.com, vimeo.com
img-src:     i.vimeocdn.com, cdn.prod.website-files.com
connect-src: api.telegram.org, countriesnow.space, ipapi.co
```

## 📊 SEO & Structured Data

### Schema.org Markup

- **Organization**: Company information, social links
- **Service**: Crypto recovery service details
- **WebSite**: Site metadata
- **FAQPage**: FAQ with rich results
- **Article**: Blog post schema
- **BreadcrumbList**: Navigation structure

### Meta Tags

- Title tags: 50-60 characters
- Meta descriptions: 150-160 characters
- Open Graph: Full coverage
- Twitter Cards: Large image

## 🧪 Browser Support

| Browser | Version |
|---------|---------|
| Chrome | Latest 2 |
| Firefox | Latest 2 |
| Safari | Latest 2 |
| Edge | Latest 2 |
| iOS Safari | Latest 2 |
| Chrome Android | Latest 2 |

## 🐛 Troubleshooting

### Netlify Deployment Fails

**Error**: "Deploy directory 'site' does not exist"

**Solution**: The build command in `netlify.toml` creates the `site` directory. Check deploy logs for file copying errors.

### Video Not Playing

1. **CSP Blocking**: Ensure all Vimeo domains in CSP
2. **Domain Restriction**: Verify Vimeo video settings
3. **CSS Conflicts**: Check for hidden styles

**Required Vimeo Domains**:
- `player.vimeo.com` (frame-src, connect-src)
- `vimeo.com` (frame-src)
- `f.vimeocdn.com` (script-src)
- `i.vimeocdn.com` (img-src)
- `fresnel.vimeocdn.com` (connect-src)

### Console Warnings

| Warning | Explanation |
|---------|-------------|
| "License expired" | LiveChat subscription |
| "improperly configured forms" | Webflow warning (safe to ignore) |
| "overflow: visible" | Cosmetic warning |

## 📝 Development Guidelines

### Code Style

- **HTML**: 2-space indentation, semantic tags
- **CSS**: Design tokens, BEM-like naming
- **JavaScript**: ES6+, descriptive comments

### Commit Conventions

```
type: Short description

- Detailed change 1
- Detailed change 2
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `chore`

## 📈 Performance Targets

| Metric | Target |
|--------|--------|
| Lighthouse Performance | 95+ |
| Lighthouse Accessibility | 100 |
| Lighthouse Best Practices | 100 |
| Lighthouse SEO | 100 |
| LCP | < 2.5s |
| FID/INP | < 100ms |
| CLS | < 0.1 |

## 📄 License

Copyright © 2026 CountWize. All rights reserved.

## 📞 Contact

- **Website**: [countwize.co](https://countwize.co)
- **Instagram**: [@countwize_](https://www.instagram.com/countwize_)
- **LinkedIn**: [CountWize](https://www.linkedin.com/company/countwize)
- **Facebook**: [CountWize](https://www.facebook.com/profile.php?id=61572760483669)

---

*© 2026 CountWize. All rights reserved.*
