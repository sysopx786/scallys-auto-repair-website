#!/usr/bin/env python3
"""Static site generator for Scally's Auto Repair. Run: python3 src/build.py  (from site root)

Sources (edit these, never the generated HTML):
  src/site.config.json   business facts, hours, base URL (one source of truth)
  src/services.json      8 categories, 67 services (EN + ES), stable ids, page assignment
  src/pages/*.json       detailed service pages (EN + ES), one file per page
  src/images.json        service photos keyed by service id
  src/reviews.json       Google and Yelp reviews (English only)
"""
import json, re, html, hashlib, datetime
from pathlib import Path
from urllib.parse import quote_plus
ROOT=Path(__file__).resolve().parent.parent
C=json.load(open(ROOT/'src/site.config.json'))
CATS=json.load(open(ROOT/'src/services.json'))
RV=json.load(open(ROOT/'src/reviews.json'))
IMG=json.load(open(ROOT/'src/images.json'))
PAGES=[json.load(open(f)) for f in sorted((ROOT/'src/pages').glob('*.json'))]
NAME=C['name']; PH=C['phoneDisplay']; TEL=C['phoneTel']
BASE=C['baseUrl'].rstrip('/'); YRS=2026-C['since']
BIZ=BASE+'/#business'
assert 'REPLACE' not in BASE, 'Set baseUrl in src/site.config.json'
esc=lambda s:html.escape(s,quote=True)
LANGS=('en','es')
def L(x,lang='en'):
    """Pick one language from an {en,es} pair; plain strings pass through."""
    return x[lang] if isinstance(x,dict) else x
def slug(s): return re.sub(r'(^-|-$)','',re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and')))

# ---------- catalog ----------
SVC={}; CAT_BY_ID={}
for c in CATS:
    c['slug']=c['url'].strip('/')
    CAT_BY_ID[c['id']]=c
    for s in c['services']:
        s['slug']=s['id']; s['cat']=c
        SVC[s['id']]=s
PAGE_BY_ID={p['id']:p for p in PAGES}
for p in PAGES:
    p['cat']=CAT_BY_ID[p['category']]
    for sid in p['covers']:
        assert SVC[sid]['page']==p['id'], f"{sid} is covered by {p['id']} but services.json says {SVC[sid]['page']}"
ICON={c['url']:c['icon'] for c in CATS}
NSV=len(SVC)
NUMW={5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine'}
SAFE=re.compile(r'\b(safe|unsafe|dangerous|pull over|stop driving|911|fire|fumes|overheat|segur|peligr|deténgase|incendio)',re.I)
ADDR=f"{C['street']}, {C['city']}, {C['region']} {C['zip']}"
MAPS_URL="https://www.google.com/maps/search/?api=1&amp;query="+quote_plus(C['mapsQuery'])
DIR_URL="https://www.google.com/maps/dir/?api=1&amp;destination="+quote_plus(C['mapsQuery'])
GR,YR=RV['google'],RV['yelp']
TOTAL=GR['count']+YR['count']

UI={
 'en':dict(home='Home',services='Services',insp='PA Inspections',about='About',reviews='Reviews',contact='Contact',all='All services',
   see_all='See all services',see_all_sub='Browse by category or search the list',sitemap='Sitemap',privacy='Privacy',call='Call',
   find='Find a service',find_aria='Find a service (shortcut: slash)',search_ph='Search {n} services…',search_aria='Search services',
   close_search='Close search',skip='Skip to content',menu='Open menu',home_aria='home',back_home='Back to home',
   ftr_services='Services',ftr_more='More services',company='Company',hours_ftr='Mon–Fri 9 AM–6 PM<br>Sat 9 AM–1 PM · Sun closed',
   legal='Official Pennsylvania inspection station (OIS #{ois}).',cta_t='Need your car looked at?',cta_x='Call us {hs}.',
   directions='Get directions',n_services='{n} services',in_cat='In this category',other='Other services',
   faq='Frequently asked questions',sources='Sources',related='Related services',on_page='On this page',details='Full details',
   covers='This page covers',hs=C['hoursShort'],other_lang='Español',other_short='ES',other_aria='Ver esta página en español',
   cat_q='Questions about {x}?',cat_x='Call us {hs}. We will tell you what we can do.',
   req_t='Request service at {name}',req_x='Call {ph} to set up a time or ask a question. {hs}.',
   moved='Transmission, clutch, differential and axle work now has its own category:',
   svc_note='This list shows some of the services we offer. Not sure if we cover your repair? Call us {hs}.',
   show_list='Show the list',explore='Explore',en_only=''),
 'es':dict(home='Inicio',services='Servicios',insp='Inspecciones PA',about='Nosotros',reviews='Reseñas',contact='Contacto',all='Todos los servicios',
   see_all='Ver todos los servicios',see_all_sub='Busque por categoría o en la lista',sitemap='Mapa del sitio',privacy='Privacidad',call='Llame al',
   find='Buscar un servicio',find_aria='Buscar un servicio (atajo: barra /)',search_ph='Buscar entre {n} servicios…',search_aria='Buscar servicios',
   close_search='Cerrar búsqueda',skip='Ir al contenido',menu='Abrir menú',home_aria='inicio',back_home='Volver al inicio',
   ftr_services='Servicios',ftr_more='Más servicios',company='Empresa',hours_ftr='Lun–Vie 9 AM–6 PM<br>Sáb 9 AM–1 PM · Dom cerrado',
   legal='Estación oficial de inspección de Pensilvania (OIS #{ois}).',cta_t='¿Necesita que revisemos su auto?',cta_x='Llámenos {hs}.',
   directions='Cómo llegar',n_services='{n} servicios',in_cat='En esta categoría',other='Otros servicios',
   faq='Preguntas frecuentes',sources='Fuentes',related='Servicios relacionados',on_page='En esta página',details='Más detalles',
   covers='Esta página incluye',hs=C['hoursShortEs'],other_lang='English',other_short='EN',other_aria='View this page in English',
   cat_q='¿Preguntas sobre {x}?',cat_x='Llámenos {hs}. Le diremos qué podemos hacer.',
   req_t='Solicite servicio en {name}',req_x='Llame al {ph} para hacer una cita o hacer una pregunta. {hs}.',
   moved='Los trabajos de transmisión, clutch, diferencial y ejes ahora tienen su propia categoría:',
   svc_note='Esta lista muestra los servicios que ofrecemos. ¿No sabe si hacemos su reparación? Llámenos {hs}.',
   show_list='Ver la lista',explore='Ver más',en_only=' (en inglés)'),
}
def T(lang,key,**kw):
    s=UI[lang][key]
    return s.format(**kw) if kw else s

def P(lang,url):
    """Path for a page in a language. English lives at the root, Spanish under /es/."""
    if lang=='en': return url
    return '/es' if url=='/' else '/es'+url
def depth_of(url): return 0 if url=='/' else url.strip('/').count('/')+1
def page_url(p): return '/'+p['slug']
def dest(sid,lang):
    """Where a service lives: its detailed page (anchored unless it is the page's lead service) or its category hub."""
    s=SVC[sid]; p=PAGE_BY_ID.get(s['page'])
    if p: return P(lang,page_url(p)), ('' if p['covers'][0]==sid else '#'+sid)
    return P(lang,s['cat']['url']), '#'+sid
def fill(t):
    return t.replace('{name}',NAME).replace('{street}',C['street']).replace('{city}',C['city']).replace('{phone}',PH).replace('{since}',str(C['since']))

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
<symbol id="i-shift" viewBox="0 0 24 24"><circle cx="6" cy="5" r="1.6"/><circle cx="12" cy="5" r="1.6"/><circle cx="18" cy="5" r="1.6"/><path d="M6 7v12M12 7v12M18 7v5H6"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></symbol>
</defs></svg>'''
def ic(n,cls=''): return f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{n}"/></svg>'

def rel(depth): return '../'*depth
def pagepath(url): return url.strip('/')
def link(url,depth,frag=''):
    p=pagepath(url)
    return rel(depth)+(p+'/' if p else '')+frag
def canon_of(url): return BASE+'/' if url=='/' else BASE+url.rstrip('/')+'/'

def svc_index(lang):
    out=[]
    for c in CATS:
        for s in c['services']:
            u,f=dest(s['id'],lang)
            out.append({'n':esc(L(s['name'],lang)),'c':esc(L(c['short'],lang)),'u':(pagepath(u)+'/' if pagepath(u) else '')+f})
    return out

def head(page,depth,title,desc,url,ld=None,og_type='website',lang='en',alt=None):
    """alt: {'en': url, 'es': url} when the page exists in both languages (adds reciprocal hreflang)."""
    r=rel(depth); canon=canon_of(url)
    ld_s=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>\n' for x in (ld or []))
    hl=''
    if alt:
        hl=''.join(f'<link rel="alternate" hreflang="{k}" href="{canon_of(v)}">' for k,v in alt.items())+f'<link rel="alternate" hreflang="x-default" href="{canon_of(alt["en"])}">\n'
    loc='es_US' if lang=='es' else 'en_US'
    return f'''<!doctype html>
<html lang="{lang}" data-base="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{hl}<meta name="theme-color" content="#14213A">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{esc(NAME)}"><meta property="og:locale" content="{loc}">
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

def header(depth,current,lang='en',alt=None):
    """alt: the URL of this page in the other language. Without one, the switch goes to the other language's services hub."""
    r=rel(depth); u=UI[lang]; other='es' if lang=='en' else 'en'
    eo=u['en_only']
    def a(label,url,key,en_only=False):
        cur=' aria-current="page"' if current==key else ''
        x=f' hreflang="en"' if (en_only and lang=='es') else ''
        return f'<a href="{link(url,depth)}"{cur}{x}>{label}</a>'
    mega=''.join(f'<a href="{link(P(lang,c["url"]),depth)}">{ic(ICON[c["url"]])}<span><b>{esc(L(c["short"],lang))}</b><small>{T(lang,"n_services",n=len(c["services"]))}</small></span></a>' for c in CATS)
    status=f'<span class="status hdr-status" data-status><i></i><span class="t">{u["hs"]}</span></span>'
    sw=alt or P(other,'/services')
    insp=P(lang,'/inspections-emissions')
    return f'''<body>
<a class="skip" href="#main">{u['skip']}</a>
{SPRITE}
<header class="hdr"><div class="wrap">
<a class="brand" href="{link('/',depth)}" aria-label="{esc(NAME)}, {u['home_aria']}"><picture><source media="(prefers-color-scheme: dark)" srcset="{r}assets/img/logo-flat-dark.svg"><img src="{r}assets/img/logo-flat.svg" alt="{esc(NAME)}" width="178" height="52"></picture></a>
<nav class="nav" id="nav" aria-label="{'Principal' if lang=='es' else 'Main'}">
{a(u['home'],'/','home',True)}
<div class="has-mega"><button type="button" aria-expanded="false" aria-controls="mega"{' aria-current="true"' if current=='services' else ''}>{u['services']} {ic('chev')}</button>
<div class="mega" id="mega">{mega}<a class="all" href="{link(P(lang,'/services'),depth)}"><span><b>{u['see_all']}</b><small>{u['see_all_sub']}</small></span>{ic('arrow')}</a></div></div>
{a(u['insp'],insp,'insp')}
{a(u['about'],'/about','about',True)}
{a(u['reviews'],'/reviews','reviews',True)}
{a(u['contact'],'/contact','contact',True)}
<a class="nav-x" href="{link(P(lang,'/services'),depth)}">{u['all']}</a>
<a class="nav-x" href="{link('/sitemap',depth)}"{' aria-current="page"' if current=='sitemap' else ''}>{u['sitemap']}{eo}</a>
<a class="nav-x" href="{link('/privacy',depth)}">{u['privacy']}{eo}</a>
<a class="nav-x nav-call" href="tel:{TEL}">{ic('phone')} {u['call']} {PH}</a>
<a class="nav-x" href="{MAPS_URL}" target="_blank" rel="noopener">{ic('pin')} {C['street']}, {C['city']}</a>
</nav>
<div class="hdr-actions">{status}
<a class="lang-sw" href="{link(sw,depth)}" hreflang="{other}" lang="{other}" aria-label="{u['other_aria']}">{ic('globe')}<span>{u['other_short']}</span></a>
<button class="kbd-btn" type="button" data-open-pal aria-label="{u['find_aria']}">{ic('search')}<span class="lbl">{u['find']}</span><kbd>/</kbd></button>
<a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} <span class="cl">{u['call']}</span> {PH}</a>
<button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="{u['menu']}">{ic('menu')}</button>
</div></div></header>
'''

def footer(depth,lang='en'):
    r=rel(depth); u=UI[lang]; eo=u['en_only']
    cl=''.join(f'<li><a href="{link(P(lang,c["url"]),depth)}">{esc(L(c["short"],lang))}</a></li>' for c in CATS[:4])
    cl2=''.join(f'<li><a href="{link(P(lang,c["url"]),depth)}">{esc(L(c["short"],lang))}</a></li>' for c in CATS[4:])
    idx=json.dumps(svc_index(lang),ensure_ascii=False)
    return f'''
<footer class="ftr"><div class="wrap"><div class="ftr-grid">
<div><a class="brand" href="{link('/',depth)}" aria-label="{esc(NAME)}, {u['home_aria']}"><img src="{r}assets/img/logo-flat-dark.svg" alt="{esc(NAME)}" width="192" height="56"></a>
<p style="margin-top:1rem">{C['street']}<br>{C['city']}, {C['region']} {C['zip']}</p>
<p><a href="tel:{TEL}">{PH}</a><br>{u['hours_ftr']}</p></div>
<div><h2>{u['ftr_services']}</h2><ul>{cl}</ul></div>
<div><h2>{u['ftr_more']}</h2><ul>{cl2}</ul></div>
<div><h2>{u['company']}</h2><ul><li><a href="{link('/about',depth)}">{u['about']}{eo}</a></li><li><a href="{link('/reviews',depth)}">{u['reviews']}{eo}</a></li><li><a href="{link('/contact',depth)}">{u['contact']}{eo}</a></li><li><a href="{link(P(lang,'/services'),depth)}">{u['all']}</a></li><li><a href="{link('/privacy',depth)}">{u['privacy']}{eo}</a></li><li><a href="{link('/sitemap',depth)}">{u['sitemap']}{eo}</a></li></ul></div>
</div><div class="legal"><span>© <span id="yr">2026</span> {esc(NAME)}. {T(lang,'legal',ois=C['ois'])}</span><span>{C['street']}, {C['city']}, {C['region']}</span></div></div></footer>
<a class="to-home" href="{link('/',depth)}" aria-label="{u['back_home']}" hidden>{ic('home')}<span>{u['home']}</span></a>
<dialog class="pal" id="pal" aria-label="{u['find']}"><div class="pal-in">{ic('search')}<input type="text" placeholder="{T(lang,'search_ph',n=NSV)}" aria-label="{u['search_aria']}" autocomplete="off"><button class="kbd-btn" type="button" onclick="this.closest('dialog').close()" aria-label="{u['close_search']}">{ic('close')}</button></div><ul class="pal-list"></ul></dialog>
<script>window.__SERVICES={idx};window.__HOURS={json.dumps([[h[0],h[3],h[4]] for h in C['hours']])};document.getElementById('yr').textContent=new Date().getFullYear()</script>
<script src="{r}assets/js/site.js" defer></script>
</body></html>
'''

def cta(depth,title=None,text=None,lang='en'):
    title=title or T(lang,'cta_t')
    text=text or T(lang,'cta_x',hs=UI[lang]['hs'])
    return f'''<div class="cta rv"><div><h2>{title}</h2><p>{text}</p></div><div class="cta-row" style="margin:0"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} {UI[lang]['call']} {PH}</a><a class="btn btn-ghost btn-onDark" href="{DIR_URL}" rel="noopener">{ic('pin')} {UI[lang]['directions']}</a></div></div>'''

def crumbs(items,lang='en'):
    lbl='Ruta de navegación' if lang=='es' else 'Breadcrumb'
    return f'<nav aria-label="{lbl}"><ol class="crumbs">'+''.join((f'<li><a href="{u}">{esc(t)}</a></li>' if u else f'<li aria-current="page">{esc(t)}</li>') for t,u in items)+'</ol></nav>'
def bc_node(items,url=None):
    n={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":t,"item":canon_of(u)} for i,(t,u) in enumerate(items)]}
    if url: n["@id"]=canon_of(url)+'#breadcrumb'
    return n
def bc_ld(items):
    n=bc_node(items); n["@context"]="https://schema.org"; return n
def graph(*nodes): return {"@context":"https://schema.org","@graph":[n for n in nodes if n]}

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

def business_node(full=False):
    """One AutoRepair entity, same @id on every page. Only verified facts; hours are left out until confirmed."""
    n={"@type":"AutoRepair","@id":BIZ,"name":NAME,"url":BASE+"/","telephone":TEL,
       "address":{"@type":"PostalAddress","streetAddress":C['street'],"addressLocality":C['city'],"addressRegion":C['region'],"postalCode":C['zip'],"addressCountry":"US"}}
    if full:
        n.update({"image":BASE+"/assets/img/og-image.jpg","foundingDate":str(C['since']),"sameAs":[C['yelpUrl']]})
        if C.get('hoursVerified'):
            days={'Mon':'Monday','Tue':'Tuesday','Wed':'Wednesday','Thu':'Thursday','Fri':'Friday','Sat':'Saturday','Sun':'Sunday'}
            n["openingHoursSpecification"]=[{"@type":"OpeningHoursSpecification","dayOfWeek":days[h[0]],"opens":h[3],"closes":h[4]} for h in C['hours'] if h[3]]
    return n
def website_node(): return {"@type":"WebSite","@id":BASE+"/#website","url":BASE+"/","name":NAME,"publisher":{"@id":BIZ}}
def webpage_node(url,title,lang,crumb=True):
    n={"@type":"WebPage","@id":canon_of(url)+'#webpage',"url":canon_of(url),"name":title,"inLanguage":lang,"isPartOf":{"@id":BASE+"/#website"},"about":{"@id":BIZ}}
    if crumb: n["breadcrumb"]={"@id":canon_of(url)+'#breadcrumb'}
    return n
def faq_node(faqs,lang):
    if not faqs: return None
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":L(f['q'],lang),"acceptedAnswer":{"@type":"Answer","text":L(f['a'],lang)}} for f in faqs]}

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
    h=head('home',d,title,desc,'/',[graph(business_node(True),website_node(),webpage_node('/',title,'en',False))])+header(d,'home')
    cards=''
    for c in CATS:
        smp=''.join(f'<li>{esc(L(s["name"]))}</li>' for s in c['services'][:3])
        cards+=f'''<a class="card rv" href="{link(c['url'],d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{len(c['services'])} services</span><h3>{esc(L(c['short']))}</h3><p>{esc(L(c['intro']))}</p><ul class="samples">{smp}</ul><span class="more">Explore {ic('arrow')}</span></a>'''
    mq=''.join(f'<span>{esc(L(s["name"]))}</span>' for c in CATS for s in c['services'])
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

SVC_HUB={
 'en':dict(title=f'Auto Repair Services in Primos, PA | {NAME}',
   desc=f'Diagnostics, electrical, brakes, steering, suspension, engine, transmission, exhaust, oil changes, A/C, tires, body work, glass and PA inspections in Primos. Call {PH}.',
   eyebrow='Services',h1='Repairs, maintenance and inspections.',
   lede="From check engine lights and brake jobs to oil changes and Pennsylvania inspections, we handle the work most cars need at one Secane Avenue shop. Don't see your repair? Call and ask.",
   ph='Try “brakes”, “oil change”, “inspection”…',vh='Service categories',lbl='Search services'),
 'es':dict(title=f'Servicios de mecánica en Primos, PA | {NAME}',
   desc=f'Diagnóstico, eléctrico, frenos, dirección, suspensión, motor, transmisión, escape, aceite, A/C, llantas, carrocería, cristales e inspecciones en Primos. {PH}.',
   eyebrow='Servicios',h1='Reparaciones, mantenimiento e inspecciones.',
   lede='Desde la luz de check engine y los frenos hasta cambios de aceite e inspecciones de Pensilvania, hacemos en nuestro taller de Secane Avenue el trabajo que la mayoría de los autos necesitan. ¿No ve su reparación? Llame y pregunte.',
   ph='Pruebe “frenos”, “aceite”, “inspección”…',vh='Categorías de servicios',lbl='Buscar servicios'),
}
def home_crumb(lang,d):
    """Breadcrumb root: English starts at Home; Spanish starts at the Spanish services hub."""
    return [('Home',link('/',d)),('Services',link('/services',d))] if lang=='en' else [('Servicios',link('/es/services',d))]
def home_crumb_ld(lang):
    return [('Home','/'),('Services','/services')] if lang=='en' else [('Servicios','/es/services')]

def page_services(lang='en'):
    url=P(lang,'/services'); d=depth_of(url); u=UI[lang]; X=SVC_HUB[lang]
    bc=home_crumb_ld(lang)
    h=head('services',d,X['title'],X['desc'],url,[graph(business_node(),website_node(),webpage_node(url,X['title'],lang),bc_node(bc,url))],lang=lang,alt={'en':'/services','es':'/es/services'})+header(d,'services',lang,P('es' if lang=='en' else 'en','/services'))
    cards=''
    for c in CATS:
        lis=''.join(f'<li><a href="{link(*dest(s["id"],lang)[:1],d,dest(s["id"],lang)[1])}">{esc(L(s["name"],lang))}</a></li>' for s in c['services'])
        cards+=f'''<div class="card hub-card rv"><a class="card-top" href="{link(P(lang,c['url']),d)}"><span class="ico">{ic(ICON[c['url']])}</span><span class="meta">{T(lang,'n_services',n=len(c['services']))}</span><h3>{esc(L(c['short'],lang))}</h3><p>{esc(L(c['intro'],lang))}</p></a>
<details><summary>{u['show_list']} {ic('chev')}</summary><ul>{lis}</ul></details></div>'''
    hc=home_crumb(lang,d); cr=hc[:-1]+[(hc[-1][0],None)]
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs(cr,lang)}
<span class="eyebrow">{X['eyebrow']}</span><h1>{X['h1']}</h1>
<p class="lede">{X['lede']}</p>
<div class="finder"><label class="vh" for="finder-in">{X['lbl']}</label>{ic('search')}<input id="finder-in" type="search" placeholder="{X['ph']}" autocomplete="off"><div id="finder-out" class="finder-out" aria-live="polite"></div></div></div></div>
<section style="padding-top:clamp(32px,5vw,56px)"><div class="wrap"><h2 class="vh">{X['vh']}</h2><div class="grid3">{cards}</div>
<p class="note rv" style="margin-top:2rem">{T(lang,'svc_note',hs=u['hs'])}</p>
<div style="margin-top:2rem">{cta(d,lang=lang)}</div></div></section></main>'''+footer(d,lang)
    write(url,h)

def faq_html(faqs,key,lang='en'):
    out=[]
    for f in faqs:
        a=L(f['a'],lang)
        safety=' safety' if SAFE.search(a) else ''
        out.append(f'<details name="faq-{key}"><summary>{esc(L(f["q"],lang))}{ic("chev")}</summary><div class="ans{safety}">{autolink_phone(a)}</div></details>')
    return '<div class="acc">'+''.join(out)+'</div>'

def page_category(c,lang='en'):
    url=P(lang,c['url']); d=depth_of(url); sh=L(c['short'],lang); u=UI[lang]
    faqs_all=[f for s in c['services'] for f in s['faqs']]
    bc=home_crumb_ld(lang)+[(sh,url)]
    ld=[graph(business_node(),website_node(),webpage_node(url,L(c['title'],lang),lang),bc_node(bc,url),faq_node(faqs_all,lang))]
    other='es' if lang=='en' else 'en'
    h=head('cat',d,L(c['title'],lang),L(c['meta'],lang),url,ld,lang=lang,alt={'en':c['url'],'es':'/es'+c['url']})+header(d,'insp' if c['url']=='/inspections-emissions' else 'services',lang,P(other,c['url']))
    rail=''.join(f'<li><a href="#{s["slug"]}">{esc(L(s["name"],lang))}</a></li>' for s in c['services'])
    chips=''.join(f'<a href="#{s["slug"]}">{esc(L(s["name"],lang))}</a>' for s in c['services'])
    extra=''
    if c['url']=='/inspections-emissions':
        extra=(f'''<div class="callout rv" style="margin-bottom:2rem">{ic('shield')}<div><p><b>Official Pennsylvania inspection station (OIS #{C['ois']}).</b> Cars, trailers and medium trucks. OBD and visual emissions testing. Call to confirm we can inspect your vehicle type.</p><p class="note" style="margin-top:.5rem">Bring your current registration and proof of insurance. Call <a href="tel:{TEL}">{PH}</a> to book.</p></div></div>''' if lang=='en' else
               f'''<div class="callout rv" style="margin-bottom:2rem">{ic('shield')}<div><p><b>Estación oficial de inspección de Pensilvania (OIS #{C['ois']}).</b> Autos, remolques y camiones medianos. Pruebas de emisiones OBD y visuales. Llame para confirmar que podemos inspeccionar su tipo de vehículo.</p><p class="note" style="margin-top:.5rem">Traiga su registro vigente y comprobante de seguro. Llame al <a href="tel:{TEL}">{PH}</a> para hacer una cita.</p></div></div>''')
    if c.get('legacyAnchors'):
        tc=CAT_BY_ID['transmission-drivetrain']
        spans=''.join(f'<span id="{x}"></span>' for x in c['legacyAnchors'])
        extra+=f'''<p class="callout rv" style="margin-bottom:2rem">{spans}{ic('shift')}<span>{u['moved']} <a href="{link(P(lang,tc['url']),d)}">{esc(L(tc['name'],lang))}</a>.</span></p>'''
    body=''
    for s in c['services']:
        faqs=f'<h3 class="q">{"Questions about" if lang=="en" else "Preguntas sobre"} {esc(L(s["name"],lang))}</h3>'+faq_html(s['faqs'],s['slug'],lang) if s['faqs'] else ''
        im=IMG.get(s['id']); fig=''
        if im:
            b=f'{"../"*d}assets/img/svc/{im["file"]}'
            fig=f'<figure class="svc-img"><img src="{b}-1168.webp" srcset="{b}-640.webp 640w, {b}-1168.webp 1168w" sizes="(max-width:700px) 92vw, 560px" width="1168" height="880" loading="lazy" decoding="async" alt="{esc(L(im["alt"],lang))}"></figure>'
        more=''
        p=PAGE_BY_ID.get(s['page'])
        if p:
            du,df=dest(s['id'],lang)
            more=f'<p class="svc-more"><a class="more" href="{link(du,d,df)}">{u["details"]}: {esc(L(p["h1"],lang))} {ic("arrow")}</a></p>'
        body+=f'<article class="svc rv" id="{s["slug"]}"><h2>{esc(L(s["name"],lang))}</h2><p>{esc(L(s["desc"],lang))}</p>{more}{fig}{faqs}</article>'
    others=''.join(f'<a href="{link(P(lang,o["url"]),d)}">{ic(ICON[o["url"]])}{esc(L(o["short"],lang))}</a>' for o in CATS if o is not c)
    cr=home_crumb(lang,d)+[(sh,None)]
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs(cr,lang)}
<span class="eyebrow">{T(lang,'n_services',n=len(c['services']))}</span><h1>{esc(sh)}</h1><p class="lede">{esc(L(c['intro'],lang))}</p>
<div class="meta-row"><span class="pill">{ic('pin')} {C['street']}, {C['city']}</span><span class="pill">{ic('clock')} {u['hs']}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} {u['call']} {PH}</a></div></div></div>
<nav class="chips" data-spy aria-label="{u['in_cat']}">{chips}</nav>
<div class="wrap cat-layout"><aside class="rail" data-spy><h2>{u['in_cat']}</h2><ol>{rail}</ol><a class="btn btn-call btn-sm call" href="tel:{TEL}">{ic('phone')} {u['call']} {PH}</a></aside>
<div>{extra}{body}</div></div>
<section><div class="wrap">{cta(d,T(lang,'cat_q',x=sh.lower() if lang=='en' else sh.lower()),T(lang,'cat_x',hs=u['hs']),lang)}
<h2 style="font-size:1.4rem;margin:3rem 0 1rem">{u['other']}</h2><div class="others">{others}</div></div></section></main>'''+footer(d,lang)
    write(url,h)

# ---------- detailed service pages ----------
LINK_RE=re.compile(r'\[([^\]]+)\]\((svc|page|cat|url):([^)]+)\)')
def inline(text,lang,d):
    """Escape text, then turn [label](svc:id|page:id|cat:id|url:https://…) into links."""
    t=esc(fill(text))
    def rep(m):
        label,kind,target=m.group(1),m.group(2),html.unescape(m.group(3))
        if kind=='svc': u,f=dest(target,lang); return f'<a href="{link(u,d,f)}">{label}</a>'
        if kind=='page':
            if target in PAGE_BY_ID: return f'<a href="{link(P(lang,page_url(PAGE_BY_ID[target])),d)}">{label}</a>'
            raise SystemExit(f'link to unbuilt page {target}')
        if kind=='cat': return f'<a href="{link(P(lang,CAT_BY_ID[target]["url"]),d)}">{label}</a>'
        return f'<a href="{esc(target)}" rel="noopener" target="_blank">{label}</a>'
    return LINK_RE.sub(rep,t)
def block_id(b):
    return b[2] if len(b)>2 and b[2] else slug(L(b[1],'en'))[:48]
def render_blocks(blocks,lang,d):
    out=[];toc=[]
    for b in blocks:
        k=b[0]
        if k in('h2','h3'):
            i=block_id(b); txt=L(b[1],lang)
            if k=='h2': toc.append((i,txt))
            out.append(f'<{k} id="{i}">{inline(txt,lang,d)}</{k}>')
        elif k=='p': out.append(f'<p>{inline(L(b[1],lang),lang,d)}</p>')
        elif k=='ul': out.append('<ul class="svc-list">'+''.join(f'<li>{inline(L(x,lang),lang,d)}</li>' for x in b[1])+'</ul>')
        else: raise SystemExit(f'unknown block {k}')
    return ''.join(out),toc

def page_service(p,lang='en'):
    url=P(lang,page_url(p)); d=depth_of(url); u=UI[lang]; c=p['cat']; other='es' if lang=='en' else 'en'
    title=L(p['title'],lang); h1=L(p['h1'],lang)
    bc=home_crumb_ld(lang)+[(L(c['short'],lang),P(lang,c['url'])),(L(p['crumb'],lang),url)]
    svc={"@type":"Service","@id":canon_of(url)+'#service',"name":h1,"serviceType":L(p['service_type'],lang),"provider":{"@id":BIZ},"url":canon_of(url),"mainEntityOfPage":{"@id":canon_of(url)+'#webpage'}}
    ld=[graph(business_node(),website_node(),webpage_node(url,title,lang),svc,bc_node(bc,url),faq_node(p['faq'],lang))]
    h=head('svc',d,title,L(p['desc'],lang),url,ld,lang=lang,alt={'en':page_url(p),'es':'/es'+page_url(p)})+header(d,'services',lang,P(other,page_url(p)))
    body,toc=render_blocks(p['blocks'],lang,d)
    toc.append(('faq',u['faq']))
    rail=''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i,t in toc)
    covers=''.join(f'<li><a href="#{sid}">{esc(L(SVC[sid]["name"],lang))}</a></li>' for sid in p['covers'])
    rel_links=''.join(f'<a href="{link(*dest(sid,lang)[:1],d,dest(sid,lang)[1])}">{ic(ICON[SVC[sid]["cat"]["url"]])}{esc(L(SVC[sid]["name"],lang))}</a>' for sid in p['related'])
    srcs=''.join(f'<li><a href="{esc(s[1])}" rel="noopener" target="_blank">{esc(s[0])}</a>{(" "+u["en_only"].strip()) if lang=="es" else ""}</li>' for s in p.get('sources',[]))
    cr=home_crumb(lang,d)+[(L(c['short'],lang),link(P(lang,c['url']),d)),(L(p['crumb'],lang),None)]
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs(cr,lang)}
<span class="eyebrow">{esc(L(c['name'],lang))}</span><h1>{esc(h1)}</h1><p class="lede">{inline(L(p['lead'],lang),lang,d)}</p>
<div class="meta-row"><span class="pill">{ic('pin')} {C['street']}, {C['city']}</span><span class="pill">{ic('clock')} {u['hs']}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic('phone')} {u['call']} {PH}</a></div></div></div>
<div class="wrap cat-layout"><aside class="rail" data-spy><h2>{u['on_page']}</h2><ol>{rail}</ol><a class="btn btn-call btn-sm call" href="tel:{TEL}">{ic('phone')} {u['call']} {PH}</a></aside>
<div class="svc-body" id="{p['covers'][0]}">
<div class="covers rv"><h2 class="covers-h">{u['covers']}</h2><ul>{covers}</ul></div>
{body}
<h2 id="faq">{u['faq']}</h2>{faq_html(p['faq'],p['id'],lang)}
<h2 class="rel-h">{u['related']}</h2><div class="others">{rel_links}</div>
{f'<h2 class="src-h">{u["sources"]}</h2><ul class="sources">{srcs}</ul>' if srcs else ''}
</div></div>
<section><div class="wrap">{cta(d,T(lang,'req_t',name=NAME),T(lang,'req_x',ph=PH,hs=u['hs']),lang)}</div></section></main>'''+footer(d,lang)
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

def page_404():
    d=0
    h=head('404',d,f'Page not found | {NAME}','That page does not exist.','/404.html',None)
    h=h.replace('<meta name="description"','<meta name="robots" content="noindex"><meta name="description"',1)
    h=h.replace('<head>',f'<head><base href="{C.get("basePath","/")}">',1)
    h+=header(d,'')+f'''<main id="main"><div class="wrap err"><div><div class="n" aria-hidden="true">404</div><h1 style="font-size:clamp(1.8rem,3vw,2.6rem)">This page took a wrong turn.</h1><p class="lede" style="margin-inline:auto">Try the services list, or call us at <a href="tel:{TEL}">{PH}</a>.</p><div class="cta-row" style="justify-content:center"><a class="btn btn-call" href="./">Back to home</a><a class="btn btn-ghost" href="services/">Browse services</a></div></div></div></main>'''+footer(d)
    (ROOT/'404.html').write_text(postprocess(h),encoding='utf-8')

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
<div id="pickup"><dt>Pick-up, drop-off &amp; after hours</dt><dd>We can pick up your car and bring it back, and set up drop-off or pick-up outside shop hours. Call to arrange it.</dd></div></dl>
<div class="cta-row" style="margin:0 0 2rem"><a class="btn btn-call" href="tel:{TEL}">{ic('phone')} Call the shop</a><a class="btn btn-ghost" href="{DIR_URL}" rel="noopener">{ic('pin')} Get directions</a></div>
<h2 style="font-size:1.4rem">Hours</h2><table class="hours"><caption class="vh">Opening hours</caption><tbody>{rows}</tbody></table></div>
<div class="mapbox rv" data-map="{esc(emb)}" data-title="Map showing {esc(NAME)} at {esc(ADDR)}"><div class="gridbg"></div><div class="inner">{ic('pin')}<p><b>{C['street']}, {C['city']}</b></p><button class="btn btn-ghost" type="button">Load the map</button><p class="note" style="margin-top:.8rem">Loading the map connects to Google.</p></div></div></div></section></main>'''+footer(d)
    write(url,h)

def page_sitemap():
    d=1; url='/sitemap'
    h=head('sitemap',d,f'Sitemap | {NAME}',f'Every page and service on the {NAME} website.',url,None)+header(d,'sitemap')
    main_pages=[('Home','/'),('All services','/services'),('About','/about'),('Reviews','/reviews'),('Contact','/contact'),('Privacy','/privacy')]
    mp=''.join(f'<li><a href="{link(u,d)}">{lbl}</a></li>' for lbl,u in main_pages)+f'<li><a href="{rel(d)}sitemap.xml">sitemap.xml (for search engines)</a></li>'
    def svc_li(sv):
        u,f=dest(sv['id'],'en'); return f'<li><a href="{link(u,d,f)}">{esc(L(sv["name"]))}</a></li>'
    cats=''.join(f'<div class="sm-col"><h2><a href="{link(c["url"],d)}">{esc(L(c["short"]))}</a></h2><ul>'+''.join(svc_li(sv) for sv in c['services'])+'</ul></div>' for c in CATS)
    es=''.join(f'<li><a href="{link("/es"+c["url"],d)}" hreflang="es" lang="es">{esc(L(c["short"],"es"))}</a></li>' for c in CATS)+''.join(f'<li><a href="{link("/es"+page_url(p),d)}" hreflang="es" lang="es">{esc(L(p["h1"],"es"))}</a></li>' for p in PAGES)
    h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumbs([('Home',link('/',d)),('Sitemap',None)])}<h1>Sitemap</h1><p class="lede">Every page and service on this site.</p></div></div>
<section><div class="wrap"><div class="sitemap"><div class="sm-col"><h2>Pages</h2><ul>{mp}</ul></div>{cats}
<div class="sm-col" lang="es"><h2><a href="{link('/es/services',d)}" hreflang="es">Páginas en español</a></h2><ul>{es}</ul></div></div></div></section></main>'''+footer(d)
    write(url,h)

LASTMOD=ROOT/'src/lastmod.json'
def indexable_urls():
    en=['/','/services','/about','/reviews','/contact','/sitemap']+[c['url'] for c in CATS]+[page_url(p) for p in PAGES]
    es=['/es/services']+['/es'+c['url'] for c in CATS]+['/es'+page_url(p) for p in PAGES]
    return en+es
def misc():
    """sitemap.xml with lastmod that only moves when a page's <main> changes; robots.txt; .nojekyll."""
    old=json.loads(LASTMOD.read_text()) if LASTMOD.exists() else {}
    today=datetime.date.today().isoformat(); new={}
    for u in indexable_urls():
        f=(ROOT if u=='/' else ROOT/pagepath(u))/'index.html'
        m=re.search(r'<main\b.*?</main>',f.read_text(encoding='utf-8'),re.S)
        hsh=hashlib.sha1(m.group(0).encode()).hexdigest()[:12]
        prev=old.get(u)
        new[u]={'hash':hsh,'date':prev['date'] if prev and prev['hash']==hsh else today}
    LASTMOD.write_text(json.dumps(new,indent=1)+'\n')
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{canon_of(u)}</loc><lastmod>{new[u]["date"]}</lastmod></url>\n' for u in new)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sm)
    bots=['GPTBot','OAI-SearchBot','ChatGPT-User','ClaudeBot','Claude-SearchBot','Claude-User','PerplexityBot','Google-Extended','Applebot-Extended']
    rb='User-agent: *\nAllow: /\n\n'+''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots)+f'Sitemap: {BASE}/sitemap.xml\n'
    (ROOT/'robots.txt').write_text(rb); (ROOT/'.nojekyll').write_text('')
    return len(new)

if __name__=='__main__':
    page_home()
    for lang in LANGS:
        page_services(lang)
        for c in CATS: page_category(c,lang)
        for p in PAGES: page_service(p,lang)
    page_about(); page_reviews(); page_contact(); page_privacy(); page_sitemap(); page_404()
    n=misc()
    print(f'built {n} indexable pages ({len(PAGES)} detailed service pages x 2 languages) + privacy + 404')
