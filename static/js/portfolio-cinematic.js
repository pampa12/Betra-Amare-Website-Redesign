/* Progressive enhancement: understated reveal-on-scroll for portfolio sections.
   No animations are required for content visibility or navigation. */
document.addEventListener('DOMContentLoaded', () => {
  if (!window.matchMedia('(prefers-reduced-motion: no-preference)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  const selectors = [
    '.cp-about-copy',
    '.cp-about-visual',
    '.cp-showcase-copy',
    '.cp-device-display',
    '.cp-partnerships-heading',
    '.cp-brand-devices',
    '.cp-brand-empty',
    '.cp-skills-intro',
    '.cp-skill-grid',
    '.cp-gallery-heading',
    '.cp-connect-grid'
  ];
  const elements = document.querySelectorAll(selectors.join(','));
  if (!elements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('cinematic-inview');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.09, rootMargin: '0px 0px 50px 0px' });

  elements.forEach((el) => {
    // Visible immediately for any section already in or above the viewport.
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight) return;
    el.classList.add('cinematic-enter');
    observer.observe(el);
  });
});
