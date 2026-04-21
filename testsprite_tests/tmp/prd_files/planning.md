# CountWize QA Implementation Plan
## Actionable Bug Fix Plan for Claude Code

**Total Issues:** 41  
**Priority Phases:** 4  
**Estimated Timeline:** 14 days

---

## Quick Reference

| Phase | Focus | Days | Issues |
|-------|-------|------|--------|
| 1 | Critical Infrastructure | 1-3 | 11 |
| 2 | Content Integrity | 4-7 | 10 |
| 3 | Brand Consistency | 8-10 | 16 |
| 4 | Layout Polish | 11-14 | 6 |

---

## Phase 1: Critical Infrastructure (Days 1-3)

> ⚠️ **CRITICAL:** These issues render major features unusable. Fix immediately.

---

### Task 1.1: Fix Embedded Content Failures
**Issues:** #005, #039  
**Complexity:** Complex

**Files to Modify:**
- `about-us.html` — Line ~295
- `index.html` — Line ~337 (lightbox JSON)
- `netlify.toml` — CSP headers (if needed)

**What to Change:**

Replace Embedly wrapper iframes with direct Vimeo embeds:

```html
<!-- BEFORE (broken): -->
<iframe class="embedly-embed" src="https://cdn.embedly.com/widgets/media.html?src=https%3A%2F%2Fplayer.vimeo.com..." ...></iframe>

<!-- AFTER (fixed): -->
<iframe 
  src="https://player.vimeo.com/video/1061354345?title=0&byline=0&portrait=0&dnt=1&badge=0&controls=1&color=07B96A" 
  style="border: none; background-color: #000;"
  allow="autoplay; fullscreen; picture-in-picture; encrypted-media"
  allowfullscreen
  title="CountWize"
></iframe>
```

**Acceptance Criteria:**
- [ ] Embedded content loads without error on About page
- [ ] Embedded content loads without error on Home page
- [ ] No "content blocked" message visible to users

---

### Task 1.2: Fix Video Player Integration
**Issues:** #022, #037, #040  
**Complexity:** Complex

**Files to Modify:**
- `index.html` — Hero video button (~line 327), Lessons section
- `crypto-education.html` — Lessons For You section

**What to Change:**

**Fix #037 (Hero video button redirects to registration):**
```html
<!-- BEFORE (deceptive): -->
<a href="/recovery-questionnaire.html" class="watch-video-btn">Watch video</a>

<!-- AFTER option A - actual video link: -->
<a href="https://vimeo.com/1061354345" class="watch-video-btn" target="_blank">Watch video</a>

<!-- AFTER option B - remove if no video exists: -->
<!-- Delete the entire watch-video element -->
```

**Fix #022, #040 (Video cards non-functional):**
Verify lesson cards have proper click handlers - they already have `data-video-url` attributes, ensure JavaScript is switching the player iframe src.

**Acceptance Criteria:**
- [ ] "Watch video" hero button plays a video (not registration redirect)
- [ ] OR hero "Watch video" button is removed if no video exists
- [ ] Lesson cards on Home and Education pages play videos when clicked

---

### Task 1.3: Fix News Feed Integration
**Issues:** #030, #031, #032, #033, #034, #041  
**Complexity:** Complex

**Files to Modify:**
- `index.html` — Social News section (~line 1160+)
- `news.html` — All news sections

**What to Change:**

Replace placeholder cards with curated static content:

```html
<!-- BEFORE (placeholder): -->
<div id="source-name1" class="source-name-new">Binance Twitter</div>
<div id="time-since1" class="time-since-new">3h ago</div>
<div id="title-link1" class="title-link-new">Text Link</div>
<a id="buttonLink1" href="#">...</a>

<!-- AFTER (real content): -->
<div id="source-name1" class="source-name-new">CoinDesk</div>
<div id="time-since1" class="time-since-new">Jan 15, 2026</div>
<div id="title-link1" class="title-link-new">Bitcoin Hits New All-Time High Amid ETF Inflows</div>
<a id="buttonLink1" href="https://coindesk.com/article-url" target="_blank" rel="noopener">...</a>
```

**For duplicate articles (#033):** Ensure each Trending card has unique content.

**Acceptance Criteria:**
- [ ] No "Cannot load link" errors visible
- [ ] No identical placeholder cards ("Binance Twitter", "3h ago")
- [ ] All news links work and open external articles
- [ ] No duplicate articles in Trending section

---

## Phase 2: Content Integrity (Days 4-7)

> **IMPORTANT:** Fix broken images and misplaced content affecting visual quality.

---

### Task 2.1: Fix Missing/Broken Images
**Issues:** #002, #009, #011, #014, #023  
**Complexity:** Medium

**Files to Modify:**
- `about-us.html` — Mission & Vision icons (~line 168, 173)
- `crypto-recovery-guide.html` — Multiple broken images
- `crypto-education.html` — Book covers
- `images/` — May need new assets

**What to Change:**

**#002 (Mission & Vision use same icon):**
```html
<!-- BEFORE: -->
<img src="images/vector_2.svg" loading="lazy" alt="icon"> <!-- Used for both -->

<!-- AFTER: -->
<!-- Mission: Use target/compass icon -->
<img src="images/mission-icon.svg" loading="lazy" alt="Our Mission">
<!-- Vision: Use telescope/eye icon -->
<img src="images/vision-icon.svg" loading="lazy" alt="Our Vision">
```

**#009 (5 recovery reason cards missing icons):**
Create/upload icons for:
1. Loss of recovery phrase → key icon
2. Phishing → hook icon
3. Erroneous translation → wrong arrow icon
4. Malicious software → bug icon
5. Unreliable network → broken wifi icon

**#011, #014:** Search for `alt="bitcoin"` and `alt="crypto-recovery"` and fix image paths.

**Acceptance Criteria:**
- [ ] Mission and Vision show distinct, contextual icons
- [ ] All 5 recovery reason cards show relevant icons
- [ ] All section images display properly

---

### Task 2.2: Remove Misplaced Images from Text
**Issues:** #016, #020  
**Complexity:** Simple

**Files to Modify:**
- `crypto-recovery-guide.html` — Real Case Example section
- `crypto-education.html` — EBooks description

**What to Change:**

**#016:**
```html
<!-- BEFORE: -->
<p>If your crypto is compromised<img src="..." alt="using an unreliable network">lost...</p>

<!-- AFTER: -->
<p>If your crypto is compromised or access is lost, contact us immediately.</p>
```

**#020:**
```html
<!-- BEFORE: -->
<p>...to s<img alt="lesson cover">ahead in the world...</p>

<!-- AFTER: -->
<p>...to stay ahead in the world of crypto, blockchain, and finance.</p>
```

**Acceptance Criteria:**
- [ ] No alt text visible within paragraph content
- [ ] Text reads smoothly without embedded images

---

### Task 2.3: Fix Empty Team Section
**Issues:** #004  
**Complexity:** Medium

**Files to Modify:**
- `about-us.html` — Experts section

**What to Change:**

Option A: The team content already exists (~line 264-283). Verify it's rendering.

Option B: Add link to team.html:
```html
<a href="team.html" class="btn">Meet Our Full Team →</a>
```

Option C: Remove empty section heading if no content planned.

**Acceptance Criteria:**
- [ ] Section shows team members, links to team.html, or is removed

---

### Task 2.4: Fix Wrong Video in EBooks
**Issues:** #021  
**Complexity:** Simple

**Files to Modify:**
- `crypto-education.html` — EBooks section

**What to Change:**
```html
<!-- Option A: Replace with correct video -->
<button onclick="playVideo('CORRECT_EBOOK_VIDEO_ID')">Play video</button>

<!-- Option B: Change CTA to match section -->
<a href="#books-section" class="btn">Browse eBooks</a>
```

**Acceptance Criteria:**
- [ ] Video button plays eBook-related content OR CTA matches section purpose

---

### Task 2.5: Fix Platform Links
**Issues:** #038  
**Complexity:** Simple

**Files to Modify:**
- `index.html` — Supported Platforms section (~line 387-395)

**What to Change:**

Verify links work (they appear to already have real URLs):
```html
<a href="https://www.binance.com/en/square/post/22994522805130" target="_blank">
  <img src="images/binance_logo-1.svg" alt="Binance">
</a>
```

If any platform link is dead, either update URL or remove logo.

**Acceptance Criteria:**
- [ ] Each platform logo links to actual CountWize content
- [ ] OR misleading logos removed if no actual presence

---

## Phase 3: Brand Consistency (Days 8-10)

> **WARNING:** Brand name must be "CountWize" everywhere. No variations.

---

### Task 3.1: Fix "Count Wise" → "CountWize" (Site-wide)
**Issues:** #003, #018, #019 + many more  
**Complexity:** Simple (bulk find/replace)

**Files to Modify:**
- `about-us.html` — Line 186
- `faq-crypto-recovery.html` — Lines 242, 248, 274, 282, 287, 300, 313, 352
- `crypto-tax.html` — Lines 361, 367, 372, 378, 383, 400, 427
- `crypto-recovery.html` — Lines 356, 361, 387, 395, 400, 413, 426, 465
- `crypto-recovery-guide.html` — Line 449+
- `team.html` — Lines 115, 182, 188, 193, 199, 204, 221, 248
- `recovery.html` — Lines 264, 628, 661, 672, 677, 685, 707, 718
- `blog.html` — Lines 249, 254, 280, 288, 293, 306, 319, 358

**What to Change:**
```bash
# Bulk replacement:
sed -i 's/Count Wise/CountWize/g' *.html
```

```html
<!-- BEFORE: -->
<h2>Core Values Guiding Count Wise</h2>
<div class="faq-question">What services does Count Wise offer?</div>

<!-- AFTER: -->
<h2>Core Values Guiding CountWize</h2>
<div class="faq-question">What services does CountWize offer?</div>
```

**Acceptance Criteria:**
- [ ] Zero instances of "Count Wise" (two words) in codebase
- [ ] `grep -r "Count Wise" *.html` returns empty

---

### Task 3.2: Fix "Count Wize" → "CountWize"
**Issues:** #026  
**Complexity:** Simple

**Files to Modify:**
- `blog.html` — Line 139

**What to Change:**
```html
<!-- BEFORE: -->
<h1 class="hero-heading"><span class="highlighted-word">Blog</span> Count Wize</h1>

<!-- AFTER: -->
<h1 class="hero-heading"><span class="highlighted-word">Blog</span> CountWize</h1>
```

**Acceptance Criteria:**
- [ ] Blog page header reads "Blog CountWize"

---

### Task 3.3: Remove Dashes from Content (Site-wide)
**Issues:** #001, #007, #008, #010, #012, #013, #015, #017, #028, #029, #035  
**Complexity:** Medium (requires judgment)

**Files to Modify:**
- `about-us.html` — Hero headline (line 139)
- `index.html` — Hero headline (line 245)
- `crypto-recovery.html` — Multiple sections
- `crypto-recovery-guide.html` — Multiple sections
- `blog/` — Blog posts

**What to Change:**

| Pattern | Replacement |
|---------|-------------|
| `Services—Handled` | `Services. Handled.` |
| `-Your Assets` | `Your Assets` |
| `Crypto Recovery - Lost` | `Crypto Recovery: Lost` |
| `happens - don't` | `happens, don't` |
| `consultation-just` | `consultation. Just` |

```html
<!-- BEFORE (#035): -->
<h1>Crypto Recovery <br>Services—Handled</h1>

<!-- AFTER: -->
<h1>Crypto Recovery <br>Services. Handled.</h1>
```

```html
<!-- BEFORE (#001): -->
<h1>Your Trusted Tool Recovery Services<br>-Your Assets, Our Expertise</h1>

<!-- AFTER: -->
<h1>Your Trusted Tool Recovery Services<br>Your Assets, Our Expertise</h1>
```

> **Note:** "two-factor" and "step-by-step" are acceptable compound words.

**Acceptance Criteria:**
- [ ] No em-dashes (—) in headlines
- [ ] No spaced hyphens ( - ) used as punctuation

---

### Task 3.4: Regenerate Book Cover Images
**Issues:** #024  
**Complexity:** Complex (requires design work)

**Files to Modify:**
- Book cover image files in `images/`

**What to Change:**

This is a design task, not code:
1. Identify all book cover image files
2. Re-export with corrected "CountWize" spelling (not "CountWise")
3. Replace files in `images/` folder

**Acceptance Criteria:**
- [ ] All book cover images show "CountWize" (with 'z')

---

## Phase 4: Layout Polish (Days 11-14)

---

### Task 4.1: Fix Core Values Layout
**Issues:** #003 (layout aspect)  
**Complexity:** Simple

**Files to Modify:**
- `css/main.css` — Core values section styles
- Or inline in `about-us.html`

**What to Change:**
```css
/* Find .core-values-heading-wrapper and change: */
.core-values-heading-wrapper {
  display: flex;
  flex-direction: column; /* Changed from row */
  align-items: center;
  text-align: center;
}
```

**Acceptance Criteria:**
- [ ] Section heading appears above description text (not beside)

---

### Task 4.2: Fix Footer Layout
**Issues:** #006  
**Complexity:** Medium

**Files to Modify:**
- `css/main.css` — Footer styles

**What to Change:**
```css
.footer-contact-groups-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.footer-social-wrapper {
  /* Associate with contact section, not floating */
  margin-top: 1rem;
}
```

**Acceptance Criteria:**
- [ ] Phone, email, social grouped together
- [ ] Location clearly separated
- [ ] Social icons not floating disconnected

---

### Task 4.3: Fix Blog Grid Centering
**Issues:** #027  
**Complexity:** Simple

**Files to Modify:**
- `css/main.css` or `blog.html`

**What to Change:**
```css
.blog-articles-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.blog-article-card {
  flex: 0 0 calc(50% - 1rem);
  max-width: 500px;
}
```

**Acceptance Criteria:**
- [ ] Odd-numbered last article is centered

---

### Task 4.4: Fix Hero CTA Button Position
**Issues:** #036  
**Complexity:** Simple

**Files to Modify:**
- `css/main.css` — Hero section styles

**What to Change:**
```css
.hero-content-wrapper {
  display: flex;
  flex-direction: column; /* Stack vertically */
  align-items: flex-start;
  gap: 1.5rem;
}
```

**Acceptance Criteria:**
- [ ] Hero layout: Headline → Subtext → CTA (stacked vertically)

---

### Task 4.5: Improve Book Cover Designs
**Issues:** #025  
**Complexity:** Complex (design work)

**What to Change:**

Design task - create unique covers for each book:
- Legal Framework: Gavel, scales
- Wallet Recovery: Key, lock
- Blockchain Forensics: Magnifying glass
- Beware of Scams: Warning signs
- Case Studies: Success icons

**Acceptance Criteria:**
- [ ] Each book has visually distinct cover

---

## Verification Commands

```bash
# Check for remaining brand name issues:
grep -r "Count Wise" *.html
grep -r "Count Wize" *.html

# Check for obvious dash punctuation:
grep -r " - " *.html | head -20
grep -r "—" *.html | head -20

# Start local server for testing:
cd "/Users/hamzeh/Desktop/GitHub/CountWize  - Website"
python3 -m http.server 8000
# Visit http://localhost:8000
```

---

## Manual Testing Checklist

| Page | What to Check |
|------|---------------|
| `/` (Home) | Hero CTA below headline; Video button works; Lessons play; News functional |
| `/about-us.html` | Embed works; Icons distinct; Team visible; Core Values vertical |
| `/crypto-recovery-guide.html` | All images display; No misplaced images in text |
| `/crypto-education.html` | Book covers display; EBooks text clean |
| `/news.html` | All sections load; No placeholders; Links work |
| `/blog.html` | Brand name correct; Grid centers odd items |
| **All pages** | "CountWize" consistent; No dashes in copy |

---

*Generated from 41-issue QA report — January 2026*
