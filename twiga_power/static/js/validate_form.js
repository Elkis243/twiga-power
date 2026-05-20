// Validation Bootstrap — contact (#customValidationForm) et modales Mon espace (.js-contact-form)
function applyTrimValidation(field) {
  const isTextarea = field.tagName === "TEXTAREA";
  const isTextInput = field.tagName === "INPUT" && field.type === "text";

  if (!isTextarea && !isTextInput) {
    return;
  }

  const trimmed = field.value.trim();
  const min = field.minLength > 0 ? field.minLength : 0;
  const emptyMsg =
    field.getAttribute("data-msg-empty") ||
    "Ce champ ne peut pas être laissé vide !";

  if (field.required && !trimmed) {
    field.setCustomValidity(emptyMsg);
    return;
  }

  if (min && trimmed.length < min) {
    field.setCustomValidity(
      `Ce champ doit contenir au moins ${min} caractères !`,
    );
    return;
  }

  field.setCustomValidity("");
}

function initContactForm(form) {
  const inputs = form.querySelectorAll(
    "input:not([type='hidden']), textarea, select",
  );

  function getInvalidFeedback(field) {
    let el = field.nextElementSibling;
    while (el && !el.classList.contains("invalid-feedback")) {
      el = el.nextElementSibling;
    }
    return el;
  }

  function validateField(field) {
    const feedback = getInvalidFeedback(field);
    if (!feedback) return;

    if (field.validity.valid) {
      field.classList.remove("is-invalid");
      field.classList.add("is-valid");
      feedback.textContent = "";
      feedback.classList.remove("d-block");
    } else {
      field.classList.remove("is-valid");
      field.classList.add("is-invalid");
      feedback.classList.add("d-block");

      if (field.validity.valueMissing) {
        feedback.textContent =
          field.getAttribute("data-msg-empty") ||
          "Ce champ ne peut pas être laissé vide !";
      } else if (field.validity.customError) {
        feedback.textContent = field.validationMessage;
      } else if (field.validity.tooShort) {
        feedback.textContent = `Ce champ doit contenir au moins ${field.minLength || 0} caractères !`;
      } else if (field.validity.tooLong) {
        feedback.textContent = `Ce champ ne doit pas dépasser ${field.maxLength || 0} caractères !`;
      } else if (field.validity.patternMismatch) {
        feedback.textContent =
          "Veuillez respecter le format requis pour ce champ !";
      } else if (field.type === "radio" && !isRadioGroupValid(field)) {
        feedback.textContent = "Ce champ ne peut pas être laissé vide !";
      } else if (field.type === "checkbox" && !isCheckboxValid(field)) {
        feedback.textContent = "Ce champ ne peut pas être laissé vide !";
      } else {
        feedback.textContent = "Ce champ est invalide !";
      }
    }
  }

  function isRadioGroupValid(radio) {
    const radioGroup = document.querySelectorAll(`input[name="${radio.name}"]`);
    return Array.from(radioGroup).some((r) => r.checked);
  }

  function isCheckboxValid(checkbox) {
    return checkbox.checked;
  }

  function prepareFieldsForValidation() {
    inputs.forEach((input) => {
      if (input.type === "file" && input.hasAttribute("data-max-bytes")) {
        const max = parseInt(input.getAttribute("data-max-bytes"), 10);
        if (input.files && input.files[0] && input.files[0].size > max) {
          const msg =
            input.getAttribute("data-msg-max-size") ||
            "Le fichier ne doit pas dépasser 5 Mo.";
          input.setCustomValidity(msg);
        } else {
          input.setCustomValidity("");
        }
      } else {
        applyTrimValidation(input);
      }
    });
  }

  form.addEventListener(
    "submit",
    (event) => {
      prepareFieldsForValidation();

      let isValid = true;
      let firstInvalid = null;

      inputs.forEach((input) => {
        if (!input.checkValidity()) {
          isValid = false;
          if (!firstInvalid) {
            firstInvalid = input;
          }
        }
        validateField(input);
      });

      if (!isValid) {
        event.preventDefault();
        event.stopImmediatePropagation();
        form.classList.add("was-validated");
        firstInvalid?.focus();
        return;
      }

      inputs.forEach((input) => {
        if (input.tagName === "TEXTAREA" || input.type === "text") {
          input.value = input.value.trim();
        }
      });
    },
    true,
  );

  inputs.forEach((input) => {
    const handler = () => {
      if (input.type === "file") {
        input.setCustomValidity("");
      } else {
        applyTrimValidation(input);
      }
      validateField(input);
    };

    if (input.type === "file") {
      input.addEventListener("change", handler);
    } else {
      input.addEventListener("input", handler);
    }
    input.addEventListener("blur", handler);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const forms = new Set([
    ...document.querySelectorAll(".js-contact-form:not(.mon-espace-modal__form)"),
    document.getElementById("customValidationForm"),
  ].filter(Boolean));

  forms.forEach(initContactForm);
});
