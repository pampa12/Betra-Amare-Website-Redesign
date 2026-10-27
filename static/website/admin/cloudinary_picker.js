/* Django-admin-only browser for images already stored in Cloudinary.
 * The browser receives only public IDs and thumbnail URLs; Cloudinary credentials
 * remain server-side. Normal Django image upload inputs are unchanged.
 */
document.addEventListener('DOMContentLoaded', () => {
  const inputs = Array.from(document.querySelectorAll('.cloudinary-picker-input[data-picker-url]'));
  if (!inputs.length) return;

  const dialog = document.createElement('dialog');
  dialog.className = 'cloudinary-picker-dialog';
  dialog.setAttribute('aria-label', 'Choose an existing Cloudinary photo');

  const heading = document.createElement('h2');
  heading.textContent = 'Choose from Cloudinary';
  const help = document.createElement('p');
  help.textContent = 'Browse your existing images. Search matches the beginning of a Cloudinary public ID. No new copy is uploaded.';

  const searchForm = document.createElement('form');
  searchForm.className = 'cloudinary-picker-search';
  searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    searchPrefix = search.value.trim();
    cursors = [''];
    showPage(0);
  });

  const search = document.createElement('input');
  search.type = 'search';
  search.placeholder = 'Search public ID prefix';
  search.setAttribute('aria-label', 'Search Cloudinary image public IDs');
  search.maxLength = 100;
  const searchButton = document.createElement('button');
  searchButton.type = 'submit';
  searchButton.textContent = 'Search';
  searchForm.append(search, searchButton);

  const status = document.createElement('p');
  status.className = 'cloudinary-picker-status';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  const grid = document.createElement('div');
  grid.className = 'cloudinary-picker-grid';

  const footer = document.createElement('div');
  footer.className = 'cloudinary-picker-footer';
  const previous = document.createElement('button');
  previous.type = 'button';
  previous.textContent = 'Previous';
  const next = document.createElement('button');
  next.type = 'button';
  next.textContent = 'Next';
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = 'Close';
  close.addEventListener('click', () => dialog.close());
  footer.append(previous, next, close);
  dialog.append(heading, help, searchForm, status, grid, footer);
  document.body.appendChild(dialog);

  let selectedInput = null;
  let searchPrefix = '';
  let cursors = [''];
  let currentPage = 0;
  let serial = 0;

  function refreshSelected(input) {
    const area = input._cloudinarySelection;
    if (!area) return;
    area.textContent = input.value ? `Selected: ${input.value}` : 'No library photo selected';
    input._cloudinaryClear.disabled = !input.value;
  }

  inputs.forEach((input) => {
    const controls = document.createElement('div');
    controls.className = 'cloudinary-picker-controls';

    const open = document.createElement('button');
    open.type = 'button';
    open.textContent = 'Choose from Cloudinary';
    open.addEventListener('click', () => {
      selectedInput = input;
      searchPrefix = '';
      search.value = '';
      cursors = [''];
      heading.textContent = `Choose photo for ${input.dataset.imageLabel || 'image'}`;
      dialog.showModal();
      showPage(0);
      search.focus();
    });

    const selection = document.createElement('span');
    selection.className = 'cloudinary-picker-selection';
    input._cloudinarySelection = selection;
    const clear = document.createElement('button');
    clear.type = 'button';
    clear.textContent = 'Clear selection';
    clear.addEventListener('click', () => {
      input.value = '';
      refreshSelected(input);
    });
    input._cloudinaryClear = clear;

    controls.append(open, clear, selection);
    input.insertAdjacentElement('afterend', controls);
    refreshSelected(input);
  });

  previous.addEventListener('click', () => {
    if (currentPage > 0) showPage(currentPage - 1);
  });
  next.addEventListener('click', () => {
    if (cursors[currentPage + 1]) showPage(currentPage + 1);
  });

  async function showPage(page) {
    if (!selectedInput) return;
    const requestNumber = ++serial;
    currentPage = page;
    grid.replaceChildren();
    status.textContent = 'Loading images…';
    previous.disabled = true;
    next.disabled = true;

    const url = new URL(selectedInput.dataset.pickerUrl, window.location.href);
    if (searchPrefix) url.searchParams.set('q', searchPrefix);
    if (cursors[page]) url.searchParams.set('cursor', cursors[page]);

    try {
      const response = await fetch(url, {
        credentials: 'same-origin',
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) throw new Error('Unable to load photos (' + response.status + ').');
      const data = await response.json();
      if (requestNumber !== serial) return;
      if (!Array.isArray(data.images)) throw new Error('Unexpected response from the photo browser.');

      data.images.forEach((item) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'cloudinary-picker-tile';
        button.setAttribute('aria-label', 'Use photo ' + item.public_id);

        const img = document.createElement('img');
        img.src = item.preview_url;
        img.alt = '';
        img.loading = 'lazy';

        const name = document.createElement('span');
        name.textContent = item.public_id;
        button.append(img, name);
        button.addEventListener('click', () => {
          selectedInput.value = item.public_id;
          refreshSelected(selectedInput);
          dialog.close();
        });
        grid.appendChild(button);
      });

      if (data.next_cursor) cursors[page + 1] = data.next_cursor;
      else cursors = cursors.slice(0, page + 1);
      previous.disabled = page === 0;
      next.disabled = !data.next_cursor;
      status.textContent = data.images.length
        ? `Page ${page + 1}. Choose a photo or move to another page.`
        : 'No matching images. Try a shorter prefix.';
    } catch (error) {
      if (requestNumber !== serial) return;
      status.textContent = error.message || 'Could not load Cloudinary photos.';
    }
  }
});
