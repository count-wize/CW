# Phase A Implementation

**Generated:** 2026-01-21T06:08:10.487667
**Tasks:** 5
**Estimated tokens:** ~799

---

## Instructions

Execute the following tasks in order. After completing ALL tasks:

1. Stage and commit: `git add -A && git commit -m "fix: Phase {phase_id} - [description]"`
2. Push: `git push`
3. **CRITICAL:** Update `.ai-workflow/status.json`:

```json
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["list", "of", "files"],
  "errors": []
}
```

---

## Tasks

### 1. Fix Broken Start Recovery Navigation Link

**Priority:** Critical  
**Files:** `index.html`

The "Start" button in the hero alternative section (line 320) links to `/recovery-questionnaire` without the `.html` extension, causing 404 errors on static hosting environments.

**Required Actions:**
1. Open `index.html` and locate line 320
2. Update the href from `/recovery-questionnaire` to `/recovery-questionnaire.html`
3. Test the link to ensure it properly navigates to the recovery questionnaire page

---

---

### 2. Resolve Non-ASCII Filename Compatibility Issue

**Priority:** Critical  
**Files:** `images/группа2.svg`, all HTML files referencing this image

The file `группа2.svg` (Cyrillic characters) exists in the images directory and will cause 404 errors on many web servers and file systems that don't properly handle non-ASCII characters.

**Required Actions:**
1. Rename `images/группа2.svg` to `images/group2.svg`
2. Search all HTML files for references to `группа2.svg` and update them to `group2.svg`
3. Verify the image displays correctly across all pages after renaming

---

---

### 3. Fix Video Player Cross-Origin Security Error

**Priority:** Critical  
**Files:** `index.html`

The Vimeo video player in the "Discover CountWize" section (lines 414-426) displays as a black/blank box due to SecurityError: "Blocked a frame with origin" cross-origin access issue.

**Required Actions:**
1. Verify the Vimeo video ID `1061354345` is correct and the video is not set to private
2. Check Vimeo embed settings to ensure the domain is whitelisted for embedding
3. Test alternative embed parameters or consider adding the video to an allowed domains list
4. If the video ID is incorrect or private, obtain the correct public video ID and update line 418

---

---

### 4. Implement Recovery Form Processing Backend

**Priority:** Critical  
**Files:** `recovery-questionnaire.html`

The recovery questionnaire form has no defined backend endpoint for the `action` attribute, meaning user submissions may go nowhere if the Webflow form handler isn't properly configured.

**Required Actions:**
1. Review the form element in `recovery-questionnaire.html` to identify the current action/submission configuration
2. Implement or verify a backend endpoint for form processing (Webflow handler, custom API, or email service)
3. Add proper form validation and success/error messaging
4. Test the complete form submission flow from frontend to backend

---

---

### 5. Fix Handpicked News Feed Broken Links

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

---

## Completion Checklist

- [ ] All tasks completed
- [ ] Changes tested
- [ ] Git commit created
- [ ] Git push completed
- [ ] **status.json updated**

**IMPORTANT:** Update `.ai-workflow/status.json` when done!