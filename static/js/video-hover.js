/* Hover-to-play for TikTok embeds.
 * TikTok's player only starts its control API once playback begins, so each
 * player loads muted with autoplay, is paused as soon as it starts, and then
 * plays while the pointer is over its card. On touch screens (no hover) the
 * video most in view plays instead, one at a time.
 * Markup: a card with [data-hover-card] containing iframe[data-hover-video].
 */
(() => {
  const noHover = window.matchMedia('(hover: none)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const frames = () => Array.from(document.querySelectorAll('iframe[data-hover-video]'));
  const cards = () => Array.from(document.querySelectorAll('[data-hover-card]'));
  const stateOf = frame => frame.hoverState || (frame.hoverState = { ready: false, want: false, playing: false });

  const send = (frame, type, value = null) => {
    if (frame.contentWindow) frame.contentWindow.postMessage({ type, value, 'x-tiktok-player': true }, '*');
  };

  const apply = frame => {
    const state = stateOf(frame);
    if (!state.ready) return;
    send(frame, state.want ? 'play' : 'pause');
  };

  const setWant = (card, want) => {
    if (!card) return;
    card.querySelectorAll('iframe[data-hover-video]').forEach(frame => {
      const state = stateOf(frame);
      if (state.want === want) return;
      state.want = want;
      if (!want && state.ready) send(frame, 'seekTo', 0);
      apply(frame);
    });
    card.classList.toggle('is-previewing', want);
  };

  window.addEventListener('message', event => {
    let host = '';
    try { host = new URL(event.origin).hostname; } catch (error) { return; }
    if (host !== 'tiktok.com' && !host.endsWith('.tiktok.com')) return;
    let data = event.data;
    if (typeof data === 'string') {
      try { data = JSON.parse(data); } catch (error) { return; }
    }
    if (!data || !data['x-tiktok-player']) return;
    const frame = frames().find(f => f.contentWindow === event.source);
    if (!frame) return;
    const state = stateOf(frame);
    if (data.type === 'onPlayerReady') {
      state.ready = true;
      apply(frame);
    } else if (data.type === 'onStateChange') {
      state.ready = true;
      state.playing = data.value === 1;
      // Autoplay is only used to wake the player up; hold it until wanted.
      if (state.playing && !state.want) send(frame, 'pause');
      const card = frame.closest('[data-hover-card]');
      if (card) card.classList.toggle('is-playing', state.playing && state.want);
    }
  });

  // A transparent layer over each video catches the pointer (an iframe would
  // swallow it). Clicking or tapping it toggles the preview.
  document.addEventListener('click', event => {
    const shield = event.target.closest && event.target.closest('[data-hover-shield]');
    if (!shield) return;
    const card = shield.closest('[data-hover-card]');
    if (card) setWant(card, !card.classList.contains('is-previewing'));
  });

  // Pointer hover (mouse and pen)
  document.addEventListener('pointerover', event => {
    if (event.pointerType === 'touch' || noHover.matches) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    if (card && !card.contains(event.relatedTarget)) setWant(card, true);
  });
  document.addEventListener('pointerout', event => {
    if (event.pointerType === 'touch' || noHover.matches) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    if (card && !card.contains(event.relatedTarget)) setWant(card, false);
  });
  // Safety net for fast pointer moves that skip a pointerout.
  document.addEventListener('pointermove', event => {
    if (event.pointerType === 'touch' || noHover.matches) return;
    const over = event.target.closest && event.target.closest('[data-hover-card]');
    cards().forEach(card => {
      if (card !== over && card.classList.contains('is-previewing')) setWant(card, false);
    });
  }, { passive: true });

  // Keyboard users: focusing a card's link previews its video.
  document.addEventListener('focusin', event => {
    // Only keyboard focus; a mouse click or tap is handled by the click toggle.
    if (!event.target.matches || !event.target.matches(':focus-visible')) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    cards().forEach(other => { if (other !== card && other.classList.contains('is-previewing') && !other.matches(':hover')) setWant(other, false); });
    if (card) setWant(card, true);
  });

  // Touch screens: play the one video most in view.
  const ratios = new Map();
  const pickForTouch = () => {
    if (!noHover.matches || reducedMotion.matches || document.hidden) {
      if (noHover.matches) cards().forEach(card => setWant(card, false));
      return;
    }
    const visible = cards().filter(card => (ratios.get(card) || 0) >= 0.6 && card.querySelector('iframe[data-hover-video]'));
    let chosen = visible.find(card => card.classList.contains('is-active'));
    if (!chosen) chosen = visible.sort((a, b) => (ratios.get(b) || 0) - (ratios.get(a) || 0))[0];
    cards().forEach(card => setWant(card, card === chosen));
  };
  if ('IntersectionObserver' in window) {
    const watch = new IntersectionObserver(entries => {
      entries.forEach(entry => ratios.set(entry.target, entry.intersectionRatio));
      pickForTouch();
    }, { threshold: [0, 0.3, 0.6, 0.85, 1] });
    const observeAll = () => cards().forEach(card => watch.observe(card));
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', observeAll);
    else observeAll();
  }
  document.addEventListener('reels:active', pickForTouch);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cards().forEach(card => setWant(card, false));
    else pickForTouch();
  });
})();
