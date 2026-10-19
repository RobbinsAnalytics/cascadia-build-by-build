#!/usr/bin/env python3
"""Build the portfolio extension, retaining the original frozen inventory.
Run extend_inventory.py first; this renderer uses committed local inputs only.
"""
from pathlib import Path
import hashlib, html, json, shutil, sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
from extend_inventory import outputs

def esc(value): return html.escape(str(value),quote=True)
def load(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    for name,raw in outputs().items():
        assert (ROOT/name).read_bytes()==raw, 'Regenerate '+name
    rows=load('data/builds-expanded.json'); catalog=load('governance/surface-catalog.json'); cells=load('data/cell-evidence.json')
    # Stable numbers identify surfaces; band order places 16 with Numbers and
    # 15 with Operation. They are column IDs, never a score or sequence of merit.
    groups=['Data','Numbers','Presentation','Operation']
    ordered=[s for group in groups for s in catalog if s['group']==group]
    symbols={'recorded':'●','limited':'◐','absent':'−','not_assessed':'?'}
    names={'recorded':'Artifact recorded','limited':'Limited evidence','absent':'Not carried','not_assessed':'Not assessed'}
    bandheads=''.join(f'<th scope="colgroup" colspan="{sum(s["group"]==g for s in ordered)}">{g}</th>' for g in groups)
    short_labels={1:'Rebuild',2:'Frozen inputs',3:'Sources',4:'Row counts',5:'Report',6:'Code tests',7:'Second path',8:'Golden cases',9:'Faults',10:'Charts',11:'Panel',12:'Metrics',13:'Run health',14:'Recon.',15:'Due work',16:'Detector eval.'}
    heads=''.join(f'<th scope="col" data-group="{s["group"]}"><button class="column-head" type="button" data-definition="{s["id"]}" aria-label="{s["number"]:02d} {esc(s["label"])}" title="Read definition: {esc(s["label"])}"><span>{s["number"]:02d}</span>{short_labels[s["number"]]}</button></th>' for s in ordered)
    table=[]
    for n,row in enumerate(rows,1):
        key=row['key']; short=row['name'].removeprefix('Cascadia ')
        titlelink=row.get('case_study','/projects/'+row['site_slug']+'.html')
        if not titlelink.startswith(('/', 'https://')): titlelink='/'+titlelink
        cols=[]
        for s in ordered:
            c=cells[key][s['id']]; state=c['state']; label=f'{short}: {s["label"]}. {names[state]}. Result: {c["result"]}. Select for evidence.'
            cols.append(f'<td data-group="{s["group"]}"><button type="button" class="cell {state}" data-build="{key}" data-surface="{s["id"]}" aria-label="{esc(label)}" aria-pressed="false" title="{esc(label)}">{symbols[state]}</button></td>')
        table.append(f'<tr data-row="{key}" class="{"latest" if key=="cascadia-claim-integrity" else ""}"><th scope="row"><span class="row-number">{n:02d}</span><a href="{titlelink}">{esc(short)}</a><small>{row["first_commit"]}{" · New" if key=="cascadia-claim-integrity" else ""}</small></th>'+''.join(cols)+'</tr>')
    definitions=[]
    for group in groups:
        details=''.join(f'<details id="definition-{s["id"]}"><summary><span class="definition-number">{s["number"]:02d}</span>{esc(s["label"])}{"<span class=tag>Added</span>" if s["new"] else ""}</summary><p>{esc(s["description"])}</p><a href="reference/surfaces.md">Read the counting rule</a></details>' for s in catalog if s['group']==group)
        definitions.append(f'<section class="definition-group"><h3>{group}</h3>{details}</section>')
    standard=load('data/standard.json')
    lane=''.join(f'<li><strong>v{esc(s["version"])}</strong><span>{esc(s["date"] or "Date not established")}</span></li>' for s in standard)
    options=''.join(f'<option value="{r["key"]}">{esc(r["name"].removeprefix("Cascadia "))}</option>' for r in rows)
    legend=''.join(f'<li><span class="legend-mark {key}" aria-hidden="true">{symbol}</span><span>{names[key]}</span></li>' for key,symbol in symbols.items())
    payload=json.dumps(dict(rows=rows,surfaces=catalog,cells=cells),ensure_ascii=False).replace('<','\\u003c')
    page=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>Build by Build | Robbins Analytics</title><meta name="description" content="Eleven Cascadia builds, sixteen test surfaces, and the evidence and limits behind each recorded artifact.">
<link rel="canonical" href="https://www.robbinsanalytics.com/cascadia-build-by-build/">
<meta property="og:title" content="Build by Build: evidence, with its limits"><meta property="og:image" content="https://www.robbinsanalytics.com/assets/thumb-build-by-build.png">
<link rel="icon" href="assets/brand/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@1,500&family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/portfolio-extension.css"><script defer src="assets/portfolio-extension.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="header"><a class="wordmark" href="/"><img src="assets/brand/robbins-mark.svg" width="28" height="28" alt="">Robbins <em>Analytics.</em></a><nav aria-label="Site"><a href="/cascadia.html">Cascadia</a><a href="/case-studies.html">Case studies</a><a href="/cascadia-claim-integrity/">Latest build <span aria-hidden="true">↗</span></a></nav></header>
<main id="main" class="container"><section class="hero"><div><p class="eyebrow">The Cascadia portfolio · Evidence inventory</p><h1>Build by <em>Build.</em></h1><p class="lede">What each build could check.<br>What the evidence can actually say.</p><p>Eleven independent portfolio builds. Sixteen test surfaces. A way to trace the controls each project carried, with failures and limits kept in view.</p><div class="actions"><a class="button dark" href="#matrix">Explore the evidence <span aria-hidden="true">↓</span></a><a class="button outline" href="#new">What changed</a></div></div>
<aside class="guide"><p class="eyebrow">Follow the evidence</p><h2>A file is a start.<br><em>Its result matters.</em></h2><p>A filled cell records an artifact. It does not say a check passed, every requirement was met, or the build is production ready.</p><a href="#matrix">Choose a cell to see why <span aria-hidden="true">↘</span></a></aside></section>
<section class="stats" aria-label="Inventory scope"><div><span>01 / Builds</span><strong>{len(rows)}</strong><p>Independent projects, in first-commit order</p></div><div><span>02 / Test surfaces</span><strong>{len(catalog)}</strong><p>The original fourteen, plus two additional definitions</p></div><div><span>03 / Added with this build</span><strong>2</strong><p>Expected events and detector evaluation</p></div></section>
<section id="new" class="section"><div class="section-head"><div><p class="eyebrow">The latest addition</p><h2>Missing work needs<br><em>its own evidence.</em></h2></div><p>Claim Integrity starts with claims and follows the evidence into downstream encounters. Two additional surfaces make absence and detection measurable.</p></div>
<div class="two-cards"><article class="feature"><span class="tag">15 / Operation</span><h3>Account for what should exist</h3><p>Expected event accounting starts from the triggering facts, rather than only the records that arrived. A missing claim or promised response remains an obligation.</p><p class="consequence">The question: what was due, at which cutoff, and is it still missing?</p><a href="#definition-expected_event_accounting">Read the definition ↓</a></article><article class="feature tint"><span class="tag">16 / Numbers</span><h3>Test the detection itself</h3><p>Detection evaluation retains the eligible failures and clean opportunities, including misses, false alarms and timing. Selected successful injections are not enough.</p><p class="consequence">Claim Integrity carries limited, historical evidence here. Independent evaluator custody was not established.</p><a href="#definition-detection_evaluation">Read the definition ↓</a></article></div>
<p class="scope-note">The two columns are additional inventory definitions. Earlier builds have not been assessed against them. No first-ever capability claim or estate-wide standards change is implied.</p></section>
<section id="matrix" class="section matrix-section"><div class="section-head"><div><p class="eyebrow">The comparison</p><h2>Find the artifact.<br><em>Read the outcome.</em></h2></div><p>Filter by build or kind of check. Select a mark for the recorded result, source path and available evidence. Column numbers are stable identifiers, not scores.</p></div>
<div class="controls"><label>Build<select id="build-filter" aria-label="Build"><option value="all">All eleven builds</option>{options}</select></label><label>Kind of check<select id="group-filter" aria-label="Kind of check"><option value="all">All four groups</option>{''.join(f'<option>{g}</option>' for g in groups)}</select></label><button class="button outline" type="button" id="reset">Reset view</button></div>
<ul class="legend" aria-label="Cell legend">{legend}</ul><p class="matrix-hint" id="matrix-hint">Scroll inside the table to see every column and build. Headers and build names stay in view. Artifact recorded is not a pass rating.</p>
<div class="matrix-scroll" tabindex="0" role="region" aria-label="Evidence matrix, horizontally and vertically scrollable" aria-describedby="matrix-hint"><table><caption class="sr-only">Eleven builds by sixteen test surfaces. Each mark opens its evidence and scope.</caption><thead><tr class="bands"><th rowspan="2" scope="col" class="corner">Build / first commit</th>{bandheads}</tr><tr class="columns">{heads}</tr></thead><tbody>{''.join(table)}</tbody></table></div>
<p class="selection-count" id="selection-count" role="status">Showing 11 builds and 16 test surfaces.</p>
<article id="evidence-detail" class="evidence-detail" aria-live="polite"><p class="eyebrow">Selected evidence / Cascadia Claim Integrity</p><h3>15 · Expected event accounting</h3><span class="result">Recorded result: pass</span><p>Independent obligations accounted at each cutoff. This is the frozen public verification result, not a new execution.</p><p><code>governance/expected-event-accounting.md</code></p><a href="/cascadia-claim-integrity/evidence/expected-event-accounting.md">Open the served snapshot artifact ↗</a></article>
<noscript><p>The complete matrix and definitions remain visible. Interactive selection requires JavaScript; the <a href="reference/cell-evidence.json">complete evidence register</a> contains every path and recorded outcome.</p></noscript>
<p class="scope-note">Original ten builds: inventory frozen October 7, 2026, without a new outcome audit. Claim Integrity: repository evidence pinned to e936d1a; statuses come from its frozen public verification snapshot. A served snapshot can differ from a later repository artifact; the evidence register keeps both identities.</p></section>
<section class="section" id="definitions"><div class="section-head"><div><p class="eyebrow">A shared vocabulary</p><h2>What each surface<br><em>is looking for.</em></h2></div><p>Open a definition for its purpose. The counting rules state which artifacts qualify and which do not. Limited evidence stays distinct from a completed requirement.</p></div><div class="definitions">{''.join(definitions)}</div></section>
<section class="section limits"><p class="eyebrow">How far the comparison goes</p><h2>Traceable evidence.<br><em>Bounded claims.</em></h2><div class="three-cards"><article><h3>A chronology, not a league table</h3><p>Different problems need different controls. A count of artifacts is not a score for quality, maturity or business impact. An absent historical cell creates no remediation debt.</p></article><article><h3>Acceptance retains the failures</h3><p>Claim Integrity is accepted for a personal website as a frozen synthetic snapshot. Re-derivation matched all 22,173 published cells, while its recorded surface result remains fail. Current chart re-review is deferred; the restricted simulated panel retains four minor open items.</p></article><article><h3>Historical detection has limits</h3><p>Unblinded attempt 2 met must-catch in 20 of 26 represented classes, with 36 registered. Six missed targets and ten unrepresented classes remain disclosed. No independent evaluator custody or effectiveness of the final controls is claimed. A successful scheduled receipt is outside the accepted frozen-snapshot scope.</p></article></div><a class="button dark" href="/cascadia-claim-integrity/case-study.html">Read the Claim Integrity case study ↗</a></section>
<section class="section provenance"><details><summary>Inventory provenance and design-standard history</summary><p>The original 10 × 14 inventory and standards history retain their October 7 freeze at <code>66b9de6</code>. This is an additive October 19 extension, not a claim that all eleven repositories were audited on one date. The new row reads commit <code>e936d1ada2b5cfc54919157e4d9b8b9cd833506c</code>.</p><p><a href="reference/extension-provenance.json">Provenance record</a> · <a href="reference/builds.json">Original ten-build snapshot</a> · <a href="reference/builds-expanded.json">Extended inventory</a> · <a href="reference/cell-evidence.json">Evidence and outcomes</a> · <a href="reference/surfaces.md">All counting rules</a></p><h3>VIZ-PRINCIPLES history in the original inventory</h3><ul class="standard-lane">{lane}</ul><p>Dates not established by the original history remain unknown. This lane is historical and does not claim current chart-review completion.</p></details></section>
</main><footer><a class="wordmark" href="/"><img src="assets/brand/robbins-mark-reversed.svg" width="28" height="28" alt="">Robbins <em>Analytics.</em></a><p>Portfolio projects. Evidence, scope and unresolved findings kept together.</p><a href="/case-studies.html">All case studies ↗</a></footer><script id="inventory-data" type="application/json">{payload}</script></body></html>'''
    (ROOT/'docs/index.html').write_text(page,encoding='utf-8',newline='\n')
    ref=ROOT/'docs/reference';ref.mkdir(exist_ok=True)
    for name in ['data/builds.json','data/builds-expanded.json','data/cell-evidence.json','data/standard.json','governance/surfaces.md','governance/extension-provenance.json','governance/surface-catalog.json','governance/claim-integrity-extension.json']:
        shutil.copyfile(ROOT/name,ref/Path(name).name)
    print('Rendered 11 × 16 matrix with outcomes, definitions and bounded claims.')
if __name__=='__main__': main()
