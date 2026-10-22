# Architecture

## Public site

index.html owns the public page content, semantic structure, title and social metadata, Organization JSON-LD, service-card illustrations, and contact-options dialog. css/styles.css defines the visual system, responsive layouts, dialog, and lightweight transitions. js/config.js stores public contact settings. js/main.js progressively enhances the mobile navigation, reveal effects, current year, optional WhatsApp link, and fine-pointer hero tilt.

The homepage introduces four services: WhatsApp chatbot automation, business websites, logo and graphic design, and video/social campaign support including Meta Ads. Each service card contains a small HTML illustration whose motion is styled in CSS. The visuals are decorative and are not client examples or performance evidence.

js/workflow-demo.js contains three fictional WhatsApp chatbot examples and animates them inside one reusable conversation panel. It shows a greeting, suggested replies, customer choices, and an illustrative route toward the business's existing product, checkout, booking, or ordering flow. The simulation does not call an AI service, send messages, create bookings, or process payments.

js/contact-actions.js intercepts email and phone links only when the native dialog API is available. It lets the visitor choose Gmail compose or copy for email, and the device phone app or copy for a phone number. If JavaScript or dialog support is unavailable, the original mailto: and tel: links remain usable.

The primary identity uses the Connected Monogram in assets/logo.svg and its matching square symbol in assets/logo-mark.svg and the favicon. The two-line wordmark uses the local system sans-serif stack so it stays legible without downloading a font. Header logo links use relative homepage routes from root and nested pages. CSS adds a small hover lift and disables it for reduced-motion preferences. Three directions can be reviewed in docs/logo-exploration.html. The hero artwork is made from CSS and HTML rather than a 3D engine. Decorative service illustrations use CSS keyframes; the larger WhatsApp demonstration is JavaScript-controlled. Reduced-motion preferences suppress movement. SVG files provide the favicon and social-sharing artwork.

## Sign-in scaffold

login.html and portal/index.html load the Supabase JavaScript client. js/auth-config.js contains a project URL, public publishable key, and redirect base. js/auth.js calls Supabase Auth for sign-in, password recovery, session checks, and sign-out.

The login page uses email as the account name. It does not implement public account creation and never writes a password into this repository. Supabase Auth owns the credential database and password hashing. The configuration is blank, so sign-in is disabled until a project is configured.

## Security boundary

GitHub Pages publishes static files. Hiding a page with JavaScript, a route, robots.txt, or noindex does not make its content private. The portal currently contains only a public placeholder and no client records. Any future database query must be protected by server-enforced authorization such as Supabase Row Level Security (RLS), with a policy for every table and storage bucket. Do not ship secret keys to the browser.

For confidential data, use a server-side application or API that validates the session and enforces access on every request. A static page may display the result, but it cannot be the security boundary.

## Files

- index.html — public marketing page, animated service sketches, and verified Organization metadata.
- css/styles.css — public visual system, responsive page styles, service-card motion, WhatsApp demo motion, and contact dialog.
- js/config.js and js/main.js — public settings and general page interactions.
- js/workflow-demo.js — fictional scripted businesses for the interactive WhatsApp chatbot demonstration.
- js/contact-actions.js — accessible contact-choice dialog with Gmail, telephone, and copy actions.
- login.html — invite-only sign-in and password recovery forms.
- portal/index.html — empty portal shell, marked noindex.
- css/auth.css, js/auth-config.js, and js/auth.js — separate authentication styling, provider settings, and behavior.
- assets/ — primary and alternate SVG logo concepts, standalone mark, favicon, and social-sharing artwork.
- robots.txt and sitemap.xml — crawler hints, not access control.
- [SECURITY_AUTH.md](SECURITY_AUTH.md) — provider setup and security guidance.
