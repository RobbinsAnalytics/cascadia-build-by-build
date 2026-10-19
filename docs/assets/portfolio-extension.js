'use strict';
(() => {
  const data = JSON.parse(document.getElementById('inventory-data').textContent);
  const builds = new Map(data.rows.map(r => [r.key, r]));
  const surfaces = new Map(data.surfaces.map(s => [s.id, s]));
  const build = document.getElementById('build-filter');
  const group = document.getElementById('group-filter');
  const panel = document.getElementById('evidence-detail');
  const stateNames = {recorded:'Artifact recorded', limited:'Limited evidence', absent:'Not carried in baseline', not_assessed:'Not assessed', not_applicable:'Not applicable'};
  const node = (tag, text, className) => {
    const el = document.createElement(tag); el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  function selectCell(button) {
    document.querySelectorAll('.cell[aria-pressed="true"]').forEach(b => b.setAttribute('aria-pressed','false'));
    button.setAttribute('aria-pressed','true');
    const row = builds.get(button.dataset.build), s = surfaces.get(button.dataset.surface);
    const c = data.cells[row.key][s.id];
    if (!panel) return;  // the selected-evidence panel was removed (owner, 2026-10-19)
    panel.replaceChildren(node('p', 'Selected evidence / '+row.name, 'eyebrow'),
      node('h3', String(s.number).padStart(2,'0')+' · '+s.label),
      node('span', stateNames[c.state]+' / recorded result: '+c.result, 'result '+c.state),
      node('p', c.summary));
    if (c.path) { const p=node('p',''); p.append(node('code',c.path)); panel.append(p); }
    if (c.result_basis) panel.append(node('p',c.result_basis+'.','detail-meta'));
    if (c.snapshot_differs_from_repository) panel.append(node('p','The served snapshot differs from the pinned repository artifact. This link opens the historical public snapshot, not the later repository bytes.','detail-meta'));
    if (c.source_commit) panel.append(node('p','Repository source: '+c.source_commit+'. Public summary: frozen verification snapshot.','detail-meta'));
    if (c.href) { const a=node('a', row.key==='cascadia-claim-integrity' ? (c.access==='served snapshot artifact'?'Open the served snapshot artifact ↗':'Open the public verification summary ↗') : 'Open the historical repository artifact ↗'); a.href=c.href; panel.append(a); }
    else panel.append(node('p',c.state==='not_assessed'?'Presence and absence have not been established.':'No artifact link was recorded for this cell.','detail-meta'));
    const definition=node('a','Read the surface definition ↓'); definition.href='#definition-'+s.id;
    const p=node('p','');p.append(definition);panel.append(p);
  }
  document.querySelectorAll('.cell').forEach(b=>b.addEventListener('click',()=>selectCell(b)));
  document.querySelectorAll('[data-definition]').forEach(b=>b.addEventListener('click',()=>{
    const d=document.getElementById('definition-'+b.dataset.definition);d.open=true;d.scrollIntoView({block:'center',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});d.querySelector('summary').focus();
  }));
  document.addEventListener('click',e=>{const a=e.target.closest('a[href^="#definition-"]');if(a){const d=document.querySelector(a.getAttribute('href'));if(d)d.open=true;}});
  function filter() {
    let count=0;
    document.querySelectorAll('[data-row]').forEach(r=>{r.hidden=build.value!=='all'&&r.dataset.row!==build.value;if(!r.hidden)count++;});
    document.querySelectorAll('[data-group]').forEach(c=>c.hidden=group.value!=='all'&&c.dataset.group!==group.value);
    document.querySelectorAll('.bands th[scope="colgroup"]').forEach(c=>c.hidden=group.value!=='all'&&c.textContent!==group.value);
    const n=group.value==='all'?data.surfaces.length:data.surfaces.filter(s=>s.group===group.value).length;
    document.getElementById('selection-count').textContent=`Showing ${count} build${count===1?'':'s'} and ${n} test surfaces.`;
    document.querySelector('table').classList.toggle('filtered',group.value!=='all');
    const first=document.querySelector(`tr[data-row="${build.value==='all'?'cascadia-claim-integrity':build.value}"] .cell${group.value==='all'?'':`[data-surface="${data.surfaces.find(s=>s.group===group.value).id}"]`}`);
    if(first)selectCell(first);
  }
  build.addEventListener('change',filter);group.addEventListener('change',filter);
  document.getElementById('reset').addEventListener('click',()=>{build.value='all';group.value='all';filter();});
  selectCell(document.querySelector('[data-build="cascadia-claim-integrity"][data-surface="expected_event_accounting"]'));
})();
