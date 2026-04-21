# Phase B Implementation

**Generated:** 2026-01-21T06:08:10.487921
**Tasks:** 5
**Estimated tokens:** ~883

---

## Instructions

Execute the following tasks in order. After completing ALL tasks:

1. Stage and commit: `git add -A && git commit -m "fix: Phase {phase_id} - [description]"`
2. Push: `git push`
3. **CRITICAL:** Update `.ai-workflow/status.json`:

```json
{
  "state": "completed",
  "current_phase": "B",
  "phases_completed": ["B"],
  "files_modified": ["list", "of", "files"],
  "errors": []
}
```

---

## Tasks

### 1. Optimize Severely Bloated Images for Performance

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

---

### 2. Fix CoinPress Logo Size Inconsistency

**Priority:** High  
**Files:** `index.html`, `css/main.css`

The CoinPress logo (line 360 in index.html) is significantly smaller and thinner than the other platform logos (Binance, Medium, Barchart, Digital Journal), breaking visual harmony in the "Our Supported Platforms" section.

**Required Actions:**
1. Inspect the CoinPress SVG file (`images/vector-1_3.svg`) to check intrinsic dimensions
2. Add CSS rules to ensure minimum width/height matching other logos (target ~120-150px width)
3. Alternatively, replace the SVG with a properly sized version
4. Verify all platform logos align consistently at the same visual weight

---

---

### 3. Fix Third Service Icon Missing Glow Effect

**Priority:** High  
**Files:** `index.html`, `images/group_1.svg`, `css/main.css`

The third service card "Lost Assets? We'll Find Them" (lines 550-558) has an icon that appears dark/turned off while the first two cards have bright green glowing icons.

**Required Actions:**
1. Compare the SVG files: `group_1.svg` (3rd icon) vs `glyph.svg` and `group.svg` (1st and 2nd icons)
2. Identify the fill color or glow effect difference in the SVG markup
3. Update `group_1.svg` to match the green glow appearance of the other icons
4. Alternatively, add CSS filters or animations to create the glow effect consistently

---

---

### 4. Fix Mindmap Circle Border Visibility Issue

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

---

### 5. Fix Social News Ticker Logo Clipping and Text Overlap

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

---

## Completion Checklist

- [ ] All tasks completed
- [ ] Changes tested
- [ ] Git commit created
- [ ] Git push completed
- [ ] **status.json updated**

**IMPORTANT:** Update `.ai-workflow/status.json` when done!