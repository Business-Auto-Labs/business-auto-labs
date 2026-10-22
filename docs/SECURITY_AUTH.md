# Login and data security

## Current state

The marketing website works on GitHub Pages. The login page is an integration scaffold, not a live authentication system: js/auth-config.js has empty values, no users have been invited, and the portal contains only a public placeholder. Do not place private documents or client records in this repository.

GitHub Pages serves static files publicly. A password form, client-side redirect, noindex tag, or robots.txt rule does not stop someone from opening a static file directly. Do not treat this scaffold as a protected client portal until an identity provider is configured and private data is enforced by a backend.

## Why the website does not keep passwords

Use an identity provider such as Supabase Auth. Its Auth service stores credentials as salted password hashes and checks them on its servers over HTTPS. The account email is the login name. Do not create a public table for passwords, do not log them, and never commit them.

The only browser key allowed here is the project's publishable key (or legacy anon key). It is designed to be visible and is safe only when database access rules are correct. A service-role or secret key bypasses those rules and must stay server-side.

## Configure Supabase before inviting users

1. Create a Supabase project and enable email/password authentication.
2. In js/auth-config.js, set supabaseUrl and publishableKey. These values are public configuration; never paste a secret key.
3. In Supabase Authentication URL settings, use the intended Pages site URL https://business-auto-labs.github.io/business-auto-labs and allow the exact redirect https://business-auto-labs.github.io/business-auto-labs/login.html?mode=recovery. Add localhost redirects only for development. Update both when a custom domain is active. These settings are documented for later setup; the current Supabase configuration is blank and sign-in is inactive.
4. Disable public sign-ups and anonymous sign-ins. Invite only known users from the Supabase dashboard, and require email confirmation.
5. Configure a minimum password length of at least 12 characters. Require MFA for administrators. Keep recovery tied to a verified email.
6. Review the project's current Auth rate limits. Supabase documents endpoint-specific per-IP limits; its token endpoint currently allows 150 requests per five-minute window by default, with bursts, while several signup, recovery, and email endpoints have separate 30-request defaults. Confirm the current settings and tune them for the project. These limits slow automated guessing but do not make brute force impossible and are not a permanent per-account lockout.
7. Consider enabling a CAPTCHA provider supported by Supabase Auth, such as hCaptcha or Cloudflare Turnstile. This page does not include the CAPTCHA widget/token yet, so do not turn provider-side CAPTCHA on until the matching browser component is added and verified.
8. Before adding any data, enable RLS on every table and storage bucket. Write policies that check the signed-in user and their role or tenant for every operation. Test with a normal user, not only a project administrator.
9. Publish a privacy notice that explains what account and contact data is collected before inviting clients.

Official references: [Supabase Auth](https://supabase.com/docs/guides/auth), [password security](https://supabase.com/docs/guides/auth/password-security), [rate limits](https://supabase.com/docs/guides/auth/rate-limits), [CAPTCHA setup](https://supabase.com/docs/guides/auth/auth-captcha), and [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security).

## Before this can hold real client information

The portal route checks a Supabase session in browser JavaScript. That is only suitable for a sign-in shell with no secrets. A client can still download any static page or asset from GitHub Pages. For private records, request data from Supabase with RLS or from an authenticated server API; never embed records in HTML, a JSON file, or JavaScript. For highly sensitive work, move the portal to a server-rendered application with server-managed sessions and secure, HttpOnly cookies.

The current page does not create accounts, store profiles, or expose an application table. Supabase Auth's internal auth schema owns credentials. Add profile or project tables only when their access model is defined and RLS policies are ready.
