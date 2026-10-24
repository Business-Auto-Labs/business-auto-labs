// The sample journeys are fictional. They demonstrate the customer path,
// not client work, guaranteed sales, or a specific connected platform.
(() => {
  const demo = document.querySelector("[data-workflow-demo]");
  if (!demo) return;

  const workflows = {
    retail: {
      tabId: "tab-retail",
      businessName: "FICTIONAL EXAMPLE · MORROW HOME",
      steps: [
        {
          title: "A customer starts with “Hi”",
          description: "A specific welcome makes it easy to choose what to do next.",
          revenue: "Clear choices can help an interested shopper find a product without searching through the whole site.",
          messages: [
            {
              speaker: "AI chatbot",
              text: "Hi! Welcome to Morrow Home. What are you looking for today?",
              choices: ["Browse products", "Track an order", "Talk to a person"]
            }
          ]
        },
        {
          title: "Understand what they want",
          description: "A short follow-up narrows the conversation to the customer’s interest.",
          revenue: "The chatbot can guide the customer toward a relevant collection or product page.",
          messages: [
            { speaker: "Customer", text: "Browse products" },
            {
              speaker: "AI chatbot",
              text: "What would you like to see?",
              choices: ["Home décor", "Gifts", "New arrivals"]
            }
          ]
        },
        {
          title: "Share a useful product link",
          description: "The chatbot can point the customer to the business’s own product information.",
          revenue: "A direct route makes it simpler to compare products and continue to the shop’s checkout.",
          messages: [
            { speaker: "Customer", text: "Gifts" },
            {
              speaker: "AI chatbot",
              text: "Here’s the gift collection. You can review the products and choose what fits.",
              link: {
                label: "EXAMPLE WEBSITE LINK",
                title: "Browse the gift collection",
                detail: "A link to the shop’s own product page"
              }
            }
          ]
        },
        {
          title: "Let the customer decide",
          description: "The shopper can continue to checkout or ask the team for help.",
          revenue: "Payment and fulfillment remain with the shop’s normal checkout. A chatbot can support the path, but it cannot guarantee a purchase.",
          messages: [
            { speaker: "Customer", text: "I found one I like" },
            {
              speaker: "AI chatbot",
              text: "Great. The shop’s checkout can handle payment and delivery details.",
              link: {
                label: "EXAMPLE CHECKOUT STEP",
                title: "Continue on the shop website",
                detail: "The business completes the order through its existing checkout"
              }
            }
          ]
        }
      ]
    },
    appointments: {
      tabId: "tab-appointments",
      businessName: "FICTIONAL EXAMPLE · SORA STUDIO",
      steps: [
        {
          title: "Welcome the customer",
          description: "The first reply offers common next steps and an easy route to the team.",
          revenue: "A clear booking path can help a prospective customer move from a question to a service request.",
          messages: [
            {
              speaker: "AI chatbot",
              text: "Hi! Welcome to Sora Studio. How can we help today?",
              choices: ["Book an appointment", "See services", "Talk to a person"]
            }
          ]
        },
        {
          title: "Collect the booking details",
          description: "The chatbot asks what the customer wants and when they would like to visit.",
          revenue: "Collecting the right details can make a booking request easier for both the customer and the studio.",
          messages: [
            { speaker: "Customer", text: "Book an appointment" },
            {
              speaker: "AI chatbot",
              text: "What service are you interested in, and which day works for you?",
              choices: ["Choose a service", "Pick a day", "Ask the team"]
            }
          ]
        },
        {
          title: "Show the booking step",
          description: "A booking link or request can move the customer to the studio’s actual availability process.",
          revenue: "The customer can continue to a booking calendar, or the studio can confirm the request using its normal process.",
          messages: [
            { speaker: "Customer", text: "A haircut tomorrow" },
            {
              speaker: "AI chatbot",
              text: "I can help you continue to the studio’s booking options.",
              link: {
                label: "EXAMPLE BOOKING LINK",
                title: "Choose an available time",
                detail: "Availability comes from the studio’s booking setup"
              }
            }
          ]
        },
        {
          title: "Confirm through the real process",
          description: "The studio’s calendar or team confirms the appointment details.",
          revenue: "The workflow helps a prospective booking reach the studio. Availability, confirmation, and payment depend on its actual setup.",
          messages: [
            { speaker: "Customer", text: "I’d like the 4:30 option" },
            {
              speaker: "AI chatbot",
              text: "I’ll pass your request into the studio’s booking process so the time can be confirmed.",
              choices: ["Review booking details", "Talk to the team"]
            }
          ]
        }
      ]
    },
    cafe: {
      tabId: "tab-cafe",
      businessName: "FICTIONAL EXAMPLE · LITTLE CEDAR CAFÉ",
      steps: [
        {
          title: "Open with a useful menu",
          description: "The welcome message can offer menu, ordering, and customer-support choices.",
          revenue: "A direct route to the menu can help a hungry customer decide whether to place an order.",
          messages: [
            {
              speaker: "AI chatbot",
              text: "Hi! Welcome to Little Cedar Café. What would you like to do?",
              choices: ["See the menu", "Start an order", "Hours & location"]
            }
          ]
        },
        {
          title: "Find the order type",
          description: "A quick choice helps the café understand how the customer wants to order.",
          revenue: "The flow can guide customers to the pickup or delivery option the café actually supports.",
          messages: [
            { speaker: "Customer", text: "Start an order" },
            {
              speaker: "AI chatbot",
              text: "Would you like to order for pickup or delivery?",
              choices: ["Pickup", "Delivery", "View the menu first"]
            }
          ]
        },
        {
          title: "Guide the customer to the menu",
          description: "The chatbot can share the café’s menu and ordering information.",
          revenue: "A menu or ordering link gives customers a direct way to review items and continue.",
          messages: [
            { speaker: "Customer", text: "Pickup" },
            {
              speaker: "AI chatbot",
              text: "Here’s the pickup menu. You can review the available items before ordering.",
              link: {
                label: "EXAMPLE MENU LINK",
                title: "View the pickup menu",
                detail: "A link to the café’s menu or order page"
              }
            }
          ]
        },
        {
          title: "Move toward checkout",
          description: "The café’s actual ordering process handles the order review, payment, and fulfillment.",
          revenue: "The chatbot helps a customer reach the order flow. The café’s setup controls payment, availability, and pickup.",
          messages: [
            { speaker: "Customer", text: "I’m ready to order" },
            {
              speaker: "AI chatbot",
              text: "Continue to the café’s order page to review your order and complete the next step.",
              choices: ["Continue to order page", "Ask the café"]
            }
          ]
        }
      ]
    }
  };

  const tabs = Array.from(demo.querySelectorAll("[data-workflow-tab]"));
  const panel = demo.querySelector("[role='tabpanel']");
  const transcript = demo.querySelector("[data-chat-transcript]");
  const businessName = demo.querySelector("[data-business-name]");
  const typingIndicator = demo.querySelector("[data-typing-indicator]");
  const count = demo.querySelector("[data-step-count]");
  const outcomeTitle = demo.querySelector("[data-outcome-title]");
  const outcomeCopy = demo.querySelector("[data-outcome-copy]");
  const revenueCopy = demo.querySelector("[data-revenue-copy]");
  const status = demo.querySelector("[data-workflow-status]");
  const progressSteps = Array.from(demo.querySelectorAll("[data-progress-step]"));
  const playButton = demo.querySelector("[data-play-workflow]");
  const playLabel = demo.querySelector("[data-play-label]");
  const playIcon = demo.querySelector("[data-play-icon]");
  const replayButton = demo.querySelector("[data-replay-workflow]");

  if (!panel || !transcript || !playButton || !playLabel || !playIcon || !replayButton) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let activeWorkflowName = "retail";
  let activeStepIndex = 0;
  let activeMessageIndex = 0;
  let activeStepStarted = false;
  let playing = false;
  let playbackToken = 0;

  function wait(milliseconds) {
    // Keep enough reading time even when reduced motion is enabled; that
    // preference disables visual movement, not the time needed to read text.
    return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
  }

  function setPlayLabel(label, icon = "▶") {
    playLabel.textContent = label;
    playIcon.textContent = icon;
  }

  function makeMessage(message) {
    const bubble = document.createElement("article");
    const isCustomer = message.speaker === "Customer";
    bubble.className = "chat-bubble " + (isCustomer ? "chat-bubble--customer" : "chat-bubble--bot");

    const speaker = document.createElement("span");
    speaker.className = "chat-bubble__speaker";
    speaker.textContent = message.speaker;

    const text = document.createElement("p");
    text.textContent = message.text;
    bubble.append(speaker, text);
    transcript.append(bubble);

    if (message.choices?.length) {
      const choices = document.createElement("ul");
      choices.className = "chat-choices";
      choices.setAttribute("aria-label", "Example quick replies");

      message.choices.forEach((choice) => {
        const item = document.createElement("li");
        item.textContent = choice;
        choices.append(item);
      });
      transcript.append(choices);
    }

    if (message.link) {
      const linkCard = document.createElement("div");
      linkCard.className = "chat-link-card";

      const label = document.createElement("span");
      label.className = "chat-link-card__label";
      label.textContent = message.link.label;

      const title = document.createElement("strong");
      title.textContent = message.link.title;

      const detail = document.createElement("p");
      detail.textContent = message.link.detail;

      linkCard.append(label, title, detail);
      transcript.append(linkCard);
    }

    transcript.scrollTo({
      top: transcript.scrollHeight,
      behavior: reducedMotion.matches ? "auto" : "smooth"
    });
  }

  function updateProgress(stepIndex) {
    progressSteps.forEach((item, index) => {
      item.classList.toggle("is-current", index === stepIndex);
      item.classList.toggle("is-complete", index < stepIndex);
    });
  }

  function showStep(stepIndex) {
    const workflow = workflows[activeWorkflowName];
    const step = workflow.steps[stepIndex];
    count.textContent = String(stepIndex + 1).padStart(2, "0") + " / " + String(workflow.steps.length).padStart(2, "0");
    outcomeTitle.textContent = step.title;
    outcomeCopy.textContent = step.description;
    revenueCopy.textContent = step.revenue;
    updateProgress(stepIndex);
  }

  function setPlayingState(isPlaying) {
    playing = isPlaying;
    playButton.setAttribute("aria-pressed", String(isPlaying));
    playIcon.textContent = isPlaying ? "Ⅱ" : "▶";
  }

  function readingTime(message) {
    const wordCount = message.text.trim().split(/\s+/).length;
    const choiceCount = message.choices?.length || 0;
    const minimum = message.speaker === "AI chatbot" ? 2600 : 850;
    return Math.min(5200, Math.max(minimum, wordCount * 170 + choiceCount * 400));
  }

  function resetWorkflow() {
    playbackToken += 1;
    setPlayingState(false);
    activeStepIndex = 1;
    activeMessageIndex = 0;
    activeStepStarted = false;
    typingIndicator.hidden = true;

    const workflow = workflows[activeWorkflowName];
    businessName.textContent = workflow.businessName;
    panel.setAttribute("aria-labelledby", workflow.tabId);
    transcript.replaceChildren();

    // The customer says “Hi” first. The first prewritten AI greeting and quick
    // replies are shown immediately, just as the opening menu would appear.
    makeMessage({ speaker: "Customer", text: "Hi" });
    makeMessage(workflow.steps[0].messages[0]);
    showStep(0);

    status.textContent = "A customer has sent “Hi”. The chatbot greeting and choices are on screen. Play to follow the example.";
    setPlayLabel("See a WhatsApp flow in action");
  }

  function revealAnimation() {
    const animation = demo.querySelector(".chat-simulator");
    animation?.scrollIntoView({
      behavior: reducedMotion.matches ? "auto" : "smooth",
      block: "start",
    });
  }

  async function runWorkflow() {
    revealAnimation();
    if (playing) {
      playbackToken += 1;
      setPlayingState(false);
      typingIndicator.hidden = true;
      setPlayLabel("Resume the walkthrough", "▶");
      status.textContent = "Paused. Resume when you’re ready to see the next message.";
      return;
    }

    const workflow = workflows[activeWorkflowName];
    if (activeStepIndex >= workflow.steps.length) {
      resetWorkflow();
    }

    const token = ++playbackToken;
    setPlayingState(true);
    setPlayLabel("Pause the walkthrough", "Ⅱ");

    while (activeStepIndex < workflow.steps.length) {
      const step = workflow.steps[activeStepIndex];
      if (!activeStepStarted) {
        showStep(activeStepIndex);
        status.textContent = "Step " + (activeStepIndex + 1) + " of " + workflow.steps.length + ": " + step.title + ".";
        activeStepStarted = true;
        await wait(450);
        if (token !== playbackToken) return;
      }

      while (activeMessageIndex < step.messages.length) {
        const message = step.messages[activeMessageIndex];
        if (message.speaker === "AI chatbot") {
          typingIndicator.hidden = false;
          await wait(950);
          if (token !== playbackToken) return;
          typingIndicator.hidden = true;
        }

        makeMessage(message);
        activeMessageIndex += 1;
        await wait(readingTime(message));
        if (token !== playbackToken) return;
      }

      activeStepIndex += 1;
      activeMessageIndex = 0;
      activeStepStarted = false;
    }

    setPlayingState(false);
    updateProgress(workflow.steps.length);
    setPlayLabel("Replay the flow");
    status.textContent = "Example complete. The customer reaches the business’s normal order or booking process; no sale or booking is guaranteed.";
  }

  function selectWorkflow(name, moveFocus = false) {
    if (!workflows[name]) return;
    activeWorkflowName = name;

    tabs.forEach((tab) => {
      const selected = tab.dataset.workflowTab === name;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
      tab.classList.toggle("is-active", selected);
      if (selected && moveFocus) tab.focus();
    });

    resetWorkflow();
  }

  tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => selectWorkflow(tab.dataset.workflowTab));
    tab.addEventListener("keydown", (event) => {
      let nextIndex = index;
      if (event.key === "ArrowRight") nextIndex = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft") nextIndex = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") nextIndex = 0;
      else if (event.key === "End") nextIndex = tabs.length - 1;
      else return;

      event.preventDefault();
      selectWorkflow(tabs[nextIndex].dataset.workflowTab, true);
    });
  });

  playButton.addEventListener("click", runWorkflow);
  replayButton.addEventListener("click", () => {
    resetWorkflow();
    revealAnimation();
  });
  resetWorkflow();
})();
