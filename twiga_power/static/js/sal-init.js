(function () {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const salOptions = {
    threshold: 0.12,
    once: true,
    disabled: prefersReducedMotion,
  };

  window.initPageAnimations = function () {
    if (typeof sal !== "function" || prefersReducedMotion) {
      return;
    }
    sal(salOptions);
  };

  window.refreshPageAnimations = function () {
    if (typeof sal !== "function" || prefersReducedMotion) {
      return;
    }
    if (typeof sal.update === "function") {
      sal.update();
    } else {
      sal(salOptions);
    }
  };

  document.addEventListener("DOMContentLoaded", window.initPageAnimations);

  window.addEventListener("load", function () {
    window.refreshPageAnimations();
  });
})();
