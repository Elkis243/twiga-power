// Validation Bootstrap — formulaires #customValidationForm (contact, postuler, etc.)
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#customValidationForm");
  if (!form) return;

  const inputs = form.querySelectorAll("input, textarea, select");

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
    } else {
      field.classList.remove("is-valid");
      field.classList.add("is-invalid");

      if (field.validity.valueMissing) {
        feedback.textContent = "Ce champ ne peut pas être laissé vide !";
      } else if (field.validity.customError) {
        feedback.textContent = field.validationMessage;
      } else if (field.validity.tooShort) {
        feedback.textContent = `Ce champ doit contenir au moins ${field.minLength || 0} caractères !`;
      } else if (field.validity.tooLong) {
        feedback.textContent = `Ce champ ne doit pas dépasser ${field.maxLength || 0} caractères !`;
      } else if (field.validity.patternMismatch) {
        feedback.textContent = "Veuillez respecter le format requis pour ce champ !";
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

  form.addEventListener("submit", (event) => {
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
      }
    });

    let isValid = true;
    inputs.forEach((input) => {
      if (!input.checkValidity()) {
        isValid = false;
        validateField(input);
      } else {
        validateField(input);
      }
    });

    if (!isValid) {
      event.preventDefault();
      event.stopPropagation();
      form.classList.add("was-validated");
    }
  });

  inputs.forEach((input) => {
    const handler = () => {
      if (input.type === "file") {
        input.setCustomValidity("");
      }
      validateField(input);
    };
    if (input.type === "file") {
      input.addEventListener("change", handler);
    } else {
      input.addEventListener("input", handler);
    }
    input.addEventListener("blur", () => validateField(input));
  });
});
