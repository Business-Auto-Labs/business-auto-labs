# Website launch and search visibility checklist

Use this as a reusable starting point for a new website. Adapt it to the actual host, domain, public pages, audience, and privacy needs. A checklist item is complete only after checking the live site or the relevant service dashboard.

## Before launch

1. **Choose one public URL.** Decide whether the canonical address is `https://example.com/` or `https://www.example.com/`. Configure the host and DNS to serve that version securely and redirect alternate versions to it.
2. **Align URL signals.** Each indexable page should have its own canonical URL. Keep the homepage's canonical, Open Graph URL, structured-data URL, sitemap entries, and absolute social-image URL on the chosen host. Confirm every referenced image exists and loads publicly.
3. **Check the sitemap.** List only canonical pages intended for search results. Use absolute HTTPS URLs. Leave sign-in pages, private areas, thank-you pages, previews, and other pages out unless there is a specific reason to index them.
4. **Check robots.txt.** Allow search crawlers to reach public pages and point its Sitemap line to the live sitemap. A robots rule is not an access-control system; never rely on it to protect private files.
5. **Write page-specific metadata.** Give every public page a useful, accurate title and description. Describe the actual page and offer; avoid keyword stuffing or unsupported promises. Search engines may choose different title links or snippets.
6. **Test the real visitor path on a phone.** Check navigation, text size, buttons, calls, email links, forms, interactive demos, and page scrolling. Also check keyboard focus and reduced-motion behavior where applicable.
7. **Measure speed once the public build is available.** Run PageSpeed Insights for mobile and desktop. Review actual diagnostics and prioritize user-visible problems; a single lab score varies and does not replace real-user data.
8. **Decide whether analytics is useful.** If you will review the data, add an analytics property and track meaningful events such as qualified contact clicks or form completions. Avoid collecting private message contents or data you do not need. Add privacy and consent handling appropriate to the audience and setup.

## After launch: search tools

### Google Search Console

- Add a **Domain property** to cover the domain across HTTP/HTTPS and subdomains. It requires a DNS TXT verification record. A URL-prefix property is an alternative when DNS access is unavailable, but it covers only the specified prefix.
- Google's Search Console TXT value is separate from a host's domain-verification record. Add the exact Google-issued value at the active DNS provider and keep it there after verification.
- After verification, confirm the live sitemap lists only the published canonical URLs, then submit it. Inspect the canonical homepage with URL Inspection and review sitemap processing and indexing reports over time.
- Request indexing for a changed or new page when useful. Verification, sitemap submission, and indexing requests do not guarantee that Google will crawl or show a page.

### Bing Webmaster Tools

- Add and verify the site, submit the same canonical sitemap, and use URL Inspection or Site Explorer to diagnose crawl and indexing issues.
- If an import-from-Google option is offered, it can save setup time; still check that the correct domain and sitemap were imported.

### Analytics

- Create the property and web data stream for the production domain, install the official tag, and confirm activity with the service's real-time/debug view.
- Define a small number of useful events before adding tracking. Examples: contact CTA clicked, form successfully submitted, or demo started.
- Keep tracking consent, retention, and privacy notice aligned with the site's actual data collection and visitor locations.

## Business listings and reviews

- Use directories that your actual customers consult and where the business is eligible to appear. Keep name, contact details, service area, and website consistent.
- Ask only real customers for honest feedback based on their actual experience. Do not buy, fabricate, or selectively manipulate reviews.
- A listing or review profile is not automatically useful for every online business; confirm eligibility and maintain it before creating one.

## Ongoing checks

After each deployment, confirm that the preferred HTTPS URL loads, the page returns successfully, the canonical and social URLs still match, the sitemap and robots file are reachable, and contact paths work. Recheck Search Console and Bing for crawl errors. When adding a public page, give it a unique title and description and update the sitemap if needed.

## Details to collect for a future site-specific audit or prompt

- Project and business name
- Production domain and preferred canonical host
- Hosting platform, repository, and deployment method
- List of public pages and pages that must stay out of search
- Main visitor goal and primary contact/conversion actions
- Search Console and Bing verification status
- Sitemap and robots.txt locations
- Analytics tool, key events, and privacy/consent plan
- Target devices, audiences, service regions, and any factual-claim constraints
- Whether you want a report only, local edits, or an explicitly requested publication

When asking for a future website prompt, include these details and ask for a file-by-file audit, current-state checks, accurate claims, mobile review, and a final report. State clearly whether the work should be published or remain local.
