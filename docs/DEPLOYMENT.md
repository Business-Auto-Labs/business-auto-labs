# GitHub Pages deployment

## Preview locally

Open this folder in VS Code and use Live Server, or run python -m http.server 8000 from this project folder and visit http://localhost:8000. The static marketing page needs no build step. Login remains unavailable until a provider is configured with a localhost redirect URL.

## Publish with GitHub Pages

The repository is Business-Auto-Labs/business-auto-labs. The configured public domain is `https://businessautomationlabs.com/`, and the root `CNAME` file names `businessautomationlabs.com`. The homepage canonical, social metadata, sitemap, robots sitemap reference, structured-data URL, and browser authentication redirect base use this domain. Check repository Settings → Pages and the latest Pages workflow to confirm DNS, HTTPS, and deployment status.

1. Save and review changes in VS Code.
2. From the project folder, run git status and git diff. Then stage and commit the intended files with a clear message.
3. Push the main branch using your normal GitHub sign-in method.
4. In GitHub, open repository Settings → Pages and confirm the source. Check that the Pages deployment completes successfully.
5. Open the published URL, review phone and desktop layouts, click contact links, and check for browser console errors.

Do not commit private keys, passwords, real client records, or private project files. js/auth-config.js may contain only the Supabase project URL and public publishable key.

## Supabase login setup

The public Client login link stays hidden while js/auth-config.js has blank Supabase settings. Follow SECURITY_AUTH.md before enabling accounts. If the domain changes, update the Supabase Site URL and allowed redirects, siteBaseUrl in js/auth-config.js, canonical and Open Graph URLs, structured-data URL, robots.txt, and sitemap.xml together.

## Verify the custom domain on GitHub Pages

The repository is configured to use businessautomationlabs.com. The following steps help verify or repair GitHub and Namecheap settings if the domain or HTTPS check fails. Keep the site URLs on the custom HTTPS domain once the domain is resolving correctly.

### 1. Verify domain ownership with GitHub

Check that GitHub has verified ownership of `businessautomationlabs.com`. If verification is missing, open **Settings → Code and automation → Pages → Add a domain**, copy the TXT hostname and value GitHub provides, add that exact record at the active DNS provider, and verify again. Keep the TXT record in DNS.

### 2. Confirm the domain on the repository

Open the `Business-Auto-Labs/business-auto-labs` repository and choose **Settings → Pages**. Confirm that **Custom domain** is `businessautomationlabs.com`. For branch-based Pages publishing, the root `CNAME` file should contain that domain. A custom GitHub Actions workflow does not need the file.

### 3. Point Namecheap DNS to GitHub Pages

In Namecheap, open **Domain List → Manage → Advanced DNS**. Host records are editable there when the domain uses Namecheap BasicDNS, PremiumDNS, or FreeDNS. If the domain uses other nameservers, make the records at the DNS provider those nameservers belong to.

Confirm these records are present at the active DNS provider:

| Type | Host | Value |
| --- | --- | --- |
| A Record | `@` | `185.199.108.153` |
| A Record | `@` | `185.199.109.153` |
| A Record | `@` | `185.199.110.153` |
| A Record | `@` | `185.199.111.153` |
| CNAME Record | `www` | `business-auto-labs.github.io` |

The `www` value is the GitHub organization domain only; do not append `/business-auto-labs/`. Remove conflicting Namecheap parking or redirect records for `@` and the parking CNAME for `www` if present. Keep any mail-related MX and TXT records. Do not add wildcard records. GitHub Pages will redirect `www.businessautomationlabs.com` to the apex domain when both are configured correctly.

### 4. Wait for DNS and enable HTTPS

DNS changes can take up to 24 hours to propagate. Return to **Repository Settings → Pages** and wait for GitHub's DNS check and certificate provisioning to finish. When the option is available, turn on **Enforce HTTPS**. Test both `https://businessautomationlabs.com` and `https://www.businessautomationlabs.com`; the final URL should resolve securely and the latter should redirect to the apex address.

### 5. Keep the site URLs aligned and publish

The site source now targets `https://businessautomationlabs.com/`. Keep these values aligned in future edits:

- `index.html`: canonical URL, Open Graph URL/image URL, and structured-data URL.
- `robots.txt` and `sitemap.xml`: keep using `https://businessautomationlabs.com/`.
- `js/auth-config.js` and Supabase allowed redirect URLs: update only if authentication is configured.
- `README.md` and this deployment guide: describe the active domain accurately.

Review the changed files, then publish through the existing GitHub workflow when ready. After the Pages workflow succeeds, open the custom domain and check that the CSS, images, contact links, and navigation load correctly. This source change alone does not confirm a deployment.

### 6. Request Google Search discovery

The **Domain property** for `businessautomationlabs.com` is verified in Google Search Console using its TXT record in Namecheap. Keep that record in DNS. After publishing, confirm the live sitemap lists the custom-domain homepage, then submit `https://businessautomationlabs.com/sitemap.xml` and use URL Inspection to check the homepage. Google controls crawling and indexing; setup and sitemap submission do not guarantee that the site will appear in search.

Official instructions: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-your-custom-domain-for-your-github-pages-site), [GitHub domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages), [GitHub HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), [Namecheap host records](https://www.namecheap.com/support/knowledgebase/article.aspx/434/2237/how-do-i-set-up-host-records-for-a-domain/), and [Google Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
