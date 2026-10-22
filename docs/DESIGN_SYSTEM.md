# Design system

## Direction

The visual system combines warm ivory, natural beige, forest green, charcoal, and restrained metallic-gold details. Editorial serif headings add contrast; a system sans-serif keeps body copy readable and avoids remote font loading. The emphasized second line in the process heading is set upright in the same sans-serif stack for a clearer, more dependable finish. Content has a compact rhythm with enough room for clear reading and touch controls.

## Logo

The live identity uses the Connected Monogram: a BA symbol with a fine gold path, forest-green tile, and ivory strokes. Its two-line wordmark uses the website’s system sans-serif stack (Aptos, Segoe UI, Arial) with restrained tracking and a stronger weight for “AUTOMATION LABS.” The familiar system fonts keep the mark professional and dependable without a remote font download. The lockup is in assets/logo.svg; assets/logo-mark.svg is the matching square symbol used by the favicon. Hover and keyboard focus give it a slight lift, while reduced-motion users see a still logo. Compare the other directions in docs/logo-exploration.html.

## Tokens and layout

Edit the variables at the top of css/styles.css: --paper, --ink, --green, --gold, the font stacks, --page, and --section-space. Section spacing uses a responsive token. Descriptive text is at least 16px with comfortable line height; labels and captions are smaller supporting details. Avoid using gold for long passages. Cards and controls have visible focus and hover states; check contrast after changing colors.

The layout uses a two-column hero and workflow panel on larger screens. Service cards become two columns on tablets and one column on phones. The workflow demo stacks the chat before its business-outcome panel on narrow screens. Navigation becomes a disclosure button on phones; controls keep a large touch target.

## Four service illustrations

The “What we build” cards use small, hand-authored HTML/CSS sketches to give visitors an immediate visual clue about each service:

- **WhatsApp automation:** a sample incoming message moves into a product choice and link handoff.
- **Business websites:** a small page preview presents an offer and a product image.
- **Graphic design:** a brand-board sketch combines a logo mark, banner/campaign label, and palette.
- **Video and social campaigns:** a product-video frame and editing track lead into posting and Meta Ads.

These are decorative service explanations, not client work, generated videos, or evidence of results. Their nearby headings and paragraphs contain the meaningful information, so animation is never the only way to learn what a service includes. No image or animation library is needed.

Motion is limited to gentle entrance, float, rotation, or timeline movement. The reduced-motion rule stops the service-card keyframes and reduces other page motion. Check the static frame after changing keyframes, and avoid adding flashing or fast repeated movement.

## WhatsApp workflow animation

The separate workflow demonstration is hand-authored HTML, CSS, and vanilla JavaScript. It is not a video file and does not call an AI model at runtime. Visitors can choose a fictional shop, appointment studio, or café and play a conversation. The opening “Hi” and chatbot greeting are shown before playback; later messages, quick replies, progress, and outcome notes enter in sequence.

The animation explains how a chatbot may guide a customer toward a product page, checkout, booking flow, or order process. Every business name and chat is labeled fictional. Commercial-path text describes an opportunity, not a promised sale, completed payment, or verified client result. The animation starts only after the visitor chooses Play.

## Contact dialog and accessibility

Email links offer Gmail compose and copy actions. Phone links offer the device's calling app and copy actions. The native HTML dialog keeps focus contained while open and returns focus to the link that opened it. Original mailto: and tel: links remain as a fallback when the dialog script is unavailable. Clipboard denial reveals a selectable contact value.

Keep semantic headings in order, test every control with a keyboard, and preserve visible focus. Do not use animation as the only way to communicate a workflow step. Update the dialog labels if the business changes its preferred contact options.

## Research notes

A small review of public automation-studio pages informed the information hierarchy, not copied text or visual assets. Betterlane groups WhatsApp assistants with workflow automation and explains human handoff. B3TA connects WhatsApp to business tools and presents discovery, build, and maintenance. BOTKILAT organizes its story around process discovery, design, delivery, and handover. The current homepage presents WhatsApp as one offer alongside websites, design, and social campaigns.

References: [Betterlane](https://betterlaneagency.com/ai-automation-agency), [B3TA](https://b3ta.us/en/automation/), [BOTKILAT](https://botkilat.com/en), [Motion](https://motion.dev/), and [Webflow's GSAP license announcement](https://webflow.com/updates/gsap-becomes-free).
