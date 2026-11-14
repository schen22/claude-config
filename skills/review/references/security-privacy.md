---
name: security-privacy-review-lens
description: A fast, tiered code review lens to prevent credential leaks, PII exposure, injection vulnerabilities, and header misconfigurations.
---

# Lens: Security & Privacy

> **Core Question:** Does this change leak credentials/PII, execute untrusted input, or expose unprotected public surfaces?
> **Rule:** Secrets in history require credential rotation, not just commit removal.

---

## Gate 1: CI Automations (Blocking Pre-Merge)

_Automated via CI/pre-commit hooks—do not run manually:_

- **Secret Scanning:** Reject exposed API keys, private keys (`.pem`, `.key`), tokens, or `.env` files.
- **Image Metadata:** Run `exiftool` on new image assets to strip GPS/camera metadata automatically.

---

## Gate 2: Diff Review (Manual Fast-Scan)

- **Exposed PII & Private Links:** Check diffs for plain-text personal data (addresses, personal emails, coordinates) or unauthenticated URLs (Google Docs, deploy hooks, admin paths).
- **Unprotected Client Storage:** Ensure sensitive user/auth data is not stored in `localStorage` or `sessionStorage`.
- **Public Asset Boundaries:** Confirm new files added to static/public publish directories are explicitly intended for public access.

---

## Gate 3: Deep Review (Triggered Only by Related Changes)

_Trigger this section ONLY if the PR touches data rendering, third-party embeds, dynamic redirects, or app headers:_

- **Injection Vectors:**
  - Unescaped template output (`| safe`, `raw`, triple braces).
  - Direct DOM injections (`innerHTML`, `eval`, `document.write`).
  - Dynamic user input used directly in URLs, redirects, or `location` assignments.
- **Third-Party Embeds & Links:**
  - External links require `rel="noopener noreferrer"`.
  - `<iframe>` elements must include restrictive `sandbox` and `referrerpolicy` attributes.
- **Security Headers & Network Data:**
  - Changes to CSP, `X-Content-Type-Options`, or `Referrer-Policy`.
  - New external network calls (font CDNs, analytics, hotlinked images).

---

## Output Requirement

State findings clearly:
`[Vulnerability/Leak Vector]` → `[Exploit or Privacy Risk]` → `[Remediation / Required Rotation]`
