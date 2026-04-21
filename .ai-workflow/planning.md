# CountWize Website - Fix Implementation Plan

**Project:** CountWize Website Issues Resolution  
**Plan Version:** 1.0  
**Date:** January 21, 2026  
**Planning System:** AI Workflow System v4.0  
**Source:** Combined analysis of R1.md and R2.md audit reports

---

## Overview

This plan addresses **23+ distinct issues** identified across two comprehensive audits of the CountWize website. Issues are organized into 4 phases based on severity and impact, prioritizing functional blockers and user-facing problems before optimization and polish.

**Total Tasks:** 23  
- **PHASE A (Critical):** 5 tasks - Broken functionality, navigation, compatibility
- **PHASE B (High Priority):** 5 tasks - Visual inconsistencies, performance bottlenecks
- **PHASE C (Medium Priority):** 7 tasks - SEO, code quality, content errors
- **PHASE D (Low Priority):** 6 tasks - Accessibility, file organization, polish

---

## PHASE A: Critical - Broken Functionality & Navigation

### Task A1: Fix Broken Start Recovery Navigation Link
**Priority:** Critical  
**Files:** `index.html`

The "Start" button in the hero alternative section (line 320) links to `/recovery-questionnaire` without the `.html` extension, causing 404 errors on static hosting environments.

**Required Actions:**
1. Open `index.html` and locate line 320
2. Update the href from `/recovery-questionnaire` to `/recovery-questionnaire.html`
3. Test the link to ensure it properly navigates to the recovery questionnaire page

---

### Task A2: Resolve Non-ASCII Filename Compatibility Issue
**Priority:** Critical  
**Files:** `images/группа2.svg`, all HTML files referencing this image

The file `группа2.svg` (Cyrillic characters) exists in the images directory and will cause 404 errors on many web servers and file systems that don't properly handle non-ASCII characters.

**Required Actions:**
1. Rename `images/группа2.svg` to `images/group2.svg`
2. Search all HTML files for references to `группа2.svg` and update them to `group2.svg`
3. Verify the image displays correctly across all pages after renaming

---

### Task A3: Fix Video Player Cross-Origin Security Error
**Priority:** Critical  
**Files:** `index.html`

The Vimeo video player in the "Discover CountWize" section (lines 414-426) displays as a black/blank box due to SecurityError: "Blocked a frame with origin" cross-origin access issue.

**Required Actions:**
1. Verify the Vimeo video ID `1061354345` is correct and the video is not set to private
2. Check Vimeo embed settings to ensure the domain is whitelisted for embedding
3. Test alternative embed parameters or consider adding the video to an allowed domains list
4. If the video ID is incorrect or private, obtain the correct public video ID and update line 418

---

### Task A4: Implement Recovery Form Processing Backend
**Priority:** Critical  
**Files:** `recovery-questionnaire.html`

The recovery questionnaire form has no defined backend endpoint for the `action` attribute, meaning user submissions may go nowhere if the Webflow form handler isn't properly configured.

**Required Actions:**
1. Review the form element in `recovery-questionnaire.html` to identify the current action/submission configuration
2. Implement or verify a backend endpoint for form processing (Webflow handler, custom API, or email service)
3. Add proper form validation and success/error messaging
4. Test the complete form submission flow from frontend to backend

---

### Task A5: Fix Handpicked News Feed Broken Links
**Priority:** Critical  
**Files:** `index.html`, potentially external API integration files

Multiple news cards in the "Handpicked News" section display "Cannot load link" error messages, indicating broken data fetching, dead external links, or API integration failure.

**Required Actions:**
1. Identify the data source for the news feed (API endpoint, RSS feed, or static data)
2. Test all news feed URLs to identify which links are broken
3. Update or replace broken links with working alternatives
4. If using an API, verify the API key, endpoint URL, and response format are correct
5. Implement error handling to gracefully display when news items fail to load

---

## PHASE B: High Priority - Visual & Performance Issues

### Task B1: Optimize Severely Bloated Images for Performance
**Priority:** High  
**Files:** `images/05e6b...1.jpg`, `images/a5100d73...png`, `images/3.jpg`, `images/1.jpg`

Multiple images are catastrophically large (2.25MB, 1.92MB, 1.5MB, 1.06MB), causing severe page load performance issues and poor Mobile LCP scores.

**Required Actions:**
1. Identify all images over 500KB in the images directory
2. Convert images to modern formats (WebP or AVIF) with 80-85% quality
3. Resize images to their actual display dimensions (not full resolution)
4. Replace original files with optimized versions
5. Update HTML img tags to use responsive srcset if images are displayed at multiple sizes
6. Test page load speed before and after optimization to verify improvements

---

### Task B2: Fix CoinPress Logo Size Inconsistency
**Priority:** High  
**Files:** `index.html`, `css/main.css`

The CoinPress logo (line 360 in index.html) is significantly smaller and thinner than the other platform logos (Binance, Medium, Barchart, Digital Journal), breaking visual harmony in the "Our Supported Platforms" section.

**Required Actions:**
1. Inspect the CoinPress SVG file (`images/vector-1_3.svg`) to check intrinsic dimensions
2. Add CSS rules to ensure minimum width/height matching other logos (target ~120-150px width)
3. Alternatively, replace the SVG with a properly sized version
4. Verify all platform logos align consistently at the same visual weight

---

### Task B3: Fix Third Service Icon Missing Glow Effect
**Priority:** High  
**Files:** `index.html`, `images/group_1.svg`, `css/main.css`

The third service card "Lost Assets? We'll Find Them" (lines 550-558) has an icon that appears dark/turned off while the first two cards have bright green glowing icons.

**Required Actions:**
1. Compare the SVG files: `group_1.svg` (3rd icon) vs `glyph.svg` and `group.svg` (1st and 2nd icons)
2. Identify the fill color or glow effect difference in the SVG markup
3. Update `group_1.svg` to match the green glow appearance of the other icons
4. Alternatively, add CSS filters or animations to create the glow effect consistently

---

### Task B4: Fix Mindmap Circle Border Visibility Issue
**Priority:** High  
**Files:** `index.html`, `css/main.css`

The decorative circular glow behind the mindmap/branching section (lines 675-725) has a visible hard white/gray border at its lower edge that doesn't blend smoothly into the black background.

**Required Actions:**
1. Locate the `.circle-block` class in `main.css` (lines 18032-18044)
2. Increase the blur filter value from 100px to 150-200px for softer edges
3. Check if parent container has `overflow: hidden` that might be clipping the blur
4. Consider increasing the circle size or adjusting opacity to improve the blend
5. Test the effect on different screen sizes to ensure consistent appearance

---

### Task B5: Fix Social News Ticker Logo Clipping and Text Overlap
**Priority:** High  
**Files:** `index.html`, `css/main.css`

The scrolling news ticker (lines 730-800) displays fragmented text like "inDe CoinDesk", "Decry Decrypt", and "ne Bl The Block" due to logo clipping and improper text overlay.

**Required Actions:**
1. Inspect the `.div-block-152` container and child elements for height/overflow constraints
2. Adjust container height to accommodate full logo and text height
3. Fix text positioning to prevent overlap with logo images
4. Ensure proper spacing between news items in the ticker animation
5. Test the ticker scroll animation at different viewport widths

---

## PHASE C: Medium Priority - SEO, Code Quality & Content

### Task C1: Fix Duplicate Text Content in Mindmap Cards
**Priority:** Medium  
**Files:** `index.html`

The "Lost Crypto?" card (line 706) and "Security?" card (line 716) have identical description text about crypto recovery, which appears to be a copy-paste placeholder error.

**Required Actions:**
1. Review the "Security?" card content requirements with stakeholders
2. Write unique, appropriate description text for the Security card
3. Update line 716 in `index.html` with the new Security-focused content
4. Verify all other mindmap cards have unique, relevant descriptions

---

### Task C2: Fix Typo - "Specialis" to "Specialist"
**Priority:** Medium  
**Files:** `index.html`

Team member position is misspelled as "Compliance & Data Specialis" instead of "Compliance & Data Specialist" on line 627.

**Required Actions:**
1. Open `index.html` and locate line 627
2. Update the text from "Specialis" to "Specialist"
3. Search for any other instances of this typo across all HTML files

---

### Task C3: Add Missing Structured Data to Subpages
**Priority:** Medium  
**Files:** `about-us.html`, `recovery-questionnaire.html`, `contact-us.html`

While `index.html` has excellent Schema.org markup, key subpages are missing BreadcrumbList, Service/Organization schema, and OG:Image tags for proper SEO.

**Required Actions:**
1. Add BreadcrumbList Schema.org markup to all subpages for search result navigation
2. Duplicate appropriate Organization schema from `index.html` to relevant subpages
3. Add `og:image` meta tags to `recovery-questionnaire.html` and other pages missing them
4. Validate all Schema markup using Google's Structured Data Testing Tool
5. Ensure consistent organization/brand information across all pages

---

### Task C4: Update Insecure HTTP Links to HTTPS
**Priority:** Medium  
**Files:** `cookie-policy.html`, `privacy-policy.html`, potentially other policy pages

Links using `http://` instead of `https://` trigger "Not Secure" warnings in browsers and violate modern security best practices.

**Required Actions:**
1. Search all HTML files for `href="http://` references
2. Update all http:// links to https:// equivalents
3. Verify that all external links properly redirect or serve content over HTTPS
4. Test all updated links to ensure they resolve correctly

---

### Task C5: Replace Empty Hash Links with Proper Handlers
**Priority:** Medium  
**Files:** All HTML files (`contact-us.html`, `news.html`, `index.html`, etc.)

Numerous anchor tags use `href="#"` which causes unexpected page jumps to the top, creating jarring UX.

**Required Actions:**
1. Search all HTML files for `href="#"` occurrences
2. For links that should have no action, replace with `href="javascript:void(0)"`
3. For interactive elements that aren't links, convert `<a>` tags to `<button>` tags
4. Add proper click handlers where needed for functional interactions
5. Test all previously hash-linked elements to ensure they behave correctly

---

### Task C6: Remove Heavy Inline Styles and !important Overrides
**Priority:** Medium  
**Files:** `index.html`, `css/main.css`

Inline styles with `!important` declarations (e.g., line 362: `style="opacity:1!important;visibility:visible!important..."`) make the code unmaintainable and override-resistant.

**Required Actions:**
1. Identify all instances of inline styles with `!important` in HTML files
2. Move these styles to appropriate CSS classes in `main.css`
3. Remove `!important` declarations and use proper CSS specificity instead
4. Update HTML elements to use the new CSS classes
5. Test styling to ensure visual appearance remains identical

---

### Task C7: Refactor Repetitive Recovery Questionnaire JavaScript
**Priority:** Medium  
**Files:** `recovery-questionnaire.html`, create new `js/recovery-form.js`

The "Other" option toggle script is copy-pasted identically for every single question (lines 269, 328, 390, 526, 588, etc.), creating bloated, unmaintainable code.

**Required Actions:**
1. Create a new file `js/recovery-form.js`
2. Write a single reusable function `handleRadioToggle(groupId, inputId)` that handles all cases
3. Replace all inline script blocks in `recovery-questionnaire.html` with calls to this function
4. Add the new JS file reference to the HTML
5. Test all radio button interactions to ensure they still work correctly
6. Reduce overall file size and improve maintainability

---

## PHASE D: Low Priority - Accessibility, Polish & Cleanup

### Task D1: Improve Alt Text Descriptiveness and Consistency
**Priority:** Low  
**Files:** All HTML files

Functional images have inconsistent alt text implementation - some use descriptive text, others use `alt=""` without proper `role="presentation"`, and logos just say "Logo" instead of descriptive text.

**Required Actions:**
1. Audit all `<img>` tags across all HTML files
2. For decorative images, ensure they have both `alt=""` AND `aria-hidden="true"`
3. For functional images, add descriptive alt text (e.g., "Email icon" not just "")
4. Update logo alt text from "Logo" to "CountWize Home" or "CountWize - Crypto Recovery Service"
5. Verify all images meet WCAG accessibility standards

---

### Task D2: Standardize Image Filename Conventions
**Priority:** Low  
**Files:** `images/` directory, all HTML files

The images directory has inconsistent naming: typo "toutube-icon.svg" (should be youtube), mixing dashes and underscores (vector-1.svg vs vector_1.svg), and duplicate formats (ethereum.png vs ethereum-1.webp).

**Required Actions:**
1. Create a standardized naming convention (e.g., kebab-case: word-word.ext)
2. Rename all files to follow the standard: `toutube-icon.svg` → `youtube-icon.svg`
3. Consolidate duplicate formats (choose WebP over PNG where possible)
4. Update all HTML references to renamed files
5. Document the naming convention for future asset additions

---

### Task D3: Implement Dynamic Date System for News Items
**Priority:** Low  
**Files:** `index.html`, potentially create `js/news-dates.js`

News items in the "Social News" section (lines 740, 763, 786) have hardcoded static dates ("Jan 15, 2026", "Jan 14, 2026") that will become stale and look unprofessional.

**Required Actions:**
1. Identify if news items are from a dynamic feed or static content
2. If static, add data attributes with relative dates (e.g., `data-days-ago="6"`)
3. Create JavaScript to convert relative dates to formatted display dates
4. Update the dates dynamically on page load based on current date
5. Alternatively, fetch news from an API that provides fresh dates

---

### Task D4: Fix Form Validation Error Message Display
**Priority:** Low  
**Files:** `index.html`, `css/main.css`

Phone validation error message (line 243) has `class="hide"` applied inline, which may prevent the error from ever displaying if the "hide" class isn't properly toggled by JavaScript.

**Required Actions:**
1. Review the JavaScript that controls the error message visibility
2. Verify that the "hide" class is properly toggled on validation
3. Test form validation to ensure errors display correctly
4. Consider using `display: none` in CSS instead of a "hide" class for better control
5. Ensure error messages are accessible to screen readers

---

### Task D5: Add rel="nofollow" to External Partner Links
**Priority:** Low  
**Files:** All HTML files with external links

External links to partners (Binance, Medium, CoinPress, etc.) have `rel="noopener noreferrer"` but would benefit from `rel="nofollow"` for SEO best practices, especially for sponsored/partner links.

**Required Actions:**
1. Identify all external partner/sponsor links across all pages
2. Update rel attributes to `rel="noopener noreferrer nofollow"` for paid/partner links
3. Keep `rel="noopener noreferrer"` without nofollow for editorial/organic links
4. Document which types of links should use nofollow for future reference

---

### Task D6: Optimize Large SVG File Sizes
**Priority:** Low  
**Files:** `images/vector-1_4.svg` and other large SVG files

The file `vector-1_4.svg` is ~30KB (29,827 bytes) which could be optimized for faster loading and better performance.

**Required Actions:**
1. Identify all SVG files over 10KB in the images directory
2. Use SVGO or similar tool to optimize SVG files (remove metadata, simplify paths)
3. Verify optimized SVGs render identically to originals
4. Replace original files with optimized versions
5. Document target maximum SVG file size for future assets

---

## Implementation Notes

**Execution Order:**
- Complete all PHASE A tasks first (critical blockers)
- Move to PHASE B (user-facing visual issues)
- Address PHASE C (quality and SEO improvements)
- Finish with PHASE D (polish and optimization)

**Testing Requirements:**
- Test all fixes in Chrome, Firefox, and Safari
- Verify mobile responsiveness on iOS and Android
- Run Lighthouse audits before and after to measure improvements
- Validate all HTML and CSS after changes

**Backup Strategy:**
- Create a full backup before starting PHASE A
- Commit changes to version control after each completed task
- Tag releases after completing each phase

---

**End of Plan**
