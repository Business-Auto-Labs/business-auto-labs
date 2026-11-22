// Public browser configuration only. Keep Supabase service-role and provider secrets server-side.
// Sign-in buttons stay disabled until Supabase, Google OAuth, WhatsApp OTP, abuse controls,
// redirects, and backend access policies have been configured and reviewed.
window.BUSINESS_AUTH_CONFIG = {
  supabaseUrl: "",
  publishableKey: "",
  googleEnabled: false,
  whatsappEnabled: false,
  siteBaseUrl: "https://businessautomationlabs.com"
};
