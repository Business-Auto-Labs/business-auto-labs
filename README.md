# Business Automation Labs

A responsive, accessible static website introducing four business services: WhatsApp chatbot automation, business websites, logo and graphic design, and edited social content with Meta Ads campaign support. The public site uses HTML, CSS, and vanilla JavaScript; it has no build step or animation framework.

## Open and preview

1. Open this folder in VS Code.
2. Preview with Live Server, or run python -m http.server 8000 in this folder and open http://localhost:8000.
3. Read the [code walkthrough](docs/CODE_WALKTHROUGH.md) alongside the source.

## Project map

- index.html — page content, semantic sections, SEO and social metadata, service illustrations, and contact-options dialog.
- css/styles.css — color and type tokens, responsive layout, accessible dialog, and light CSS motion for service illustrations.
- js/config.js — public contact email and optional WhatsApp configuration.
- js/main.js — mobile navigation, reveal effects, current year, and optional WhatsApp link.
- js/workflow-demo.js — three selectable, illustrative WhatsApp chatbot journeys for a shop, appointment studio, and café.
- js/contact-actions.js — Gmail compose, phone-app call, and copy choices.
- login.html, portal/index.html, js/auth-config.js, js/auth.js, and css/auth.css — inactive Supabase login scaffold and empty client-area shell.
- assets/ — primary logo lockup, standalone mark, two alternate logo concepts, favicon, and social-sharing artwork.
- robots.txt and sitemap.xml — crawler guidance for the intended Pages URL.
- docs/ — architecture, deployment, SEO, learning, security, and case-study guidance.

## Logo directions

Three vector logo concepts are available for review in the [logo comparison preview](docs/logo-exploration.html). The Connected Monogram is the current site logo. Its wordmark uses the site’s dependable Aptos, Segoe UI, and Arial sans-serif stack for a clear, professional finish. The header logo links home on every existing page; its subtle hover lift is disabled for reduced-motion preferences.

## What we offer

1. **WhatsApp automation** — chatbots that can answer common questions, share product links, collect order or booking details, and hand requests to a person.
2. **Business websites** — responsive websites that explain an offer and guide visitors to a useful next step.
3. **Logos and graphic design** — logo, banner, and campaign-graphic design.
4. **Video and social campaigns** — product-video and photo editing, social posts, and agreed Meta Ads campaign support.

The four small service illustrations are animated HTML and CSS sketches. They help visitors picture the kinds of work offered; they are not recordings of client projects or proof of campaign results. A separate interactive demo explains WhatsApp chatbot flows using fictional businesses. It does not send messages, process orders, take bookings, or promise sales.

Add a real case study only after its details are verified and permission to publish is confirmed. Use [docs/CASE_STUDY_WORKSHEET.md](docs/CASE_STUDY_WORKSHEET.md). Campaign copy should describe agreed deliverables and must not promise sales, reach, or audience growth.

## Contact and login

The public contact email and supplied phone numbers appear on the page. With JavaScript enabled, selecting them opens a dialog to open Gmail or the device's phone app, or copy the address or number. Without JavaScript, their mailto: and tel: links still work. The phone links keep the supplied digits; no country code or WhatsApp line is inferred.

The WhatsApp button stays hidden until the owner confirms the correct line's full international number and sets its confirmation flag in js/config.js. The static site has no contact-form backend.

The login page is a Supabase Auth scaffold, not an active client portal. Its project URL and public key are blank, and no private project records are included. GitHub Pages publishes static files; it cannot enforce private access. Read [docs/SECURITY_AUTH.md](docs/SECURITY_AUTH.md) before configuring authentication or storing private data.

## Animation approach

The four service-card previews use hand-authored HTML and CSS: a WhatsApp conversation, website preview, brand-board sketch, and social-campaign editing sequence. They run without a library or external asset. They are decorative; the visible headings and 16px descriptions explain each service. The reduced-motion setting freezes the decorative movement.

The larger WhatsApp workflow demo is a vanilla JavaScript simulation. A visitor selects a fictional business and starts the conversation. Reduced-motion settings remove movement, and the conversation remains readable as ordinary page content.

## Publish

The current SEO metadata points to the GitHub Pages URL `https://business-auto-labs.github.io/business-auto-labs/`. The purchased custom domain, businessautomationlabs.com, is not connected to Pages yet. Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) if you choose to connect it later. Local edits do not confirm a live deployment, and a sitemap does not guarantee indexing.
