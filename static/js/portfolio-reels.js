/* Stories in Motion reel strips.
 * Centered "focus" carousel: the video nearest the middle is full size, its
 * neighbours shrink, dim and angle away in 3D. Motion is eased every frame so
 * scrolling, dragging, arrows and auto-advance all glide. Embeds load lazily.
 */
document.addEventListener('DOMContentLoaded', () => {
  const reducedQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const canObserve = 'IntersectionObserver' in window;
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const lerp = (a, b, t) => a + (b - a) * t;

  document.querySelectorAll('[data-film-reels]').forEach(root => {
    const track = root.querySelector('[data-reel-track]');
    if (!track) return;
    const cards = Array.from(track.querySelectorAll('.film-reel-card'));
    if (!cards.length) return;
    const arrows = root.querySelectorAll('[data-reel-step]');
    const filters = root.querySelectorAll('[data-reel-filter]');
    const bar = root.querySelector('[data-reel-progress]');
    const section = root.closest('section') || root;
    let reduced = reducedQuery.matches;

    // ---- Entrance (content stays visible without JS or with reduced motion)
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

    // ---- Lazy embeds
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
      }, { rootMargin: '400px 80%' });
      cards.forEach(card => lazy.observe(card));
    } else {
      cards.forEach(loadEmbed);
    }

    // ---- Uploaded clips play only while on screen
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
      }, { threshold: 0.5 });
      clips.forEach(video => playback.observe(video));
    }

    // ---- Geometry helpers
    const visibleCards = () => cards.filter(card => !card.classList.contains('is-hidden'));
    const centerOf = card => card.offsetLeft + card.offsetWidth / 2;
    const trackCenter = () => track.scrollLeft + track.clientWidth / 2;
    const nearestIndex = () => {
      const list = visibleCards();
      const mid = trackCenter();
      let best = 0;
      let bestDist = Infinity;
      list.forEach((card, i) => {
        const dist = Math.abs(centerOf(card) - mid);
        if (dist < bestDist) { bestDist = dist; best = i; }
      });
      return best;
    };
    const scrollToIndex = (index, smooth = true) => {
      const list = visibleCards();
      if (!list.length) return;
      const card = list[clamp(index, 0, list.length - 1)];
      track.scrollTo({ left: centerOf(card) - track.clientWidth / 2, behavior: smooth && !reduced ? 'smooth' : 'auto' });
    };

    // Two modes. When every video fits on screen, the row stays centered and a
    // spotlight moves between videos ("fitted"). When there are more than fit,
    // the row slides so the focused video sits in the middle ("carousel").
    let fits = false;
    let activeIndex = 0;
    const layout = () => {
      const list = visibleCards();
      const first = list[0];
      if (!first) return;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 24;
      const total = list.reduce((sum, card) => sum + card.offsetWidth, 0) + gap * (list.length - 1);
      fits = total <= track.clientWidth - 48;
      root.classList.toggle('is-fitted', fits);
      if (fits) {
        track.style.paddingLeft = '';
        track.style.paddingRight = '';
        track.scrollLeft = 0;
        activeIndex = clamp(activeIndex, 0, list.length - 1);
      } else {
        const pad = Math.max(24, (track.clientWidth - first.offsetWidth) / 2);
        track.style.paddingLeft = `${pad}px`;
        track.style.paddingRight = `${pad}px`;
      }
    };
    const currentIndex = () => (fits ? activeIndex : nearestIndex());
    const goTo = (index, smooth = true) => {
      const list = visibleCards();
      if (!list.length) return;
      if (fits) {
        activeIndex = clamp(index, 0, list.length - 1);
        updateUi();
        schedule();
      } else {
        scrollToIndex(index, smooth);
      }
    };

    // ---- Progress + arrows
    const updateUi = () => {
      const list = visibleCards();
      const index = currentIndex();
      if (bar) {
        const share = list.length ? 1 / list.length : 1;
        const progress = list.length > 1 ? index / (list.length - 1) : 0;
        bar.style.width = `${share * 100}%`;
        bar.style.transform = `translateX(${progress * (list.length - 1) * 100}%)`;
      }
      arrows.forEach(btn => {
        const dir = Number(btn.dataset.reelStep);
        btn.disabled = list.length < 2 || (dir < 0 ? index === 0 : index === list.length - 1);
      });
      cards.forEach(card => card.classList.remove('is-active'));
      if (list[index]) list[index].classList.add('is-active');
    };

    // ---- Per-frame focus + parallax, eased toward targets
    const state = new Map(cards.map(card => [card, { s: 1, ry: 0, y: 0, o: 1, b: 1 }]));
    let inView = false;
    let frame = 0;
    const render = () => {
      frame = 0;
      if (reduced) return;
      const mid = trackCenter();
      const spot = activeIndex;
      const sectionRect = section.getBoundingClientRect();
      // -1 when the section enters from below, +1 as it leaves at the top
      const pageProgress = clamp((window.innerHeight / 2 - (sectionRect.top + sectionRect.height / 2)) / window.innerHeight, -1.2, 1.2);
      let moving = false;
      visibleCards().forEach((card, i) => {
        const step = card.offsetWidth + 24;
        const d = fits ? clamp(i - spot, -2, 2) : clamp((centerOf(card) - mid) / step, -2, 2);
        const ad = Math.min(Math.abs(d), 1.4);
        const near = Math.min(ad, 1);
        // Fitted rows stay level and centered: a gentle spotlight, no 3D swing.
        const target = fits ? {
          s: 1 - 0.06 * near,
          ry: clamp(-d * 3, -5, 5),
          o: 1 - 0.1 * near,
          b: 1 - 0.25 * near,
          y: pageProgress * (i % 2 ? -22 : 18) + near * 10,
        } : {
          s: 1 - 0.14 * ad,
          ry: clamp(-d * 16, -24, 24),
          o: 1 - 0.22 * near,
          b: 1 - 0.3 * near,
          y: pageProgress * (i % 2 ? -28 : 22) + ad * 14,
        };
        const cur = state.get(card);
        for (const key of ['s', 'ry', 'o', 'y', 'b']) {
          const next = lerp(cur[key], target[key], 0.16);
          if (Math.abs(next - target[key]) > 0.002) moving = true;
          cur[key] = next;
        }
        card.style.transform = `translate3d(0, ${cur.y.toFixed(1)}px, 0) rotateY(${cur.ry.toFixed(2)}deg) scale(${cur.s.toFixed(4)})`;
        card.style.opacity = cur.o.toFixed(3);
        card.style.setProperty('--reel-dim', cur.b.toFixed(3));
        card.style.zIndex = String(100 - Math.round(ad * 10));
      });
      if (inView && (moving || coasting || dragging)) schedule();
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(render); };

    if (canObserve) {
      new IntersectionObserver(entries => {
        inView = entries.some(e => e.isIntersecting);
        if (inView) { schedule(); startAuto(); } else { stopAuto(); }
      }, { rootMargin: '120px 0px' }).observe(root);
    } else {
      inView = true;
    }
    window.addEventListener('scroll', () => { if (inView) schedule(); }, { passive: true });
    track.addEventListener('scroll', () => { updateUi(); schedule(); }, { passive: true });
    window.addEventListener('resize', () => {
      const index = currentIndex();
      activeIndex = index;
      layout();
      if (!fits) scrollToIndex(index, false);
      updateUi();
      schedule();
    });

    // ---- Auto-advance (stops for good once someone interacts)
    let autoTimer = 0;
    let userTookOver = false;
    let hovering = false;
    const AUTO_MS = 5200;
    function startAuto() {
      if (reduced || userTookOver || autoTimer || visibleCards().length < 2) return;
      autoTimer = window.setInterval(() => {
        if (hovering || document.hidden || !inView) return;
        const list = visibleCards();
        const next = currentIndex() + 1;
        goTo(next >= list.length ? 0 : next);
      }, AUTO_MS);
    }
    function stopAuto() {
      window.clearInterval(autoTimer);
      autoTimer = 0;
    }
    const takeOver = () => { userTookOver = true; stopAuto(); };
    root.addEventListener('pointerenter', () => { hovering = true; });
    root.addEventListener('pointerleave', () => { hovering = false; });
    track.addEventListener('touchstart', takeOver, { passive: true });
    track.addEventListener('wheel', event => { if (Math.abs(event.deltaX) > Math.abs(event.deltaY)) takeOver(); }, { passive: true });
    root.addEventListener('focusin', takeOver);
    // Clicking into a TikTok/Instagram player moves focus into its iframe.
    window.addEventListener('blur', () => {
      window.setTimeout(() => {
        const focused = document.activeElement;
        if (!track.contains(focused)) return;
        takeOver();
        const index = visibleCards().findIndex(card => card.contains(focused));
        if (index >= 0) goTo(index);
      }, 0);
    });

    // ---- Arrows and keys
    arrows.forEach(btn => btn.addEventListener('click', () => {
      takeOver();
      goTo(currentIndex() + Number(btn.dataset.reelStep));
    }));
    // In a fitted row, pressing a video (or its caption) moves the spotlight to it.
    cards.forEach(card => card.addEventListener('pointerdown', () => {
      if (!fits) return;
      takeOver();
      goTo(visibleCards().indexOf(card));
    }));
    track.addEventListener('keydown', event => {
      if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
      event.preventDefault();
      takeOver();
      goTo(currentIndex() + (event.key === 'ArrowRight' ? 1 : -1));
    });

    // ---- Mouse drag with momentum, then settle on the nearest video
    let dragging = false;
    let coasting = false;
    let moved = false;
    let startX = 0;
    let startScroll = 0;
    let lastX = 0;
    let lastT = 0;
    let velocity = 0;
    track.addEventListener('pointerdown', event => {
      if (fits || event.pointerType !== 'mouse' || event.button !== 0) return;
      dragging = true;
      coasting = false;
      moved = false;
      startX = lastX = event.clientX;
      startScroll = track.scrollLeft;
      lastT = performance.now();
      velocity = 0;
    });
    window.addEventListener('pointermove', event => {
      if (!dragging) return;
      const dx = event.clientX - startX;
      if (!moved && Math.abs(dx) > 5) {
        moved = true;
        takeOver();
        track.classList.add('is-dragging');
      }
      if (!moved) return;
      const now = performance.now();
      velocity = lerp(velocity, (event.clientX - lastX) / Math.max(now - lastT, 1), 0.4);
      lastX = event.clientX;
      lastT = now;
      track.scrollLeft = startScroll - dx;
      schedule();
    });
    window.addEventListener('pointerup', () => {
      if (!dragging) return;
      dragging = false;
      if (!moved) return;
      coasting = true;
      let v = -velocity * 16; // px per frame
      const glide = () => {
        if (!coasting) return;
        v *= 0.92;
        track.scrollLeft += v;
        schedule();
        if (Math.abs(v) > 0.6) {
          requestAnimationFrame(glide);
        } else {
          coasting = false;
          track.classList.remove('is-dragging');
          scrollToIndex(nearestIndex());
        }
      };
      requestAnimationFrame(glide);
    });
    track.addEventListener('click', event => {
      if (moved) {
        event.preventDefault();
        event.stopPropagation();
        moved = false;
      }
    }, true);

    // ---- Filters
    filters.forEach(btn => btn.addEventListener('click', () => {
      takeOver();
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
      activeIndex = 0;
      layout();
      goTo(0, false);
      updateUi();
      schedule();
    }));

    const onMotionChange = () => {
      reduced = reducedQuery.matches;
      if (reduced) {
        stopAuto();
        cards.forEach(card => { card.style.transform = ''; card.style.opacity = ''; card.style.removeProperty('--reel-dim'); });
      } else {
        schedule();
      }
    };
    if (typeof reducedQuery.addEventListener === 'function') reducedQuery.addEventListener('change', onMotionChange);

    // ---- Start: center the second video when there are a few, so both sides show
    root.classList.add('is-carousel');
    layout();
    const startIndex = visibleCards().length > 2 ? 1 : 0;
    activeIndex = startIndex;
    goTo(startIndex, false);
    updateUi();
    schedule();
  });
});
