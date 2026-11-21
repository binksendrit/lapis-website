# LAPIS Immobilienverwaltung

Private review website, with a second visual direction matching the owner’s supplied architecture mockup. Based on the approved LAPIS Brandbook V1.0 (19 November 2026) and the supplied website briefing. `LAPIS_KI_Designleitfaden_V1.0` was intentionally excluded.

## Editing and building

- `src/*.html`: page content.
- `build.py`: central HTML template, navigation, footer, metadata and static headers.
- `site.json`: verified company contact details. Empty fields are deliberately unconfirmed.
- `dist/assets/styles.css`: shared design tokens and responsive styles.
- `dist/assets/site.js`: accessible navigation and browser-local inquiry preparation.
- `dist/assets/`: local fonts and imagery.

Run `python3 build.py` after changing content or company configuration. No dependency installation, paid service, runtime framework or external API is needed. `dist/` contains the portable static website. It can later be served by another static host.

## Inquiry handling

This version **does not send messages**. It validates an inquiry, prepares its text locally, and lets the visitor copy or download it. No form data is sent to a server, stored in cookies or local storage. Once a verified email is set in `site.json`, the contact page also offers an explicitly labelled email-app handoff. A server form endpoint is a separate future decision, not simulated here.

## Publication state

The first deployment is owner-private. All pages use noindex/nofollow and robots.txt disallows crawling. This is a review version, not a publicly launched business website. Do not remove the draft protections until the company information, services, founder presentation, privacy notice, provider details and domain are approved.

See `docs/RELEASE.md` for open items and `docs/ASSETS.md` for image provenance.
