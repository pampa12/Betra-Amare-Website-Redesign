/* Moving content for the single realistic portfolio phone.
 * Real Cloudinary video plays first; photos get a gently animated fallback.
 * Respects reduced-motion settings and pauses when offscreen.
 */
document.addEventListener('DOMContentLoaded', () => {
  const phone = document.querySelector('[data-portfolio-phone]');
  if (!phone) return;

  const video = phone.querySelector('[data-portfolio-reel]');
  const iframe = phone.querySelector('.cp-phone-tiktok');
  const gallery = phone.querySelector('[data-phone-slideshow]');
  const slides = gallery ? [...gallery.querySelectorAll('.cp-reel-image')] : [];
  const toggle = document.querySelector('[data-phone-motion-button]');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let visible = true;
  let pausedByUser = false;
  let explicitlyPlayed = false;
  let slideIndex = 0;
  let slideshowTimer = null;

  function stopSlideTimer() {
    if (slideshowTimer !== null) {
      clearInterval(slideshowTimer);
      slideshowTimer = null;
    }
  }

  function nextSlide() {
    if (slides.length < 2) return;
    const old = slides[slideIndex];
    slideIndex = (slideIndex + 1) % slides.length;
    const current = slides[slideIndex];
    old.classList.remove('is-active');
    old.setAttribute('aria-hidden', 'true');
    current.classList.add('is-active');
    current.setAttribute('aria-hidden', 'false');
  }

  function playbackAllowed() {
    return visible && !document.hidden && !pausedByUser &&
      (!prefersReducedMotion.matches || explicitlyPlayed);
  }

  function syncMotion() {
    const playing = playbackAllowed();
    if (video) {
      if (playing) {
        const attempt = video.play();
        if (attempt && typeof attempt.catch === 'function') {
          attempt.catch(() => {
            pausedByUser = true;
            updateButton();
          });
        }
      } else {
        video.pause();
      }
    }

    if (gallery) {
      gallery.classList.toggle('is-playing', playing);
      stopSlideTimer();
      if (playing && slides.length > 1) {
        slideshowTimer = window.setInterval(nextSlide, 4500);
      }
    }

    // TikTok's player is cross-origin; only use its documented, scoped
    // postMessage interface. Playback may still be blocked by the browser.
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage(
        { type: playing ? 'play' : 'pause', value: undefined, 'x-tiktok-player': true },
        'https://www.tiktok.com'
      );
    }
    updateButton();
  }

  function updateButton() {
    if (!toggle) return;
    const paused = !playbackAllowed();
    const mediaLabel = video ? 'video' : 'slideshow';
    toggle.textContent = (paused ? 'Play ' : 'Pause ') + mediaLabel;
    toggle.setAttribute('aria-pressed', String(paused));
  }

  if (toggle) {
    toggle.addEventListener('click', () => {
      if (playbackAllowed()) {
        pausedByUser = true;
      } else {
        pausedByUser = false;
        explicitlyPlayed = true;
      }
      syncMotion();
    });
  }

  document.addEventListener('visibilitychange', syncMotion);
  if (typeof prefersReducedMotion.addEventListener === 'function') {
    prefersReducedMotion.addEventListener('change', syncMotion);
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      visible = entries[0]?.isIntersecting ?? false;
      syncMotion();
    }, { threshold: 0.18 });
    observer.observe(phone);
  }
  if (iframe) iframe.addEventListener('load', syncMotion);
  syncMotion();
});
