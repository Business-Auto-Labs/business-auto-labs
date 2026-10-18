# Architecture

## How the pieces fit

index.html owns the document structure, content, metadata, and Organization structured data. css/styles.css gives those semantic regions their visual layout and adapts them to screen sizes. js/config.js contains safe public configuration; js/main.js enhances the page after parsing. Relative references let it work at a GitHub Pages project URL as well as a domain root.

The core content works without JavaScript: navigation links, services, portfolio status, process, FAQ answers, and contact information are in HTML. JavaScript improves the mobile menu, year, email link, and decorative pointer response.

## File guide

- index.html: semantic content and document head.
- css/styles.css: tokens, base styles, component layouts, breakpoints, and reduced-motion behavior.
- js/config.js: editable contact email.
- js/main.js: progressive enhancement without a framework.
- assets/favicon.svg and assets/og-image.svg: vector favicon and social preview image.
- robots.txt and sitemap.xml: crawler files with domain placeholders.
- docs/: implementation and learning references.

## Technical decisions

The hero uses layered CSS gradients, perspective, and transforms. It adds depth without WebGL, a rendering library, or a build step. The effect is decorative, remains still on touch devices, and respects reduced-motion preferences.

There is no fake form. The contact link uses mailto and opens a visitor's configured email application. A web form needs a real hosted service because GitHub Pages serves static files only.

The Organization schema includes only the studio name and general description. Client names, outcomes, testimonials, credentials, founder names, and contact details are omitted until verified.
