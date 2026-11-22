# Architecture

## Public routes and shared behavior

The site is a static HTML, CSS, and vanilla JavaScript project. index.html is the homepage; whatsapp-automation.html, web-development.html, graphic-design.html, and meta-ads.html are the dedicated service pages. Each route owns its page copy, title, description, canonical and Open Graph metadata, and Service structured data. Shared CSS and JavaScript provide the visual system, navigation, contact choices, and motion. The repeated HTML header/footer are static markup; behavior and styling remain centralized.

The homepage explains the four offers and links each service card to its own page. The visual sketches use HTML/CSS and are explanatory, not client work or results. js/workflow-demo.js contains the three fictional retail, appointment, and café chatbot flows. The demo does not call an AI service, send messages, create bookings, or process payments.

js/contact-actions.js enhances the supplied email and phone links with a dialog for app and copy choices. The original mailto: and tel: links remain as fallbacks. Contact details are configured in js/config.js.

The Connected Monogram is in assets/logo.svg; assets/logo-mark.svg is the matching icon. Page links route the mark to the homepage. CSS respects reduced-motion preferences. docs/logo-exploration.html compares the logo directions.

## Sign-in scaffold (inactive)

login.html, portal/index.html, css/auth.css, js/auth-config.js, and js/auth.js form an inactive sign-in scaffold. Supabase URL and publishable key are blank; Google and WhatsApp provider flags are false. Login is not linked in the public navigation. The UI has a Google account-selection action and a WhatsApp OTP flow followed by a nickname step, but provider controls stay disabled until actual Supabase, Google OAuth, Twilio WhatsApp, redirect, abuse-protection, and authorization settings are configured.

Google's account selector asks Google to show accounts available to the visitor's browser. The site cannot enumerate all of a visitor's Gmail accounts. WhatsApp OTP requires a supported, configured provider and sender. The nickname is display metadata only and never grants access.

The portal contains no client data. GitHub Pages serves static public files and cannot enforce privacy or protect a database. Any future private data needs server-enforced authorization, such as correctly scoped Supabase Row Level Security (RLS), on every table and storage bucket.

## Lead capture and Sheets (not active)

There is no website request form, booking calendar, backend endpoint, or Google Sheets connection. The proposed safe design is browser → protected Supabase Edge Function → private Google Sheet. The function must validate, rate-limit, apply anti-abuse checks, and use credentials held only in server secrets. See docs/LEAD_INTAKE_GOOGLE_SHEETS.md; do not add service-account credentials or an unrestricted public Apps Script URL to browser code.

## Files

- index.html — homepage, shared navigation/footer markup, homepage metadata and service overview.
- whatsapp-automation.html, web-development.html, graphic-design.html, meta-ads.html — dedicated service routes and route-specific SEO metadata.
- css/styles.css — public design tokens, responsive layouts, service illustrations, workflow demo, contact dialog, and light motion.
- js/config.js, js/main.js — public contact settings and general page interactions.
- js/workflow-demo.js — fictional WhatsApp workflow data and playback.
- js/contact-actions.js — accessible email/phone contact-choice dialog.
- login.html, portal/index.html, css/auth.css, js/auth-config.js, js/auth.js — inactive auth scaffold; no private portal data.
- docs/SECURITY_AUTH.md, docs/LEAD_INTAKE_GOOGLE_SHEETS.md — auth boundary and future secure intake plan.
- robots.txt, sitemap.xml, CNAME — crawl hints and custom-domain configuration, not access control.
