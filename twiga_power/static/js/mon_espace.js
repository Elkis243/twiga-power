function getMessageFeedback(textarea) {
  let el = textarea.nextElementSibling;
  while (el && !el.classList.contains("invalid-feedback")) {
    el = el.nextElementSibling;
  }
  return el;
}

function setMessageFieldError(textarea, message) {
  const form = textarea.closest("form");
  const feedback = getMessageFeedback(textarea);

  textarea.classList.remove("is-valid");
  textarea.classList.add("is-invalid");
  textarea.setCustomValidity(message);

  if (feedback) {
    feedback.textContent = message;
    feedback.classList.add("d-block");
  }

  if (form) {
    form.classList.add("was-validated");
  }
}

function clearMessageFieldState(textarea) {
  const form = textarea.closest("form");
  const feedback = getMessageFeedback(textarea);

  textarea.classList.remove("is-invalid", "is-valid");
  textarea.setCustomValidity("");
  textarea.value = "";

  if (feedback) {
    feedback.classList.remove("d-block");
    feedback.textContent = feedback.dataset.defaultMessage || "";
  }

  if (form) {
    form.classList.remove("was-validated");
  }
}

function validateMonEspaceMessage(textarea) {
  const trimmed = textarea.value.trim();
  const minLength = Number(textarea.getAttribute("minlength")) || 10;
  const emptyMessage =
    textarea.getAttribute("data-msg-empty") || "Message requis !";

  if (!trimmed) {
    setMessageFieldError(textarea, emptyMessage);
    return false;
  }

  if (trimmed.length < minLength) {
    setMessageFieldError(
      textarea,
      `Ce champ doit contenir au moins ${minLength} caractères !`,
    );
    return false;
  }

  textarea.classList.remove("is-invalid");
  textarea.classList.add("is-valid");
  textarea.setCustomValidity("");

  const feedback = getMessageFeedback(textarea);
  if (feedback) {
    feedback.classList.remove("d-block");
    feedback.textContent = "";
  }

  return true;
}

function initMonEspaceModalForm(form) {
  if (form.dataset.monEspaceValidationInit === "true") {
    return;
  }
  form.dataset.monEspaceValidationInit = "true";

  const textarea = form.querySelector("textarea[name='message']");
  if (!textarea) {
    return;
  }

  const feedback = getMessageFeedback(textarea);
  if (feedback && !feedback.dataset.defaultMessage) {
    feedback.dataset.defaultMessage = feedback.textContent.trim();
  }

  form.addEventListener(
    "submit",
    (event) => {
      if (!validateMonEspaceMessage(textarea)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        textarea.focus();
        return;
      }

      textarea.value = textarea.value.trim();
    },
    true,
  );

  textarea.addEventListener("input", () => {
    if (textarea.classList.contains("is-invalid")) {
      validateMonEspaceMessage(textarea);
    }
  });

  textarea.addEventListener("blur", () => {
    const trimmed = textarea.value.trim();
    if (!trimmed) {
      setMessageFieldError(
        textarea,
        textarea.getAttribute("data-msg-empty") || "Message requis !",
      );
      return;
    }
    validateMonEspaceMessage(textarea);
  });

  const modal = form.closest(".mon-espace-modal");
  if (modal) {
    modal.addEventListener("show.bs.modal", () => {
      clearMessageFieldState(textarea);
    });
    modal.addEventListener("hidden.bs.modal", () => {
      clearMessageFieldState(textarea);
    });
  }
}

function initAllMonEspaceModalForms() {
  document
    .querySelectorAll(".mon-espace-modal__form")
    .forEach(initMonEspaceModalForm);
}

document.addEventListener("DOMContentLoaded", () => {
  initAllMonEspaceModalForms();

  const params = new URLSearchParams(window.location.search);
  const service = params.get("service");
  if (!service) {
    return;
  }

  const modalEl = document.getElementById(`modal-${service}`);
  if (!modalEl || typeof bootstrap === "undefined") {
    return;
  }

  bootstrap.Modal.getOrCreateInstance(modalEl).show();
});
