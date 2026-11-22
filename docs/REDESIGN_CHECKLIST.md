# Business Automation Labs redesign checklist

**Scope:** local redesign only. Do not commit, push, deploy, or publish until Neel has reviewed and approved the complete result.

**Baseline:** static HTML, CSS, and vanilla JavaScript; branch main; source was clean before task notes/design artifacts were created; custom domain https://businessautomationlabs.com/.

## Working rules

- Preserve useful behavior, supplied contact details, and confirmed brand assets.
- Keep shared styling and interaction logic centralized. Page-specific copy belongs in its own HTML file.
- Finish and review each service page before moving on; record PASS or fixes in the progress log.
- Keep authentication and lead submission inactive until trusted provider/backend setup is complete. Never put service-role keys, Google service-account keys, or other secrets in browser files.
- Treat Google Sheets as a restricted lead-list destination, not authentication or access control.
- Keep all changes local. Final user review is the release gate.

## Phase 0 — Baseline

- [x] Inspect files, stack, current routes, assets, and Git state.
- [x] Read page, auth, workflow, contact, SEO, and deployment behavior.
- [x] Record features to preserve, improve, or replace and why.
- [x] Record factual constraints: no invented client names, results, credentials, pricing, or publishing permission.
- [x] Record backend prerequisites without requesting secrets in chat.
- [ ] Capture before and after at desktop, tablet, and phone widths. Desktop reference was observed; the inspector's Chrome launch failed and the available browser cannot set viewports. Do not claim tablet/phone visual review until a viewport-capable preview is available.

### Feature decisions

| Existing feature | Decision | Reason |
| --- | --- | --- |
| Connected Monogram and ivory/forest/gold palette | Preserve | Confirmed identity; expand into a consistent multi-page system. |
| WhatsApp retail, appointment, and café workflow demo | Preserve and improve | It explains the central service; retain fictional labels and accurate claims. |
| Business email, Dhruv and Neil phone numbers, contact-choice dialog | Preserve | Supplied business contacts; carry to every route and keep functional fallbacks. |
| Password-first login and empty portal | Replace sign-in UI with Google and WhatsApp OTP scaffolding; leave inactive | Supabase configuration is blank and static hosting cannot enforce private record access. |
| Client stories and results | Keep truthful placeholder | No unverified client, project permission, result, or contribution may be invented. |
| HTML/CSS/vanilla JS | Preserve | No framework or heavy animation library is needed. |
| Website-to-Sheets form | Do not activate in the static site | Browser credentials or an unrestricted public endpoint would expose lead data and/or secrets. |

**Baseline review:** the homepage, auth scaffold, workflow demo, supplied contact lines, metadata, sitemap, robots and deployment docs were inspected. Desktop screenshot exists in the in-app browser history; tablet/phone baseline capture is unavailable. No backend, calendar, Supabase keys, Google Sheets integration, public project proof, or privacy/retention policy is configured.

## Phase 1 — Information architecture and conversion

- [x] Homepage plus four dedicated pages: WhatsApp automation, web development, logo/graphic design, and Meta Ads/social content (including the existing video-editing offer).
- [x] One shared header/footer, design system, mobile navigation, contact behavior, and homepage-linked logo.
- [x] Primary CTA: **Talk through a project**. Service pages will open a prefilled WhatsApp draft naming the service; the visitor still chooses whether to send. Direct calls and email stay available.
- [x] No real booking calendar is configured. The CTA requests a conversation and does not promise a confirmed time. Use direct contacts now; configure a calendar later if the owners choose one.
- [x] No website login requirement for browsing, service enquiries, or contacting the studio. The client portal remains separate and invite-only until its access policy is ready.
- [x] No contact form that appears active but has no endpoint. An eventual callback form requires the server-side flow below.
- [x] SEO targets and metadata are mapped per route; no city or ranking claim is assumed.

### Conversion and data flow

- A discovery conversation fits a high-consideration service better than a “buy now” CTA. The current static project has no scheduler, so a service-specific WhatsApp request is the honest low-friction primary action. Calls and email remain direct alternatives. There is no Business Automation Labs conversion experiment yet, so this is a reasoned starting point, not a measured uplift claim.
- Google account sign-in is one Google OAuth action using the account chooser (select_account). Google shows accounts available to that browser and “Use another account”; the website cannot list every Gmail account.
- WhatsApp phone sign-in is a one-time code delivered through a configured provider. Supabase currently supports WhatsApp OTP only with Twilio/Twilio Verify and a configured WhatsApp sender. Keep it unavailable until provider, abuse controls, redirect allowlist, and applicable country rules are verified.
- Ask for a nickname only after successful authentication; store it as display metadata, never as permission or identity proof.
- A future callback form should collect only name, requested service, contact channel, and one email/phone value plus explicit consent. A Supabase Edge Function should validate, rate-limit, verify anti-abuse tokens, and append to a private Google Sheet using server-side credentials. Keep the service account restricted to that Sheet, limit collaborators, set retention, and never log contact values. No submission or Sheets write is active in this local build.

**Review gate:** the route map, CTA hierarchy, contact data, privacy boundary, and external dependencies are recorded.

## Phase 2 — Shared shell and homepage

**Chosen direction:** a high-contrast editorial studio site. The connected BA monogram and ivory/forest/gold palette remain, with a full-bleed forest hero, cream chat card, gold focus rail, and a featured WhatsApp service card. Visuals use crafted fictional interfaces rather than stock or unapproved client photography. Service illustrations explain categories; they are not claims of client work.

- [x] Establish the visual direction from the existing brand and real assets; use the workflow itself as the central visual idea, not stock client proof.
- [x] Build shared responsive navigation, footer, contact actions, and homepage logo links.
- [x] Clarify the hero: practical WhatsApp chatbots first, followed by the three other service categories.
- [x] Preserve workflow tabs, playback, replay, and reduced-motion handling; static source review passed. Browser behavior at phone/tablet sizes was not executable or visually verified in this environment.
- [x] Retain fictional-demo labels and supplied phone/email details.

**Homepage review gate:** semantics, keyboard/focus, reduced motion, responsive source review, links, and preserved workflow controls reviewed before service pages.

## Phase 3 — Service pages, one at a time

For each page: create it, inspect its source and links, correct issues, record PASS, then move on.

### WhatsApp automation
- [x] Show customer message → approved chatbot reply/options → product/order/booking link or human handoff.
- [x] Explain business-specific setup and limits; never promise sales or fully autonomous support.
- [x] Include the service-specific project-conversation CTA, direct phone/email options, and unique SEO metadata.
- **Review:** PASS — unique metadata, canonical, local assets, IDs, and internal targets checked; wording preserves the real checkout/booking boundary. Visual browser review unavailable in this session.

### Web development
- [x] Explain responsive websites and scope agreed with each client; do not imply unsupported hosting, checkout, or integrations.
- [x] Include the service-specific project-conversation CTA, direct phone/email options, and unique SEO metadata.
- **Review:** PASS — service copy and scope limits checked; unique metadata/canonical, IDs, local assets, and internal links verified. Visual browser review unavailable in this session.

### Logo and graphic design
- [x] Explain logo, banner, and campaign-graphic creation and handoff without inventing client work.
- [x] Include the service-specific project-conversation CTA, direct phone/email options, and unique SEO metadata.
- **Review:** PASS — deliverables, revision scope, licensing and trademark boundaries are stated; unique metadata/canonical, IDs, assets, and internal links checked. No fabricated project proof. Visual browser review unavailable in this session.

### Meta Ads and social content
- [x] Include agreed video/photo editing, social post preparation, and Meta Ads setup/management.
- [x] State that budget approval and ad-account ownership remain with the client; results depend on creative, audience, budget, and platform delivery.
- [x] Include the service-specific project-conversation CTA, direct phone/email options, and unique SEO metadata.
- **Review:** PASS — creative scope, client approval, ad account/spend responsibility, and no-results-guarantee language checked; unique metadata/canonical, IDs, assets, and internal links verified. Visual browser review unavailable in this session.

## Phase 4 — Login and identity

- [x] Replace the password-first UI with Google account-selection and WhatsApp OTP scaffolds plus the post-auth nickname step; controls remain disabled.
- [x] Request Google account selection; explain that the website cannot enumerate every Gmail account.
- [x] Document supported WhatsApp OTP provider/sender and regional compliance requirements; no provider is configured.
- [x] Keep provider controls disabled and omit the public Client login link while credentials and backend policies are unconfigured.
- [x] Keep the portal empty of private data; document server-enforced authorization and RLS requirements for any future records.
- **Review:** PASS by static source review — no credentials in config, provider switches are false, no public login link, no private portal records, and nickname is display metadata only. Supabase/Google/Twilio setup and live auth testing remain unverified.

## Phase 5 — Enquiry and Google Sheets

- [x] Document the future secure request flow: browser → Supabase Edge Function → Google Sheets API.
- [x] Document that service-account credentials must stay server-side and unrestricted Apps Script endpoints are not acceptable.
- [x] Document server-only secrets and a service account restricted to one private Sheet.
- [x] Specify proposed fields, consent, access, retention, error, abuse, and deletion practices in the intake plan; these policies must be agreed before activation.
- [x] Keep the site on working WhatsApp, telephone, and email links; no fake form or submit button is present.
- **Review:** PASS by static source review — no lead form, sheet endpoint, browser credential, or public database write; future setup is documented. No live intake is active.

## Phase 6 — SEO and accessibility

- [x] Add unique titles, descriptions, canonicals, Open Graph metadata, and suitable structured data to each public route.
- [x] List the homepage and four service pages in sitemap.xml; exclude login and portal.
- [x] Static-check robots, internal links, image alternatives, heading order, visible focus styles, dialogs, navigation, and reduced-motion rules.
- [x] Keep descriptive copy at least 16px where it fits and provide phone/tablet/desktop CSS breakpoints. Visual overflow inspection remains pending a safe viewport-capable preview.
- **Review:** PASS after final static metadata/sitemap/link checks — public routes are listed; login and portal are noindex and excluded. Search indexing is not verified.

## Phase 7 — Security and final local review

- [x] Source-review auth, session, contact intake, Sheets, third-party script, and GitHub Pages trust boundaries.
- [x] Record the security boundary and remaining backend/deployment work; no claim of absolute security is made.
- [x] Check JavaScript syntax, internal links, local asset paths, duplicate IDs, metadata/sitemap/canonical consistency, and git diff --check.
- [x] Recheck per-page source gates and preserved interaction hooks; disclose that runtime and visual viewport inspection are unavailable.
- [x] Update design, SEO, security/auth, deployment, and code-walkthrough documentation.
- [ ] Review the complete local diff and checklist with Neel. No commit, push, deployment, or external lead write without later approval.

**Final gate:** local static checks and source review are recorded; remaining placeholders and backend prerequisites are explicit. Neel approved a local commit on 2026-11-22. No push or deployment is included.

## Progress log

| Subtask | Status | Review notes |
| --- | --- | --- |
| Baseline inventory | Reviewed | main was clean before task notes; static HTML/CSS/JS. Desktop baseline seen; tablet/phone visual capture unavailable. |
| Architecture and conversion path | Reviewed | Four service routes, consistent WhatsApp-first project CTA, phone/email alternatives, no fake calendar/form; secure future Sheets flow documented. |
| Homepage and shared shell | Reviewed | Hero names WhatsApp chatbots and practical customer tasks; the visual refinement adds a forest-green hero, cream chat object, gold service rail, and featured WhatsApp card; four service cards link to dedicated routes. Static HTML/ID/anchor review passed. No safe visual preview at target widths is available under this session’s execution restrictions. Shared navigation, contact choices, logo-home links, and workflow controls were source-reviewed. Runtime and viewport review remain unavailable. |
| WhatsApp automation page | Reviewed | Source review PASS: dedicated service copy, clear CTA, contact routes, fictional illustration, unique metadata, no duplicate IDs, local asset paths and internal links resolved. Visual browser review unavailable. |
| Web development page | Reviewed | Source review PASS: responsive website scope and boundaries stated, contact routes present, unique metadata and all page links/assets/IDs checked. Visual browser review unavailable. |
| Logo/graphic design page | Reviewed | Source review PASS: logo/graphic offer and handoff limits are accurate; unique metadata, IDs, assets, contact routes, and internal links checked. Visual browser review unavailable. |
| Meta Ads/social content page | Reviewed | Source review PASS: video/photo/social scope and client budget/account approval boundaries stated; unique metadata, contact routes, IDs, assets, and internal links checked. Visual browser review unavailable. |
| Login/identity | Reviewed | Google account selection and WhatsApp OTP are scaffolds; provider flags remain false, controls are disabled, public login link omitted, portal empty. Supabase, Google OAuth, Twilio and live abuse/access controls still need setup. |
| Enquiry/Sheets flow | Reviewed | Secure future Supabase Edge Function → private Google Sheet design is documented. No form, endpoint, sheet, or credentials are configured. |
| SEO/accessibility | Reviewed statically | Per-route metadata and sitemap scope are in place; final parser/link/accessibility source checks passed; viewport review remains unavailable. Visual viewport and live Search Console checks not performed. |
| Security/final local review | Reviewed statically; local commit approved |
