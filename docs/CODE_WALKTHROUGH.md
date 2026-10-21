# Code walkthrough


## Start with index.html


The head defines language, responsive viewport, title, description, canonical GitHub Pages URL, Open Graph fields, favicon, stylesheet, and limited Organization JSON-LD. The body uses a skip link, labeled navigation, one main landmark, and sections with headings. The footer closes the page.


The hero contains a heading, explanation, and actions. Its CSS illustration is decorative and has an accessible label. Services, process, FAQ, and contact are standard HTML. FAQ uses native details and summary controls, so it works with a keyboard without a custom script.


## Follow the styling


At the top of css/styles.css, the root variables define colors, typefaces, content width, and easing. Below them are base styles and each section's layout. Tablet rules tighten spacing; phone rules change the menu, hero, columns, and footer. Reduced-motion rules prevent smooth scrolling and collapse transitions.


The hero is a perspective scene made from rounded layers with shading and depth transforms. JavaScript turns pointer position into small CSS custom property values. The motion is visual only; the content never depends on hover.


## Follow the script


config.js provides the email address. main.js toggles the mobile navigation, updates the displayed year, applies the configured email if it is no longer the example value, and attaches the pointer handler only when the device supports hover and the visitor has not requested reduced motion. Scripts are deferred until HTML parsing is complete.


## Safe edits


- Change content in the corresponding section of index.html and keep heading order and link labels clear.
- Change the monitored inbox in js/config.js.
- Adjust the palette in the root variables in css/styles.css.
- Add portfolio items only when details are real and authorized for public use.
- Replace all domain placeholders together when the final domain is serving HTTPS.
- Preview after each edit at desktop and narrow mobile widths, using keyboard navigation and reduced motion.

