/**
 * Mon espace — ouverture de la modale après redirection (?service=) et reset du formulaire.
 */
(function () {
  function clearModalForm(form) {
    if (!form) {
      return;
    }
    form.reset();
    form.querySelectorAll(".is-invalid").forEach((el) => {
      el.classList.remove("is-invalid");
    });
    form.querySelectorAll(".invalid-feedback.d-block").forEach((el) => {
      if (!el.textContent.trim()) {
        el.classList.remove("d-block");
      }
    });
  }

  function initMonEspaceModal(modal) {
    const form = modal.querySelector(".mon-espace-modal__form");
    if (!form) {
      return;
    }
    modal.addEventListener("show.bs.modal", () => clearModalForm(form));
    modal.addEventListener("hidden.bs.modal", () => clearModalForm(form));
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".mon-espace-modal").forEach(initMonEspaceModal);

    const params = new URLSearchParams(window.location.search);
    const section = document.querySelector("[data-open-service-modal]");
    const service =
      params.get("service") || section?.dataset.openServiceModal || "";
    if (!service) {
      return;
    }

    const modalEl = document.getElementById(`modal-${service}`);
    if (!modalEl || typeof bootstrap === "undefined") {
      return;
    }

    bootstrap.Modal.getOrCreateInstance(modalEl).show();
  });
})();
