# Phase C Implementation

**Generated:** 2026-01-21T06:08:10.488277
**Tasks:** 6
**Estimated tokens:** ~902

---

## Instructions

Execute the following tasks in order. After completing ALL tasks:

1. Stage and commit: `git add -A && git commit -m "fix: Phase {phase_id} - [description]"`
2. Push: `git push`
3. **CRITICAL:** Update `.ai-workflow/status.json`:

```json
{
  "state": "completed",
  "current_phase": "C",
  "phases_completed": ["C"],
  "files_modified": ["list", "of", "files"],
  "errors": []
}
```

---

## Tasks

### 1. Fix Duplicate Text Content in Mindmap Cards

**Priority:** Medium  
**Files:** `index.html`

The "Lost Crypto?" card (line 706) and "Security?" card (line 716) have identical description text about crypto recovery, which appears to be a copy-paste placeholder error.

**Required Actions:**
1. Review the "Security?" card content requirements with stakeholders
2. Write unique, appropriate description text for the Security card
3. Update line 716 in `index.html` with the new Security-focused content
4. Verify all other mindmap cards have unique, relevant descriptions

---

---

### 2. Fix Typo - "Specialis" to "Specialist"

**Priority:** Medium  
**Files:** `index.html`

Team member position is misspelled as "Compliance & Data Specialis" instead of "Compliance & Data Specialist" on line 627.

**Required Actions:**
1. Open `index.html` and locate line 627
2. Update the text from "Specialis" to "Specialist"
3. Search for any other instances of this typo across all HTML files

---

---

### 3. Add Missing Structured Data to Subpages

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

---

### 4. Update Insecure HTTP Links to HTTPS

**Priority:** Medium  
**Files:** `cookie-policy.html`, `privacy-policy.html`, potentially other policy pages

Links using `http://` instead of `https://` trigger "Not Secure" warnings in browsers and violate modern security best practices.

**Required Actions:**
1. Search all HTML files for `href="http://` references
2. Update all http:// links to https:// equivalents
3. Verify that all external links properly redirect or serve content over HTTPS
4. Test all updated links to ensure they resolve correctly

---

---

### 5. Replace Empty Hash Links with Proper Handlers

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

---

### 6. Remove Heavy Inline Styles and !important Overrides

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

---

## Completion Checklist

- [ ] All tasks completed
- [ ] Changes tested
- [ ] Git commit created
- [ ] Git push completed
- [ ] **status.json updated**

**IMPORTANT:** Update `.ai-workflow/status.json` when done!