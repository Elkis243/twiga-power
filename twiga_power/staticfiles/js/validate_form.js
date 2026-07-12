/**
 * Validation Bootstrap 5 — Twiga Power
 *
 * Active la validation HTML5 native sur tous les formulaires portant
 * les classes `needs-validation` et l'attribut `novalidate`.
 *
 * Pattern officiel Bootstrap : https://getbootstrap.com/docs/5.3/forms/validation/
 */
(function () {
  "use strict";

  /** Sélecteur des formulaires à valider */
  var FORM_SELECTOR = ".needs-validation";

  /** Champs pris en charge (hors hidden, checkbox et radio) */
  var FIELD_SELECTOR =
    "input:not([type='hidden']):not([type='checkbox']):not([type='radio']), textarea, select";

  /**
   * Retourne le bloc `.invalid-feedback` associé à un champ.
   * Cherche d'abord le sibling direct, puis dans le conteneur parent.
   */
  function getInvalidFeedback(field) {
    var sibling = field.nextElementSibling;
    if (sibling && sibling.classList.contains("invalid-feedback")) {
      return sibling;
    }

    var parent = field.closest(".contact-page__field, .col-md-6, .modal-body");
    if (parent) {
      return parent.querySelector(".invalid-feedback");
    }

    return null;
  }

  /**
   * Applique les règles métier via setCustomValidity() avant checkValidity().
   * Réinitialise d'abord les messages personnalisés du navigateur.
   */
  function applyCustomRules(field) {
    field.setCustomValidity("");

    /* --- Fichiers (CV PDF, taille max) --- */
    if (field.type === "file") {
      var file = field.files && field.files[0];
      var maxBytes = parseInt(field.getAttribute("data-max-bytes") || "0", 10);

      if (field.required && !file) {
        field.setCustomValidity(
          field.getAttribute("data-msg-required") ||
            "Veuillez sélectionner un fichier.",
        );
        return;
      }

      if (file && maxBytes > 0 && file.size > maxBytes) {
        field.setCustomValidity(
          field.getAttribute("data-msg-max-size") ||
            "Le fichier ne doit pas dépasser 5 Mo.",
        );
        return;
      }

      if (file) {
        var isPdf =
          file.type === "application/pdf" ||
          file.name.toLowerCase().endsWith(".pdf");
        if (!isPdf) {
          field.setCustomValidity(
            field.getAttribute("data-msg-type") ||
              "Le fichier doit être au format PDF.",
          );
        }
      }
      return;
    }

    /* --- Correspondance de mot de passe (inscription) --- */
    var matchName = field.getAttribute("data-match-field");
    if (matchName && field.form) {
      var matchField = field.form.querySelector('[name="' + matchName + '"]');
      if (matchField && field.value !== matchField.value) {
        field.setCustomValidity(
          field.getAttribute("data-msg-mismatch") ||
            "Les mots de passe ne correspondent pas.",
        );
        return;
      }
    }

    /* --- Champs texte / textarea : trim + longueur minimale --- */
    var isTextInput = field.tagName === "INPUT" && field.type === "text";
    var isTextarea = field.tagName === "TEXTAREA";
    var isEmail = field.type === "email";

    if (isTextInput || isTextarea || isEmail) {
      var trimmed = field.value.trim();

      if (field.required && trimmed === "") {
        field.setCustomValidity(
          field.getAttribute("data-msg-required") ||
            "Ce champ ne peut pas être laissé vide.",
        );
        return;
      }

      if (field.minLength > 0 && trimmed.length > 0 && trimmed.length < field.minLength) {
        field.setCustomValidity(
          field.getAttribute("data-msg-minlength") ||
            "Ce champ ne respecte pas la longueur minimale requise.",
        );
        return;
      }

      if (field.hasAttribute("data-no-digits") && /\d/.test(trimmed)) {
        field.setCustomValidity(
          field.getAttribute("data-msg-no-digits") ||
            "Ce champ ne doit pas contenir de chiffres.",
        );
      }
    }
  }

  /**
   * Met à jour l'état visuel des champs fichier (input masqué dans .cv-upload).
   */
  function syncFileFieldVisual(field, isFormValidated) {
    if (field.type !== "file") {
      return;
    }

    var uploadRoot = field.closest(".cv-upload");
    if (!uploadRoot) {
      return;
    }

    if (isFormValidated && !field.checkValidity()) {
      uploadRoot.classList.add("cv-upload--error", "is-invalid");
    } else if (field.files && field.files[0]) {
      uploadRoot.classList.remove("cv-upload--error", "is-invalid");
    }
  }

  /**
   * Affiche le message d'erreur personnalisé dans `.invalid-feedback`
   * lorsque le navigateur renvoie une erreur customError ou valueMissing.
   */
  function syncFeedbackMessage(field) {
    var feedback = getInvalidFeedback(field);
    if (!feedback || field.validity.valid) {
      return;
    }

    if (field.validity.customError || field.validationMessage) {
      feedback.textContent = field.validationMessage;
    }
  }

  /**
   * Supprime les espaces superflus avant l'envoi du formulaire.
   */
  function trimFieldsBeforeSubmit(fields) {
    fields.forEach(function (field) {
      if (
        field.tagName === "TEXTAREA" ||
        (field.tagName === "INPUT" &&
          (field.type === "text" || field.type === "email"))
      ) {
        field.value = field.value.trim();
      }
    });
  }

  /**
   * Initialise un formulaire : écouteurs submit + revalidation après saisie.
   */
  function initForm(form) {
    var fields = form.querySelectorAll(FIELD_SELECTOR);

    form.addEventListener(
      "submit",
      function (event) {
        /* Appliquer les règles métier avant la validation native */
        fields.forEach(applyCustomRules);

        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        } else {
          trimFieldsBeforeSubmit(fields);
        }

        /* Classe Bootstrap : active les styles :invalid / .invalid-feedback */
        form.classList.add("was-validated");

        fields.forEach(function (field) {
          syncFileFieldVisual(field, true);
          syncFeedbackMessage(field);
        });

        var firstInvalid = form.querySelector(":invalid");
        if (firstInvalid) {
          firstInvalid.focus();
        }
      },
      false,
    );

    /* Revalidation en direct après la première tentative de soumission */
    fields.forEach(function (field) {
      function revalidate() {
        if (!form.classList.contains("was-validated")) {
          return;
        }
        applyCustomRules(field);
        syncFileFieldVisual(field, true);
        syncFeedbackMessage(field);
      }

      field.addEventListener("input", revalidate);
      field.addEventListener("blur", revalidate);
      if (field.type === "file") {
        field.addEventListener("change", revalidate);
      }
    });

    /* Revalider la confirmation mot de passe quand le mot de passe change */
    var passwordFields = form.querySelectorAll("[data-match-field]");
    passwordFields.forEach(function (confirmField) {
      var matchName = confirmField.getAttribute("data-match-field");
      var sourceField = form.querySelector('[name="' + matchName + '"]');
      if (sourceField) {
        sourceField.addEventListener("input", function () {
          if (form.classList.contains("was-validated")) {
            applyCustomRules(confirmField);
            syncFeedbackMessage(confirmField);
          }
        });
      }
    });
  }

  /**
   * Point d'entrée : attacher la validation à tous les formulaires concernés.
   */
  function initAllForms() {
    document.querySelectorAll(FORM_SELECTOR).forEach(initForm);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAllForms);
  } else {
    initAllForms();
  }
})();
