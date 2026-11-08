#!/usr/bin/env python3
"""Checks the built site. Run after `python3 src/build.py`:  python3 tests/check_site.py
Exits 1 on any failure. Prints word counts for detailed service pages."""
import json, re, sys, subprocess
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
C=json.load(open(ROOT/'src/site.config.json')); BASE=C['baseUrl'].rstrip('/')
CATS=json.load(open(ROOT/'src/services.json'))
PAGES=[json.load(open(f)) for f in sorted((ROOT/'src/pages').glob('*.json'))]
FAIL=[]
def fail(m): FAIL.append(m)

# ---- catalog ----
S=[s for c in CATS for s in c['services']]
if len(CATS)!=8: fail(f'expected 8 categories, got {len(CATS)}')
if len(S)!=67: fail(f'expected 67 services, got {len(S)}')
if sum(1 for s in S if s.get('new'))!=26: fail('expected 26 services marked new')
ids=[s['id'] for s in S]
if len(set(ids))!=len(ids): fail('duplicate service ids')
if len(set(c['url'] for c in CATS))!=8: fail('duplicate category urls')
if len(set(p['slug'] for p in PAGES))!=len(PAGES): fail('duplicate page slugs')
FORBIDDEN=re.compile(r'retread|notary|fleet repair|classic car|vintage car|motorcycle inspection|tags? (?:and|&) titles?|towing|tesla',re.I)
def walk(x,path='',lang_pairs=True):
    if isinstance(x,dict):
        if set(x)=={'en','es'}:
            for k in ('en','es'):
                if not isinstance(x[k],str) or not x[k].strip(): fail(f'missing {k} text at {path}')
            if x['en'].strip()==x['es'].strip() and len(x['en'])>12: fail(f'Spanish identical to English at {path}')
            return
        for k,v in x.items(): walk(v,f'{path}.{k}')
    elif isinstance(x,list):
        for i,v in enumerate(x): walk(v,f'{path}[{i}]')
walk(CATS,'services.json')
for s in S:
    if FORBIDDEN.search(json.dumps(s,ensure_ascii=False)): fail(f'forbidden service wording in {s["id"]}')
for p in PAGES:
    walk({k:v for k,v in p.items() if k not in('secondary_kws','verify','sources','adaptedFrom')},p['id'])
    if not 5<=len(p['faq'])<=8: fail(f'{p["id"]}: {len(p["faq"])} FAQs (want 5-8)')
    for sid in p['covers']+p['related']:
        if sid not in ids: fail(f'{p["id"]}: unknown service {sid}')
    if FORBIDDEN.search(json.dumps(p,ensure_ascii=False)): fail(f'forbidden wording in page {p["id"]}')

# ---- built HTML ----
class Parse(HTMLParser):
    def __init__(s):
        super().__init__(); s.ids=set(); s.hrefs=[]; s.h1=0; s.titles=0; s.desc=0; s.canon=[]; s.alts={}; s.lang=None
        s.text=[]; s.skip=0; s.ld=[]; s.inld=False; s.robots=''
    def handle_starttag(s,t,a):
        a=dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t=='html': s.lang=a.get('lang')
        if t=='a' and a.get('href'): s.hrefs.append(a['href'])
        if t=='h1': s.h1+=1
        if t=='title': s.titles+=1
        if t=='meta' and a.get('name')=='description': s.desc+=1
        if t=='meta' and a.get('name')=='robots': s.robots=a.get('content','')
        if t=='link' and a.get('rel')=='canonical': s.canon.append(a['href'])
        if t=='link' and a.get('rel')=='alternate' and a.get('hreflang'): s.alts[a['hreflang']]=a['href']
        if t in('script','style','svg','title','dialog'): s.skip+=1
        if t=='script' and a.get('type')=='application/ld+json': s.inld=True
    def handle_endtag(s,t):
        if t in('script','style','svg','title','dialog'): s.skip=max(0,s.skip-1)
        if t=='script': s.inld=False
    def handle_data(s,d):
        if s.inld: s.ld.append(d)
        elif not s.skip: s.text.append(d)
files=sorted(ROOT.glob('**/index.html'))+[ROOT/'404.html']
files=[f for f in files if '.git' not in f.parts and 'node_modules' not in f.parts and 'tests' not in f.parts]
DOC={}
for f in files:
    p=Parse(); p.feed(f.read_text(encoding='utf-8')); DOC[f]=p
def url_of(f):
    r=f.relative_to(ROOT).parent.as_posix()
    return BASE+'/' if r=='.' else BASE+'/'+r+'/'
ESWORDS=re.compile(r"\b(the|and|your|with|our|you|we|call us|repairs?|brakes?|engine|services|shop|hours)\b",re.I)
ES_OK=["Scally's Auto Repair","Secane Ave","Secane Avenue","check engine","AMSOIL","English","OIS","Primos","Clifton Heights","ABS","Google","Yelp"]
for f,p in DOC.items():
    rel=f.relative_to(ROOT).as_posix()
    if p.titles!=1: fail(f'{rel}: {p.titles} <title>')
    if p.desc!=1: fail(f'{rel}: {p.desc} meta descriptions')
    if p.h1!=1: fail(f'{rel}: {p.h1} h1')
    if f.name=='index.html':
        if len(p.canon)!=1 or p.canon[0]!=url_of(f): fail(f'{rel}: canonical {p.canon} != {url_of(f)}')
    raw=f.read_text(encoding='utf-8')
    if 'REPLACE-WITH-DOMAIN' in raw or 'scallysautorepair.com' in raw: fail(f'{rel}: placeholder or dead domain')
    txt=' '.join(p.text)
    for bad in ('Diverse','Phoenixville','ASE-certified','ASE certified','Chester County','Pawlings'):
        if bad in raw: fail(f'{rel}: contains "{bad}"')
    if 'reviews' not in rel and rel!='sitemap/index.html' and '/brands/' not in '/'+rel and not rel.startswith('brands/') and FORBIDDEN.search(txt): fail(f'{rel}: forbidden service wording "{FORBIDDEN.search(txt).group(0)}"')
    for block in p.ld:
        try: json.loads(block)
        except Exception as e: fail(f'{rel}: bad JSON-LD {e}')
    # internal links resolve, fragments exist
    for h in p.hrefs:
        if re.match(r'^(https?:|tel:|mailto:|#$)',h): continue
        path,_,frag=h.partition('#')
        tgt=(f.parent/path).resolve() if path else f
        if tgt.is_dir(): tgt=tgt/'index.html'
        if not tgt.exists(): fail(f'{rel}: broken link {h}'); continue
        if frag and tgt in DOC and frag not in DOC[tgt].ids: fail(f'{rel}: missing anchor {h}')
    # hreflang reciprocity
    for lang,u in p.alts.items():
        if lang=='x-default': continue
        g=ROOT/(u[len(BASE)+1:] or '')/'index.html' if u!=BASE+'/' else ROOT/'index.html'
        if g not in DOC: fail(f'{rel}: hreflang {lang} -> missing {u}'); continue
        if DOC[g].alts.get('en')!=p.alts.get('en') or DOC[g].alts.get('es')!=p.alts.get('es'): fail(f'{rel}: hreflang not reciprocal with {u}')
        if DOC[g].lang!=lang: fail(f'{rel}: hreflang {lang} points at lang={DOC[g].lang}')
    if p.lang=='es' and not (rel.startswith('es/brands/') or rel.startswith('brands/')):
        t=txt
        for ok in ES_OK: t=t.replace(ok,' ')
        hits=sorted(set(m.group(0).lower() for m in ESWORDS.finditer(t)))
        if hits: fail(f'{rel}: English words on Spanish page: {hits}')

# ---- sitemap ----
sm=(ROOT/'sitemap.xml').read_text()
locs=re.findall(r'<loc>([^<]+)</loc>',sm)
if len(locs)!=len(set(locs)): fail('duplicate sitemap URLs')
for u in locs:
    g=ROOT/'index.html' if u==BASE+'/' else ROOT/u[len(BASE)+1:]/'index.html'
    if g not in DOC: fail(f'sitemap URL with no page: {u}')
    elif 'noindex' in DOC[g].robots: fail(f'noindex page in sitemap: {u}')
for p in PAGES:
    for pre in ('','/es'):
        if f'{BASE}{pre}/{p["slug"]}/' not in locs: fail(f'sitemap missing {pre}/{p["slug"]}/')
if f'Sitemap: {BASE}/sitemap.xml' not in (ROOT/'robots.txt').read_text(): fail('robots.txt sitemap line wrong')

# ---- every service reachable from its category hub, both languages ----
for c in CATS:
    for lang,pre in (('en',''),('es','/es')):
        g=ROOT/(pre.strip('/')+c['url']).strip('/')/'index.html'
        for s in c['services']:
            if s['id'] not in DOC[g].ids: fail(f'{pre}{c["url"]}: no anchor for {s["id"]}')

# ---- detailed pages: covered services anchored ----
WC={}
for p in PAGES:
    for lang,pre in (('en',''),('es','es/')):
        g=ROOT/(pre+p['slug'])/'index.html'
        for sid in p['covers'][1:]:
            if sid not in DOC[g].ids: fail(f'{pre}{p["slug"]}: no anchor for covered service {sid}')
        m=re.search(r'<main\b.*?</main>',g.read_text(encoding='utf-8'),re.S).group(0)
        body=re.sub(r'<[^>]+>',' ',re.sub(r'<(script|svg)\b.*?</\1>','',m,flags=re.S))
        WC[(p['slug'],lang)]=len(body.split())

# ---- reviews and contact facts unchanged vs main ----
def at_main(path):
    try: return subprocess.run(['git','-C',str(ROOT),'show','origin/main:'+path],capture_output=True,text=True,check=True).stdout
    except Exception: return None
old=at_main('src/reviews.json')
if old is not None and json.loads(old)!=json.load(open(ROOT/'src/reviews.json')): fail('src/reviews.json changed')
oc=at_main('src/site.config.json')
if oc:
    oc=json.loads(oc)
    for k in ('name','phoneDisplay','phoneTel','street','city','region','zip','hours','ois','since','googleReviewUrl','yelpUrl'):
        if oc.get(k)!=C.get(k): fail(f'site.config {k} changed')

print(f'{len(DOC)} pages checked, {len(locs)} sitemap URLs, {len(S)} services in {len(CATS)} categories, {len(PAGES)} detailed pages')
for (sl,lang),n in sorted(WC.items()): print(f'  words  {lang}  {sl:24} {n}')
if FAIL:
    print(f'\n{len(FAIL)} FAILURES'); [print(' -',x) for x in FAIL]; sys.exit(1)
print('ALL CHECKS PASSED')
