# Scally's Auto Repair: service expansion plan and status

Branch `service-expansion`. The first 3 pages were merged to `main` on Nov 3, 2026; later batches go live only when merged.
Last updated: November 4, 2026 UTC (Batch 2 generated and QA passed on service-expansion; merge and deployment next).

## Status

| Item | Status |
|---|---|
| 67 services in 8 categories, 26 new, retreads removed | Done (EN + ES) |
| New category: Transmission & Drivetrain (`/transmission-drivetrain/`) | Done |
| Spanish versions: services hub, 8 category pages, detailed pages | Done for what is built |
| Language switch, hreflang, self-canonicals, sitemap `lastmod` | Done |
| Structured data: one `AutoRepair` entity (`/#business`), WebPage, Service, BreadcrumbList, FAQPage | Done |
| Detailed service pages | 23 of 34 built and tested on `service-expansion` (18 already on `main`); 11 detailed pages remain after Batch 2 |
| Automated checks (`tests/check_site.py`) | ALL CHECKS PASSED after 18-page rebuild on GitHub Actions run 41765832517 |
| Batch 1 full build and responsive QA | ALL BROWSER CHECKS PASSED: 60 checks, 0 failures |
| Batch 2 build and responsive QA | ALL CHECKS PASSED; ALL BROWSER CHECKS PASSED (120 checks, 0 failures) — [run 41771079049](https://github.com/sysopx786/scallys-auto-repair-website/actions/runs/41771079049) |

## Batch 1 (November 4, 2026 UTC) — built and tested on service-expansion

Five bilingual JSON records and their generated English/Spanish pages are committed on `service-expansion`. GitHub Actions ran `python3 src/build.py` (59 indexable pages, 18 detailed page pairs), `python3 tests/check_site.py` (`ALL CHECKS PASSED`), and Chromium checks of ten new pages at six widths (`ALL BROWSER CHECKS PASSED`, zero failures). The QA artifact includes a detailed browser report and 20 full-page screenshots. `main` has not been changed; these five pages are not live.

| Page | Covers | EN / ES rendered page words | Status |
|---|---|---:|---|
| `pa-state-inspection` | `pa-safety-inspections`, `emissions-testing` | 1,054 / 1,104 | Built and browser-tested on branch |
| `emissions-repair` | `emissions-control` | 1,130 / 1,256 | Built and browser-tested on branch |
| `pre-purchase-inspection` | `pre-purchase-inspections` | 1,206 / 1,224 | Built and browser-tested on branch |
| `timing-belt-chain` | `timing-belt`, `timing-chain` | 1,235 / 1,269 | Built and browser-tested on branch |
| `engine-tune-up` | `engine-tune-ups`, `spark-plugs`, `ignition-system-repair` | 1,188 / 1,282 | Built and browser-tested on branch |

PennDOT safety/emissions and PA DEP OBD pages were read and cited where applicable. No universal timing-belt or spark-plug interval, inspection price, guarantee, or fixed pre-purchase checklist was invented. Service-specific `verify` questions remain for Jerry. JSON catalog, anchors, languages, titles, descriptions, FAQ counts, full generated-site tests and 60 Chromium viewport checks passed. See [GitHub Actions run 41765832517](https://github.com/sysopx786/scallys-auto-repair-website/actions/runs/41765832517) and generated-file commit `7290a3cb797a8308e17e5a64b36d57d5d3ce3f41`.

**Batch 1 complete on the development branch:** Build, full tests, responsive browser tests and generated-file commit passed. Still to do: review Jerry's `verify` questions, synchronize this plan to the separate Claude project document `claude/scallys-service-expansion-plan.md` (not yet synced through this GitHub connection), obtain native-speaker Spanish review when possible, and await the explicit word `merge` before publishing.

## Batch 2 (November 4, 2026 UTC) — built, tested, awaiting merge

The following five bilingual JSON source files and their generated HTML are committed on `service-expansion`. `python3 src/build.py` generated **69 indexable pages**, including **23 detailed pages in each language**. `python3 tests/check_site.py` printed `ALL CHECKS PASSED`. The expanded Chromium suite printed `ALL BROWSER CHECKS PASSED` after **120 checks with zero failures**. GitHub Actions committed the generated files (commit `bf5c5bc86c8fb50dda75627c9c310283c09638f3`).

| Page | Services covered | EN / ES rendered page words | Source status |
|---|---|---:|---|
| `electrical-repair` | Electrical Repair & Wiring | 959 / 1,028 | Built; QA passed; merge pending |
| `auto-light-repair` | Auto Light Repair | 973 / 1,048 | Built; QA passed; merge pending |
| `power-windows-locks` | Power Window Repair, Power Door Lock Repair | 1,053 / 1,045 | Built; QA passed; merge pending |
| `wheel-bearings-hubs` | Wheel Bearings, Wheel Hubs | 1,051 / 1,114 | Built; QA passed; merge pending |
| `oil-leak-repair` | Oil Leak & Gasket Repair | 1,116 / 1,155 | Built; QA passed; merge pending |

All new pages use Primos, Secane and Clifton Heights; avoid the unrelated Diverse business claims, named diagnostic equipment, prices, guarantees and universal maintenance intervals. They contain full US Spanish copy, SEO fields, relevant related services, covered-service anchors and six FAQs each. Owner-confirmation notes remain in each JSON file's `verify` section. Pennsylvania inspection claims are supported by PennDOT consumer guidance; a NHTSA-hosted Audi service bulletin is cited only for the narrow point that tire and bearing noises can sound alike.

The browser test covered all ten new pages across Batches 1 and 2 in English and Spanish at 320, 390, 768, 1100, 1280 and 1600 px, and passed all **120 checks** with no HTTP, browser-script, or horizontal-overflow failures. The QA artifact contains 40 full-page screenshots and a machine-readable report. Next: merge the passing branch into `main` and verify GitHub Pages deployment; the user already gave authorization.

## Decisions that need your OK before merge

1. **Page consolidation: 34 detailed pages, not 67.** Diverse Auto Works covers its ~83 services with 26 detailed pages. One page per service would create near-duplicate pages competing for the same searches (wheel bearings vs wheel hubs, motor mounts vs transmission mounts, spark plugs vs ignition vs tune-ups). Every one of the 67 services still has its own anchor, its own entry on its category page, its own search entry, and a link to the page that covers it. Reverting a service to its own page is a one-field change (`page` in `src/services.json`) plus a new page file.
2. **Canonical domain.** `baseUrl` is now the GitHub Pages preview (`https://sysopx786.github.io/scallys-auto-repair-website`). If this merges before a custom domain exists, Google indexes the github.io URLs, and you redo the move later. Alternatives: wait for the domain, or merge now and switch `baseUrl` + `basePath` when the domain is live.
3. **Hours removed from structured data.** Directories disagree on hours, so `openingHoursSpecification` is off until Jerry confirms (`"hoursVerified": true` in `src/site.config.json` turns it back on). Hours still show on the pages.
4. **Service-area towns.** Copy names only Primos, Secane and Clifton Heights. Springfield, Aldan, Drexel Hill and Lansdowne stay out until Jerry says he gets customers from there.
5. **Header change.** The mega menu now lists the 8 categories (with counts) instead of every service, so it stays short with 67 services. The desktop open/closed pill is hidden at all desktop widths: it never fit beside the nav once the language switch was added (it already overflowed by 25px at 1561-1620px before this change). It still shows on phones and tablets.

## Detailed pages (proposed)

| Page | Covers | Status |
|---|---|---|
| `/pa-state-inspection/` | PA Safety Inspections, Emissions Testing | built (EN+ES); full QA passed |
| `/emissions-repair/` | Emissions Control | built (EN+ES); full QA passed |
| `/pre-purchase-inspection/` | Pre-Purchase Inspections | built (EN+ES); full QA passed |
| `/check-engine-light/` | Computer Diagnostics, Check Engine Light | built (EN+ES) |
| `/electrical-repair/` | Electrical Repair & Wiring | built (EN+ES); QA passed; merge pending |
| `/battery-alternator-starter/` | Charging & Starting Systems, Battery Testing & Replacement | built (EN+ES) |
| `/auto-light-repair/` | Auto Light Repair | built (EN+ES); QA passed; merge pending |
| `/power-windows-locks/` | Power Window Repair, Power Door Lock Repair | built (EN+ES); QA passed; merge pending |
| `/brake-repair/` | Brake Repair, Rotor Resurfacing, Brake Fluid Flush | built (EN+ES) |
| `/suspension-repair/` | Steering & Suspension, Sway Bar Links, Shocks & Struts | built (EN+ES) |
| `/steering-repair/` | Power Steering Repair, Ball Joints, Control Arms, Tie Rods | built (EN+ES) |
| `/wheel-bearings-hubs/` | Wheel Bearings, Wheel Hubs | built (EN+ES); QA passed; merge pending |
| `/wheel-alignment/` | Front End Alignment | built (EN+ES) |
| `/engine-repair/` | Engine Repair, Engine Rebuilding, Engine Replacement, Cylinder Head & Block Repair | built (EN+ES) |
| `/engine-tune-up/` | Engine Tune-Ups, Spark Plugs, Ignition System Repair | built (EN+ES); full QA passed |
| `/oil-leak-repair/` | Oil Leak & Gasket Repair | built (EN+ES); QA passed; merge pending |
| `/timing-belt-chain/` | Timing Belt, Timing Chain | built (EN+ES); full QA passed |
| `/exhaust-muffler-repair/` | Mufflers & Exhaust | built (EN+ES) |
| `/fuel-system-repair/` | Fuel System Service, Gas Tanks | queued |
| `/transmission-repair/` | Transmission Repair, Transmission Rebuilding, Transmission Replacement, Transmission Fluid Service | built (EN+ES) |
| `/clutch-repair/` | Clutch Repair | queued |
| `/engine-transmission-mounts/` | Motor Mounts, Transmission Mounts | queued |
| `/cv-axle-differential/` | Differential Repair, CV Axles & Joints, Rear Axle Bearings & Seals | queued |
| `/oil-change/` | Oil Changes, Filter Replacement | built (EN+ES) |
| `/cooling-system/` | Fan & Accessory Belts, Cooling Systems | built (EN+ES) |
| `/ac-heating/` | Air Conditioning & Heating | built (EN+ES) |
| `/hybrid-service/` | Basic Hybrid Service | queued |
| `/tires/` | Tires & Flat Repair, Tire Rotation, Wheel Balancing | built (EN+ES) |
| `/wheel-repair/` | Wheels, Wheel Repair | queued |
| `/auto-body-repair/` | Auto Body Repair | queued |
| `/rust-repair/` | Rust Repair & Corrosion Control | queued |
| `/auto-glass/` | Auto Glass Installation & Repair, Windshield Wiper Replacement | queued |
| `/window-tinting/` | Window Tinting | queued |
| `/import-car-repair/` | Imports | queued |

34 detailed pages for 65 services. General Auto Repair stays on the home page; Pick-up/Drop-off stays on /contact/#pickup.


Next recommended batch: electrical repair, auto light repair, power windows and locks, wheel bearings and hubs, and oil leak repair. Then follow the remaining batch order in the completion prompt. Body, glass, tinting and imports need additional research; Pennsylvania tint rules must be checked before the tint page is written.

## 67-service matrix

Status: NEW = added in this expansion; moved = moved to Transmission & Drivetrain; renamed = new display name, same anchor.
Old anchors for moved services (`/engine-exhaust-transmission/#transmission-repair`, `#differential-repair`, `#axles`) still resolve: they land on a note that links to the new category.

| # | Service | Category | Status | Old URL | Destination | Built | Diverse source |
|---|---|---|---|---|---|---|---|
| 1 | PA Safety Inspections | Inspections & Emissions | existing | `/inspections-emissions/#pa-safety-inspections` | `/pa-state-inspection/` | ✅ | content.py inspections page |
| 2 | Emissions Testing | Inspections & Emissions | existing | `/inspections-emissions/#emissions-testing` | `/pa-state-inspection/` | ✅ | content.py inspections page |
| 3 | Emissions Control | Inspections & Emissions | existing | `/inspections-emissions/#emissions-control` | `/emissions-repair/` | ✅ | svc_emissions |
| 4 | Pre-Purchase Inspections | Inspections & Emissions | existing | `/inspections-emissions/#pre-purchase-inspections` | `/pre-purchase-inspection/` | ✅ | svc_prepurchase |
| 5 | Computer Diagnostics | Diagnostics & Electrical | existing | `/diagnostics-electrical/#computer-diagnostics` | `/check-engine-light/` | ✅ | svc_engine (CEL part) |
| 6 | Check Engine Light | Diagnostics & Electrical | existing | `/diagnostics-electrical/#check-engine-light` | `/check-engine-light/` | ✅ | svc_engine (CEL part) |
| 7 | Electrical Repair & Wiring | Diagnostics & Electrical | renamed | `/diagnostics-electrical/#electrical-repair` | `/electrical-repair/` | ✅ (branch) | svc_electrical |
| 8 | Charging & Starting Systems | Diagnostics & Electrical | existing | `/diagnostics-electrical/#charging-and-starting-systems` | `/battery-alternator-starter/` | ✅ | svc_battery + svc_electrical |
| 9 | Battery Testing & Replacement | Diagnostics & Electrical | renamed | `/diagnostics-electrical/#battery-service` | `/battery-alternator-starter/` | ✅ | svc_battery + svc_electrical |
| 10 | Auto Light Repair | Diagnostics & Electrical | existing | `/diagnostics-electrical/#auto-light-repair` | `/auto-light-repair/` | ✅ (branch) | svc_lights |
| 11 | Power Window Repair | Diagnostics & Electrical | NEW | `—` | `/power-windows-locks/` | ✅ (branch) | svc_windowlock |
| 12 | Power Door Lock Repair | Diagnostics & Electrical | NEW | `—` | `/power-windows-locks/` | ✅ (branch) | svc_windowlock |
| 13 | Brake Repair | Brakes, Steering & Suspension | existing | `/brakes-steering-suspension/#brake-repair` | `/brake-repair/` | ✅ | svc_brakes |
| 14 | Rotor Resurfacing | Brakes, Steering & Suspension | existing | `/brakes-steering-suspension/#rotor-resurfacing` | `/brake-repair/#rotor-resurfacing` | ✅ | svc_brakes |
| 15 | Brake Fluid Flush | Brakes, Steering & Suspension | NEW | `—` | `/brake-repair/#brake-fluid-flush` | ✅ | svc_brakes |
| 16 | Steering & Suspension | Brakes, Steering & Suspension | existing | `/brakes-steering-suspension/#steering-and-suspension` | `/suspension-repair/` | ✅ | svc_suspension |
| 17 | Power Steering Repair | Brakes, Steering & Suspension | NEW | `—` | `/steering-repair/` | ✅ | svc_steering |
| 18 | Ball Joints | Brakes, Steering & Suspension | existing | `/brakes-steering-suspension/#ball-joints` | `/steering-repair/` | ✅ | svc_steering |
| 19 | Control Arms | Brakes, Steering & Suspension | NEW | `—` | `/steering-repair/` | ✅ | svc_steering |
| 20 | Tie Rods | Brakes, Steering & Suspension | NEW | `—` | `/steering-repair/` | ✅ | svc_steering |
| 21 | Sway Bar Links | Brakes, Steering & Suspension | NEW | `—` | `/suspension-repair/` | ✅ | svc_suspension |
| 22 | Shocks & Struts | Brakes, Steering & Suspension | NEW | `—` | `/suspension-repair/` | ✅ | svc_suspension |
| 23 | Wheel Bearings | Brakes, Steering & Suspension | NEW | `—` | `/wheel-bearings-hubs/` | ✅ (branch) | svc_bearing |
| 24 | Wheel Hubs | Brakes, Steering & Suspension | NEW | `—` | `/wheel-bearings-hubs/` | ✅ (branch) | svc_bearing |
| 25 | Front End Alignment | Brakes, Steering & Suspension | existing | `/brakes-steering-suspension/#front-end-alignment` | `/wheel-alignment/` | ✅ | svc_tires (alignment) |
| 26 | General Auto Repair | Engine & Exhaust | existing | `/engine-exhaust-transmission/#general-auto-repair` | `/ (home page)` | n/a | n/a |
| 27 | Engine Repair | Engine & Exhaust | existing | `/engine-exhaust-transmission/#engine-repair` | `/engine-repair/` | ✅ | svc_engine |
| 28 | Engine Tune-Ups | Engine & Exhaust | NEW | `—` | `/engine-tune-up/` | ✅ | svc_engine (tune-up part) |
| 29 | Engine Rebuilding | Engine & Exhaust | NEW | `—` | `/engine-repair/#engine-rebuilding` | ✅ | svc_engine |
| 30 | Engine Replacement | Engine & Exhaust | existing | `/engine-exhaust-transmission/#engine-replacement` | `/engine-repair/#engine-replacement` | ✅ | svc_engine |
| 31 | Cylinder Head & Block Repair | Engine & Exhaust | existing | `/engine-exhaust-transmission/#cylinder-head-and-block-repair` | `/engine-repair/#cylinder-head-and-block-repair` | ✅ | svc_engine |
| 32 | Oil Leak & Gasket Repair | Engine & Exhaust | NEW | `—` | `/oil-leak-repair/` | ✅ (branch) | svc_oilleak |
| 33 | Spark Plugs | Engine & Exhaust | existing | `/engine-exhaust-transmission/#spark-plugs` | `/engine-tune-up/` | ✅ | svc_engine (tune-up part) |
| 34 | Ignition System Repair | Engine & Exhaust | NEW | `—` | `/engine-tune-up/` | ✅ | svc_engine (tune-up part) |
| 35 | Timing Belt | Engine & Exhaust | NEW | `—` | `/timing-belt-chain/` | ✅ | svc_timing |
| 36 | Timing Chain | Engine & Exhaust | NEW | `—` | `/timing-belt-chain/` | ✅ | svc_timing |
| 37 | Mufflers & Exhaust | Engine & Exhaust | existing | `/engine-exhaust-transmission/#mufflers-and-exhaust` | `/exhaust-muffler-repair/` | ✅ | svc_exhaust |
| 38 | Fuel System Service | Engine & Exhaust | existing | `/engine-exhaust-transmission/#fuel-system-service` | `/fuel-system-repair/` | queued | svc_fuel |
| 39 | Gas Tanks | Engine & Exhaust | existing | `/engine-exhaust-transmission/#gas-tanks` | `/fuel-system-repair/` | queued | svc_fuel |
| 40 | Transmission Repair | Transmission & Drivetrain | moved | `/engine-exhaust-transmission/#transmission-repair` | `/transmission-repair/` | ✅ | svc_transmission |
| 41 | Transmission Rebuilding | Transmission & Drivetrain | NEW | `—` | `/transmission-repair/#transmission-rebuilding` | ✅ | svc_transmission |
| 42 | Transmission Replacement | Transmission & Drivetrain | NEW | `—` | `/transmission-repair/#transmission-replacement` | ✅ | svc_transmission |
| 43 | Transmission Fluid Service | Transmission & Drivetrain | NEW | `—` | `/transmission-repair/#transmission-fluid-service` | ✅ | svc_transmission |
| 44 | Clutch Repair | Transmission & Drivetrain | NEW | `—` | `/clutch-repair/` | queued | svc_clutch |
| 45 | Motor Mounts | Transmission & Drivetrain | NEW | `—` | `/engine-transmission-mounts/` | queued | svc_transmission (mounts) |
| 46 | Transmission Mounts | Transmission & Drivetrain | NEW | `—` | `/engine-transmission-mounts/` | queued | svc_transmission (mounts) |
| 47 | Differential Repair | Transmission & Drivetrain | moved | `/engine-exhaust-transmission/#differential-repair` | `/cv-axle-differential/` | queued | svc_axle + svc_transmission (rear axle) |
| 48 | CV Axles & Joints | Transmission & Drivetrain | moved | `/engine-exhaust-transmission/#axles` | `/cv-axle-differential/` | queued | svc_axle + svc_transmission (rear axle) |
| 49 | Rear Axle Bearings & Seals | Transmission & Drivetrain | NEW | `—` | `/cv-axle-differential/` | queued | svc_axle + svc_transmission (rear axle) |
| 50 | Oil Changes | Maintenance, A/C & Cooling | existing | `/maintenance/#oil-changes` | `/oil-change/` | ✅ | svc_oil |
| 51 | Filter Replacement | Maintenance, A/C & Cooling | existing | `/maintenance/#filter-replacement` | `/oil-change/` | ✅ | svc_oil |
| 52 | Fan & Accessory Belts | Maintenance, A/C & Cooling | NEW | `—` | `/cooling-system/` | ✅ | svc_cooling |
| 53 | Air Conditioning & Heating | Maintenance, A/C & Cooling | existing | `/maintenance/#air-conditioning-and-heating` | `/ac-heating/` | ✅ | svc_climate |
| 54 | Cooling Systems | Maintenance, A/C & Cooling | existing | `/maintenance/#cooling-systems` | `/cooling-system/` | ✅ | svc_cooling |
| 55 | Basic Hybrid Service | Maintenance, A/C & Cooling | NEW | `—` | `/hybrid-service/` | queued | svc_hybrid (EV/HV claims stripped) |
| 56 | Tires & Flat Repair | Tires & Wheels | existing | `/tires-wheels/#tires-and-flat-repair` | `/tires/` | ✅ | svc_tires |
| 57 | Tire Rotation | Tires & Wheels | existing | `/tires-wheels/#tire-rotation` | `/tires/` | ✅ | svc_tires |
| 58 | Wheel Balancing | Tires & Wheels | NEW | `—` | `/tires/` | ✅ | svc_tires |
| 59 | Wheels | Tires & Wheels | existing | `/tires-wheels/#wheels` | `/wheel-repair/` | queued | svc_tires (wheels) |
| 60 | Wheel Repair | Tires & Wheels | existing | `/tires-wheels/#wheel-repair` | `/wheel-repair/` | queued | svc_tires (wheels) |
| 61 | Auto Body Repair | Body, Glass & Imports | existing | `/body-pickup/#auto-body-repair` | `/auto-body-repair/` | queued | none |
| 62 | Rust Repair & Corrosion Control | Body, Glass & Imports | existing | `/body-pickup/#rust-repair-and-corrosion-control` | `/rust-repair/` | queued | svc_rust |
| 63 | Auto Glass Installation & Repair | Body, Glass & Imports | existing | `/body-pickup/#auto-glass-installation-and-repair` | `/auto-glass/` | queued | none |
| 64 | Window Tinting | Body, Glass & Imports | existing | `/body-pickup/#window-tinting` | `/window-tinting/` | queued | none |
| 65 | Windshield Wiper Replacement | Body, Glass & Imports | existing | `/body-pickup/#windshield-wiper-replacement` | `/auto-glass/` | queued | none |
| 66 | Imports | Body, Glass & Imports | existing | `/body-pickup/#imports` | `/import-car-repair/` | queued | none |
| 67 | Pick-up, Drop-off & After-Hours Arrangements | Body, Glass & Imports | renamed | `/body-pickup/#pick-up-and-delivery` | `/contact/#pickup` | n/a | n/a |

## Facts for Jerry to confirm

- Hours (directories disagree). Then set `hoursVerified`.
- Founded 1987; OIS station number M602; AMSOIL authorized retailer/installer (current status).
- Service-area towns beyond Primos, Secane, Clifton Heights.
- Engine: machine work in-house or sent out; replacement engines new, remanufactured or used.
- Transmission: rebuilds in-house or sent to a rebuilder; CVT and dual-clutch included or not.
- Brakes: caliper, line and hose work; drum brakes.
- After-hours drop-off and pick-up: how it works (key drop, hours, range).
- Hybrid: confirm the stated limit (no high-voltage battery, inverter, electric drive or software repairs).

## What was audited

**Diverse Auto Works (read only).** Content lives in Python modules (`tools/service_pages_batch1-8.py`, 26 records). Each record: key, slug, covers, primary/secondary keywords, page (title, desc, h1, lead, crumb), service type, body blocks (h2/h3/p/ul), 5-7 FAQs, CTA, search terms, sources, verify notes; every string is an EN/ES pair. Diverse-specific claims not carried over: ASE certification, towing, Chester County emissions wording, Phoenixville towns, forms, tracking tags, Cloudflare files.

**Scally's (before).** 42 services in 7 categories as anchors on category pages, English only, `baseUrl` placeholder `https://REPLACE-WITH-DOMAIN` in every canonical and in the sitemap, `AutoRepair` schema with unverified hours, 2 FAQs site-wide, no detailed service pages.

## How the system works

- `src/services.json`: categories and services. Each service has a stable `id` (its anchor), EN/ES `name` and `desc`, optional `faqs`, `new`, and `page` (the detailed page that covers it).
- `src/pages/<id>.json`: one detailed page. Body blocks are `["h2"|"h3"|"p", {en,es}, "anchor-id"]` or `["ul", [{en,es}, ...]]`. Links in text: `[label](svc:<service-id>)`, `[label](cat:<category-id>)`, `[label](url:https://...)`. Placeholders `{name}`, `{street}`, `{city}`, `{phone}`, `{since}` come from `site.config.json`. `verify` notes are never rendered.
- A service links to its detailed page only once that page file exists; until then it links to its category anchor, so nothing is orphaned and no thin pages go out.
- Build: `python3 src/build.py`. Check: `python3 tests/check_site.py`.

## Known limits

- `robots.txt` at `/scallys-auto-repair-website/robots.txt` is ignored by crawlers on a GitHub Pages project URL (robots.txt only counts at the host root). Submit `sitemap.xml` in Search Console instead until the custom domain is live.
- About, Reviews, Contact, Privacy, Sitemap and the home page are English only. On those pages the language switch goes to the Spanish services hub, and the Spanish navigation marks them `hreflang="en"`.
- The Spanish has not had a native-speaker review.
- The pilot pages cite no outside sources: the PennDOT FAQ could not be fetched from this session, so PA statements were kept to what the existing site already says (official station, emissions test for most Delaware County cars, brakes are part of the safety inspection).
- FAQPage markup is kept because it matches visible content; it does not earn FAQ rich results for a business like this.
