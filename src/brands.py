#!/usr/bin/env python3
"""Scally's bilingual vehicle pages from the full Diverse Auto Works brand source inventory.

Keeps source content in src/brand_sources for future regeneration. The source
shop's address, limits, certification claims and CTAs must NOT be carried over.
Run via python3 src/build.py. Every page uses Scally's shared header/footer/schema.
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "brand_sources"))
from brand_pages import BRAND_PAGES

BRAND_SLUGS = [p["slug"].split("/")[-1] for p in BRAND_PAGES]
assert len(BRAND_SLUGS) == 35 and len(set(BRAND_SLUGS)) == 35, "Unexpected source brand count"
BRAND_KEY = {p["key"]: p for p in BRAND_PAGES}

GROUPS = [
    ("American", "Estadounidenses", "ford chevrolet gmc buick cadillac lincoln chrysler dodge jeep ram tesla".split()),
    ("Asian", "Asiáticas", "toyota honda nissan mazda subaru mitsubishi hyundai kia lexus acura infiniti genesis".split()),
    ("European", "Europeas", "bmw mercedes-benz audi volkswagen volvo porsche mini jaguar land-rover fiat alfa-romeo maserati".split()),
]
assert sorted(x for _, _, group in GROUPS for x in group) == sorted(BRAND_SLUGS)

# Source shop-specific exclusions don't apply to Jerry's shop. On unfamiliar
# high-voltage/software repairs we avoid promising unsupported specialist work.
LIMITED = re.compile(
    r"\b(?:fleet|flotas?|we (?:don't|do not|only)|no hacemos|no reparamos|"
    r"lo que no hacemos|what we don't do)\b", re.I
)
def localized(x, lang):
    return x[lang] if isinstance(x, dict) else x

def adapt(x, lang, name):
    s = localized(x, lang)
    s = re.sub(r"Diverse\s+Auto\s*works(?:,\s*Inc\.)?", name, s, flags=re.I)
    s = s.replace("Phoenixville", "Primos")
    s = s.replace("Chester and Montgomery counties", "Delaware County")
    s = s.replace("Chester and Montgomery Counties", "Delaware County")
    s = s.replace("Chester County", "Delaware County")
    s = s.replace("condados de Chester y Montgomery", "condado de Delaware")
    s = s.replace("condado de Chester", "condado de Delaware")
    s = re.sub(r"\bOur ASE-certified technicians\b", "Our experienced mechanics", s, flags=re.I)
    s = re.sub(r"\bASE-certified technicians\b", "experienced mechanics", s, flags=re.I)
    s = re.sub(r"\bASE-certified technician\b", "experienced mechanic", s, flags=re.I)
    s = re.sub(r"\bASE-certified\b", "experienced", s, flags=re.I)
    s = re.sub(r"\bNuestros técnicos certificados por ASE\b", "Nuestros mecánicos con experiencia", s, flags=re.I)
    s = re.sub(r"\btécnicos certificados por ASE\b", "mecánicos con experiencia", s, flags=re.I)
    s = re.sub(r"\btécnico certificado por ASE\b", "mecánico con experiencia", s, flags=re.I)
    s = re.sub(r"\bcertificados por ASE\b", "con experiencia", s, flags=re.I)
    s = s.replace("No high-voltage repairs.", "Call about model-specific repairs.")
    s = s.replace("Sin reparaciones de alto voltaje.", "Consulte por reparaciones específicas.")
    s = s.replace("We don't do high-voltage battery or software repairs; those go to Tesla.", "Call us to discuss model-specific repair needs.")
    s = s.replace("No hacemos reparaciones de la batería de alto voltaje ni de software; esas van a Tesla.", "Llámenos para consultar las necesidades de reparación de su modelo.")
    return s

BRAND_CSS = """<style>
.brand-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:12px;margin:20px 0 38px}
.brand-tile{display:block;background:var(--paper,#fff);color:inherit;border:1px solid var(--line,#d4dbe2);border-radius:12px;padding:18px;text-decoration:none;font-weight:700;transition:transform .16s,border-color .16s}
.brand-tile:hover,.brand-tile:focus-visible{transform:translateY(-2px);border-color:var(--teal,#327e85)}
.brand-section{padding:30px 0 0}.brand-section h2{margin:0 0 10px}
.brand-spec{width:100%;border-collapse:collapse;margin:18px 0;display:table}
.brand-spec th,.brand-spec td{border:1px solid #d9dee6;padding:12px;text-align:left;vertical-align:top}
.brand-spec th{background:#eef2f6;color:#14213a}
.brand-note{font-size:.92rem;opacity:.85}
.brand-body h2,.brand-body h3{scroll-margin-top:100px}
.brand-body ul{padding-left:1.5em}
@media(max-width:560px){.brand-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.brand-tile{padding:14px;font-size:.91rem}}
</style>"""

def generate_brand_pages(site):
    NAME=site["NAME"]; TEL=site["TEL"]; PH=site["PH"]; C=site["C"]
    esc=site["esc"]; L=site["L"]; ic=site["ic"]; P=site["P"]
    link=site["link"]; head=site["head"]; header=site["header"]
    footer=site["footer"]; write=site["write"]; cta=site["cta"]
    graph=site["graph"]; business_node=site["business_node"]
    website_node=site["website_node"]; webpage_node=site["webpage_node"]
    bc_node=site["bc_node"]; faq_node=site["faq_node"]; faq_html=site["faq_html"]
    depth_of=site["depth_of"]; canon_of=site["canon_of"]; U=site["UI"]
    slugify=site["slug"]

    def body_link(text, lang, depth):
        s=esc(adapt(text,lang,NAME))
        def convert(m):
            label,target=m.group(1),html.unescape(m.group(2))
            raw=target.split("#",1)[0]
            if raw.startswith("brand_") and raw in BRAND_KEY:
                url="/"+BRAND_KEY[raw]["slug"]
            elif raw=="inspections": url="/pa-state-inspection"
            elif raw=="services" or raw=="fleet": url="/services"
            elif raw.startswith("contact"): url="/contact"
            else: url="/services"
            return '<a href="'+link(P(lang,url),depth)+'">'+label+'</a>'
        return re.sub(r"\[([^\]]+)\]\(([^)]+)\)",convert,s)

    def blocks_html(blocks,lang,depth):
        pieces=[]; toc=[]; skip_next=False
        for b in blocks:
            kind=b[0]
            raw=localized(b[1],lang) if kind not in ("ul","table") else ""
            if kind in ("p","h2","h3") and LIMITED.search(raw):
                continue
            if kind in ("h2","h3"):
                title=adapt(b[1],lang,NAME)
                anchor=slugify(localized(b[1],"en"))[:70]
                if kind=="h2": toc.append((anchor,title))
                pieces.append(f'<{kind} id="{anchor}">{esc(title)}</{kind}>')
            elif kind=="p":
                pieces.append(f'<p>{body_link(b[1],lang,depth)}</p>')
            elif kind=="ul":
                items=[x for x in b[1] if not LIMITED.search(localized(x,lang))]
                pieces.append('<ul class="svc-list">'+''.join('<li>'+body_link(x,lang,depth)+'</li>' for x in items)+'</ul>')
            elif kind=="table":
                hd,rows=b[1],b[2]
                tbl='<table class="brand-spec"><thead><tr>'+''.join('<th scope="col">'+esc(adapt(x,lang,NAME))+'</th>' for x in hd)+'</tr></thead><tbody>'
                tbl+=''.join('<tr>'+''.join('<td>'+esc(adapt(v,lang,NAME))+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table>'
                pieces.append('<div style="overflow-x:auto">'+tbl+'</div>')
            else:
                raise ValueError("Unsupported brand source block: "+str(kind))
        return "\n".join(pieces),toc

    for lang in ("en","es"):
        other="es" if lang=="en" else "en"
        hub=P(lang,"/brands"); dep=depth_of(hub)
        title=("Car Brands We Service in Primos, PA" if lang=="en" else "Marcas de autos que atendemos en Primos, PA")+" | "+NAME
        desc=(f"Explore all 35 vehicle makes serviced by {NAME} in Primos, Delaware County, PA. Family-owned neighborhood repair since 1987."
              if lang=="en" else f"Conozca las 35 marcas de vehículos que atiende {NAME} en Primos, condado de Delaware. Taller del vecindario desde 1987.")
        crumbs=[("Home" if lang=="en" else "Inicio", "/"),("Car Brands" if lang=="en" else "Marcas",hub)]
        ld=[graph(business_node(),website_node(),webpage_node(hub,title,lang),bc_node(crumbs,hub))]
        h=head("brands",dep,title,desc,hub,ld,lang=lang,alt={"en":"/brands","es":"/es/brands"}).replace("</head>",BRAND_CSS+"</head>")
        h+=header(dep,"brands",lang,P(other,"/brands"))
        cards=""
        for name_en,name_es,names in GROUPS:
            label=name_es if lang=="es" else name_en
            tiles="".join(f'<a class="brand-tile" href="{link(P(lang,"/brands/"+sl),dep)}">{esc(next(b["name"] for b in BRAND_PAGES if b["slug"].endswith("/"+sl)))} →</a>' for sl in sorted(names))
            cards+=f'<section class="brand-section"><h2>{esc(label)}</h2><div class="brand-grid">{tiles}</div></section>'
        ctext=("Find your vehicle manufacturer below. Each page explains common repairs, maintenance, inspections and the models we service."
               if lang=="en" else "Busque la marca de su vehículo. Cada página explica reparaciones, mantenimiento, inspecciones y modelos que atendemos.")
        blabel="Vehicle Brands We Service" if lang=="en" else "Marcas de vehículos que atendemos"
        h+=f'<main id="main"><div class="phero"><div class="wrap"><h1>{blabel}</h1><p class="lede">{ctext}</p><div class="meta-row"><span class="pill">{ic("pin")} {C["street"]}, {C["city"]}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic("phone")} {PH}</a></div></div></div><div class="wrap">{cards}<p><a href="{link(P(lang,"/services"),dep)}">{"Browse all repair services" if lang=="en" else "Ver todos los servicios de reparación"}</a></p></div><section><div class="wrap">{cta(dep,lang=lang)}</div></section></main>'+footer(dep,lang)
        write(hub,h)

        for b in BRAND_PAGES:
            slug=b["slug"]; url=P(lang,"/"+slug); d=depth_of(url)
            page=b["page"]; name=b["name"]
            title=adapt(page["title"],lang,NAME)
            desc=adapt(page["desc"],lang,NAME)
            h1=adapt(page["h1"],lang,NAME)
            lead=body_link(page["lead"],lang,d)
            rawfaqs=[(adapt(q,lang,NAME),adapt(a,lang,NAME)) for q,a in b.get("faq",[])]
            faqs=[]
            for q,a in rawfaqs:
                if LIMITED.search(q):
                    continue
                if LIMITED.search(a):
                    a=("Please call Scally's Auto Repair to discuss the specific work your vehicle needs."
                       if lang=="en" else "Llame a Scally's Auto Repair para consultar las reparaciones que necesita su vehículo.")
                faqs.append({"q":q,"a":a})
            bc=[("Home" if lang=="en" else "Inicio","/"),("Car Brands" if lang=="en" else "Marcas",P(lang,"/brands")),(name,url)]
            svc={"@type":"Service","@id":canon_of(url)+"#service","name":h1,"serviceType":adapt(b["service_type"],lang,NAME),"url":canon_of(url),"provider":{"@id":site["BIZ"]},"areaServed":{"@type":"City","name":"Primos"}}
            ld=[graph(business_node(),website_node(),webpage_node(url,title,lang),svc,bc_node(bc,url),faq_node(faqs,lang))]
            h=head("brand",d,title,desc,url,ld,lang=lang,alt={"en":"/"+slug,"es":"/es/"+slug}).replace("</head>",BRAND_CSS+"</head>")
            h+=header(d,"brands",lang,P(other,"/"+slug))
            content,toc=blocks_html(b["blocks"],lang,d)
            toc.append(("faq","Preguntas frecuentes" if lang=="es" else "Frequently asked questions"))
            rail="".join(f'<li><a href="#{slugify(a)}">{esc(z)}</a></li>' if a=="faq" else f'<li><a href="#{a}">{esc(z)}</a></li>' for a,z in toc)
            crumb_html=site["crumbs"]([("Home" if lang=="en" else "Inicio",link("/",d)),("Car Brands" if lang=="en" else "Marcas",link(P(lang,"/brands"),d)),(name,None)],lang)
            related=(("Inspección estatal","/pa-state-inspection"),("Diagnóstico del motor","/check-engine-light"),("Reparación de frenos","/brake-repair"),("Llantas","/tires"),("Mantenimiento","/oil-change")) if lang=="es" else (("PA Inspections","/pa-state-inspection"),("Engine Diagnostics","/check-engine-light"),("Brake Repair","/brake-repair"),("Tires","/tires"),("Maintenance","/oil-change"))
            rel_links="".join(f'<a href="{link(P(lang,t),d)}">{ic("car")}{esc(label)}</a>' for label,t in related)
            label="Preguntas frecuentes" if lang=="es" else "Frequently asked questions"
            h+=f'''<main id="main"><div class="phero"><div class="wrap">{crumb_html}
<span class="eyebrow">{'Reparación de vehículos en Primos' if lang=="es" else "Vehicle repair in Primos"}</span><h1>{esc(h1)}</h1><p class="lede">{lead}</p>
<div class="meta-row"><span class="pill">{ic("pin")} {C["street"]}, {C["city"]}</span><a class="btn btn-call btn-sm" href="tel:{TEL}">{ic("phone")} {PH}</a></div></div></div>
<div class="wrap cat-layout"><aside class="rail" data-spy><h2>{'En esta página' if lang=="es" else "On this page"}</h2><ol>{rail}</ol></aside>
<article class="svc-body brand-body">{content}
<h2 id="faq">{label}</h2>{faq_html(faqs,"brand-"+slug.split("/")[-1],lang)}
<h2>{'Servicios relacionados' if lang=="es" else "Related services"}</h2><div class="others">{rel_links}</div>
<p class="brand-note"><a href="{link(P(lang,"/brands"),d)}">{'← Volver a todas las marcas' if lang=="es" else "← Back to all brands"}</a></p></article></div>
<section><div class="wrap">{cta(d,lang=lang)}</div></section></main>'''+footer(d,lang)
            write(url,h)
    print("Generated",len(BRAND_PAGES),"brand pages in English and Spanish + 2 brand directories")
