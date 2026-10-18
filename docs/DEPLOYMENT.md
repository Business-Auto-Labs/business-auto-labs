# GitHub Pages and custom domain

## Preview locally

Open the folder in VS Code and use Live Preview or Live Server, or run python -m http.server 8000 in this project folder. Open http://localhost:8000. This is a static site and needs no install or build command.

## Publish with GitHub Pages

1. Create a GitHub repository for the site. Files in a public repository are public; do not add secrets.
2. In VS Code's terminal, run these commands, replacing the sample repository details:

   git init
   git add .
   git commit -m "Build Business Automation Labs website"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPOSITORY.git
   git push -u origin main

3. On GitHub, open Settings, then Pages. Choose Deploy from a branch, select main and the root folder, then save.
4. Wait for the deployment to complete. Open the URL shown in Pages and check desktop, phone, links, and the browser console.

A project repository URL contains /REPOSITORY/. CSS, JavaScript, and image references are relative so they can resolve under this subdirectory.

## Add a custom domain

Register the domain. In Pages settings, enter it and save. Configure DNS at the registrar using GitHub's current instructions for either an apex domain or subdomain. DNS updates can take time. Once the domain is correctly serving the site, enable Enforce HTTPS when available.

The canonical URL is initially https://code-neel.github.io/business-auto-labs/. After configuring a custom domain, update the canonical and Open Graph URLs, robots.txt sitemap URL, and sitemap.xml URL together. Verify the social image URL and test the preferred hostname and its redirect.

## Updates and rollback

Make a small change, preview it, then commit and push. Pages republishes the configured branch. Use commit history to inspect or revert a change. Before launch, check that Pages shows a successful build and the deployed certificate is valid.

This guide describes the setup steps; the project owner should verify each deployment in GitHub Pages. GitHub interface and DNS instructions can change, so use the linked current Pages documentation before editing records.

## Official GitHub guidance
- [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-your-custom-domain-for-your-github-pages-site)
- [Securing GitHub Pages with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)

### DNS record examples
For an apex domain such as example.com, GitHub currently documents four A records with host @ and values 185.199.108.153, 185.199.109.153, 185.199.110.153, and 185.199.111.153. Its optional IPv6 AAAA records are listed in the official HTTPS guide below.
For a subdomain such as www.example.com, create a CNAME with host www pointing to USERNAME.github.io (replace USERNAME with the account or organization that owns the Pages site). Do not point a CNAME at the domain apex or use a wildcard DNS record. DNS providers label fields differently; check the linked official instructions for the chosen domain type before saving changes.


