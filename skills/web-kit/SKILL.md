---
name: web-kit
description: >-
  Start a new website, or add/update the shared header and light/dark theme toggle in
  one of Sarah's 11ty sites, from ~/Documents/projects/web-kit. Use on "new site",
  "new website", "start a site", "add a header", "theme toggle", "dark mode toggle",
  "add web-kit", "update web-kit".
---

# web-kit

Source: `~/Documents/projects/web-kit` (read its `README.md` for the file list and
contract). Plan, then wait, as always.

## New site

1. Ask: name, slug, one-line description, folder (default
   `~/Documents/projects/<slug>`), GitHub repo or not.
2. `cp -R ~/Documents/projects/web-kit/starter <folder>`, then
   `~/Documents/projects/web-kit/scripts/copy-into.sh <folder>/src/_includes
   <folder>/src/assets/css/components <folder>/src/assets/js`.
3. Replace placeholders: `SITE_NAME`, `SITE_SLUG`, `SITE_DESCRIPTION`, `CREATED_DATE`,
   `WEB_KIT_VERSION` (`grep -rl` them; none may remain).
4. `git init -b main`, `npm install`, `npm run gate` (expect all pass), first commit.
5. Offer `frontend-design` for the visual direction; the palette in `tokens.css` is a
   placeholder until its contrast pairs are verified in `docs/design-system.md`.

## Add to an existing site

1. Read the site's header, toggle, base layout, tokens and tests first. List what the
   site's tests assert about them (labels, classes) — those change.
2. Plan: which files to copy (`copy-into.sh`, never overwrites), the token mapping
   block (`tokens/mapping.example.css`), include lines, what to delete, test updates.
   Keep the site's icons/wordmark by moving them into `wk-icon-*` / `wk-wordmark`.
3. After the change: the site's gate, plus copy `scripts/browser-check.mjs` in and run
   it against a page that shows the header. Visual sign-off is Sarah's.
4. Record `web-kit <version>` in the site's `PLAN.md` Decisions.

## Update a site

Diff each web-kit-stamped file against web-kit; keep intentional local edits; bump the
stamp; gate + browser check; record the version. Never overwrite blindly.

## Change web-kit itself

Edit in `~/Documents/projects/web-kit`, bump `VERSION` and all stamps, `npm run gate`,
run the browser check in a scratch site built from `starter/`, add a CHANGELOG line.
