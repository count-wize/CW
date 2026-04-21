# Phase E Implementation

**Generated:** 2026-01-21T06:08:10.488712
**Tasks:** 6
**Estimated tokens:** ~1,167

---

## Instructions

Execute the following tasks in order. After completing ALL tasks:

1. Stage and commit: `git add -A && git commit -m "fix: Phase {phase_id} - [description]"`
2. Push: `git push`
3. **CRITICAL:** Update `.ai-workflow/status.json`:

```json
{
  "state": "completed",
  "current_phase": "E",
  "phases_completed": ["E"],
  "files_modified": ["list", "of", "files"],
  "errors": []
}
```

---

## Tasks

### 1. Improve Alt Text Descriptiveness and Consistency

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

---

### 2. Standardize Image Filename Conventions

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

---

### 3. Implement Dynamic Date System for News Items

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

---

### 4. Fix Form Validation Error Message Display

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

---

### 5. Add rel="nofollow" to External Partner Links

**Priority:** Low  
**Files:** All HTML files with external links

External links to partners (Binance, Medium, CoinPress, etc.) have `rel="noopener noreferrer"` but would benefit from `rel="nofollow"` for SEO best practices, especially for sponsored/partner links.

**Required Actions:**
1. Identify all external partner/sponsor links across all pages
2. Update rel attributes to `rel="noopener noreferrer nofollow"` for paid/partner links
3. Keep `rel="noopener noreferrer"` without nofollow for editorial/organic links
4. Document which types of links should use nofollow for future reference

---

---

### 6. Optimize Large SVG File Sizes

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

---

## Completion Checklist

- [ ] All tasks completed
- [ ] Changes tested
- [ ] Git commit created
- [ ] Git push completed
- [ ] **status.json updated**

**IMPORTANT:** Update `.ai-workflow/status.json` when done!