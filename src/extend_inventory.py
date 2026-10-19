#!/usr/bin/env python3
"""Add a pinned Claim Integrity row without re-reading the ten-build freeze.

python src/extend_inventory.py [--check]
The original inventory.py and its protected files are unchanged. --check does
not write. No sibling commands, detector execution or evaluation occurs here.
"""
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parent.parent
def read(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(name): return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
def encoded(obj): return (json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()
def outputs():
    prov=read('governance/extension-provenance.json')
    baseline=read(prov['baseline']['path'])
    assert sha(prov['baseline']['path'])==prov['baseline']['sha256'], 'Original freeze changed'
    ext=read(prov['extension']['path'])
    assert sha(prov['extension']['path'])==prov['extension']['sha256'], 'Extension bytes differ from provenance'
    catalog=read('governance/surface-catalog.json')
    assert [s['number'] for s in catalog]==list(range(1,16))
    assert all(s['id']!='detection_evaluation' for s in catalog)
    assert len(baseline)==10 and all(len(b['surfaces'])==14 for b in baseline)
    rows=[]; cells={}
    for old in baseline:
        row=dict(old); row['surfaces']=dict(old['surfaces']); detail={}
        for s in catalog:
            key=s['id']; path=old['surfaces'].get(key)
            if s['new']:
                row['surfaces'][key]=None
                detail[key]=dict(state='not_assessed',result='not assessed',path=None,summary='Not assessed against this additional definition. The fourteen-column baseline cannot establish presence or absence.',href=None)
            else:
                href=('https://github.com/RobbinsAnalytics/'+old['remote']+'/'+('tree' if path.endswith('/') else 'blob')+'/'+old['default_branch']+'/'+path) if path else None
                detail[key]=dict(state='recorded' if path else 'absent',result='artifact recorded' if path else 'not carried in baseline',path=path,href=href,summary='Artifact recorded in the October 7 inventory; this extension does not re-score that historical check.' if path else 'No qualifying artifact was recorded by the original inventory. This is not a current audit and creates no remediation debt.')
        rows.append(row); cells[row['key']]=detail
    rows.append(ext['row']); cells[ext['row']['key']]=ext['cells']
    assert len({r['key'] for r in rows})==11
    assert all(set(r['surfaces'])=={s['id'] for s in catalog} for r in rows)
    for s in catalog:
        c=cells[ext['row']['key']][s['id']]
        assert c['state'] in ['recorded','limited','not_applicable']
        assert c['path']==ext['row']['surfaces'][s['id']]
        assert len(c['sha256'])==64 and c['source_commit']==ext['source_commit']
    assert cells['cascadia-claim-integrity']['scheduled_run_with_health']['state']=='not_applicable'
    rederive=cells['cascadia-claim-integrity']['independent_rederivation']
    assert (rederive['state']=='recorded') == (rederive['result']=='pass')
    rows.sort(key=lambda r:r['first_commit'])
    return {'data/builds-expanded.json':encoded(rows),'data/cell-evidence.json':encoded(cells)}
def main():
    for name,raw in outputs().items():
        p=ROOT/name
        if '--check' in sys.argv:
            assert p.exists() and p.read_bytes()==raw, name+' differs; regenerate extension'
        else:
            p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(raw)
    print('Current inventory: 11 builds, 15 columns; 140 baseline cells preserved; 10 new legacy cells not assessed. Detection evaluation is build forward only.')
if __name__=='__main__': main()
