// Supabase Auth manages identities and password hashes. This website never stores
// or logs passwords in its own files or tables.
const authSettings = window.BUSINESS_AUTH_CONFIG || {};
const authStatus = document.querySelector("[data-auth-status]");
const setupNotice = document.querySelector("[data-auth-setup]");
const loginForm = document.querySelector("[data-login-form]");
const recoveryForm = document.querySelector("[data-recovery-form]");
const resetButton = document.querySelector("[data-reset-button]");
const signoutButton = document.querySelector("[data-signout]");
const portalEmail = document.querySelector("[data-portal-email]");
const isConfigured = Boolean(authSettings.supabaseUrl && authSettings.publishableKey);
const isPortal = Boolean(signoutButton);
const isRecovery = new URLSearchParams(location.search).get("mode") === "recovery";
let authClient = null;

function showMessage(message, isError) {
  if (!authStatus) return;
  authStatus.textContent = message;
  authStatus.classList.toggle("is-error", Boolean(isError));
}
function setBusy(form, busy) {
  const button = form?.querySelector('button[type="submit"]');
  if (button) { button.disabled = busy; button.setAttribute("aria-busy", String(busy)); }
}
function disableLoginControls() {
  [loginForm, recoveryForm].filter(Boolean).forEach((form) => {
    form.querySelectorAll("input,button").forEach((field) => { field.disabled = true; });
  });
  if (resetButton) resetButton.disabled = true;
}
function isRateLimited(error) {
  return error?.status === 429 || /rate limit|too many/i.test(error?.message || "");
}

document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

if (setupNotice) setupNotice.hidden = isConfigured;

if (isConfigured && window.supabase?.createClient) {
  try {
    authClient = window.supabase.createClient(authSettings.supabaseUrl, authSettings.publishableKey);
    authClient.auth.onAuthStateChange((event, session) => {
      if (isPortal && portalEmail && session?.user?.email) portalEmail.textContent = "Signed in as " + session.user.email;
      if (event === "PASSWORD_RECOVERY" && recoveryForm) {
        recoveryForm.hidden = false;
        if (loginForm) loginForm.hidden = true;
        if (resetButton) resetButton.hidden = true;
        showMessage("Choose a new password for your account.", false);
      }
    });
    authClient.auth.getSession().then(({ data }) => {
      const session = data?.session;
      if (isPortal && !session) { location.replace("../login.html?message=session"); return; }
      if (isPortal && portalEmail && session?.user?.email) {
        portalEmail.textContent = "Signed in as " + session.user.email;
        showMessage("You are signed in. No private project data is connected yet.", false);
      }
      if (!isPortal && session && !isRecovery) location.replace("portal/");
    }).catch(() => showMessage("We could not check your session. Refresh the page and try again.", true));
  } catch {
    authClient = null;
    disableLoginControls();
    if (setupNotice) {
      setupNotice.hidden = false;
      setupNotice.textContent = "The sign-in service could not be initialized. Check the public provider settings and try again.";
    }
  }
} else {
  disableLoginControls();
  if (isPortal) showMessage("Portal setup is incomplete. Sign-in is not active yet.", true);
  if (isConfigured && setupNotice) {
    setupNotice.hidden = false;
    setupNotice.textContent = "The sign-in library could not be loaded. Check your connection and reload this page.";
  }
}

if (loginForm) loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!authClient) { showMessage("Sign-in is not configured yet.", true); return; }
  const values = new FormData(loginForm);
  const email = String(values.get("email") || "").trim();
  const password = String(values.get("password") || "");
  setBusy(loginForm, true);
  showMessage("Signing in…", false);
  try {
    const { error } = await authClient.auth.signInWithPassword({ email, password });
    if (error) {
      showMessage(isRateLimited(error) ? "Too many attempts. Please wait a few minutes before trying again." : "We could not sign you in with those details. Check them or contact the studio.", true);
      return;
    }
    location.assign("portal/");
  } catch {
    showMessage("The sign-in service is unavailable right now. Please try again shortly.", true);
  } finally {
    setBusy(loginForm, false);
  }
});

if (resetButton) resetButton.addEventListener("click", async () => {
  if (!authClient) { showMessage("Password recovery is not configured yet.", true); return; }
  const emailInput = document.querySelector("#email");
  const email = emailInput?.value.trim();
  if (!email) {
    emailInput?.focus();
    showMessage("Enter your business email above, then choose password reset again.", true);
    return;
  }
  resetButton.disabled = true;
  showMessage("Sending a reset link if this account is eligible…", false);
  const redirectUrl = authSettings.siteBaseUrl.replace(/\/$/, "") + "/login.html?mode=recovery";
  try {
    const { error } = await authClient.auth.resetPasswordForEmail(email, { redirectTo: redirectUrl });
    if (error && isRateLimited(error)) {
      showMessage("Too many requests. Please wait before requesting another email.", true);
      return;
    }
    // Use the same response for known and unknown accounts to avoid account discovery.
    showMessage("If the account is eligible, a password reset link will arrive by email.", false);
  } catch {
    showMessage("The reset service is unavailable. Please try again shortly.", true);
  } finally {
    resetButton.disabled = false;
  }
});

if (recoveryForm) recoveryForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!authClient) { showMessage("Password recovery is not configured yet.", true); return; }
  const values = new FormData(recoveryForm);
  const password = String(values.get("new-password") || "");
  const confirmation = String(values.get("confirm-password") || "");
  if (password.length < 12) { showMessage("Use at least 12 characters for your new password.", true); return; }
  if (password !== confirmation) { showMessage("The password fields do not match.", true); return; }
  setBusy(recoveryForm, true);
  try {
    const { error } = await authClient.auth.updateUser({ password });
    if (error) { showMessage("We could not update the password. Request a fresh reset link and try again.", true); return; }
    showMessage("Password updated. You can now sign in with the new password.", false);
    recoveryForm.hidden = true;
    if (loginForm) loginForm.hidden = false;
    if (resetButton) resetButton.hidden = false;
    document.querySelector("#password")?.focus();
  } catch {
    showMessage("The password service is unavailable. Please try again shortly.", true);
  } finally {
    setBusy(recoveryForm, false);
  }
});

if (signoutButton) signoutButton.addEventListener("click", async () => {
  if (!authClient) { showMessage("Sign-out is not configured.", true); return; }
  signoutButton.disabled = true;
  try {
    const { error } = await authClient.auth.signOut();
    if (error) { showMessage("We could not sign you out. Please try again.", true); signoutButton.disabled = false; return; }
    location.replace("../login.html");
  } catch {
    signoutButton.disabled = false;
    showMessage("The sign-out service is unavailable. Please try again.", true);
  }
});

if (new URLSearchParams(location.search).get("message") === "session" && !isPortal) {
  showMessage("Please sign in to continue.", false);
}