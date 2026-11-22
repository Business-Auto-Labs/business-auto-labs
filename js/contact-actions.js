// Contact actions keep mail and phone links usable without JavaScript.
// When JavaScript is available, a small dialog offers the matching app action
// and a copy option. The visitor always chooses before an app is opened.
(() => {
  function createContactDialog() {
    const dialog = document.createElement("dialog");
    dialog.className = "contact-dialog";
    dialog.setAttribute("data-contact-dialog", "");
    dialog.setAttribute("aria-labelledby", "contact-dialog-title");
    dialog.setAttribute("aria-describedby", "contact-dialog-description");

    const closeForm = document.createElement("form");
    closeForm.method = "dialog";
    closeForm.className = "contact-dialog__close-form";
    const closeButton = document.createElement("button");
    closeButton.type = "submit";
    closeButton.className = "contact-dialog__close";
    closeButton.setAttribute("aria-label", "Close contact options");
    closeButton.textContent = "×";
    closeForm.append(closeButton);

    const kicker = document.createElement("p");
    kicker.className = "eyebrow";
    kicker.textContent = "CONTACT OPTIONS";
    const title = document.createElement("h2");
    title.id = "contact-dialog-title";
    title.setAttribute("data-contact-dialog-title", "");
    title.textContent = "Choose how to contact us";
    const description = document.createElement("p");
    description.id = "contact-dialog-description";
    description.className = "contact-dialog__description";
    description.setAttribute("data-contact-dialog-description", "");
    const actions = document.createElement("div");
    actions.className = "contact-dialog__actions";
    actions.setAttribute("data-contact-dialog-actions", "");

    const fallback = document.createElement("label");
    fallback.className = "contact-copy-fallback";
    fallback.setAttribute("data-contact-copy-fallback", "");
    fallback.hidden = true;
    fallback.append(document.createTextNode("Contact detail"));
    const fallbackInput = document.createElement("input");
    fallbackInput.type = "text";
    fallbackInput.readOnly = true;
    fallbackInput.setAttribute("data-contact-copy-value", "");
    fallback.append(fallbackInput);

    const status = document.createElement("p");
    status.className = "contact-dialog__status";
    status.setAttribute("data-contact-dialog-status", "");
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");

    dialog.append(closeForm, kicker, title, description, actions, fallback, status);
    document.body.append(dialog);
    return dialog;
  }

  const dialog = createContactDialog();
  if (typeof dialog.showModal !== "function") return;
  const siteConfig = window.BUSINESS_SITE_CONFIG || {};

  const title = dialog.querySelector("[data-contact-dialog-title]");
  const description = dialog.querySelector("[data-contact-dialog-description]");
  const actions = dialog.querySelector("[data-contact-dialog-actions]");
  const status = dialog.querySelector("[data-contact-dialog-status]");
  const fallback = dialog.querySelector("[data-contact-copy-fallback]");
  const fallbackInput = dialog.querySelector("[data-contact-copy-value]");
  let lastTrigger = null;

  function makeAction(label, className, href, newTab = false) {
    const link = document.createElement("a");
    link.className = "contact-option " + className;
    link.href = href;
    link.textContent = label + " ";

    const arrow = document.createElement("span");
    arrow.setAttribute("aria-hidden", "true");
    arrow.textContent = "↗";
    link.append(arrow);

    if (newTab) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }

    actions.append(link);
    return link;
  }

  function makeCopyAction(value, label) {
    const button = document.createElement("button");
    button.className = "contact-option";
    button.type = "button";
    button.textContent = label + " ";

    const copyMark = document.createElement("span");
    copyMark.setAttribute("aria-hidden", "true");
    copyMark.textContent = "⧉";
    button.append(copyMark);

    button.addEventListener("click", async () => {
      try {
        if (!navigator.clipboard || !navigator.clipboard.writeText) {
          throw new Error("Clipboard access is unavailable.");
        }
        await navigator.clipboard.writeText(value);
        fallback.hidden = true;
        status.textContent = "Copied to your clipboard.";
      } catch {
        // Keep a selectable value visible if browser clipboard access is denied.
        fallbackInput.value = value;
        fallback.hidden = false;
        fallbackInput.focus();
        fallbackInput.select();
        status.textContent = "Select the highlighted detail and copy it.";
      }
    });

    actions.append(button);
  }

  function openOptions(trigger) {
    const type = trigger.dataset.contactType;
    const rawHref = trigger.getAttribute("href") || "";
    const value = rawHref.replace(/^(mailto:|tel:)/i, "");
    if (!value) return;

    lastTrigger = trigger;
    actions.replaceChildren();
    status.textContent = "";
    fallback.hidden = true;

    if (type === "email") {
      title.textContent = "Email Business Automation Labs";
      description.textContent = "Open a new message in Gmail or copy the business email address.";
      const composeUrl = new URL("https://mail.google.com/mail/");
      composeUrl.searchParams.set("view", "cm");
      composeUrl.searchParams.set("fs", "1");
      composeUrl.searchParams.set("to", value);
      const firstAction = makeAction("Open Gmail to compose", "contact-option--primary", composeUrl.toString(), true);
      makeCopyAction(value, "Copy email address");
      dialog.showModal();
      firstAction.focus();
      return;
    }

    if (type === "phone") {
      const contact = siteConfig.phoneContacts?.[trigger.dataset.contactId];
      const name = contact?.name || trigger.dataset.contactId || "this contact";
      const cleanNumber = value.replace(/[^\d+]/g, "");
      title.textContent = "Contact " + name;
      description.textContent = "Choose how you’d like to reach " + name + ".";
      const firstAction = makeAction("Call " + name, "contact-option--primary", "tel:" + cleanNumber);
      makeCopyAction(cleanNumber, "Copy " + name + "’s number");

      const waNumber = contact?.whatsappNumber || "";
      const waDigits = waNumber.replace(/\D/g, "");
      const phoneDigits = cleanNumber.replace(/\D/g, "");
      const waReady = contact?.whatsappConfirmed === true
        && /^\+[1-9]\d{7,14}$/.test(waNumber)
        && waDigits === phoneDigits;
      if (waReady) {
        const whatsappUrl = new URL("https://wa.me/" + waDigits);
        if (contact.message) whatsappUrl.searchParams.set("text", contact.message);
        makeAction("Message " + name + " on WhatsApp", "", whatsappUrl.toString(), true);
      }

      dialog.showModal();
      firstAction.focus();
    }
  }

  document.querySelectorAll("[data-contact-type]").forEach((trigger) => {
    trigger.addEventListener("click", (event) => {
      if (!dialog.open) {
        event.preventDefault();
        openOptions(trigger);
      }
    });
  });

  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener("close", () => {
    status.textContent = "";
    fallback.hidden = true;
    if (lastTrigger?.isConnected) lastTrigger.focus();
  });
})();
