// Small progressive enhancements: mobile navigation, contact configuration, date, and decorative hero pointer response.
const navigationButton = document.querySelector(".menu-toggle");
const primaryNavigation = document.querySelector(".primary-navigation");

if (navigationButton && primaryNavigation) {
  navigationButton.addEventListener("click", () => {
    const isOpen = navigationButton.getAttribute("aria-expanded") === "true";
    navigationButton.setAttribute("aria-expanded", String(!isOpen));
    primaryNavigation.classList.toggle("is-open", !isOpen);
  });
  primaryNavigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      navigationButton.setAttribute("aria-expanded", "false");
      primaryNavigation.classList.remove("is-open");
    }
  });
}

const configuredEmail = window.BUSINESS_SITE_CONFIG?.contactEmail?.trim();
const emailPlaceholder = document.querySelector("[data-contact-email]");
const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(configuredEmail || "");

if (emailPlaceholder && validEmail) {
  const emailLink = document.createElement("a");
  emailLink.className = "contact-email";
  emailLink.href = "mailto:" + configuredEmail;
  emailLink.append(document.createTextNode(configuredEmail + " "));
  const arrow = document.createElement("span");
  arrow.setAttribute("aria-hidden", "true");
  arrow.textContent = "↗";
  emailLink.append(arrow);
  emailPlaceholder.replaceWith(emailLink);
}

document.querySelectorAll("[data-current-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});

// Only mouse-like pointers tilt the decorative art; touch users and reduced-motion users keep it still.
const heroArtwork = document.querySelector(".hero-art");
const motionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");
const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");

if (heroArtwork && finePointer.matches && !motionPreference.matches) {
  heroArtwork.addEventListener("pointermove", (event) => {
    const bounds = heroArtwork.getBoundingClientRect();
    const horizontal = (event.clientX - bounds.left) / bounds.width - 0.5;
    const vertical = (event.clientY - bounds.top) / bounds.height - 0.5;
    heroArtwork.style.setProperty("--tilt-x", `${(vertical * -5).toFixed(2)}deg`);
    heroArtwork.style.setProperty("--tilt-y", `${(horizontal * 5).toFixed(2)}deg`);
    heroArtwork.style.setProperty("--shift-x", `${(horizontal * 7).toFixed(1)}px`);
    heroArtwork.style.setProperty("--shift-y", `${(vertical * 7).toFixed(1)}px`);
  });
  heroArtwork.addEventListener("pointerleave", () => {
    ["--tilt-x", "--tilt-y", "--shift-x", "--shift-y"].forEach((property) => heroArtwork.style.removeProperty(property));
  });
}
