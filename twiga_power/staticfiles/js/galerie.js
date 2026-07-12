(function () {
  "use strict";

  const lightbox = document.querySelector(".gallery-lightbox");
  const cards = document.querySelectorAll("[data-gallery-card]");

  if (!lightbox || !cards.length) {
    return;
  }

  const imageEl = lightbox.querySelector(".gallery-lightbox__image");
  const captionEl = lightbox.querySelector(".gallery-lightbox__caption");
  const closeBtn = lightbox.querySelector(".gallery-lightbox__close");
  const prevBtn = lightbox.querySelector(".gallery-lightbox__nav--prev");
  const nextBtn = lightbox.querySelector(".gallery-lightbox__nav--next");

  const items = Array.from(cards).map((card) => ({
    src: card.dataset.src,
    title: card.dataset.title || "",
  }));

  let currentIndex = 0;
  let lastFocusedElement = null;

  function showSlide(index) {
    const item = items[index];
    if (!item) {
      return;
    }
    currentIndex = index;
    imageEl.src = item.src;
    imageEl.alt = item.title;
    captionEl.textContent = item.title;
  }

  function openLightbox(index) {
    lastFocusedElement = document.activeElement;
    currentIndex = index;
    showSlide(currentIndex);
    lightbox.hidden = false;
    lightbox.setAttribute("aria-hidden", "false");
    document.body.classList.add("gallery-lightbox-open");
    closeBtn.focus();
  }

  function closeLightbox() {
    lightbox.hidden = true;
    lightbox.setAttribute("aria-hidden", "true");
    document.body.classList.remove("gallery-lightbox-open");
    imageEl.removeAttribute("src");
    if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
      lastFocusedElement.focus();
    }
  }

  function showPrev() {
    const nextIndex = (currentIndex - 1 + items.length) % items.length;
    showSlide(nextIndex);
  }

  function showNext() {
    const nextIndex = (currentIndex + 1) % items.length;
    showSlide(nextIndex);
  }

  cards.forEach((card) => {
    card.addEventListener("click", () => {
      const index = Number.parseInt(card.dataset.galleryIndex, 10);
      openLightbox(Number.isNaN(index) ? 0 : index);
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  prevBtn.addEventListener("click", showPrev);
  nextBtn.addEventListener("click", showNext);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (lightbox.hidden) {
      return;
    }
    if (event.key === "Escape") {
      closeLightbox();
    } else if (event.key === "ArrowLeft") {
      showPrev();
    } else if (event.key === "ArrowRight") {
      showNext();
    }
  });
})();
