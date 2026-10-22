# Search visibility and maintenance

## Homepage indexing

The purchased custom domain is businessautomationlabs.com, but it is not connected to GitHub Pages yet. The current homepage canonical, Open Graph URLs, structured-data URL, robots sitemap reference, sitemap, and authentication redirect base use the active Pages address https://business-auto-labs.github.io/business-auto-labs/. If the custom domain is connected later, update those URLs together after DNS and HTTPS work. See docs/DEPLOYMENT.md for the exact sequence. Keep titles, descriptions, headings, and link labels accurate.

Only the marketing homepage is listed in the sitemap. login.html and /portal/ include noindex and are excluded from the sitemap. The public navigation hides the Client login link while Supabase settings are blank; this is a visibility choice, not access control. These directives do not protect files from visitors; backend authorization such as Supabase Row Level Security must protect any private records.

The Organization structured data describes the studio's verified offers and includes the current public URL and supplied business email. It does not add unverified founder names, addresses, social profiles, client names, or results. The small animated service-card illustrations explain categories of work. The interactive WhatsApp examples use fictional businesses and are not client projects or structured case studies.

## Crawling and indexing

After the public site is live, verify the domain in Google Search Console, submit the sitemap, and use URL Inspection to request a crawl. A sitemap helps discovery but cannot guarantee crawling or indexing. Google decides whether and when to show a page in Search.

## Maintenance

After each deployment, confirm the page loads, contact links and contact-option dialog work, the social image path is valid, and no outdated claims remain. Revisit title, description, canonical, image, sitemap, and structured data if the domain or business changes.

Official Google guidance: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) and [get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
