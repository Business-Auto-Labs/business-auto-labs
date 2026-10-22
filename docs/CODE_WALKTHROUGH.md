# Code walkthrough

## Start at the homepage

Open index.html. Its head contains the title, search description, canonical URL, Open Graph metadata, favicon, and basic Organization JSON-LD based on known business facts. The page uses a skip link, labeled navigation, one main landmark, and named sections.

The shared Connected Monogram lockup is assets/logo.svg. Its wordmark uses the site’s Aptos, Segoe UI, and Arial sans-serif stack rather than an external font. assets/logo-mark.svg is reused for the favicon and portal illustration. Header logos link home from both root and nested pages. Three directions appear in the noindex comparison at docs/logo-exploration.html. CSS applies a slight hover/focus lift and turns it off under reduced-motion settings.

The hero presents WhatsApp automation, websites, design, and social campaigns. The “What we build” section contains four service cards. Each card has a heading and descriptive text that remains readable without animation, plus a decorative HTML illustration:

- WhatsApp automation shows a customer message, a product choice, and a link handoff.
- Website building shows a compact responsive-page preview.
- Graphic design shows an example brand board with a logo mark and color palette.
- Video and social campaigns show an edit, post, and Meta Ads sequence.

The illustrations are concepts, not client work. The campaign card does not claim reach, sales, or a real ad result. The contact section keeps the supplied email and two phone numbers.

## Follow the WhatsApp workflow demo

Open js/workflow-demo.js. The workflows object contains one data entry for a retail shop, an appointment studio, and a café. Each entry provides a sample business label and four conversation stages. A stage stores message text, optional quick-reply labels, an outcome explanation, and an illustrative commercial path.

The script starts by showing the visitor's “Hi” and the example business's greeting. The visitor can switch the tabs with a pointer or keyboard, then use Play, Pause, Resume, or Start over. New chat bubbles are created as HTML elements and filled with textContent, which keeps example text separate from markup. The status line announces progress to assistive technology. The visible examples are demonstrations only; a real customer's chatbot would need the business's approved information and actual checkout, calendar, or order setup.

To add an example, create another workflow data entry and a matching tab in index.html. Use a clearly fictional business label, avoid client results, and describe the real next step accurately. Do not describe a link as a completed sale or booking.

## Follow the design and motion

At the top of css/styles.css, edit the shared color, type, and page-width tokens. The file styles the header, hero, four service-card illustrations, workflow simulator, process, studio story, FAQ, contact dialog, and footer. Body copy stays readable at 16px or larger; small uppercase labels and captions are supporting details.

The page uses responsive CSS grids. The navigation becomes a disclosure menu on small screens. Service cards become two columns on tablets and one column on phones. The workflow simulator places the conversation before its outcome panel on narrow screens. The custom contact dialog fits the viewport and keeps large action targets.

CSS keyframes animate the service sketches: messages and choices appear, the website preview floats slightly, a logo mark turns gently, and an edit-timeline cursor moves across a track. These loops are intentionally restrained and contain no sound or fabricated performance data. The reduced-motion setting stops the decorative service animation. The visitor can understand each service from the heading and paragraph alone.

The larger workflow demo uses short transitions when the visitor starts playback. The visitor controls playback; it does not autoplay. The same conversation text remains readable if motion is reduced or JavaScript is unavailable.

## Follow the scripts and contact options

js/config.js contains the public contact email and optional WhatsApp number. The WhatsApp button remains hidden until the owner confirms the correct line, adds its full international number, and enables the confirmation flag. The two phone links in index.html use only the digits supplied by the owner; no country code or WhatsApp line is assumed.

js/contact-actions.js turns a click on the email address into a dialog with “Open Gmail to compose” and “Copy email address.” A click on either phone number shows “Call” and “Copy phone number.” The visitor chooses the app action; the site never dials or opens Gmail automatically. If clipboard access is blocked, a selectable input provides a manual copy fallback. Without JavaScript, the original mailto: and tel: links still work.

js/main.js handles the mobile menu, reveal effects, displayed year, configured email link, optional WhatsApp link, and subtle hero tilt for fine-pointer devices. The separate login.html page loads js/auth-config.js and js/auth.js; its provider URL and public key are blank. Follow [SECURITY_AUTH.md](SECURITY_AUTH.md) before configuring authentication. Never save passwords locally or in a public table.

## Safe edits

- Change the vector wordmark in assets/logo.svg and its symbol in assets/logo-mark.svg together; compare alternate directions in docs/logo-exploration.html.
- Change service headings and descriptions in index.html; keep claims within the work the team actually offers.
- Adjust color tokens at the beginning of css/styles.css.
- Tune the service-card animation keyframes in the same file. Keep a static visual state and preserve the reduced-motion rule.
- Edit the fictional WhatsApp examples in js/workflow-demo.js; keep their business names labeled as examples.
- Add client stories only with verified details and permission to publish.
- Describe Meta Ads work as an agreed service, not a promised outcome.
- Add a WhatsApp number only in full international format after confirming it is the correct business line.
- Configure login only by following [SECURITY_AUTH.md](SECURITY_AUTH.md). Keep secret keys out of this repository.
- Preview desktop and phone widths, navigate with Tab and arrow keys, play and pause the example, open each contact option, and enable reduced motion.
