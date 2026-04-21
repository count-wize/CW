# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CountWize is a static HTML/CSS/JavaScript website for cryptocurrency recovery services. It uses no framework (React, Vue, etc.) - just vanilla HTML5, CSS3, and JavaScript with a Webflow foundation. Deployed on Netlify with automatic CI/CD from the `main` branch.

## Development Commands

```bash
# Start local server (Python 3)
python3 -m http.server 8000

# Or with Node.js
npx serve .

# Visit http://localhost:8000
```

There is no package.json, no npm scripts, no build tools, and no test framework. The site is purely static files.

## Deployment

Push to `main` branch triggers automatic Netlify deployment. The build process (defined in `netlify.toml`) copies all files to a `site/` directory:
1. HTML files from root
2. SEO files (robots.txt, sitemap.xml)
3. Static assets (css/, js/, images/, documents/)
4. Blog content (blog/)

## Architecture

### File Structure
- **Root HTML files**: 23 pages (index.html, about-us.html, contact-us.html, recovery.html, etc.)
- **blog/**: 4 article HTML files
- **css/**: main.css (design system, 17K+ lines), webflow.css (framework), normalize.css
- **js/**: webflow.js (minified interaction engine)
- **images/**: 176 files (SVG vectors, WebP optimized images, JPG photos)

### Design System (css/main.css)

CSS custom properties define the design tokens:

| Token Pattern | Example | Usage |
|---------------|---------|-------|
| `--color-primary-*` | `--color-primary-500: #07B96A` | Brand green palette |
| `--color-neutral-*` | `--color-neutral-900: #090910` | Grayscale |
| `--font-size-*` | `--font-size-lg` | Typography scale (12px-80px) |
| `--spacing-*` | `--spacing-4` | 4px base unit spacing |
| `--shadow-*` | `--shadow-lg` | Green-tinted elevation |

Fonts: Be Vietnam Pro (body), Poppins (headings) via Google Fonts.

### Responsive Breakpoints
- Mobile: 320px - 767px
- Tablet: 768px - 991px
- Desktop: 992px - 1920px

## Key Integrations

- **Analytics**: Google Analytics 4 (GA-0NX03W5PQR) + Google Ads (AW-447543988)
- **Video**: Vimeo embeds with custom player
- **Chat**: LiveChat integration
- **Phone Input**: intl-tel-input library for international phone validation
- **Forms**: Submit to countwiseapi.space and telegram-vercel-seven.vercel.app

## Security Configuration

Security headers are configured in `netlify.toml`. When adding new external resources:

1. Check CSP (Content-Security-Policy) allows the domain
2. Add to appropriate directive: script-src, style-src, frame-src, connect-src, img-src, etc.
3. Required Vimeo domains: player.vimeo.com, vimeo.com, f.vimeocdn.com, i.vimeocdn.com, fresnel.vimeocdn.com

## SEO Requirements

When adding/modifying pages:
- Update `sitemap.xml` with new URLs
- Add Schema.org JSON-LD markup (Organization, Service, BreadcrumbList, etc.)
- Include meta title (50-60 chars), description (150-160 chars), Open Graph tags
- Ensure canonical URL is set

## Code Conventions

- HTML: 2-space indentation, semantic HTML5 tags
- CSS: Use existing design tokens, BEM-like class naming
- Commit format: `type: Short description` (types: feat, fix, docs, style, refactor, perf, chore)

## Common Issues

**Video not playing**: Check CSP in netlify.toml includes all Vimeo domains.

**Deploy fails with "site directory does not exist"**: Check netlify.toml build command for file copying errors.

**Console warnings**: "License expired" (LiveChat), "improperly configured forms" (Webflow) are safe to ignore.
