document.addEventListener('DOMContentLoaded', () => {
  const isHome = Boolean(document.querySelector('.hero-home'));

  if (isHome) {
    const main = document.querySelector('main');
    const discipline = document.querySelector('.discipline-band');
    const selected = document.querySelector('.selected-work');
    const about = document.querySelector('.about-split');
    const world = document.querySelector('#world');
    const collab = document.querySelector('.collab-section');
    const social = document.querySelector('.social-section');

    // Put the strongest work first, then introduce Betra, then show categories.
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

    const homePolish = document.createElement('style');
    homePolish.textContent = `
      /* Homepage editorial refinement */
      body { background: #fff9fb; }

      .hero-home {
        min-height: 82vh;
        max-height: 860px;
        background: #6a4051;
      }

      .hero-home .hero-photo {
        filter: saturate(.98) contrast(1.04) brightness(.98);
        object-position: center 28%;
      }

      .hero-home .hero-shade {
        background:
          linear-gradient(90deg, rgba(41, 16, 30, .62) 0%, rgba(63, 28, 46, .30) 38%, rgba(79, 44, 62, .05) 70%),
          linear-gradient(0deg, rgba(42, 17, 31, .42) 0%, transparent 46%);
      }

      .hero-home .hero-content {
        padding: 165px 0 64px;
      }

      .hero-home .hero-content h1 {
        max-width: 850px;
        font-size: clamp(3.9rem, 7vw, 7rem);
        line-height: .9;
        text-shadow: 0 4px 26px rgba(35, 12, 25, .22);
      }

      .hero-home .hero-copy {
        max-width: 470px;
        font-size: .96rem;
        color: rgba(255, 248, 251, .92);
      }

      .site-header.light-on-hero {
        border-bottom-color: rgba(255, 235, 244, .22);
      }

      .site-header.light-on-hero .nav-inner {
        min-height: 78px;
      }

      .site-header.light-on-hero .wordmark {
        font-size: 1.4rem;
        letter-spacing: .13em;
      }

      .discipline-band {
        background: #f6e5ec;
        color: #5a3041;
        border-top: 1px solid rgba(111, 60, 81, .10);
        border-bottom: 1px solid rgba(111, 60, 81, .12);
      }

      .discipline-list {
        min-height: 52px;
        font-size: clamp(.88rem, 1.2vw, 1.05rem);
        letter-spacing: .1em;
      }

      .discipline-list i { color: #c27a96; }

      /* Put the portfolio front and center. */
      .selected-work {
        background: #fffafb;
        border-top: 0;
        padding: 88px 0 96px;
      }

      .selected-work .section-heading {
        margin-bottom: 38px;
      }

      .selected-work .display-title {
        font-size: clamp(2.8rem, 5vw, 5rem);
      }

      .selected-work .editorial-grid {
        grid-template-rows: 300px 330px;
        gap: 14px;
      }

      .selected-work .work-tile {
        background: #ead7df;
        border-radius: 2px;
      }

      /* Shorter, cleaner intro section. */
      .about-split {
        background: #f9edf2;
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
        border-color: #f9edf2;
        border-width: 8px;
      }

      .about-copy .display-title {
        font-size: clamp(2.8rem, 4.6vw, 4.8rem);
      }

      .about-copy .body-copy { max-width: 460px; }

      /* Categories become a clean three-card editorial row. */
      .section-cream {
        background: #fff9fb;
        padding: 94px 0 104px;
      }

      .section-cream .intro-grid {
        margin-bottom: 44px;
        grid-template-columns: 1.1fr .9fr;
      }

      .section-cream .display-title {
        font-size: clamp(2.8rem, 4.8vw, 4.9rem);
      }

      .section-cream .category-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
      }

      .section-cream .category-card.offset { padding-top: 0; }
      .section-cream .media-frame.tall,
      .section-cream .media-frame.tallest,
      .section-cream .media-frame.medium { aspect-ratio: 4 / 5; }
      .section-cream .media-frame { background: #ead7df; }

      .section-cream .card-caption {
        padding-top: 13px;
      }

      /* Collaboration reads like a premium closing statement, not another giant hero. */
      .collab-section {
        background: linear-gradient(135deg, #f1d6e1 0%, #f8e8ee 100%);
        padding: 96px 0;
      }

      .collab-section::before {
        right: -1vw;
        bottom: -5vw;
        color: rgba(255,255,255,.34);
      }

      .collab-inner {
        max-width: 920px;
        margin-left: auto;
        margin-right: auto;
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
      }

      .collab-inner .cta-row { justify-content: center; }

      /* Social stays visual and quiet. */
      .social-section {
        background: #fffafb;
        padding: 88px 0 96px;
      }

      .social-section .section-heading { margin-bottom: 34px; }
      .social-section .display-title {
        font-size: clamp(2.7rem, 4.6vw, 4.8rem);
      }

      .social-photo-grid { gap: 10px; }
      .social-photo { background: #ead7df; }

      .eyebrow { color: #a65f7c; }
      .signature { color: #aa6280; }

      @media (max-width: 980px) {
        .hero-home { min-height: 78vh; }
        .selected-work .editorial-grid { grid-template-rows: 260px 285px; }
        .about-visual { min-height: 520px; }
      }

      @media (max-width: 760px) {
        .hero-home { min-height: 80vh; max-height: none; }
        .hero-home .hero-photo { object-position: 58% 24%; }
        .hero-home .hero-shade {
          background: linear-gradient(0deg, rgba(42,18,32,.70), rgba(75,35,57,.18) 74%);
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
    `;
    document.head.appendChild(homePolish);
  }

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

  document.querySelectorAll('.social-photo').forEach((photo) => {
    photo.addEventListener('click', (event) => {
      event.preventDefault();
    });
  });

  const contactForm = document.querySelector('#contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const name = contactForm.querySelector('[name="name"]').value.trim();
      const email = contactForm.querySelector('[name="email"]').value.trim();
      const project = contactForm.querySelector('[name="project"]').value;
      const message = contactForm.querySelector('[name="message"]').value.trim();

      const subject = encodeURIComponent(`Website inquiry from ${name || 'a potential collaborator'}`);
      const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\nProject type: ${project}\n\n${message}`);
      window.location.href = `mailto:workwithbetra@gmail.com?subject=${subject}&body=${body}`;
    });
  }
});
