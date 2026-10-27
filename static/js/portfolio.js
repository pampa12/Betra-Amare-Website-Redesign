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
      if (category !== 'all' && !counts[category]) {
        button.hidden = true;
        button.setAttribute('aria-hidden', 'true');
      }
    });

    const applyFilter = (filter) => {
      const chosen = filterButtons.find(
        (button) => button.dataset.filter === filter && !button.hidden
      );
      const active = chosen ? filter : 'all';
      filterButtons.forEach((button) => {
        const selected = button.dataset.filter === active;
        button.classList.toggle('active', selected);
        button.setAttribute('aria-pressed', String(selected));
      });
      portfolioItems.forEach((item) => {
        item.classList.toggle('is-hidden', active !== 'all' && item.dataset.category !== active);
      });
    };

    // Home page category cards link to /portfolio/#beauty, #fashion, etc.
    // Honor those links on arrival and when navigating backward/forward.
    const filterFromHash = () => {
      const category = decodeURIComponent(window.location.hash.slice(1));
      if (category && filterButtons.some(button => button.dataset.filter === category)) {
        applyFilter(category);
      }
    };
    applyFilter('all');
    filterFromHash();
    window.addEventListener('hashchange', filterFromHash);

    filterButtons.forEach((button) => {
      button.addEventListener('click', () => {
        if (button.hidden) return;
        applyFilter(button.dataset.filter);
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
