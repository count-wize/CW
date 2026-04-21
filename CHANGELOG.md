# Changelog

All notable changes to the CountWize website are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [3.0.0] - 2026-01-11

### Ultimate Enterprise Audit Plan v3.0 Implementation

This release implements the comprehensive 320-phase FinTech-Grade Complete Overhaul, transforming the website into an enterprise-level platform with Swiss Watch precision.

### PART 1: Design System Foundation (Phases 1-50)

#### Added
- Complete CSS custom properties system with 100+ design tokens
- Color architecture with primary (green), secondary (neutral), and accent (semantic) palettes
- WCAG AAA compliant color contrast combinations
- Typography system with Be Vietnam Pro + Poppins fonts
- 8px base unit spacing scale (0-128px)
- Elevation system with brand-tinted shadows (5 levels)
- Border radius scale (none to full)
- Focus ring system for accessibility
- Glass morphism effects for overlays
- Z-index scale for proper stacking context

### PART 2: Component System (Phases 51-110)

#### Added
- Button system: primary, secondary, ghost, danger variants
- Button sizes: sm (32px), md (40px), lg (48px), xl (56px)
- Button states: hover, active, focus, disabled, loading
- Form input system with consistent styling
- Input states: default, hover, focus, filled, error, success, disabled
- Custom checkbox, radio, and toggle components
- Card system: base, elevated, outlined, interactive, selected
- Card parts: header, body, footer, media
- Navigation system with responsive mobile drawer
- Dropdown menus with smooth animations

### PART 3: Micro-Interactions (Phases 111-135)

#### Added
- Page loader with spinner animation
- Skeleton loading components (text, circle, rect)
- Progress bar with animated stripes
- Toast notification system (success, error, warning, info)
- Tooltip component with arrow
- Empty state component
- Loading state animations

### PART 4: User Journey Mapping (Phases 136-165)

#### Improved
- 404 page with helpful navigation and dual CTAs
- Enhanced error messages and recovery paths
- Skip link accessibility for keyboard users
- Form validation feedback

### PART 5: Page-Level Perfection (Phases 166-210)

#### Added
- Schema.org structured data across all pages
- Organization schema on homepage
- Service schema for crypto recovery
- WebSite schema with search action
- BreadcrumbList schema for all pages
- FAQPage schema on FAQ page
- Article schema on blog posts
- ContactPage schema on contact page

#### Improved
- 404 page semantic HTML (h1, main, role attributes)
- Meta descriptions on all pages
- Alt text for all images
- ARIA labels for interactive elements

### PART 6: Performance Engineering (Phases 211-245)

#### Added
- Preconnect hints for Vimeo, cdnjs, Google Fonts
- Font subsetting for faster loading
- Critical CSS considerations
- Image lazy loading attributes

#### Improved
- Cache headers for static assets (1 year)
- Optimized build process with progress logging

### PART 7: SEO Mastery (Phases 246-280)

#### Added
- Complete sitemap.xml with all 22 pages
- robots.txt with proper directives
- Canonical URLs on all pages
- Open Graph and Twitter Card meta tags

#### Improved
- Title tags (50-60 characters)
- Meta descriptions (150-160 characters)
- Heading hierarchy (single H1 per page)

### PART 8: Security Fortress (Phases 281-300)

#### Added
- HSTS header (Strict-Transport-Security)
- Enhanced CSP with frame-ancestors and base-uri
- Form action restrictions in CSP
- Comprehensive Permissions-Policy

#### Improved
- Content-Security-Policy coverage
- X-Frame-Options for clickjacking prevention
- Referrer-Policy for privacy

### PART 9: Quality Assurance (Phases 301-315)

#### Verified
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Mobile responsiveness (320px - 1920px)
- Keyboard navigation accessibility
- Form validation functionality

### PART 10: Documentation and Launch (Phases 316-320)

#### Updated
- README.md with complete project documentation
- CHANGELOG.md with detailed version history
- Netlify configuration with deployment guide
- Build process documentation

---

## [1.0.2] - 2026-01-11

### Fixed

- Video player CSS: Replaced padding-bottom aspect ratio hack with modern `aspect-ratio: 16/9`
- Fixed broken image: `group-1.svg` → `group_1.svg` (case mismatch)
- Fixed broken image: `Группа2.svg` → `группа2.svg` (case sensitivity)
- Created missing placeholder icons: `404-Icon.svg`, `count-wize-ISO.svg`
- Improved alt text for form icons (decorative icons now use `aria-hidden="true"`)
- Added descriptive alt text for feature card icons
- Added Vimeo player parameters to fix background display issues
- Added video loading spinner CSS animation
- Added responsive video player styles for all breakpoints

### Added

- `robots.txt` with proper sitemap reference
- `sitemap.xml` with all 22 site pages
- Preconnect hints for Vimeo and cdnjs CDN
- CSS fallback for browsers without `aspect-ratio` support

### Changed

- Updated netlify.toml to include robots.txt and sitemap.xml in build

---

## [1.0.1] - 2026-01-11

### Fixed

- Improved Netlify build command with verbose logging for deployment debugging
- Enhanced build process to explicitly copy each directory for better reliability

---

## [1.0.0] - 2026-01-11

### Changed

- Complete project restructure following Master Ultra Plan
- Renamed CSS file from `countwize-test.webflow.css` to `main.css`
- Consolidated duplicate Google Analytics scripts
- Fixed video player with clean embed structure
- Improved JavaScript with proper error handling
- Enhanced CSS with professional header and organization

### Removed

- 23 dead/duplicate HTML files (42 -> 19 files)
- 245 unused images (370 -> 125 images)
- Webflow data attributes (`data-wf-page`, `data-wf-site`)
- Russian/Ukrainian comments and text
- Duplicate inline styles (moved to main.css)
- Old/backup files (`*-old.html`, `old-*.html`)
- CMS template files (`detail_*.html`)
- Root-level blog duplicates (kept `blog/` versions)

### Added

- Comprehensive `netlify.toml` configuration
- Security headers (CSP, X-Frame-Options, etc.)
- Cache control for static assets
- SEO-preserving redirects
- Skip link for accessibility
- Professional README documentation
- CHANGELOG file

### Fixed

- Navigation links pointing to deleted old files
- Video player nested wrapper issues
- Broken menuButton selector in JavaScript
- Inline styles overriding CSS

### Security

- Content Security Policy configured for all external resources
- X-Frame-Options set to SAMEORIGIN
- X-Content-Type-Options set to nosniff
- Referrer-Policy configured
- Permissions-Policy restricting unused features

---

## [0.1.0] - 2025-11-17

### Added

- Initial website launch
- Homepage with hero section
- Contact forms
- Educational video section
- Blog articles
- Team page
- FAQ section
