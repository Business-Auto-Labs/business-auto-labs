// The browser handles identity redirects only when public auth configuration is complete.
// Supabase stores identities; this site never collects or stores passwords.
(() => {
  const settings = window.BUSINESS_AUTH_CONFIG || {};
  const status = document.querySelector("[data-auth-status]");
  const setupNotice = document.querySelector("[data-auth-setup]");
  const googleButton = document.querySelector("[data-google-login]");
  const phoneForm = document.querySelector("[data-phone-form]");
  const phoneInput = phoneForm?.querySelector("[name='phone']");
  const otpForm = document.querySelector("[data-otp-form]");
  const otpInput = otpForm?.querySelector("[name='otp']");
  const nicknameForm = document.querySelector("[data-nickname-form]");
  const nicknameInput = nicknameForm?.querySelector("[name='nickname']");
  const backToPhone = document.querySelector("[data-back-to-phone]");
  const sendOtp = document.querySelector("[data-send-otp]");
  const signoutButton = document.querySelector("[data-signout]");
  const portalGreeting = document.querySelector("[data-portal-email]");
  const isPortal = Boolean(signoutButton);
  const googleEnabled = settings.googleEnabled === true;
  const whatsappEnabled = settings.whatsappEnabled === true;
  const isConfigured = Boolean(settings.supabaseUrl && settings.publishableKey && (googleEnabled || whatsappEnabled));
  let client = null;
  let pendingUser = null;
  let lastHandledUserId = "";

  function showMessage(message, isError = false) {
    if (!status) return;
    status.textContent = message;
    status.classList.toggle("is-error", isError);
  }

  function setBusy(button, busy, busyLabel, normalLabel) {
    if (!button) return;
    button.disabled = busy;
    button.setAttribute("aria-busy", String(busy));
    if (busyLabel && normalLabel) button.textContent = busy ? busyLabel : normalLabel;
  }

  function setInitialAvailability() {
    if (googleButton) googleButton.disabled = !isConfigured || !googleEnabled;
    if (signoutButton) signoutButton.disabled = !isConfigured;
    phoneForm?.querySelectorAll("input,button").forEach((field) => {
      field.disabled = !isConfigured || !whatsappEnabled;
    });
    if (setupNotice) setupNotice.hidden = isConfigured;
    if (!isConfigured) {
      showMessage(isPortal
        ? "This public portal preview has no private data and sign-in is not configured."
        : "Sign-in is not active. Do not enter a phone number or verification code yet.");
    }
  }

  function loadSupabaseLibrary() {
    if (window.supabase?.createClient) return Promise.resolve(window.supabase);
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.118.0/dist/umd/supabase.js";
      script.crossOrigin = "anonymous";
      script.referrerPolicy = "no-referrer";
      script.onload = () => window.supabase?.createClient ? resolve(window.supabase) : reject(new Error("Sign-in library unavailable"));
      script.onerror = () => reject(new Error("Sign-in library unavailable"));
      document.head.append(script);
    });
  }

  function showNickname(user) {
    pendingUser = user;
    if (setupNotice) setupNotice.hidden = true;
    if (googleButton) googleButton.hidden = true;
    if (phoneForm) phoneForm.hidden = true;
    if (otpForm) otpForm.hidden = true;
    if (nicknameForm) nicknameForm.hidden = false;
    showMessage("Identity confirmed. Choose a nickname for your workspace.");
    nicknameInput?.focus();
  }

  function handleSignedInUser(user) {
    if (!user || user.id === lastHandledUserId) return;
    lastHandledUserId = user.id;
    const nickname = String(user.user_metadata?.nickname || "").trim();
    if (isPortal) {
      if (portalGreeting) portalGreeting.textContent = "Welcome, " + (nickname || user.email || user.phone || "client") + ".";
      showMessage("Signed in. This portal preview contains no private project records.");
      return;
    }
    if (nickname) {
      location.replace("portal/");
      return;
    }
    showNickname(user);
  }

  async function initialize() {
    document.querySelectorAll("[data-current-year]").forEach((element) => {
      element.textContent = String(new Date().getFullYear());
    });
    setInitialAvailability();
    if (!isConfigured) return;

    try {
      const supabase = await loadSupabaseLibrary();
      client = supabase.createClient(settings.supabaseUrl, settings.publishableKey, {
        auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
      });
      const { data, error } = await client.auth.getSession();
      if (error) throw error;
      if (isPortal && !data.session) {
        location.replace("../login.html?message=session");
        return;
      }
      if (data.session?.user) handleSignedInUser(data.session.user);
      client.auth.onAuthStateChange((event, session) => {
        if (event === "SIGNED_IN" && session?.user) handleSignedInUser(session.user);
        if (event === "SIGNED_OUT" && isPortal) location.replace("../login.html");
      });
      const params = new URLSearchParams(location.search);
      if (params.get("message") === "session" && !isPortal) showMessage("Please sign in to continue.");
      if (params.has("error")) showMessage("We could not complete sign-in. Please try again or contact the studio.", true);
    } catch {
      if (googleButton) googleButton.disabled = true;
      phoneForm?.querySelectorAll("input,button").forEach((field) => { field.disabled = true; });
      if (setupNotice) {
        setupNotice.hidden = false;
        setupNotice.textContent = "The sign-in service could not be initialized. Sign-in controls are disabled; contact the studio if you need access.";
      }
      showMessage("Sign-in is unavailable right now. No details were sent.", true);
    }
  }

  googleButton?.addEventListener("click", async () => {
    if (!client || !googleEnabled) return;
    setBusy(googleButton, true, "Opening Google…", "Continue with Google");
    showMessage("Continue in Google’s account chooser.");
    try {
      const redirectTo = settings.siteBaseUrl.replace(/\/$/, "") + "/login.html";
      const { error } = await client.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo, queryParams: { prompt: "select_account" } }
      });
      if (error) throw error;
    } catch {
      showMessage("We could not start Google sign-in. Check your connection or contact the studio.", true);
      setBusy(googleButton, false, "Opening Google…", "Continue with Google");
    }
  });

  phoneForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!client || !whatsappEnabled) return;
    const phone = String(new FormData(phoneForm).get("phone") || "").trim();
    if (!/^\+[1-9]\d{7,14}$/.test(phone)) {
      showMessage("Enter the full international number, including + and country code.", true);
      phoneInput?.focus();
      return;
    }
    setBusy(sendOtp, true, "Requesting code…", "Send sign-in code");
    showMessage("Checking whether this number can receive a sign-in code…");
    try {
      const { error } = await client.auth.signInWithOtp({
        phone,
        options: { channel: "whatsapp", shouldCreateUser: false }
      });
      if (error) throw error;
      phoneForm.hidden = true;
      if (otpForm) otpForm.hidden = false;
      if (otpInput) otpInput.required = true;
      showMessage("If this number is eligible, a code will arrive on WhatsApp. Enter it to continue.");
      otpInput?.focus();
    } catch {
      // Use a generic response so this public page does not reveal whether a phone is registered.
      showMessage("We could not send a code. Check the number or contact the studio.", true);
    } finally {
      setBusy(sendOtp, false, "Requesting code…", "Send sign-in code");
    }
  });

  otpForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!client || !phoneInput?.value) return;
    const token = String(new FormData(otpForm).get("otp") || "").trim();
    if (!/^\d{4,10}$/.test(token)) {
      showMessage("Enter the digits from your WhatsApp message.", true);
      otpInput?.focus();
      return;
    }
    const button = otpForm.querySelector('button[type="submit"]');
    setBusy(button, true, "Verifying…", "Verify and continue");
    showMessage("Verifying your code…");
    try {
      const { data, error } = await client.auth.verifyOtp({ phone: phoneInput.value.trim(), token, type: "sms" });
      if (error) throw error;
      if (data?.user) handleSignedInUser(data.user);
    } catch {
      showMessage("That code could not be verified. Check it or request a new one.", true);
    } finally {
      setBusy(button, false, "Verifying…", "Verify and continue");
    }
  });

  backToPhone?.addEventListener("click", () => {
    if (otpForm) otpForm.hidden = true;
    if (phoneForm) phoneForm.hidden = false;
    if (otpInput) otpInput.value = "";
    showMessage("Enter the invited WhatsApp number again.");
    phoneInput?.focus();
  });

  nicknameForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!client || !pendingUser) return;
    const nickname = String(new FormData(nicknameForm).get("nickname") || "").trim();
    if (nickname.length < 2 || nickname.length > 40) {
      showMessage("Choose a nickname from 2 to 40 characters.", true);
      nicknameInput?.focus();
      return;
    }
    const button = nicknameForm.querySelector('button[type="submit"]');
    setBusy(button, true, "Saving…", "Save nickname and continue");
    showMessage("Saving your workspace nickname…");
    try {
      const { error } = await client.auth.updateUser({ data: { nickname } });
      if (error) throw error;
      location.replace("portal/");
    } catch {
      showMessage("We could not save that nickname. Please try again.", true);
    } finally {
      setBusy(button, false, "Saving…", "Save nickname and continue");
    }
  });

  signoutButton?.addEventListener("click", async () => {
    if (!client) return;
    signoutButton.disabled = true;
    try {
      const { error } = await client.auth.signOut();
      if (error) throw error;
      location.replace("../login.html");
    } catch {
      signoutButton.disabled = false;
      showMessage("We could not sign you out. Please try again.", true);
    }
  });

  initialize();
})();
