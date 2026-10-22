# GitHub Pages deployment

## Preview locally

Open this folder in VS Code and use Live Server, or run python -m http.server 8000 from this project folder and visit http://localhost:8000. The static marketing page needs no build step. Login remains unavailable until a provider is configured with a localhost redirect URL.

## Publish with GitHub Pages

The repository is Business-Auto-Labs/business-auto-labs. GitHub Pages currently lists `https://business-auto-labs.github.io/business-auto-labs/` as the public address. The canonical, social, sitemap, robots, structured-data, and authentication redirect settings use that address. A successful Pages build is required to confirm a deployment.

1. Save and review changes in VS Code.
2. From the project folder, run git status and git diff. Then stage and commit the intended files with a clear message.
3. Push the main branch using your normal GitHub sign-in method.
4. In GitHub, open repository Settings → Pages and confirm the source. Check that the Pages deployment completes successfully.
5. Open the published URL, review phone and desktop layouts, click contact links, and check for browser console errors.

Do not commit private keys, passwords, real client records, or private project files. js/auth-config.js may contain only the Supabase project URL and public publishable key.

## Supabase login setup

The public Client login link stays hidden while js/auth-config.js has blank Supabase settings. Follow SECURITY_AUTH.md before enabling accounts. If you add a custom domain, update the Supabase Site URL and allowed redirects, siteBaseUrl in js/auth-config.js, canonical and Open Graph URLs, structured-data URL, robots.txt, and sitemap.xml.

## Connect businessautomationlabs.com to GitHub Pages

The domain is purchased, but it has not been connected to the Pages site yet. The site's public canonical, social, sitemap, robots, and authentication redirect URLs therefore still use the GitHub Pages address. Switch these only after the custom domain and HTTPS have been verified.

### 1. Verify domain ownership with GitHub

GitHub recommends verifying the domain before assigning it to the repository. In GitHub, open your profile **Settings → Code and automation → Pages → Add a domain**. Enter `businessautomationlabs.com`. GitHub will show a unique TXT record name and value. In Namecheap, open **Domain List → Manage → Advanced DNS → Host Records**, add the TXT record exactly as GitHub shows it, then return to GitHub and complete verification. If Namecheap does not let you edit host records, check which nameservers the domain uses and add the TXT record at that DNS provider instead. Keep the TXT record in DNS so the verification stays in place.

### 2. Add the domain to the repository

Open the `Business-Auto-Labs/business-auto-labs` repository and choose **Settings → Pages**. Under **Custom domain**, enter `businessautomationlabs.com` and save. For branch-based Pages publishing, GitHub adds a `CNAME` file at the publishing branch root. A custom GitHub Actions workflow does not need that file. If GitHub creates a commit, pull that change before making a later push from your local checkout.

### 3. Point Namecheap DNS to GitHub Pages

In Namecheap, open **Domain List → Manage → Advanced DNS**. Host records are editable there when the domain uses Namecheap BasicDNS, PremiumDNS, or FreeDNS. If the domain uses other nameservers, make the records at the DNS provider those nameservers belong to.

Add these records:

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

### 5. Switch the site's public URLs and publish

After the domain resolves over HTTPS, update all references together before publishing the final custom-domain version:

- `index.html`: canonical URL, Open Graph URL/image URL, and structured-data URL.
- `robots.txt` and `sitemap.xml`: use the new HTTPS domain.
- `js/auth-config.js` and Supabase allowed redirect URLs: update only if authentication is configured.
- `README.md` and this deployment guide: describe the active domain accurately.

Review the changed files in VS Code, commit the intended website changes, and push them to the `main` branch using the existing GitHub workflow. Open the custom domain after the Pages deployment succeeds and check that the CSS, images, contact links, and navigation load correctly. Do not remove the old GitHub Pages URL from use until the new domain passes these checks.

### 6. Request Google Search discovery

Once the custom domain is live, add a **Domain property** for `businessautomationlabs.com` in Google Search Console, verify it using the TXT record Google provides, and submit `https://businessautomationlabs.com/sitemap.xml`. Use URL Inspection to request a crawl. Google controls crawling and indexing; setup and sitemap submission do not guarantee that the site will appear in search.

Official instructions: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-your-custom-domain-for-your-github-pages-site), [GitHub domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages), [GitHub HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https), [Namecheap host records](https://www.namecheap.com/support/knowledgebase/article.aspx/434/2237/how-do-i-set-up-host-records-for-a-domain/), and [Google Search Console](https://developers.google.com/search/docs/monitor-debug/search-console-start).
