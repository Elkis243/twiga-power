(function () {
  function hideLoader() {
    const loadingOverlay = document.getElementById("loading");
    if (!loadingOverlay) {
      return;
    }

    loadingOverlay.classList.add("d-none");
    loadingOverlay.setAttribute("aria-hidden", "true");
  }

  if (document.readyState === "complete") {
    hideLoader();
  } else {
    window.addEventListener("load", hideLoader);
  }
})();
