// Lightweight enhancements keep the public page usable without a framework.
const menuButton = document.querySelector(".menu-toggle");
const primaryNavigation = document.querySelector(".primary-nav");

if (menuButton && primaryNavigation) {
  const closeMenu = () => {
    menuButton.setAttribute("aria-expanded", "false");
    primaryNavigation.classList.remove("is-open");
  };
  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", String(!isOpen));
    primaryNavigation.classList.toggle("is-open", !isOpen);
  });
  primaryNavigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu();
  });
}

// Reveal content only when supported and the visitor has not requested reduced motion.
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
if ("IntersectionObserver" in window && !reducedMotion.matches) {
  document.documentElement.classList.add("motion-ready");
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll("[data-reveal]").forEach((element) => revealObserver.observe(element));
}

// Tilt only the decorative hero panel on mouse-like pointers.
const tiltPanel = document.querySelector("[data-tilt]");
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
if (tiltPanel && finePointer.matches && !reducedMotion.matches) {
  tiltPanel.addEventListener("pointermove", (event) => {
    const bounds = tiltPanel.getBoundingClientRect();
    const horizontal = (event.clientX - bounds.left) / bounds.width - 0.5;
    const vertical = (event.clientY - bounds.top) / bounds.height - 0.5;
    tiltPanel.style.setProperty("--tilt-x", (vertical * -3).toFixed(2) + "deg");
    tiltPanel.style.setProperty("--tilt-y", (horizontal * 3).toFixed(2) + "deg");
  });
  tiltPanel.addEventListener("pointerleave", () => {
    tiltPanel.style.removeProperty("--tilt-x");
    tiltPanel.style.removeProperty("--tilt-y");
  });
}

document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

// Keep the visible address and mail link synchronized with the public config.
const configuredEmail = window.BUSINESS_SITE_CONFIG?.contactEmail?.trim();
if (configuredEmail && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(configuredEmail)) {
  document.querySelectorAll("[data-contact-email]").forEach((link) => {
    link.href = "mailto:" + configuredEmail;
    const text = Array.from(link.childNodes).find((node) => node.nodeType === Node.TEXT_NODE);
    if (text) text.textContent = configuredEmail + " ";
  });
}

// Only show a WhatsApp link when a complete international number is configured.
const whatsappNumber = window.BUSINESS_SITE_CONFIG?.whatsappNumber?.replace(/\D/g, "") || "";
const whatsappNumberConfirmed = window.BUSINESS_SITE_CONFIG?.whatsappNumberConfirmed === true;
const whatsappLink = document.querySelector("[data-whatsapp-link]");
// Require explicit owner confirmation and an international-length digit string.
if (whatsappLink && whatsappNumberConfirmed && /^\d{8,15}$/.test(whatsappNumber)) {
  whatsappLink.href = "https://wa.me/" + whatsappNumber;
  whatsappLink.hidden = false;
}
