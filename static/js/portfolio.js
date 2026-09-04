document.addEventListener('DOMContentLoaded', () => {
  const portfolioItems = Array.from(document.querySelectorAll('.portfolio-item[data-category]'));
  const filterButtons = Array.from(document.querySelectorAll('.filter-btn[data-filter]'));

  if (portfolioItems.length && filterButtons.length) {
    const counts = portfolioItems.reduce((result, item) => {
      const category = item.dataset.category;
      result[category] = (result[category] || 0) + 1;
      return result;
    }, {});

    filterButtons.forEach((button) => {
      const category = button.dataset.filter;
      if (category !== 'all' && (counts[category] || 0) < 3) {
        button.hidden = true;
        button.setAttribute('aria-hidden', 'true');
      }
    });

    filterButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (button.hidden) return;
        const filter = button.dataset.filter;

        filterButtons.forEach((otherButton) => otherButton.classList.remove('active'));
        button.classList.add('active');

        portfolioItems.forEach((item) => {
          const matches = filter === 'all' || item.dataset.category === filter;
          item.classList.toggle('is-hidden', !matches);
        });
      });
    });
  }

  const lightbox = document.querySelector('#portfolioLightbox');
  const stage = lightbox?.querySelector('.portfolio-lightbox-stage');
  const caption = lightbox?.querySelector('.portfolio-lightbox-caption');
  const closeButton = lightbox?.querySelector('.portfolio-lightbox-close');
  const triggers = Array.from(document.querySelectorAll('.portfolio-lightbox-trigger'));
  let lastTrigger = null;

  if (!lightbox || !stage || !caption || !closeButton || !triggers.length) return;

  const closeLightbox = () => {
    const video = stage.querySelector('video');
    if (video) video.pause();

    stage.replaceChildren();
    caption.textContent = '';
    lightbox.classList.remove('is-open');
    lightbox.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    if (lastTrigger) lastTrigger.focus();
  };

  const openLightbox = (trigger) => {
    const mediaType = trigger.dataset.mediaType;
    const mediaSrc = trigger.dataset.mediaSrc;
    const mediaAlt = trigger.dataset.mediaAlt || trigger.dataset.title || 'Portfolio media';
    const title = trigger.dataset.title || '';

    if (!mediaSrc) return;

    stage.replaceChildren();

    if (mediaType === 'video') {
      const video = document.createElement('video');
      video.controls = true;
      video.autoplay = true;
      video.playsInline = true;
      video.preload = 'metadata';
      video.setAttribute('aria-label', mediaAlt);
      if (trigger.dataset.mediaPoster) video.poster = trigger.dataset.mediaPoster;

      const source = document.createElement('source');
      source.src = mediaSrc;
      video.appendChild(source);
      stage.appendChild(video);
    } else {
      const image = document.createElement('img');
      image.src = mediaSrc;
      image.alt = mediaAlt;
      image.decoding = 'async';
      stage.appendChild(image);
    }

    caption.textContent = title;
    lastTrigger = trigger;
    lightbox.classList.add('is-open');
    lightbox.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    closeButton.focus();
  };

  triggers.forEach((trigger) => {
    trigger.addEventListener('click', () => openLightbox(trigger));
    trigger.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openLightbox(trigger);
      }
    });
  });

  closeButton.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) closeLightbox();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && lightbox.classList.contains('is-open')) {
      closeLightbox();
    }
  });
});
