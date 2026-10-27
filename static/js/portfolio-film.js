/* Cinematic portfolio: motion is progressive enhancement, never a requirement
 * for seeing content. Uses only local content or existing administrator-set media.
 */
document.addEventListener('DOMContentLoaded', () => {
  const root = document.querySelector('.film-portfolio');
  if (!root) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const film = root.querySelector('[data-film-video]');
  const stills = root.querySelector('[data-film-stills]');
  let activeIndex = 0;
  let timer = null;
  let inView = true;

  // Reveal sections on arrival rather than turning scroll into an animation lock.
  if (!reduced.matches && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('film-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px 40px 0px', threshold: 0.07 });
    root.classList.add('film-motion-ready');
    root.querySelectorAll('.film-reveal').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.95) return;
      el.classList.add('film-enter');
      observer.observe(el);
    });
  }

  const photos = stills ? Array.from(stills.querySelectorAll('.film-motion-still')) : [];
  const stop = () => {
    if (timer) window.clearInterval(timer);
    timer = null;
    stills?.classList.remove('is-running');
    film?.pause();
  };
  function advance() {
    if (photos.length < 2) return;
    photos[activeIndex].classList.remove('is-current');
    photos[activeIndex].setAttribute('aria-hidden', 'true');
    activeIndex = (activeIndex + 1) % photos.length;
    photos[activeIndex].classList.add('is-current');
    photos[activeIndex].setAttribute('aria-hidden', 'false');
  }
  function sync() {
    if (document.hidden || !inView || reduced.matches) {
      stop();
      return;
    }
    if (film) {
      const result = film.play();
      if (result && typeof result.catch === 'function') result.catch(() => {});
    }
    if (stills && photos.length > 1 && !timer) {
      stills.classList.add('is-running');
      timer = window.setInterval(advance, 5000);
    }
  }
  document.addEventListener('visibilitychange', sync);
  if (typeof reduced.addEventListener === 'function') reduced.addEventListener('change', sync);
  const stage = root.querySelector('.film-reel-stage');
  if (stage && 'IntersectionObserver' in window) {
    const viewObserver = new IntersectionObserver(entries => {
      inView = entries.some(entry => entry.isIntersecting);
      sync();
    }, { threshold: 0.13 });
    viewObserver.observe(stage);
  }
  sync();
});
