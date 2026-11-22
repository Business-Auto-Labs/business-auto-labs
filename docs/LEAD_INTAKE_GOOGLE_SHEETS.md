# Lead intake and Google Sheets — future setup

## Current state

The public website does **not** book services, submit a lead form, or write to Google Sheets. Its working contact routes are email, phone, and the confirmed WhatsApp choices. There is no configured backend, spreadsheet, privacy notice, or data-retention policy. Do not collect client information in a static form or add credentials to this repository.

A conversation or enquiry is not a confirmed booking. If the business later wants customers to select an appointment time, connect a real calendar/booking provider and keep its confirmation status separate from a lead request.

## Proposed minimum data

Create one restricted Sheet for follow-up requests, not a public customer database. Keep the form limited to the fields the team needs:

| Column | Value |
| --- | --- |
| **received_at_utc** | Set by the server when the request is accepted. |
| **name** | Customer-provided name. |
| **service_requested** | One of WhatsApp automation, web development, logo/graphic design, or social/Meta Ads. |
| **follow_up_method** | Email or phone. |
| **follow_up_contact** | One address or international phone number, matching the selected method. |
| **follow_up_consent_at_utc** | Server-recorded time after the user agrees to be contacted. |
| **status** | New, contacted, or closed; update only for actual follow-up. |

Avoid collecting passwords, payment details, identity documents, private business credentials, or unnecessary free-form sensitive information. Do not put private client project records in the lead sheet.

## Recommended request path

Website form → Supabase Edge Function → Google Sheets API → restricted Sheet

1. **Create a private Sheet.** Keep sharing restricted to named team members who need access. Require MFA on their Google accounts. Do not use “anyone with the link.”
2. **Create the Google Cloud service identity.** Enable the Sheets API and grant the service account editor access to this one Sheet only. Do not add it to a broad Drive folder or share it with the public.
3. **Build a server-side function.** Add a Supabase Edge Function that validates the allowlisted service value, name/contact lengths and formats, chosen follow-up method, and consent. Set the timestamp and status server-side. Never accept a spreadsheet ID or row range supplied by the browser.
4. **Keep credentials server-side.** Store the Google credential and spreadsheet ID only in Supabase Function secrets. Never place them in HTML, browser JavaScript, js/config.js, a public environment file, or Git. The browser may call the function, but it must never receive the Google credential or spreadsheet contents.
5. **Reduce public-endpoint abuse.** Add CAPTCHA/Turnstile or another supported challenge, request throttling, payload-size limits, origin checks as an additional signal, safe error messages, and duplicate-submit protection. An origin check alone is not authorization. Do not log contact values, OTPs, tokens, or request bodies.
6. **Explain the collection before enabling it.** Publish a privacy notice that identifies the purpose, who can see the lead, how long it is kept, how someone can request correction/deletion, and the contact for privacy questions. Ask for clear consent to the stated follow-up. Have the owner obtain appropriate local privacy-law advice before collecting real leads.
7. **Test with dummy data only.** Verify a valid request adds one row, invalid/oversized/no-consent requests are rejected, repeat clicks do not create uncontrolled duplicate rows, browser responses reveal no sheet data, and unauthorized users cannot list or read the Sheet. Confirm that deleting a test lead works. Do not test with real customers until the controls and notice are approved.
8. **Set a retention period and an owner.** Record who reviews new leads, who can edit them, how long inactive enquiries remain, and how deletions are carried out. Do not choose a retention period by guesswork.
9. **Enable the website form only after review.** Configure the backend endpoint, CAPTCHA, privacy copy, and secure secrets first. A form with no active backend stays out of the public UI.

## Separate the lead sheet from the client portal

Google Sheets is a limited follow-up queue, not an identity system or authorization layer. Keep client work files in a storage service with access controls or a backend whose authorization is enforced on every request. If private client records are ever added, every Supabase table and storage bucket needs reviewed Row Level Security policies. GitHub Pages cannot protect a static file or serve as the private-data boundary.

## Official setup references

- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Supabase Function secrets](https://supabase.com/docs/guides/functions/secrets)
- [Google Sheets values.append](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values.append)
- [Supabase CAPTCHA](https://supabase.com/docs/guides/auth/auth-captcha)

This document is a proposed implementation plan. Nothing described here is active in the website yet.
