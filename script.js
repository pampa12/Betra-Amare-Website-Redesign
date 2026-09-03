document.addEventListener('DOMContentLoaded', () => {
  const isHome = Boolean(document.querySelector('.hero-home'));

  if (isHome) {
    const main = document.querySelector('main');
    const discipline = document.querySelector('.discipline-band');
    const selected = document.querySelector('.selected-work');
    const about = document.querySelector('.about-split');
    const world = document.querySelector('#world');

    if (main && discipline && selected && about && world) {
      discipline.insertAdjacentElement('afterend', selected);
      selected.insertAdjacentElement('afterend', about);
      about.insertAdjacentElement('afterend', world);
    }

    if (selected) selected.id = 'selected-work-home';
    const scrollCue = document.querySelector('.scroll-cue');
    if (scrollCue) {
      scrollCue.setAttribute('href', '#selected-work-home');
      scrollCue.innerHTML = 'Selected work <span>↓</span>';
    }
  }

  const refinedTheme = document.createElement('style');
  refinedTheme.textContent = `
    :root {
      --ink: #342b30;
      --paper: #fffbfc;
      --cream: #f7eff3;
      --blush: #c9879f;
      --blush-soft: #ead7df;
      --muted: #786970;
      --line: rgba(71, 55, 63, .14);
    }

    body {
      background: var(--paper);
      color: var(--ink);
    }

    .site-header {
      background: rgba(255, 251, 252, .95);
      color: var(--ink);
      border-bottom-color: var(--line);
    }

    .wordmark,
    .main-nav a,
    .nav-cta,
    .page-hero h1,
    .display-title,
    .card-caption h3,
    .value-block h3 {
      color: var(--ink);
    }

    .page-hero {
      background: linear-gradient(135deg, #f6edf1 0%, #fffafc 100%);
      border-bottom-color: var(--line);
    }

    .eyebrow,
    .signature {
      color: #b36f89;
    }

    .body-copy,
    .form-note,
    .card-caption span,
    .filter-btn {
      color: var(--muted);
    }

    .dark-button {
      background: #af6c87;
      border-color: #af6c87;
      color: #fff;
    }

    .dark-button:hover {
      background: transparent;
      color: #8f566d;
      border-color: #8f566d;
    }

    .nav-cta:hover {
      background: #4a3b43;
      border-color: #4a3b43;
      color: #fff;
    }

    .contact-list a,
    .portfolio-filter,
    .card-caption {
      border-color: var(--line);
    }

    .about-page-section,
    .contact-section,
    .social-section,
    .portfolio-section,
    .selected-work {
      background: var(--paper);
    }

    .value-block { background: #fffdfd; }

    .site-footer {
      background: linear-gradient(135deg, #46363e 0%, #5a424d 100%);
      color: #fff;
    }

    .footer-top { border-bottom-color: rgba(255,255,255,.16); }
    .footer-nav a { color: rgba(255,255,255,.82); }
    .footer-bottom { color: rgba(255,255,255,.56); }

    .media-frame,
    .work-tile,
    .social-photo,
    .portfolio-item {
      background: #eadce2;
    }

    ${isHome ? `
      .hero-home {
        min-height: 82vh;
        max-height: 860px;
        background: #6a555f;
      }

      .hero-home .hero-photo {
        filter: saturate(.98) contrast(1.035) brightness(.99);
        object-position: center 28%;
      }

      .hero-home .hero-shade {
        background:
          linear-gradient(90deg, rgba(36, 28, 33, .60) 0%, rgba(64, 47, 56, .28) 40%, rgba(92, 72, 82, .04) 72%),
          linear-gradient(0deg, rgba(40, 30, 35, .36) 0%, transparent 47%);
      }

      .hero-home .hero-content { padding: 165px 0 64px; }

      .hero-home .hero-content h1 {
        max-width: 850px;
        font-size: clamp(3.9rem, 7vw, 7rem);
        line-height: .9;
        color: #fff;
        text-shadow: 0 4px 24px rgba(20, 15, 18, .20);
      }

      .hero-home .hero-copy {
        max-width: 470px;
        font-size: .96rem;
        color: rgba(255, 250, 252, .92);
      }

      .site-header.light-on-hero {
        background: transparent;
        color: #fff;
        border-bottom-color: rgba(255,255,255,.22);
      }

      .site-header.light-on-hero .wordmark,
      .site-header.light-on-hero .main-nav a,
      .site-header.light-on-hero .nav-cta {
        color: #fff;
      }

      .site-header.light-on-hero .nav-inner { min-height: 78px; }
      .site-header.light-on-hero .wordmark { font-size: 1.4rem; letter-spacing: .13em; }

      .discipline-band {
        background: #f1e3e8;
        color: #4b3b43;
        border-top: 1px solid rgba(79, 58, 68, .10);
        border-bottom: 1px solid rgba(79, 58, 68, .12);
      }

      .discipline-list {
        min-height: 52px;
        font-size: clamp(.88rem, 1.2vw, 1.05rem);
        letter-spacing: .1em;
      }

      .discipline-list i { color: #b97890; }

      .selected-work {
        padding: 88px 0 96px;
        border-top: 0;
      }

      .selected-work .section-heading { margin-bottom: 38px; }
      .selected-work .display-title { font-size: clamp(2.8rem, 5vw, 5rem); }
      .selected-work .editorial-grid { grid-template-rows: 300px 330px; gap: 14px; }

      .about-split {
        background: #f5ecef;
        padding: 92px 0;
      }

      .about-grid {
        grid-template-columns: 1.08fr .92fr;
        gap: 6vw;
      }

      .about-visual { min-height: 590px; }
      .about-main-photo { inset: 0 15% 7% 0; }
      .about-accent-photo {
        width: 38%;
        height: 39%;
        border-color: #f5ecef;
        border-width: 8px;
      }

      .about-copy .display-title { font-size: clamp(2.8rem, 4.6vw, 4.8rem); }
      .about-copy .body-copy { max-width: 460px; }

      .section-cream {
        background: #fffbfc;
        padding: 94px 0 104px;
      }

      .section-cream .intro-grid {
        margin-bottom: 44px;
        grid-template-columns: 1.1fr .9fr;
      }

      .section-cream .display-title { font-size: clamp(2.8rem, 4.8vw, 4.9rem); }
      .section-cream .category-grid { grid-template-columns: repeat(3, 1fr); gap: 18px; }
      .section-cream .category-card.offset { padding-top: 0; }
      .section-cream .media-frame.tall,
      .section-cream .media-frame.tallest,
      .section-cream .media-frame.medium { aspect-ratio: 4 / 5; }

      .collab-section {
        background: linear-gradient(135deg, #e8d3dc 0%, #f5e8ed 100%);
        padding: 96px 0;
      }

      .collab-inner {
        max-width: 920px;
        margin: 0 auto;
        text-align: center;
      }

      .collab-inner .display-title.huge {
        max-width: 820px;
        margin: 0 auto 22px;
        font-size: clamp(3rem, 5.8vw, 5.8rem);
      }

      .collab-inner .body-copy {
        margin: 0 auto 28px;
        max-width: 610px;
        color: #6f5d65;
      }

      .collab-inner .cta-row { justify-content: center; }
      .social-section { padding: 88px 0 96px; }
      .social-section .section-heading { margin-bottom: 34px; }
      .social-section .display-title { font-size: clamp(2.7rem, 4.6vw, 4.8rem); }
      .social-photo-grid { gap: 10px; }

      @media (max-width: 980px) {
        .hero-home { min-height: 78vh; }
        .selected-work .editorial-grid { grid-template-rows: 260px 285px; }
        .about-visual { min-height: 520px; }
      }

      @media (max-width: 760px) {
        .hero-home { min-height: 80vh; max-height: none; }
        .hero-home .hero-photo { object-position: 58% 24%; }
        .hero-home .hero-shade {
          background: linear-gradient(0deg, rgba(40,30,35,.68), rgba(87,66,76,.16) 74%);
        }
        .hero-home .hero-content { padding: 140px 0 50px; }
        .hero-home .hero-content h1 { font-size: clamp(3.2rem, 14vw, 4.8rem); }
        .discipline-list { padding: 13px 0; }

        .selected-work,
        .about-split,
        .section-cream,
        .collab-section,
        .social-section { padding: 72px 0; }

        .selected-work .editorial-grid {
          grid-template-columns: 1fr 1fr;
          grid-template-rows: 360px 215px 195px;
        }

        .about-grid { grid-template-columns: 1fr; gap: 40px; }
        .about-copy { order: -1; }
        .about-visual { min-height: 500px; }
        .section-cream .intro-grid { grid-template-columns: 1fr; }
        .section-cream .category-grid { display: block; }
        .section-cream .category-card { margin-bottom: 30px; }
        .collab-inner { text-align: left; }
        .collab-inner .display-title.huge,
        .collab-inner .body-copy { margin-left: 0; }
        .collab-inner .cta-row { justify-content: flex-start; }
      }
    ` : ''}
  `;
  document.head.appendChild(refinedTheme);

  const menuToggle = document.querySelector('#menuToggle');
  const mainNav = document.querySelector('#mainNav');

  if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', () => {
      const open = mainNav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', String(open));
    });

    mainNav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  document.querySelectorAll('[data-year]').forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    reveals.forEach((el) => observer.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('visible'));
  }

  const filterButtons = document.querySelectorAll('[data-filter]');
  const portfolioItems = document.querySelectorAll('[data-category]');

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const filter = button.dataset.filter;
      filterButtons.forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');

      portfolioItems.forEach((item) => {
        const matches = filter === 'all' || item.dataset.category === filter;
        item.classList.toggle('is-hidden', !matches);
      });
    });
  });
});
