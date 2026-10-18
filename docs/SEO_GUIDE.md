# Search visibility and maintenance

## Before launch

The canonical and Open Graph URLs are set to the planned GitHub Pages address, https://code-neel.github.io/business-auto-labs/. If a custom domain is configured later, update those URLs, robots.txt, and sitemap.xml together. Keep a descriptive page title, accurate summary, clear headings, useful link labels, and real page copy. The SVG share image is a template; verify it at its final public URL.

The Organization JSON-LD describes only the studio name and a general summary. Add address, founder identities, social profiles, or contact details only if they are verified and intended to be public. Structured data does not guarantee a rich search result.

## Crawling and indexing

robots.txt allows crawling and points to the sitemap. sitemap.xml lists the planned GitHub Pages homepage. If you configure a custom domain, update that sitemap URL and the robots.txt Sitemap line. A sitemap helps discovery but cannot guarantee crawling or indexing.

After the public site is live, verify the domain in Google Search Console, submit the sitemap, and use URL Inspection to request a crawl. Google decides whether and when to index a page; a request is not a promise. Ensure the site loads without login and does not accidentally block crawlers or include a noindex directive. A new site may take time to appear in search.

## Maintenance

Review the live page after deployments. Keep contact details working, remove stale offers, correct claims, and publish only portfolio examples approved for sharing. Revisit title, description, canonical, social image, sitemap, and structured data if the domain or business changes. Search visibility depends on systems and circumstances outside this repository.

## Official Google references
- [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Get started with Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start)


