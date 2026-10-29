/* Hover-to-play for TikTok embeds, with sound when the browser allows it.
 *
 * TikTok's player only starts its control API once playback begins, so each
 * player loads with autoplay (browsers force that to be muted), is paused as
 * soon as it starts, and then plays while the pointer is over its card.
 *
 * Sound: browsers only allow audio after the visitor has clicked, tapped or
 * pressed a key on the page. Before that, hover previews play muted with a
 * "Click for sound" hint; clicking the video turns sound on. After any click
 * on the page, hover previews play with sound.
 *
 * On touch screens (no hover) the video most in view plays muted, one at a
 * time; tapping it turns sound on.
 * Markup: a card with [data-hover-card] containing iframe[data-hover-video],
 * a [data-hover-shield] button over the video and an optional .video-sound-hint.
 */
(() => {
  const noHover = window.matchMedia('(hover: none)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const frames = () => Array.from(document.querySelectorAll('iframe[data-hover-video]'));
  const cards = () => Array.from(document.querySelectorAll('[data-hover-card]'));
  const stateOf = frame => frame.hoverState || (frame.hoverState = {
    ready: false, want: false, sound: false, playing: false, muted: true, retried: false,
  });

  let activated = Boolean(navigator.userActivation && navigator.userActivation.hasBeenActive);
  const markActivated = () => { activated = true; };
  ['pointerdown', 'keydown', 'touchstart'].forEach(type => {
    document.addEventListener(type, markActivated, { capture: true, passive: true });
  });

  const send = (frame, type, value = null) => {
    if (frame.contentWindow) frame.contentWindow.postMessage({ type, value, 'x-tiktok-player': true }, '*');
  };

  const paint = card => {
    if (!card) return;
    const frame = card.querySelector('iframe[data-hover-video]');
    const state = frame ? stateOf(frame) : null;
    const previewing = Boolean(state && state.want);
    card.classList.toggle('is-previewing', previewing);
    card.classList.toggle('is-playing', Boolean(state && state.want && state.playing));
    card.classList.toggle('is-muted', Boolean(state && state.want && state.muted));
    card.classList.toggle('has-sound', Boolean(state && state.want && !state.muted));
  };

  const apply = frame => {
    const state = stateOf(frame);
    if (!state.ready) return;
    if (state.want) {
      send(frame, state.sound && activated ? 'unMute' : 'mute');
      send(frame, 'play');
    } else {
      send(frame, 'pause');
    }
  };

  const setWant = (card, want, sound = false) => {
    if (!card) return;
    card.querySelectorAll('iframe[data-hover-video]').forEach(frame => {
      const state = stateOf(frame);
      if (state.want === want && state.sound === sound) return;
      const stopping = state.want && !want;
      state.want = want;
      state.sound = want && sound;
      state.retried = false;
      if (stopping && state.ready) send(frame, 'seekTo', 0);
      apply(frame);
    });
    paint(card);
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
    const card = frame.closest('[data-hover-card]');

    if (data.type === 'onPlayerReady') {
      state.ready = true;
      apply(frame);
    } else if (data.type === 'onMute') {
      state.muted = Boolean(data.value);
    } else if (data.type === 'onStateChange') {
      state.ready = true;
      state.playing = data.value === 1;
      if (state.playing && !state.want) {
        // Autoplay only wakes the player up; hold it until wanted.
        send(frame, 'pause');
      } else if (data.value === 2 && state.want && !state.retried) {
        // Turning sound on can make the browser pause the video once; resume it.
        state.retried = true;
        send(frame, 'play');
      }
    }
    paint(card);
  });

  // The shield over the video catches the pointer (an iframe would swallow it).
  // Clicking it turns sound on; clicking again while it plays with sound stops it.
  document.addEventListener('click', event => {
    const shield = event.target.closest && event.target.closest('[data-hover-shield]');
    if (!shield) return;
    const card = shield.closest('[data-hover-card]');
    if (!card) return;
    activated = true;
    if (card.classList.contains('has-sound') && card.classList.contains('is-playing')) {
      setWant(card, false);
    } else {
      cards().forEach(other => { if (other !== card) setWant(other, false); });
      setWant(card, true, true);
    }
  });

  // Mouse and pen hover
  const hoverAllowed = event => event.pointerType !== 'touch' && !noHover.matches;
  document.addEventListener('pointerover', event => {
    if (!hoverAllowed(event)) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    if (card && !card.contains(event.relatedTarget)) setWant(card, true, activated);
  });
  document.addEventListener('pointerout', event => {
    if (!hoverAllowed(event)) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    if (card && !card.contains(event.relatedTarget)) setWant(card, false);
  });
  // Safety net for fast pointer moves that skip a pointerout.
  document.addEventListener('pointermove', event => {
    if (!hoverAllowed(event)) return;
    const over = event.target.closest && event.target.closest('[data-hover-card]');
    cards().forEach(card => {
      if (card !== over && card.classList.contains('is-previewing')) setWant(card, false);
    });
  }, { passive: true });

  // Keyboard users: focusing a card previews its video.
  document.addEventListener('focusin', event => {
    if (!event.target.matches || !event.target.matches(':focus-visible')) return;
    const card = event.target.closest && event.target.closest('[data-hover-card]');
    cards().forEach(other => {
      if (other !== card && other.classList.contains('is-previewing') && !other.matches(':hover')) setWant(other, false);
    });
    if (card) setWant(card, true, activated);
  });

  // Touch screens: play the one video most in view (muted until tapped).
  const ratios = new Map();
  const pickForTouch = () => {
    if (!noHover.matches) return;
    if (reducedMotion.matches || document.hidden) {
      cards().forEach(card => setWant(card, false));
      return;
    }
    const visible = cards().filter(card => (ratios.get(card) || 0) >= 0.6 && card.querySelector('iframe[data-hover-video]'));
    let chosen = visible.find(card => card.classList.contains('is-active'));
    if (!chosen) chosen = visible.sort((a, b) => (ratios.get(b) || 0) - (ratios.get(a) || 0))[0];
    cards().forEach(card => {
      if (card === chosen) setWant(card, true, card.classList.contains('has-sound'));
      else setWant(card, false);
    });
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
