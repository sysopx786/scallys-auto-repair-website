# Scally's Auto Repair website

Static website for Scally's Auto Repair, 711 Secane Ave, Primos, PA 19018. Phone 610-626-4700.
English pages: Home, Services, 8 service categories, detailed service pages, About, Reviews, Contact, Privacy, Sitemap, 404.
Spanish pages under `/es/`: Services, the 8 categories and every detailed service page.
67 services in 8 categories. Plan, matrix and open decisions: `SERVICE-PLAN.md`.
Plain HTML, CSS and JS. No framework, cookies, analytics or forms.

Built from the `hoffman-auto-repair-website` template. All Hoffman content, branding and towing/salvage pages are removed.

**Status: pitch draft. Confirm details with the owner before promoting it.**

## Links

| | URL | Notes |
|---|---|---|
| Public site | https://sysopx786.github.io/scallys-auto-repair-website/ | Needs GitHub Pages: Settings → Pages → branch `main`, folder `/ (root)`. |
| Repository | https://github.com/sysopx786/scallys-auto-repair-website | |

## Edit and rebuild

Requires Python 3. Pages are generated, so edit the sources, not the HTML.

| To change | Edit | Then |
|---|---|---|
| Services, descriptions, FAQs (EN + ES) | `src/services.json` | `python3 src/build.py` |
| Detailed service pages (EN + ES) | `src/pages/<id>.json` | `python3 src/build.py` |
| Reviews, ratings, counts | `src/reviews.json` | `python3 src/build.py` |
| Phone, hours, address, OIS number, base URL, flags | `src/site.config.json` | `python3 src/build.py` |
| Service photos (keyed by service id) | `src/images.json` | `python3 src/build.py` |
| Page copy | `src/build.py` | `python3 src/build.py` |
| Logo, favicons, Open Graph image | `src/logo.py` | `python3 src/logo.py` (needs `fonttools brotli`, `rsvg-convert`, ImageMagick) |
| Styling, behavior | `assets/css/site.css`, `assets/js/site.js` | none |

Preview locally: `python3 -m http.server 8000`, then open http://localhost:8000.

Check the build: `python3 tests/check_site.py` (67 services, 8 categories, translations, canonicals, hreflang, links and anchors, sitemap, JSON-LD, English left on Spanish pages, forbidden services, reviews/contact unchanged). Run it before every commit.

Every English copy change ships with its Spanish in the same commit.

## Reviews

- `src/reviews.json` holds the Google and Yelp reviews shown on the site, copied word for word on November 3, 2026, including spelling.
- Google: 4.6 stars, 38 reviews. Yelp: 5.0 stars, 6 reviews.
- Google shows relative dates ("9 months ago"). They are stored as shown that day, and the page says so.
- No review stars in the schema markup. Google ignores self-served review stars for local businesses and can penalize them.

## Before launch

1. Confirm hours, services and inspection details with the owner.
2. Set `baseUrl` in `src/site.config.json` to the real domain. It is the GitHub Pages preview URL now; it feeds canonical and hreflang tags, Open Graph, structured data and `sitemap.xml`. The build refuses a `REPLACE` placeholder.
   Set `hoursVerified` to `true` once Jerry confirms the hours; until then the hours stay out of the structured data.
3. Set `basePath`: `/scallys-auto-repair-website/` on the GitHub Pages URL, `/` on a custom domain. It only affects `404.html`.
4. Rebuild, commit, push.

## Layout

```
index.html, <page>/index.html       generated pages (English)
es/<page>/index.html                generated pages (Spanish)
404.html, sitemap.xml, robots.txt   generated
assets/css, assets/js               styles and behavior
assets/fonts                        Bricolage Grotesque, Inter (self-hosted, SIL OFL)
assets/img                          logo, favicon, Open Graph image, service photos
src/                                build.py, logo.py, services.json, pages/*.json, reviews.json, images.json, site.config.json, lastmod.json
tests/check_site.py                 build checks
```
