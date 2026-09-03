document.addEventListener('DOMContentLoaded', () => {
  const heroPolish = document.createElement('style');
  heroPolish.textContent = `
    .hero-home {
      min-height: 88vh;
      background: #6f4456;
    }

    .hero-home .hero-photo {
      filter: saturate(.96) contrast(1.035) brightness(.98);
    }

    .hero-home .hero-shade {
      background:
        linear-gradient(90deg, rgba(43, 19, 34, .64) 0%, rgba(69, 31, 51, .30) 43%, rgba(82, 45, 66, .05) 78%),
        linear-gradient(0deg, rgba(37, 16, 29, .48) 0%, rgba(61, 30, 48, .10) 48%, transparent 74%);
    }

    .hero-home .hero-content {
      padding-bottom: 72px;
    }

    .hero-home h1 {
      text-shadow: 0 3px 26px rgba(35, 12, 26, .22);
    }

    .hero-home .hero-copy {
      color: rgba(255, 248, 251, .90);
      text-shadow: 0 1px 12px rgba(38, 15, 29, .22);
    }

    .site-header.light-on-hero {
      border-bottom-color: rgba(255, 235, 243, .24);
    }

    .discipline-band {
      background: #f3dce5;
      color: #542c3d;
      border-top: 1px solid rgba(113, 58, 79, .12);
      border-bottom: 1px solid rgba(113, 58, 79, .14);
    }

    .discipline-list {
      min-height: 58px;
      font-size: clamp(.95rem, 1.45vw, 1.18rem);
      letter-spacing: .08em;
    }

    .discipline-list i {
      color: #b86f8b;
    }

    @media (max-width: 760px) {
      .hero-home {
        min-height: 84vh;
      }

      .hero-home .hero-shade {
        background: linear-gradient(0deg, rgba(42, 18, 32, .66), rgba(74, 35, 57, .18) 72%);
      }

      .discipline-list {
        padding: 14px 0;
      }
    }
  `;
  document.head.appendChild(heroPolish);

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
