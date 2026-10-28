/* Stories in Motion reel strips: lazy embeds, arrows, drag, filters, progress. */
document.addEventListener('DOMContentLoaded', () => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canObserve = 'IntersectionObserver' in window;

  document.querySelectorAll('[data-film-reels]').forEach(root => {
    const track = root.querySelector('[data-reel-track]');
    if (!track) return;
    const cards = Array.from(track.querySelectorAll('.film-reel-card'));
    const arrows = root.querySelectorAll('[data-reel-step]');
    const filters = root.querySelectorAll('[data-reel-filter]');
    const bar = root.querySelector('[data-reel-progress]');

    // Kinetic entrance (content stays visible if JS or motion is unavailable)
    if (!reduced && canObserve) {
      const rect = root.getBoundingClientRect();
      if (rect.top > window.innerHeight * 0.85) {
        root.classList.add('is-armed');
        const reveal = new IntersectionObserver(entries => {
          if (entries.some(e => e.isIntersecting)) {
            root.classList.add('is-visible');
            reveal.disconnect();
          }
        }, { threshold: 0.12 });
        reveal.observe(root);
      }
    }

    // Embeds load only near the viewport so the page stays fast
    const loadEmbed = card => {
      const frame = card.querySelector('iframe[data-src]');
      if (!frame || frame.getAttribute('src')) return;
      frame.addEventListener('load', () => frame.parentElement.classList.add('is-loaded'), { once: true });
      frame.src = frame.dataset.src;
    };
    if (canObserve) {
      const lazy = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          loadEmbed(entry.target);
          lazy.unobserve(entry.target);
        });
      }, { rootMargin: '300px 500px' });
      cards.forEach(card => lazy.observe(card));
    } else {
      cards.forEach(loadEmbed);
    }

    // Uploaded clips play only while on screen
    const clips = Array.from(track.querySelectorAll('video[data-reel-video]'));
    if (clips.length && canObserve) {
      const playback = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          const video = entry.target;
          if (entry.isIntersecting && !reduced) {
            const result = video.play();
            if (result && typeof result.catch === 'function') result.catch(() => {});
          } else {
            video.pause();
          }
        });
      }, { threshold: 0.4 });
      clips.forEach(video => playback.observe(video));
    }

    const visibleCards = () => cards.filter(card => !card.classList.contains('is-hidden'));
    const step = () => {
      const first = visibleCards()[0];
      if (!first) return track.clientWidth;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 20;
      return first.getBoundingClientRect().width + gap;
    };

    const update = () => {
      const max = track.scrollWidth - track.clientWidth;
      if (bar) {
        const share = max > 0 ? track.clientWidth / track.scrollWidth : 1;
        const width = Math.max(share, 0.12);
        const progress = max > 0 ? track.scrollLeft / max : 0;
        bar.style.width = `${width * 100}%`;
        bar.style.transform = `translateX(${progress * (1 / width - 1) * 100}%)`;
      }
      arrows.forEach(btn => {
        btn.disabled = Number(btn.dataset.reelStep) < 0 ? track.scrollLeft < 4 : track.scrollLeft > max - 4;
      });
    };
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();

    arrows.forEach(btn => btn.addEventListener('click', () => {
      track.scrollBy({ left: step() * Number(btn.dataset.reelStep), behavior: reduced ? 'auto' : 'smooth' });
    }));

    track.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      event.preventDefault();
      track.scrollBy({ left: step() * (event.key === 'ArrowRight' ? 1 : -1), behavior: reduced ? 'auto' : 'smooth' });
    });

    // Click-and-drag with a mouse
    let dragging = false;
    let moved = false;
    let startX = 0;
    let startScroll = 0;
    track.addEventListener('pointerdown', event => {
      if (event.pointerType !== 'mouse' || event.button !== 0) return;
      dragging = true;
      moved = false;
      startX = event.clientX;
      startScroll = track.scrollLeft;
    });
    window.addEventListener('pointermove', event => {
      if (!dragging) return;
      const dx = event.clientX - startX;
      if (!moved && Math.abs(dx) > 5) {
        moved = true;
        track.classList.add('is-dragging');
      }
      if (moved) track.scrollLeft = startScroll - dx;
    });
    window.addEventListener('pointerup', () => {
      if (!dragging) return;
      dragging = false;
      track.classList.remove('is-dragging');
    });
    track.addEventListener('click', event => {
      if (moved) {
        event.preventDefault();
        event.stopPropagation();
        moved = false;
      }
    }, true);

    filters.forEach(btn => btn.addEventListener('click', () => {
      const value = btn.dataset.reelFilter;
      filters.forEach(other => {
        const active = other === btn;
        other.classList.toggle('is-active', active);
        other.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      cards.forEach(card => {
        const show = value === 'all' || card.dataset.category === value;
        card.classList.toggle('is-hidden', !show);
        if (show) loadEmbed(card);
      });
      track.scrollTo({ left: 0 });
      requestAnimationFrame(update);
    }));
  });
});
