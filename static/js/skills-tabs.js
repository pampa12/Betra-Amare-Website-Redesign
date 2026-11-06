/* Skills / Certifications tabs on the portfolio page (WAI-ARIA tabs pattern). */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-skill-tabs]').forEach(root => {
    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    if (tabs.length < 2) return;
    const select = (tab, focus) => {
      tabs.forEach(other => {
        const active = other === tab;
        other.classList.toggle('is-active', active);
        other.setAttribute('aria-selected', active ? 'true' : 'false');
        other.tabIndex = active ? 0 : -1;
        const panel = document.getElementById(other.getAttribute('aria-controls'));
        if (panel) panel.hidden = !active;
      });
      if (focus) tab.focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(tab, false));
      tab.addEventListener('keydown', event => {
        let next = null;
        if (event.key === 'ArrowRight') next = tabs[(index + 1) % tabs.length];
        if (event.key === 'ArrowLeft') next = tabs[(index - 1 + tabs.length) % tabs.length];
        if (event.key === 'Home') next = tabs[0];
        if (event.key === 'End') next = tabs[tabs.length - 1];
        if (next) { event.preventDefault(); select(next, true); }
      });
    });
  });
});
