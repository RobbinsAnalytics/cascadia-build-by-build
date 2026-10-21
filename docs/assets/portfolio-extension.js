'use strict';
(() => {
  const data = JSON.parse(document.getElementById('inventory-data').textContent);
  const build = document.getElementById('build-filter');
  const group = document.getElementById('group-filter');
  document.querySelectorAll('[data-definition]').forEach(button => button.addEventListener('click', () => {
    const detail = document.getElementById('definition-' + button.dataset.definition);
    detail.open = true;
    detail.scrollIntoView({block:'center', behavior:'instant'});
    detail.querySelector('summary').focus({preventScroll:true});
  }));
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#definition-"]');
    if (link) document.querySelector(link.getAttribute('href')).open = true;
  });
  function filter() {
    const anchor = document.querySelector('.controls'), before = anchor.getBoundingClientRect().top;
    const table = document.querySelector('.matrix-scroll');
    const position = [table.scrollLeft, table.scrollTop];
    let count = 0;
    document.querySelectorAll('[data-row]').forEach(row => {
      row.hidden = build.value !== 'all' && row.dataset.row !== build.value;
      if (!row.hidden) count++;
    });
    document.querySelectorAll('[data-group]').forEach(cell => cell.hidden = group.value !== 'all' && cell.dataset.group !== group.value);
    document.querySelectorAll('.bands th[scope="colgroup"]').forEach(cell => cell.hidden = group.value !== 'all' && cell.textContent !== group.value);
    const n = group.value === 'all' ? data.surfaces.length : data.surfaces.filter(s => s.group === group.value).length;
    document.getElementById('selection-count').textContent = `Showing ${count} build${count === 1 ? '' : 's'} and ${n} test surfaces. Definitions and scope notes remain fixed.`;
    document.querySelector('table').classList.toggle('filtered', group.value !== 'all');
    table.scrollLeft = position[0]; table.scrollTop = position[1];
    window.scrollBy({top:anchor.getBoundingClientRect().top - before, behavior:'instant'});
  }
  build.addEventListener('change', filter); group.addEventListener('change', filter);
  document.getElementById('reset').addEventListener('click', () => {build.value='all'; group.value='all'; filter();});
  const header = document.querySelector('.header'), index = document.querySelector('.page-index');
  const links = [...index.querySelectorAll('a')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href')));
  function track() {
    const offset = header.getBoundingClientRect().height + (matchMedia('(max-width:1000px)').matches ? index.getBoundingClientRect().height : 0);
    let active = 0;
    sections.forEach((section, i) => {if(section.getBoundingClientRect().top <= offset + 75) active = i;});
    if (window.scrollY + innerHeight >= document.documentElement.scrollHeight - 3) active = links.length - 1;
    links.forEach((link, i) => {if(i === active) link.setAttribute('aria-current','location'); else link.removeAttribute('aria-current');});
  }
  function size() {
    document.documentElement.style.setProperty('--header-height', header.getBoundingClientRect().height + 'px');
    document.documentElement.style.setProperty('--index-height', (matchMedia('(max-width:1000px)').matches ? index.getBoundingClientRect().height : 0) + 'px');
    track();
  }
  new ResizeObserver(size).observe(header); new ResizeObserver(size).observe(index);
  window.addEventListener('scroll', track, {passive:true}); window.addEventListener('resize', size); size();
})();
