#!/usr/bin/env python3
"""Check the additive inventory and its generated publication bytes only."""
from pathlib import Path
import hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
from extend_inventory import outputs, read
def main():
    for name,raw in outputs().items(): assert (ROOT/name).read_bytes()==raw,name
    rows=read('data/builds-expanded.json');cells=read('data/cell-evidence.json')
    baseline=read('data/builds.json');by_key={r['key']:r for r in rows}
    assert len(rows)==11 and len(cells)==11
    for original in baseline:
        current=by_key[original['key']]
        assert all(current[k]==v for k,v in original.items() if k!='surfaces')
        assert all(current['surfaces'][k]==v for k,v in original['surfaces'].items())
        for key in ['expected_event_accounting']:
            assert current['surfaces'][key] is None
            assert cells[original['key']][key]['state']=='not_assessed'
    index=ROOT/'docs/index.html';before=index.read_bytes()
    subprocess.run([sys.executable,str(ROOT/'src/build_expanded_page.py')],check=True)
    assert index.read_bytes()==before,'Rendered page was stale'
    text=index.read_text(encoding='utf-8')
    assert text.count('class="cell ')==165
    assert 'data-surface="detection_evaluation"' not in text
    assert 'id="definition-detection_evaluation"' not in text
    assert 'id="build-forward"' in text
    ext=read('governance/claim-integrity-extension.json')
    assert 'not assessed' in text and ext['cells']['chart_review']['result']=='pass'
    assert ext['source_commit'] in text
    for name in ['builds.json','builds-expanded.json','cell-evidence.json','standard.json']:
        assert (ROOT/'docs/reference'/name).read_bytes()==(ROOT/'data'/name).read_bytes()
    for name in ['surfaces.md','build-forward.md','extension-provenance.json','surface-catalog.json','claim-integrity-extension.json']:
        assert (ROOT/'docs/reference'/name).read_bytes()==(ROOT/'governance'/name).read_bytes()
    print('PASS: provenance, 140 original cells, 10 not-assessed cells, 165 rendered cells, N/A run health, build-forward-only evaluation, deterministic page and reference bytes.')
if __name__=='__main__': main()
