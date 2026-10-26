(function () {
  'use strict';

  const search = document.getElementById('catalog-search');
  const type = document.getElementById('catalog-type');
  const island = document.getElementById('catalog-island');
  const count = document.getElementById('catalog-count');
  const items = Array.from(document.querySelectorAll('li[data-catalog-item][data-type][data-island]'));
  if (!search || !type || !island || !count || !items.length) return;

  function apply() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;

    for (const item of items) {
      const text = item.textContent.toLowerCase();
      const matches = terms.every((term) => text.includes(term)) &&
        (!type.value || item.dataset.type === type.value) &&
        (!island.value || item.dataset.island === island.value);
      item.hidden = !matches;
      if (matches) shown++;
    }

    count.textContent = shown
      ? `Showing ${shown} of ${items.length} items.`
      : `No items match. Showing 0 of ${items.length} items.`;
  }

  search.addEventListener('input', apply);
  type.addEventListener('change', apply);
  island.addEventListener('change', apply);
  apply();
})();
