# Search visibility and maintenance

## Routes and metadata

The public site has five indexable routes: the homepage and four service pages for WhatsApp automation, web development, graphic design, and Meta Ads/social content. Each page has a distinct title, description, canonical URL, Open Graph metadata, and relevant structured data. sitemap.xml should list these five public HTTPS routes only; login.html and /portal/ are noindex and excluded. robots.txt points to the sitemap.

All public URLs use https://businessautomationlabs.com/. Keep the canonical URL, Open Graph URL/image, structured-data URL, sitemap URLs, robots sitemap reference, CNAME, and siteBaseUrl in js/auth-config.js aligned if the domain changes. The redirect base is configuration only; sign-in remains disabled while Supabase settings are blank. Check GitHub Pages custom-domain and HTTPS status after any eventual publication.

The homepage Organization data describes verified services and the supplied business email. It does not include unverified founder names, addresses, social profiles, client names, or outcomes. The four service illustrations and three WhatsApp examples are fictional/explanatory visuals, not case studies.

## Search Console

The Google Search Console Domain property for businessautomationlabs.com was verified with its Google-issued TXT record in Namecheap DNS. Keep the verification record and the separate GitHub Pages record in place; do not remove the locked SPF record. A sitemap submission helps discovery but cannot guarantee crawling, indexing, or ranking. Use URL Inspection to review URLs individually.

## Maintain after publishing

After a future deployment, confirm each public route loads, contact links work, the social image path resolves, and no outdated claims remain. Revisit route-specific metadata, structured data, sitemap entries, and internal links whenever pages or services change. Do not claim indexing or live behavior until it has been checked.

Official Google guidance: [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) and [get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
