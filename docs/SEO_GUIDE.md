# Search visibility and maintenance

## Homepage indexing

Business Automation Labs uses the custom domain https://businessautomationlabs.com/ with GitHub Pages. The homepage canonical, Open Graph URLs and image, structured-data URL, robots sitemap reference, sitemap, and authentication redirect base are set to use this HTTPS origin. The root CNAME file names businessautomationlabs.com. After publishing URL changes, verify the custom-domain and HTTPS status in repository Settings → Pages. Keep titles, descriptions, headings, and link labels accurate.

Only the marketing homepage is listed in the sitemap. login.html and /portal/ include noindex and are excluded from the sitemap. The public navigation hides the Client login link while Supabase settings are blank; this is a visibility choice, not access control. These directives do not protect files from visitors; backend authorization such as Supabase Row Level Security must protect any private records.

The Organization structured data describes the studio's verified offers and includes the current public URL and supplied business email. It does not add unverified founder names, addresses, social profiles, client names, or results. The small animated service-card illustrations explain categories of work. The interactive WhatsApp examples use fictional businesses and are not client projects or structured case studies.

## Crawling and indexing

The Google Search Console Domain property for businessautomationlabs.com is verified using its Google-issued TXT record at the root (`@`) in Namecheap Advanced DNS. The record was visible after reloading Namecheap and in a public DNS lookup. Keep it in place to retain verification. Do not remove or replace the separate GitHub Pages verification TXT record or the locked SPF record.

Before submitting `https://businessautomationlabs.com/sitemap.xml`, confirm that the live sitemap lists `https://businessautomationlabs.com/` as the homepage. Then use URL Inspection to check the homepage. A sitemap helps discovery but cannot guarantee crawling or indexing. Google decides whether and when to show a page in Search. Verification and submission do not confirm that the site has been indexed.

## Maintenance

After each deployment, confirm the page loads, contact links and contact-option dialog work, the social image path is valid, and no outdated claims remain. Revisit title, description, canonical, image, sitemap, and structured data if the domain or business changes.

Official Google guidance: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) and [get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
