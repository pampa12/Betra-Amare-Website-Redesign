document.addEventListener('DOMContentLoaded', () => {
  const navItems = document.querySelectorAll('.nav-item[data-panel]');
  const panels = document.querySelectorAll('[data-panel-content]');
  const panelTitle = document.querySelector('#panelTitle');
  const sidebar = document.querySelector('#adminSidebar');
  const mobileMenu = document.querySelector('#mobileMenu');
  const toast = document.querySelector('#toast');

  const titles = {
    dashboard: 'Dashboard',
    homepage: 'Homepage',
    portfolio: 'Portfolio',
    media: 'Media Library',
    about: 'About',
    socials: 'Socials',
    inquiries: 'Inquiries',
    collabs: 'Collaborations',
    settings: 'Settings'
  };

  function showPanel(name) {
    navItems.forEach((item) => item.classList.toggle('active', item.dataset.panel === name));
    panels.forEach((panel) => panel.classList.toggle('active', panel.dataset.panelContent === name));
    panelTitle.textContent = titles[name] || 'Admin';
    sidebar.classList.remove('open');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  navItems.forEach((item) => item.addEventListener('click', () => showPanel(item.dataset.panel)));
  document.querySelectorAll('[data-jump]').forEach((button) => button.addEventListener('click', () => showPanel(button.dataset.jump)));

  mobileMenu?.addEventListener('click', () => sidebar.classList.toggle('open'));

  function showToast(message = 'Preview mode: changes are not saved yet.') {
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(window.__adminToastTimer);
    window.__adminToastTimer = setTimeout(() => toast.classList.remove('show'), 2400);
  }

  document.querySelector('#previewBtn')?.addEventListener('click', () => window.open('index.html', '_blank'));
  document.querySelector('#publishBtn')?.addEventListener('click', () => showToast('Looks good! Publishing will work after we connect the secure backend.'));
  document.querySelectorAll('.primary-button:not(.upload-button)').forEach((button) => {
    if (button.id !== 'publishBtn') button.addEventListener('click', () => showToast('Saved in the demo UI. Permanent saving comes with the backend connection.'));
  });

  const heroUpload = document.querySelector('#heroUpload');
  const heroPreview = document.querySelector('#heroPreview');
  const miniHero = document.querySelector('#miniHero');
  heroUpload?.addEventListener('change', () => {
    const file = heroUpload.files?.[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    heroPreview.src = url;
    miniHero.src = url;
    showToast('Hero photo preview updated.');
  });

  const portfolioUpload = document.querySelector('#portfolioUpload');
  const portfolioGrid = document.querySelector('#portfolioAdminGrid');
  portfolioUpload?.addEventListener('change', () => {
    [...(portfolioUpload.files || [])].forEach((file) => {
      const card = document.createElement('article');
      card.className = 'media-card';
      const url = URL.createObjectURL(file);
      card.innerHTML = `<img src="${url}" alt="New portfolio upload"><div><select><option>Beauty</option><option>Fashion</option><option>Lifestyle</option></select><button type="button">⋯</button></div>`;
      portfolioGrid.appendChild(card);
    });
    if (portfolioUpload.files?.length) showToast(`${portfolioUpload.files.length} photo${portfolioUpload.files.length > 1 ? 's' : ''} added to the preview.`);
  });
});
