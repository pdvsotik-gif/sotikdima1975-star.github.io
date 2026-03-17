/* ===========================
         JS ЛОГИКА — ОКОЛО 150 СТРОК
         =========================== */

(function() {
  const section = document.querySelector('.wb-section');
  if (!section) return;

  const container = section.querySelector('.wb-container');
  const photoImg = section.querySelector('.wb-photo-img');

  /* ---------------------------
     SHADOW ON SCROLL
     --------------------------- */
  function updateShadow() {
    if (!container) return;
    const y = window.scrollY || 0;
    if (y > 40) {
      container.style.boxShadow = '0 10px 32px rgba(0,0,0,0.14)';
      section.classList.add('is-elevated');
    } else {
      container.style.boxShadow = '0 6px 24px rgba(0,0,0,0.06)';
      section.classList.remove('is-elevated');
    }
  }

  updateShadow();
  window.addEventListener('scroll', updateShadow);

  /* ---------------------------
     HEIGHT SYNC (PHOTO DEFINES)
     --------------------------- */
  function syncHeight() {
    if (!container || !photoImg) return;
    if (window.innerWidth <= 480) {
      section.style.minHeight = 'auto';
      return;
    }

    const rect = photoImg.getBoundingClientRect();
    const photoHeight = rect.height;

    if (photoHeight > 0) {
      container.style.height = photoHeight + 'px';
    }
  }

  function onPhotoReady() {
    syncHeight();
  }

  if (photoImg.complete) {
    onPhotoReady();
  } else {
    photoImg.addEventListener('load', onPhotoReady);
  }

  window.addEventListener('resize', syncHeight);

  /* ---------------------------
     FADE-IN ON SCROLL
     --------------------------- */
  function fadeOnScroll() {
    const rect = section.getBoundingClientRect();
    const vh = window.innerHeight || 1;
    const visible = 1 - Math.max(0, rect.top) / (vh * 0.6);
    const clamped = Math.max(0, Math.min(1, visible));
    section.style.opacity = clamped;
    section.style.transform = 'translateY(' + (20 * (1 - clamped)) + 'px)';
  }

  section.style.opacity = 0;
  section.style.transform = 'translateY(20px)';
  fadeOnScroll();
  window.addEventListener('scroll', fadeOnScroll);

  /* ---------------------------
     CTA HANDLERS (ЗАГЛУШКИ)
     --------------------------- */
  const primaryBtn = section.querySelector('.wb-btn-primary');
  const secondaryBtn = section.querySelector('.wb-btn-secondary');

  if (primaryBtn) {
    primaryBtn.addEventListener('click', function() {
      console.log('[WB] Primary CTA clicked');
    });
  }

  if (secondaryBtn) {
    secondaryBtn.addEventListener('click', function() {
      console.log('[WB] Secondary CTA clicked');
    });
  }

  /* ---------------------------
     RESIZE OBSERVER (СТАБИЛЬНОСТЬ)
     --------------------------- */
  if ('ResizeObserver' in window && photoImg) {
    const ro = new ResizeObserver(function() {
      syncHeight();
    });
    ro.observe(photoImg);
  }

})();