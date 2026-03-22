/**
 * Zone CV : nom du fichier, glisser-déposer, état visuel.
 */
(function () {
  function initCvUpload() {
    var input = document.getElementById("id_cv");
    var root = document.getElementById("cv-upload-root");
    var nameEl = document.getElementById("cv-filename-text");
    if (!input || !root || !nameEl) {
      return;
    }

    function sync() {
      var file = input.files && input.files[0];
      if (file) {
        nameEl.textContent = file.name;
        root.classList.add("has-file");
        root.classList.remove("cv-upload--error", "is-invalid");
      } else {
        nameEl.textContent = "";
        root.classList.remove("has-file");
      }
    }

    input.addEventListener("change", sync);

    /* Glisser-déposer (zone #cv-upload-root pour éviter les clignotements) */
    function onDragEnter(e) {
      e.preventDefault();
      e.stopPropagation();
      root.classList.add("cv-upload--drag");
    }

    function onDragLeave(e) {
      e.preventDefault();
      e.stopPropagation();
      var next = e.relatedTarget;
      if (next && root.contains(next)) {
        return;
      }
      root.classList.remove("cv-upload--drag");
    }

    function onDragOver(e) {
      e.preventDefault();
      e.stopPropagation();
      e.dataTransfer.dropEffect = "copy";
    }

    function onDrop(e) {
      e.preventDefault();
      e.stopPropagation();
      root.classList.remove("cv-upload--drag");
      var files = e.dataTransfer && e.dataTransfer.files;
      if (!files || !files.length) {
        return;
      }
      var f = files[0];
      if (f.type !== "application/pdf" && !f.name.toLowerCase().endsWith(".pdf")) {
        return;
      }
      try {
        var dt = new DataTransfer();
        dt.items.add(f);
        input.files = dt.files;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      } catch (err) {
        /* navigateur trop ancien */
      }
    }

    root.addEventListener("dragenter", onDragEnter);
    root.addEventListener("dragleave", onDragLeave);
    root.addEventListener("dragover", onDragOver);
    root.addEventListener("drop", onDrop);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCvUpload);
  } else {
    initCvUpload();
  }
})();
