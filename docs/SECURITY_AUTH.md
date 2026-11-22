# Authentication and data security

## Current state — not live

The website is a public static GitHub Pages site. The redesigned sign-in page shows Google and WhatsApp options, but both controls are disabled. js/auth-config.js has a blank Supabase URL and publishable key, with Google and WhatsApp flags set to false. No public navigation link exposes the sign-in page. The portal route is a public placeholder with no private records; noindex and JavaScript redirects are not access controls.

The sign-in code is a gated integration scaffold. It does not collect or store passwords. A future Google flow uses Supabase OAuth with an account-selection prompt. A future WhatsApp flow requests a one-time code for an already-created account and asks for a nickname after the identity is verified. The nickname is display metadata only; never use it for authorization. These flows have not been connected to a provider or verified against a live project.

## Static hosting boundary

GitHub Pages serves every committed HTML, CSS, JavaScript, and asset file publicly. A private-looking URL, client-side session check, noindex tag, robots rule, or hidden link cannot protect a static document. Never commit client records, credentials, private reports, or tokens. A Supabase publishable key is intended to appear in browser code, but it is safe only when database and storage policies are correct. A service-role or secret key must never reach the browser.

A browser-managed Supabase session can support public UI and RLS-protected API calls, but it is not the right boundary for highly sensitive client records. Move a private portal to a server-backed application with server-validated sessions and appropriate secure, HttpOnly cookies before placing confidential files or records there.

## Requirements before turning on sign-in

1. Create the Supabase project and configure the exact public site URL and exact redirect allowlist. Do not allow broad wildcard redirects.
2. Decide who is allowed to sign in. Disable public account creation unless an approved invite process is implemented. The WhatsApp code uses shouldCreateUser=false; Google OAuth still requires a server-side signup restriction or a before-user-created allowlist hook. Hiding buttons or checking the browser cannot enforce invitations.
3. Configure Google OAuth in the Supabase provider settings. Store the Google OAuth client secret only in Supabase/provider configuration. The account chooser can show accounts available in Google’s browser session or offer “Use another account”; the website cannot enumerate all Gmail accounts.
4. Configure WhatsApp phone OTP through a Twilio or Twilio Verify WhatsApp sender. Supabase currently documents WhatsApp OTP only with these providers. Use full E.164 numbers, verify regional requirements and message costs, and tell users why a code is sent.
5. Before enabling either provider, add CAPTCHA, set and review rate limits, monitor authentication logs, and test error behavior with invited and uninvited test identities. Use generic public responses where account existence could otherwise be exposed. Configure MFA for administrator accounts.
6. If the portal will ever read data, enable and test Row Level Security on every table and storage bucket. Policies must enforce user, project, and role boundaries on every operation. Test with ordinary invited accounts and cross-account attempts, not only an administrator.
7. Publish a privacy notice covering account identifiers, phone numbers, OTP delivery, nickname, support use, retention, and deletion before collecting real user data.
8. Review the pinned Supabase JavaScript CDN dependency and script integrity/supply-chain plan before activation. The library is loaded only when public auth configuration is set, but a third-party script executes with the page’s browser privileges.
9. Only after provider, redirect, signup, abuse controls, privacy, and access rules are configured should the owner set provider flags to true. Keep the sign-in link out of public navigation until then.

Supabase’s general Auth configuration supports disabling new-user signups; if access must be invite-only, use a server-side signup restriction rather than a UI check. Google sign-in should use the provider’s account chooser prompt, but that affects account selection only, not authorization.

## Google Sheets lead data

The public website does not submit a contact form to Google Sheets. Do not add a service-account key, unrestricted Apps Script URL, or sheet contents to browser code. If lead intake is approved later, use a server-side Edge Function to validate and append the minimal agreed fields. Keep the Google credential in server-side function secrets and grant its service account access only to the private lead Sheet. Add consent, CAPTCHA, rate limiting, retention, access ownership, and deletion before collecting real contacts. See [LEAD_INTAKE_GOOGLE_SHEETS.md](LEAD_INTAKE_GOOGLE_SHEETS.md).

## Verification status

- Public sign-in controls: disabled in the current configuration.
- Supabase URL/key: blank; no live provider requests are made by the static sign-in page.
- Client portal: placeholder only; contains no private data and is publicly served.
- Google Sheets: no form, endpoint, or credential configured.
- Security assurance: no claim that the site has no vulnerabilities or is secure for private records. A full audit and live-provider verification remain necessary before any sensitive-data feature is enabled.

## Official references

- [Supabase Auth general configuration](https://supabase.com/docs/guides/auth/general-configuration)
- [Supabase Google login](https://supabase.com/docs/guides/auth/social-login/auth-google)
- [Supabase phone login and WhatsApp support](https://supabase.com/docs/guides/auth/phone-login?showSmsProvider=Twilio)
- [Supabase JavaScript signInWithOtp](https://supabase.com/docs/reference/javascript/auth-signinwithotp)
- [Supabase CAPTCHA](https://supabase.com/docs/guides/auth/auth-captcha)
- [Supabase rate limits](https://supabase.com/docs/guides/auth/rate-limits)
- [Supabase Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase Before User Created Hook](https://supabase.com/docs/guides/auth/auth-hooks/before-user-created-hook)
- [Google OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect)
