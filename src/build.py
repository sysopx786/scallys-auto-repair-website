#!/usr/bin/env python3
"""Static site generator for Scally's Auto Repair. Run: python3 src/build.py  (from site root)"""
import json, re, html
from pathlib import Path
from urllib.parse import quote_plus
ROOT=Path(__file__).resolve().parent.parent
C=json.load(open(ROOT/'src/site.config.json'))
CATS=json.load(open(ROOT/'src/services.json'))
RV=json.load(open(ROOT/'src/reviews.json'))
IMG=json.load(open(ROOT/'src/images.json'))
NAME=C['name']; PH=C['phoneDisplay']; TEL=C['phoneTel']
BASE=C['baseUrl']; YRS=2026-C['since']
esc=lambda s:html.escape(s,quote=True)
def slug(s): return re.sub(r'(^-|-$)','',re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and')))
for c in CATS:
    c['slug']=c['url'].strip('/')
    for s in c['services']: s['slug']=slug(s['name'])
ICON={c['url']:c['icon'] for c in CATS}
SHORT={c['url']:c['name'] for c in CATS}
NSV=sum(len(c['services']) for c in CATS)
NUMW={5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine'}
SAFE=re.compile(r'\b(safe|unsafe|dangerous|pull over|stop driving|911|fire|fumes|overheat)',re.I)
ADDR=f"{C['street']}, {C['city']}, {C['region']} {C['zip']}"
MAPS_URL="https://www.google.com/maps/search/?api=1&amp;query="+quote_plus(C['mapsQuery'])
DIR_URL="https://www.google.com/maps/dir/?api=1&amp;destination="+quote_plus(C['mapsQuery'])
GR,YR=RV['google'],RV['yelp']
TOTAL=GR['count']+YR['count']

SPRITE='''<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><defs>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s7-6.2 7-11a7 7 0 1 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7"/></symbol>
<symbol id="i-chev" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></symbol>
<symbol id="i-truck" viewBox="0 0 24 24"><path d="M2 7h12v9H2zM14 10h4l3 3v3h-7"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/></symbol>
<symbol id="i-bolt" viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></symbol>
<symbol id="i-disc" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></symbol>
<symbol id="i-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3.2"/><circle cx="12" cy="12" r="6.5"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/></symbol>
<symbol id="i-tire" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/></symbol>
<symbol id="i-car" viewBox="0 0 24 24"><path d="M3 15l2-6a2 2 0 0 1 2-1.5h10a2 2 0 0 1 2 1.5l2 6v3H3z"/><path d="M3 15h18"/><circle cx="7.5" cy="18" r="1.8"/><circle cx="16.5" cy="18" r="1.8"/></symbol>
<symbol id="i-camera" viewBox="0 0 24 24"><path d="M3 8h4l2-3h6l2 3h4v11H3z"/><circle cx="12" cy="13" r="3.5"/></symbol>
<symbol id="i-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>
<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-7 9 7M5 10v10h5v-6h4v6h5V10"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.3L12 17.1l-5.7 3.1 1.2-6.3-4.7-4.4 6.4-.8z"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/></symbol>
</defs></svg>'''
def ic(n,cls=''): return f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{n}"/></svg>'

_HID=0
def stars(n,cls=''):
    n=round(n*2)/2
    global _HID
    out=''
    for i in range(5):
        if i<int(n): out+='<svg class="st on" aria-hidden="true"><use href="#i-star"/></svg>'
        elif i<n:
            _HID+=1; g=f'hs{_HID}'
            out+=f'<svg class="st half" viewBox="0 0 24 24" aria-hidden="true"><defs><linearGradient id="{g}"><stop offset="50%" stop-color="#F2A900"/><stop offset="50%" stop-color="currentColor"/></linearGradient></defs><path fill="url(#{g})" d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.3L12 17.1l-5.7 3.1 1.2-6.3-4.7-4.4 6.4-.8z"/></svg>'
        else: out+='<svg class="st" aria-hidden="true"><use href="#i-star"/></svg>'
    return f'<span class="stars {cls}" role="img" aria-label="{n:g} out of 5 stars">{out}</span>'

def rel(depth): return '../'*depth
def pagepath(url): return url.strip('/')
def link(url,depth,frag=''):
    p=pagepath(url)
    return rel(depth)+(p+'/' if p else '')+frag

def svc_index(depth):
    return [{'n':esc(s['name']),'c':esc(SHORT[c['url']]),'u':f"{c['slug']}/#{s['slug']}"} for c in CATS for s in c['services']]

def head(page,depth,title,desc,url,ld=None,og_type='website'):
    r=rel(depth); canon=BASE+'/' if url=='/' else BASE+url+('' if url.endswith('/') else '/')
    ld_s=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in (ld or []))
    return f'''<!doctype html>
<html lang="en" data-base="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#14213A">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{BASE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{BASE}/assets/img/og-image.jpg">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml"><link rel="icon" href="{r}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<link rel="preload" href="{r}assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{r}assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
{ld_s}</head>
'''

def header(depth,current):
    r=rel(depth)
    def a(label,url,key):
        cur=' aria-current="page"' if current==key else ''
        return f'<a href="{link(url,depth)}"{cur}>{label}</a>'
    mega=''.join(f'<div class="mg"><a class="mg-h" href="{link(c["url"],depth)}">{ic(ICON[c["url"]])}<span><b>{esc(SHORT[c["url"]])}</b></span></a><ul>'+''.join(f'<li><a href="{link(c["url"],depth,"#"+sv["slug"])}">{esc(sv["name"])}</a></li>' for sv in c['services'])+'</ul></div>' for c in CATS)
    status=f'<span class="status hdr-status" data-status><i></i><span class="t">{C["hoursShort"]}</span></span>'
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
<header class="hdr"><div class="wrap">
<a class="brand" href="{link('/',depth)}" aria-label="{esc(NAME)}, home"><picture><source media="(prefers-color-scheme: dark)" srcset="{r}assets/img/logo-flat-dark.svg"><img src="{r}assets/img/logo-flat.svg" alt="{esc(NAME)}" width="178" height="52"></picture></a>
<nav class="nav" id="nav" aria-label="Main">
{a('Home','/','home')}
<div class="has-mega"><button type="button" aria-expanded="false" aria-controls="mega"{' aria-current="true"' if current=='services' else ''}>Services {ic('chev')}</button>
<div class="mega" id="mega">{mega}<a class="all" href="{link('/services',depth)}"><span><b>See all services</b><small>Browse by category or search the list</small></span>{ic('arrow')}</a></div></div>
{a('PA Inspections','/inspections-emissions','insp')}
{a('About','/about','about')}
{a('Reviews','/reviews','reviews')}
{a('Contact','/contact','contact')}
<a class="nav-x" href="{link('/services',depth)}">All services</a>
<a class="nav-x" href="{link('/sitemap',depth)}"{' aria-current="page"' if current=='sitemap' else ''}>Sitemap</a>
<a class="nav-x" href="{link('/privacy',depth)}">Privacy</a>
<a class="nav-x nav-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a>
<a class="nav-x" href="{MAPS_URL}" target="_blank" rel="noopener">{ic('pin')} {C['street']}, {C['city']}</a>
</nav>
<div class="hdr-actions">{status}
<button class="kbd-btn" type="button" data-open-pal aria-label="Find a service (shortcut: slash)">{ic('search')}<span class="lbl">Find a service</span><kbd>/</kbd></button>
<a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} Call {PH}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Open menu">{ic('menu')}</button>
</div></div></header>
'''

def footer(depth):
    r=rel(depth)
    cl=''.join(f'<li><a href="{link(c["url"],depth)}">{esc(SHORT[c["url"]])}</a></li>' for c in CATS[:3])
    cl2=''.join(f'<li><a href="{link(c["url"],depth)}">{esc(SHORT[c["url"]])}</a></li>' for c in CATS[3:])
    idx=json.dumps(svc_index(depth),ensure_ascii=False)
    return f'''
<footer class="ftr"><div class="wrap"><div class="ftr-grid">
<div><a class="brand" href="{link('/',depth)}" aria-label="{esc(NAME)}, home"><img src="{r}assets/img/logo-flat-dark.svg" alt="{esc(NAME)}" width="192" height="56"></a>
<p style="margin-top:1rem">{C['street']}<br>{C['city']}, {C['region']} {C['zip']}</p>
<p><a href="tel:{TEL}">{PH}</a><br>Mon–Fri 9 AM–6 PM<br>Sat 9 AM–1 PM · Sun closed</p></div>
<div><h2>Services</h2><ul>{cl}</ul></div>
<div><h2>More services</h2><ul>{cl2}</ul></div>
<div><h2>Company</h2><ul><li><a href="{link('/about',depth)}">About</a></li><li><a href="{link('/reviews',depth)}">Reviews</a></li><li><a href="{link('/contact',depth)}">Contact</a></li><li><a href="{link('/services',depth)}">All services</a></li><li><a href="{link('/privacy',depth)}">Privacy</a></li><li><a href="{link('/sitemap',depth)}">Sitemap</a></li></ul></div>
</div><div class="legal"><span>© <span id="yr">2026</span> {esc(NAME)}. Official Pennsylvania inspection station (OIS #{C['ois']}).</span><span>{C['street']}, {C['city']}, {C['region']}</span></div></div></footer>
<a class="to-home" href="{link('/',depth)}" aria-label="Back to home" hidden>{ic('home')}<span>Home</span></a>
<dialog class="pal" id="pal" aria-label="Find a service"><div class="pal-in">{ic('search')}<input type="text" placeholder="Search {NSV} services…" aria-label="Search services" autocomplete="off"><button class="kbd-btn" type="button" onclick="this.closest('dialog').close()" aria-label="Close search">{ic('close')}</button></div><ul class="pal-list"></ul></dialog>
<script>window.__SERVICES={idx};window.__HOURS={json.dumps([[h[0],h[3],h[4]] for h in C['hours']])};document.getElementById('yr').textContent=new Date().getFullYear()</script>
<script src="{r}assets/js/site.js" defer></script>
</body></html>
'''

def cta(depth,title='Need your car looked at?',text=None):
    text=text or f'Call us {C["hoursShort"]}.'
    return f'''<div class="cta rv"><div><h2>{title}</h2><p>{text}</p></div><div class="cta-row" style="margin:0"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a><a class="btn btn-ghost btn-onDark" href="{DIR_URL}" rel="noopener">{ic('pin')} Get directions</a></div></div>'''

def crumbs(items):
    return '<nav aria-label="Breadcrumb"><ol class="crumbs">'+''.join((f'<li><a href="{u}">{esc(t)}</a></li>' if u else f'<li aria-current="page">{esc(t)}</li>') for t,u in items)+'</ol></nav>'
def bc_ld(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":BASE+u} for i,(t,u) in enumerate(items)]}

ADDR_RE=re.compile(re.escape(C['street'])+r'(<br>|,\s)'+re.escape(C['city'])+r',? '+re.escape(C['region'])+' '+C['zip']+'|'+re.escape(C['street'])+', '+re.escape(C['city'])+'|'+re.escape(C['street']))
def _linkify(seg):
    seg=ADDR_RE.sub(lambda m:f'<a class="addr-link" href="{MAPS_URL}" target="_blank" rel="noopener">{m.group(0)}</a>',seg)
    return re.sub(r'(?<![\d-])'+re.escape(PH)+r'(?![\d-])',lambda m:f'<a class="tel-link" href="tel:{TEL}">{PH}</a>',seg)
def _process(body):
    out=[];pos=0;depth_a=0;skip=None
    for m in re.finditer(r'<!--.*?-->|<[^>]+>',body,re.S):
        t=body[pos:m.start()]
        if t: out.append(t if (depth_a or skip) else _linkify(t))
        tag=m.group(0); out.append(tag); pos=m.end()
        x=re.match(r'<(/?)([a-zA-Z0-9]+)',tag)
        if x:
            closing,name=x.group(1)=='/',x.group(2).lower()
            if name=='a': depth_a=max(0,depth_a-1) if closing else depth_a+1
            if name in('script','style','title','svg','dialog','blockquote') and not tag.endswith('/>'): skip=None if closing else name
    t=body[pos:]
    if t: out.append(t if (depth_a or skip) else _linkify(t))
    return ''.join(out)
def postprocess(h):
    """Link the street address (Google Maps) and phone (tel:) in <main> and <footer> only. Review text is left alone."""
    for pat in (r'<main\b.*?</main>',r'<footer class="ftr">.*?</footer>'):
        m=re.search(pat,h,re.S)
        if m: h=h[:m.start()]+_process(m.group(0))+h[m.end():]
    return h

def write(url,content):
    content=postprocess(content)
    p=ROOT/(pagepath(url)) if url!='/' else ROOT
    p.mkdir(parents=True,exist_ok=True); (p/'index.html').write_text(content,encoding='utf-8')

def autolink_phone(t):
    return esc(t).replace(PH,f'<a href="tel:{TEL}">{PH}</a>')

def local_ld():
    days={'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday'}
    spec=[]
    for h in C['hours']:
        if h[3]: spec.append({"@type":"OpeningHoursSpecification","dayOfWeek":days[h[0]],"opens":h[3],"closes":h[4]})
    return {"@context":"https://schema.org","@type":"AutoRepair","name":NAME,"url":BASE+"/","image":BASE+"/assets/img/og-image.jpg","telephone":TEL,
     "foundingDate":str(C['since']),
     "address":{"@type":"PostalAddress","streetAddress":C['street'],"addressLocality":C['city'],"addressRegion":C['region'],"postalCode":C['zip'],"addressCountry":"US"},
     "openingHoursSpecification":spec,"sameAs":[C['yelpUrl']]}

def rating_card():
    return f'''<div class="rate-card"><div class="rc-row"><span class="rc-src">Google</span><span class="rc-num">{GR['rating']:.1f}</span>{stars(GR['rating'])}<span class="rc-n">{GR['count']} reviews</span></div>
<div class="rc-row"><span class="rc-src">Yelp</span><span class="rc-num">{YR['rating']:.1f}</span>{stars(YR['rating'])}<span class="rc-n">{YR['count']} reviews</span></div></div>'''

def pick(name):
    for r in GR['reviews']+YR['reviews']:
        if r['name']==name: return r

def page_home():
    d=0
    title=f"Auto Repair & PA Inspections in Primos, PA | {NAME}"
    desc=f"Neighborhood auto repair in Primos, Delaware County, since 1987. Diagnostics, brakes, exhaust, oil changes and PA inspections. Call {PH}."
    h=head('home',d,title,desc,'/',[local_ld()])+header(d,'home')
    cards=''
    for c in CATS:
        smp=''.join(f'<li>{esc(s["name"])}</li>' for s in c['services'][:3])
        cards+=f'''<a class="card rv" href="{link(c['url'],d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{len(c['services'])} services</span><h3>{esc(SHORT[c['url']])}</h3><p>{esc(c['intro'])}</p><ul class="samples">{smp}</ul><span class="more">Explore {ic('arrow')}</span></a>'''
    mq=''.join(f'<span>{esc(s["name"])}</span>' for c in CATS for s in c['services'])
    q=pick('Paul Taylor'); q2=pick('James Wagner')
    h+=f'''<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Primos · Delaware County, PA</span>
<h1>Your neighborhood mechanic <span class="hl">since {C['since']}.</span></h1>
<p class="lede">Honest diagnostics, fair prices, and pick-up and delivery for local customers. Official Pennsylvania inspection station.</p>
<div class="cta-row"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a><a class="btn btn-ghost btn-onDark" href="{DIR_URL}" rel="noopener">{ic('pin')} Get directions</a></div>
</div>
<div class="hero-card"><span class="eyebrow" style="color:var(--teal)">What customers say</span>
<p class="hc-quote">“{esc(q['text'])}”</p><p class="byline" style="margin-top:.4rem">{esc(q['name'])} · Google review</p>
{rating_card()}
<a class="more" href="{link('/reviews',d)}">Read reviews {ic('arrow')}</a>
<span class="chip c2">{ic('shield')} Official PA inspection station · OIS #{C['ois']}</span>
<span class="chip c1">{ic('pin')} {C['street']}, {C['city']}</span></div>
</div></section>
<div class="wrap"><div class="strip rv">
<div><b>{YRS}+ years in Delaware County.</b><p>Serving Clifton Heights and Primos since {C['since']}.</p></div>
<div><b>Honest diagnostics.</b><p>We find the problem and tell you what it takes to fix it. No unneeded work.</p></div>
<div><b>Pick-up and delivery.</b><p>We can collect your car and bring it back when it's done.</p></div></div></div>
<section><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">What we do</span><h2>Repairs, maintenance and inspections.</h2></div><p>One shop on Secane Avenue for the work most cars need.</p></div>
<div class="bento">
<a class="card tall w3 rv" href="{link('/diagnostics-electrical',d)}"><span class="ico">{ic('bolt')}</span><h3>Diagnostics and electrical repair</h3><p>Complete computer diagnostics and troubleshooting for electrical problems.</p><span class="more">Diagnostics &amp; electrical {ic('arrow')}</span></a>
<a class="card tall w3 rv" href="{link('/inspections-emissions',d)}"><span class="ico">{ic('shield')}</span><h3>Pennsylvania state inspection and emissions testing</h3><p>Official inspection station, OIS #{C['ois']}. Cars, trailers and medium trucks.</p><span class="more">PA inspections {ic('arrow')}</span></a>
<a class="card w3 rv" href="{link('/brakes-steering-suspension',d)}"><span class="ico">{ic('disc')}</span><h3>Brakes, suspension and alignment</h3><p>Brakes, rotors, ball joints, steering, suspension and front end alignment.</p><span class="more">Brakes &amp; suspension {ic('arrow')}</span></a>
<a class="card w3 rv" href="{link('/maintenance',d)}"><span class="ico">{ic('drop')}</span><h3>Oil changes with AMSOIL</h3><p>Authorized AMSOIL retailer and installer. A/C and cooling systems too.</p><span class="more">Maintenance &amp; cooling {ic('arrow')}</span></a>
</div></div></section>
<div class="marquee"><div class="marquee-track" aria-hidden="true">{mq}{mq}</div></div>
<section><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Services</span><h2>{NUMW[len(CATS)]} categories. {NSV} services.</h2></div><p>Find your job by category, or press <b>/</b> to search the full list.</p></div>
<div class="grid3">{cards}</div>
<p style="margin-top:2rem" class="rv"><a class="btn btn-ghost" href="{link('/services',d)}">Browse all services {ic('arrow')}</a></p></div></section>
<section class="band"><div class="wrap split">
<div class="rv"><span class="eyebrow" style="color:#F0A79F">PA inspections</span><h2>Pennsylvania inspections, done here.</h2>
<p>We're an official Pennsylvania inspection station (OIS #{C['ois']}). We inspect cars, trailers and medium trucks, and do OBD and visual emissions testing. Call to confirm we can inspect your vehicle type.</p>
<p><a class="btn btn-call" href="{link('/inspections-emissions',d)}">Inspections &amp; emissions {ic('arrow')}</a></p></div>
<div class="glass rv"><div class="big">OIS #{C['ois']}</div><p style="margin:.4rem 0 0">Official Pennsylvania inspection station</p>
<ul class="ticks"><li>{ic('check')}<span>Cars, trailers and medium trucks</span></li><li>{ic('check')}<span>OBD and visual emissions testing</span></li><li>{ic('check')}<span>Pre-purchase inspections before you buy</span></li></ul></div></div></section>
<section><div class="wrap split">
<blockquote class="quote-card rv"><p class="quote">{esc(q2['text'].split('. Also')[0])}…</p><p class="byline">{esc(q2['name'])}, Google review. <a href="{link('/reviews',d)}">Read all reviews</a></p></blockquote>
<div class="card rv"><span class="ico">{ic('clock')}</span><h3>Visit the shop</h3><p>{ADDR}<br>Mon–Fri 9 AM–6 PM · Sat 9 AM–1 PM · Sun closed</p><p style="margin-top:.8rem"><a class="btn btn-ghost btn-sm" href="{link('/contact',d)}">Hours &amp; map {ic('arrow')}</a></p></div></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d)}</div></section>
</main>'''+footer(d)
    write('/',h)

def page_services():
    d=1; url='/services'
    title=f'Auto Repair Services in Primos, PA | {NAME}'
    desc=f'Diagnostics, check engine lights, electrical, brakes, alignment, engine, drivetrain, exhaust, oil changes, A/C, tires, body work, rust repair, glass, tinting and PA inspections in Primos. Call {PH}.'
    h=head('services',d,title,desc,url,[bc_ld([('Home','/'),('Services','/services')])])+header(d,'services')
    cards=''
    for c in CATS:
        lis=''.join(f'<li><a href="{link(c["url"],d,"#"+s["slug"])}">{esc(s["name"])}</a></li>' for s in c['services'])
        cards+=f'''<div class="card hub-card rv"><a class="card-top" href="{link(c['url'],d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{len(c['services'])} services</span><h3>{esc(SHORT[c['url']])}</h3><p>{esc(c['intro'])}</p></a>
<details><summary>Show the list {ic('chev')}</summary><ul>{lis}</ul></details></div>'''
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Services',None)])}
<span class="eyebrow">Services</span><h1>Repairs, maintenance and inspections.</h1>
<p class="lede">From check engine lights and brake jobs to oil changes and Pennsylvania inspections, we handle the work most cars need at one Secane Avenue shop. Don't see your repair? Call and ask.</p>
<div class="finder"><label class="vh" for="finder-in">Search services</label>{ic('search')}<input id="finder-in" type="search" placeholder="Try “brakes”, “oil change”, “inspection”…" autocomplete="off"><div id="finder-out" class="finder-out" aria-live="polite"></div></div></div></div>
<section style="padding-top:clamp(32px,5vw,56px)"><div class="wrap"><h2 class="vh">Service categories</h2><div class="grid3">{cards}</div>
<p class="note rv" style="margin-top:2rem">This list shows some of the services we offer. Not sure if we cover your repair? Call us {C['hoursShort']}.</p>
<div style="margin-top:2rem">{cta(d)}</div></div></section></main>'''+footer(d)
    write(url,h)

def faq_html(s):
    out=[]
    for f in s['faqs']:
        safety=' safety' if SAFE.search(f['a']) else ''
        out.append(f'<details name="faq-{s["slug"]}"><summary>{esc(f["q"])}{ic("chev")}</summary><div class="ans{safety}">{autolink_phone(f["a"])}</div></details>')
    return '<div class="acc">'+''.join(out)+'</div>'

def page_category(c):
    d=1; url=c['url']; sh=SHORT[url]
    faqs_all=[f for s in c['services'] for f in s['faqs']]
    ld=[bc_ld([('Home','/'),('Services','/services'),(sh,url)])]
    if faqs_all: ld.insert(0,{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in faqs_all]})
    h=head('cat',d,c['title'],c['meta'],url,ld)+header(d,'insp' if url=='/inspections-emissions' else 'services')
    rail=''.join(f'<li><a href="#{s["slug"]}">{esc(s["name"])}</a></li>' for s in c['services'])
    chips=''.join(f'<a href="#{s["slug"]}">{esc(s["name"])}</a>' for s in c['services'])
    extra=''
    if url=='/inspections-emissions':
        extra=f'''<div class="callout rv" style="margin-bottom:2rem">{ic('shield')}<div><p><b>Official Pennsylvania inspection station (OIS #{C['ois']}).</b> Cars, trailers and medium trucks. OBD and visual emissions testing. Call to confirm we can inspect your vehicle type.</p><p class="note" style="margin-top:.5rem">Bring your current registration and proof of insurance. Call <a href="tel:{TEL}">{PH}</a> to book.</p></div></div>'''
    body=''
    for s in c['services']:
        faqs=f'<h3 class="q">Questions about {esc(s["name"])}</h3>'+faq_html(s) if s['faqs'] else ''
        im=IMG.get(s['name']); fig=''
        if im:
            b=f'{"../"*d}assets/img/svc/{im["file"]}'
            fig=f'<figure class="svc-img"><img src="{b}-1168.webp" srcset="{b}-640.webp 640w, {b}-1168.webp 1168w" sizes="(max-width:700px) 92vw, 560px" width="1168" height="880" loading="lazy" decoding="async" alt="{esc(im["alt"])}"></figure>'
        body+=f'<article class="svc rv" id="{s["slug"]}"><h2>{esc(s["name"])}</h2><p>{esc(s["desc"])}</p>{fig}{faqs}</article>'
    others=''.join(f'<a href="{link(o["url"],d)}">{ic(ICON[o["url"]])}{esc(SHORT[o["url"]])}</a>' for o in CATS if o is not c)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Services',link('/services',d)),(sh,None)])}
<span class="eyebrow">{len(c['services'])} services</span><h1>{esc(sh)}</h1><p class="lede">{esc(c['intro'])}</p>
<div class="meta-row"><span class="pill">{ic('pin')} {C['street']}, {C['city']}</span><span class="pill">{ic('clock')} {C['hoursShort']}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} Call {PH}</a></div></div></div>
<nav class="chips" data-spy aria-label="Services in this category">{chips}</nav>
<div class="wrap cat-layout"><aside class="rail" data-spy><h2>In this category</h2><ol>{rail}</ol><a class="btn btn-call btn-sm call" href="tel:{TEL}">{ic('phone')} Call {PH}</a></aside>
<div>{extra}{body}</div></div>
<section><div class="wrap">{cta(d,f'Questions about {sh.lower()}?',f'Call us {C["hoursShort"]}. We will tell you what we can do.')}
<h2 style="font-size:1.4rem;margin:3rem 0 1rem">Other services</h2><div class="others">{others}</div></div></section></main>'''+footer(d)
    write(url,h)

def page_about():
    d=1; url='/about'
    t=f'About {NAME} | Neighborhood Shop in Primos Since {C["since"]}'
    desc=f'{NAME} has served Clifton Heights, Primos and Delaware County since {C["since"]}. Honest diagnostics, fair prices, pick-up and delivery.'
    h=head('about',d,t,desc,url,[bc_ld([('Home','/'),('About','/about')])])+header(d,'about')
    lab='<small>Photo coming</small>' if C['showPhotoComingLabel'] else ''
    slots=''.join(f'<div class="photo-slot" data-slot="{n}" role="img" aria-label="Placeholder for photo: {n}">{ic("camera")}{lab}</div>' for n in ['shop exterior','the owner','the team','the bays'])
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('About',None)])}<span class="eyebrow">About</span><h1>A neighborhood shop since {C['since']}.</h1></div></div>
<section><div class="wrap split"><div class="prose rv"><p>Scally's Auto Repair has fixed cars for Clifton Heights and the surrounding neighborhoods since {C['since']}. We've since moved a few minutes away to a bigger, upgraded shop at {ADDR}.</p>
<p>The move didn't change how we work. We find the problem, explain it in plain terms, and fix what needs fixing. We don't sell you repairs you don't need.</p>
<p>Many customers have trusted us with their cars for years, and some families for decades. We still offer the pick-up and delivery service our customers count on.</p>
<p><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call {PH}</a></p></div>
<div class="grid3" style="grid-template-columns:1fr">
<div class="card rv"><span class="ico">{ic('info')}</span><h2 style="font-size:1.25rem">Straight answers</h2><p>We explain what's wrong and what it takes to fix it.</p></div>
<div class="card rv"><span class="ico">{ic('check')}</span><h2 style="font-size:1.25rem">Fair pricing</h2><p>Customers say it's a big reason they keep coming back.</p></div>
<div class="card rv"><span class="ico">{ic('truck')}</span><h2 style="font-size:1.25rem">Pick-up and delivery</h2><p>We can collect your car and return it when the work is done.</p></div>
<div class="card rv"><span class="ico">{ic('drop')}</span><h2 style="font-size:1.25rem">Authorized AMSOIL installer</h2><p>Oil changes with AMSOIL products.</p></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="slots rv">{slots}</div></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d,'Stop by or call.',f'{C["street"]}, {C["city"]} · {C["hoursShort"]}')}</div></section></main>'''+footer(d)
    write(url,h)

def rv_card(r,src):
    has=bool(r['text'].strip())
    body=''.join(f'<p>{esc(p)}</p>' for p in r['text'].split('\n') if p.strip()) if has else '<p class="rv-empty">Rating only, no written review.</p>'
    tags=''.join(f'<span class="rv-tag">{esc(t)}</span>' for t in r.get('tags',[]))
    loc=f' · {esc(r["location"])}' if r.get('location') else ''
    init=esc(r['name'].strip()[:1].upper())
    long=' rv-long' if len(r['text'])>420 else ''
    return f'''<article class="rv-card{long}" data-src="{src}" data-text="{1 if has else 0}" data-stars="{r['stars']}">
<header><span class="rv-av" aria-hidden="true">{init}</span><div><b>{esc(r['name'])}</b><small>{src.title()}{loc} · {esc(r['date'])}</small></div></header>
{stars(r['stars'],'sm')}{('<div class="rv-tags">'+tags+'</div>') if tags else ''}
<blockquote class="rv-text">{body}</blockquote></article>'''

def page_reviews():
    d=1; url='/reviews'
    t=f'Customer Reviews | {NAME} in Primos, PA'
    desc=f'Google and Yelp reviews of {NAME}: {GR["rating"]:.1f} stars on Google ({GR["count"]} reviews) and {YR["rating"]:.1f} on Yelp ({YR["count"]} reviews).'
    h=head('reviews',d,t,desc,url,[bc_ld([('Home','/'),('Reviews','/reviews')])])+header(d,'reviews')
    g=GR['reviews']
    y=YR['reviews']
    written=sum(1 for r in g+y if r['text'].strip())
    cards=''.join(rv_card(r,'yelp') for r in y)+''.join(rv_card(r,'google') for r in g)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Reviews',None)])}<span class="eyebrow">Reviews</span><h1>What our customers say</h1>
<p class="lede">Reviews from Google and Yelp, posted as written.</p></div></div>
<section style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
<div class="rv-sum rv">
<div class="rs-box"><span class="rs-src">Google</span><div class="rs-big">{GR['rating']:.1f}</div>{stars(GR['rating'])}<p>{GR['count']} reviews</p><a class="btn btn-ghost btn-sm" href="{C['googleReviewUrl']}" target="_blank" rel="noopener">See on Google {ic('arrow')}</a></div>
<div class="rs-box"><span class="rs-src">Yelp</span><div class="rs-big">{YR['rating']:.1f}</div>{stars(YR['rating'])}<p>{YR['count']} reviews</p><p class="note">All {YR['count']} Yelp reviews are 5 stars.</p><a class="btn btn-ghost btn-sm" href="{C['yelpUrl']}" target="_blank" rel="noopener">See on Yelp {ic('arrow')}</a></div>
</div>
<div class="rv-filter" role="group" aria-label="Filter reviews">
<button type="button" data-f="all" aria-pressed="true">All <span>{len(g)+len(y)}</span></button>
<button type="button" data-f="text" aria-pressed="false">Written <span>{written}</span></button>
<button type="button" data-f="google" aria-pressed="false">Google <span>{len(g)}</span></button>
<button type="button" data-f="yelp" aria-pressed="false">Yelp <span>{len(y)}</span></button></div>
<div class="rv-grid" id="rv-grid">{cards}</div>
<p class="note" style="margin-top:2rem">Reviews are copied word for word from Google and Yelp as they appeared on {RV['captured']}. Google dates are shown the way Google displayed them that day. Reviews belong to their authors.</p>
<p style="margin-top:1rem"><a class="btn btn-call" href="{C['googleReviewUrl']}" target="_blank" rel="noopener">{ic('star')} Leave us a Google review</a></p></div></section>
<section style="padding-top:0"><div class="wrap">{cta(d)}</div></section></main>
<script>(function(){{var b=document.querySelectorAll('.rv-filter button'),c=document.querySelectorAll('.rv-card');b.forEach(function(x){{x.addEventListener('click',function(){{var f=x.dataset.f;b.forEach(function(y){{y.setAttribute('aria-pressed',y===x)}});c.forEach(function(k){{k.hidden=!(f==='all'||(f==='text'&&k.dataset.text==='1')||k.dataset.src===f)}})}})}})}})()</script>'''+footer(d)
    write(url,h)

def page_contact():
    d=1; url='/contact'
    t=f'Contact {NAME} | {ADDR}'
    desc=f'Call {PH} or stop by {ADDR}. Open Mon–Fri 9 AM–6 PM, Sat 9 AM–1 PM.'
    h=head('contact',d,t,desc,url,[bc_ld([('Home','/'),('Contact','/contact')])])+header(d,'contact')
    rows=''.join(f'<tr data-d="{x[0]}"><th scope="row">{x[1]}</th><td>{x[2]}</td></tr>' for x in C['hours'])
    emb="https://www.google.com/maps?q="+quote_plus(C['mapsQuery'])+"&output=embed"
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Contact',None)])}<span class="eyebrow">Contact</span><h1>Call or stop by.</h1></div></div>
<section><div class="wrap contact-grid"><div class="rv">
<a class="big-phone" href="tel:{TEL}">{PH}</a>
<dl class="dl"><div><dt>Address</dt><dd>{C['street']}<br>{C['city']}, {C['region']} {C['zip']}</dd></div>
<div><dt>Pick-up &amp; delivery</dt><dd>Available for local customers. Call to arrange.</dd></div></dl>
<div class="cta-row" style="margin:0 0 2rem"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call the shop</a><a class="btn btn-ghost" href="{DIR_URL}" rel="noopener">{ic('pin')} Get directions</a></div>
<h2 style="font-size:1.4rem">Hours</h2><table class="hours"><caption class="vh">Opening hours</caption><tbody>{rows}</tbody></table></div>
<div class="mapbox rv" data-map="{esc(emb)}" data-title="Map showing {esc(NAME)} at {esc(ADDR)}"><div class="gridbg"></div><div class="inner">{ic('pin')}<p><b>{C['street']}, {C['city']}</b></p><button class="btn btn-ghost" type="button">Load the map</button><p class="note" style="margin-top:.8rem">Loading the map connects to Google.</p></div></div></div></section></main>'''+footer(d)
    write(url,h)

def page_privacy():
    d=1; url='/privacy'
    h=head('privacy',d,f'Privacy | {NAME}','How this website handles your information.',url,None)+header(d,'privacy')
    h=h.replace('<meta name="description"','<meta name="robots" content="noindex,follow"><meta name="description"',1)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Privacy',None)])}<h1>Privacy</h1></div></div>
<section><div class="wrap prose"><p>This website does not use cookies, analytics, advertising trackers, contact forms, or accounts. We do not collect your name, email, or phone number through the site.</p>
<p>The map on the Contact page loads only when you press “Load the map.” When you load it, Google receives your request under Google's own privacy terms. Links to Google and Yelp reviews open those sites under their own terms.</p>
<p>If you call the shop at <a href="tel:{TEL}">{PH}</a>, the information you give us stays with the shop and is used to help with your vehicle.</p>
<p class="note">Questions? Call us {C['hoursShort']}.</p></div></section></main>'''+footer(d)
    write(url,h)

def page_sitemap():
    d=1; url='/sitemap'
    h=head('sitemap',d,f'Sitemap | {NAME}',f'Every page and service on the {NAME} website.',url,None)+header(d,'sitemap')
    main_pages=[('Home','/'),('All services','/services'),('About','/about'),('Reviews','/reviews'),('Contact','/contact'),('Privacy','/privacy')]
    mp=''.join(f'<li><a href="{link(u,d)}">{lbl}</a></li>' for lbl,u in main_pages)+f'<li><a href="{rel(d)}sitemap.xml">sitemap.xml (for search engines)</a></li>'
    cats=''.join(f'<div class="sm-col"><h2><a href="{link(c["url"],d)}">{esc(SHORT[c["url"]])}</a></h2><ul>'+''.join(f'<li><a href="{link(c["url"],d,"#"+sv["slug"])}">{esc(sv["name"])}</a></li>' for sv in c['services'])+'</ul></div>' for c in CATS)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Sitemap',None)])}<h1>Sitemap</h1><p class="lede">Every page and service on this site.</p></div></div>
<section><div class="wrap"><div class="sitemap"><div class="sm-col"><h2>Pages</h2><ul>{mp}</ul></div>{cats}</div></div></section></main>'''+footer(d)
    write(url,h)

def page_404():
    d=0
    h=head('404',d,f'Page not found | {NAME}','That page does not exist.','/404.html',None)
    h=h.replace('<meta name="description"','<meta name="robots" content="noindex"><meta name="description"',1)
    h=h.replace('<head>',f'<head><base href="{C.get("basePath","/")}">',1)
    h+=header(d,'')+f'''<main id="main"><div class="wrap err"><div><div class="n" aria-hidden="true">404</div><h1 style="font-size:clamp(1.8rem,3vw,2.6rem)">This page took a wrong turn.</h1><p class="lede" style="margin-inline:auto">Try the services list, or call us at <a href="tel:{TEL}">{PH}</a>.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-call" href="./">Back to home</a><a class="btn btn-ghost" href="services/">Browse services</a></div></div></div></main>'''+footer(d)
    (ROOT/'404.html').write_text(postprocess(h),encoding='utf-8')

def misc():
    urls=['/','/services','/about','/reviews','/contact','/sitemap']+[c['url'] for c in CATS]
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{u}{"" if u=="/" else "/"}</loc></url>\n' for u in urls)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sm)
    bots=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-SearchBot','Claude-User','PerplexityBot','Google-Extended','Applebot-Extended']
    rb='User-agent: *\nAllow: /\n\n'+''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {BASE}/sitemap.xml\n'
    (ROOT/'robots.txt').write_text(rb); (ROOT/'.nojekyll').write_text('')

if __name__=='__main__':
    page_home(); page_services()
    for c in CATS: page_category(c)
    page_about(); page_reviews(); page_contact(); page_privacy(); page_sitemap(); page_404(); misc()
    print('built', 8+len(CATS))
