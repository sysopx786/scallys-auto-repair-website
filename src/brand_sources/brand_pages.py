# -*- coding: utf-8 -*-
"""
Dedicated brand pages (/brands/<brand>/), added Oct 30, 2026.

All 35 hub brands. US brands are defined here; Stellantis, mainstream foreign, luxury and Italian
brands are in bp_stellantis.py, bp_mainstream.py, bp_luxury.py and bp_italian.py.
Spec: diverse-autoworks-brand-pages-all.md (SEO fields, sources). Facts come from RepairPal,
the manufacturers' owner manuals / support pages and PennDOT-region sources listed there.

Rules followed:
- Only owner-confirmed services. No body work. Hybrids and EVs: basic work only (inspections, tires, alignments, brakes, suspension).
- Tesla: inspections, tires, brakes and suspension only (no high-voltage battery or software repairs).
- No phone number in page copy, no "call to confirm".
- Shop-practice claims that the owner has not confirmed are left out.

Spanish needs a native-speaker review (process rule in README).

Block types: ("h2", t), ("h3", t), ("p", t), ("ul", [t, ...]), ("table", (t, t), [(t, t), ...]).
Links in "p" text: [label](pagekey) or [label](pagekey#anchor). Page keys are build.SLUGS keys.
"""


def t(en, es):
    return {"en": en, "es": es}


# ------------------------------------------------------------------ shared lines
WARRANTY = t(
    "You don't need the dealer for routine service. Under federal law, a manufacturer or dealer can't deny your warranty coverage just because an independent shop did your routine maintenance. Keep your receipts from every service.",
    "No necesita ir al concesionario para el mantenimiento de rutina. Según la ley federal, un fabricante o concesionario no puede negarle la cobertura de la garantía solo porque un taller independiente hizo su mantenimiento de rutina. Guarde los recibos de cada servicio.")

PA_H3 = t("Pennsylvania state inspection", "Inspección estatal de Pennsylvania")
PA_P = t(
    "Pennsylvania requires an annual safety inspection. Vehicles registered in Chester and Montgomery counties also need an emissions test, done at the same visit. See [state inspections](inspections).",
    "Pennsylvania exige una inspección de seguridad anual. Los vehículos registrados en los condados de Chester y Montgomery también necesitan una prueba de emisiones, que se hace en la misma visita. Vea [inspecciones estatales](inspections).")

# Truck brands: PA emissions covers gas vehicles with a GVWR of 9,000 lb or less (67 Pa. Code 177.101),
# so heavy gas trucks and diesels need only the safety inspection. Fixed Oct 31, 2026.
PA_P_TRUCK = t(
    "Pennsylvania requires an annual safety inspection. Gas vehicles with a gross vehicle weight rating (GVWR) of 9,000 lb or less that are registered in Chester and Montgomery counties also need an emissions test, done at the same visit. Diesel trucks and heavier gas trucks need only the safety inspection. See [state inspections](inspections).",
    "Pennsylvania exige una inspección de seguridad anual. Los vehículos de gasolina con un peso bruto vehicular nominal (GVWR) de 9,000 lb o menos registrados en los condados de Chester y Montgomery también necesitan una prueba de emisiones, que se hace en la misma visita. Las camionetas diésel y las de gasolina más pesadas solo necesitan la inspección de seguridad. Vea [inspecciones estatales](inspections).")

INDUSTRY = t("compared with an industry average of about $652", "frente a un promedio de la industria de unos $652")


def faq_warranty(name):
    return (t(f"Will servicing my {name} at an independent shop void the warranty?",
              f"¿Pierdo la garantía de mi {name} si le doy servicio en un taller independiente?"),
            t("No. Under federal law, a manufacturer or dealer can't deny warranty coverage just because someone other than the dealer did your routine maintenance. Keep your receipts from every service.",
              "No. Según la ley federal, un fabricante o concesionario no puede negar la cobertura de la garantía solo porque alguien que no es el concesionario hizo su mantenimiento de rutina. Guarde los recibos de cada servicio."))


def cta(name, what_en="maintenance or repair", what_es="mantenimiento o reparación"):
    return [
        ("h2", t(f"Schedule {name} service near Phoenixville, PA", f"Programe servicio {name} cerca de Phoenixville, PA")),
        ("p", t(f"Contact Diverse Autoworks to schedule your next {name} {what_en} with an ASE-certified technician. [Request an appointment](contact#request) online.",
                f"Comuníquese con Diverse Autoworks para programar su próximo {what_es} {name} con un técnico certificado por ASE. [Solicite una cita](contact#request) en línea.")),
    ]


# common repair-list items
I_ENGINE = t("Check engine light diagnosis and engine repair", "Diagnóstico de la luz de revisión del motor y reparación del motor")
I_OIL = t("Oil changes, filters and belts", "Cambios de aceite, filtros y correas")
I_BRAKES = t("Brakes, rotors and brake fluid flush", "Frenos, rotores y cambio de líquido de frenos")
I_TIRES = t("Tires, rotation, balancing and alignments", "Llantas, rotación, balanceo y alineación")
I_COOL = t("Cooling system, water pump and thermostat", "Sistema de enfriamiento, bomba de agua y termostato")
I_CLIMATE = t("A/C, heater and cooling systems", "Aire acondicionado, calefacción y sistemas de enfriamiento")
I_ELEC = t("Batteries, alternators and starters", "Baterías, alternadores y motores de arranque")
I_EXHAUST = t("Exhaust, catalytic converters and oxygen sensors", "Escape, convertidores catalíticos y sensores de oxígeno")
I_DRIVE = t("Transmission maintenance, differential repair, rear-axle bearings and seals",
            "Mantenimiento de la transmisión, reparación del diferencial, baleros y sellos del eje trasero")

GM_ROWS = [
    (t("Change oil when the Oil Life System calls for it", "Cambie el aceite cuando lo indique el Oil Life System"),
     t("Watch for the reminder on your dash", "Esté atento al aviso en el tablero")),
    (t("Change oil and filter at least once a year", "Cambie el aceite y el filtro al menos una vez al año"),
     t("Low-mileage vehicles still need a yearly change", "Los vehículos con poco millaje también necesitan un cambio anual")),
    (t("Reset the system after each oil change", "Reinicie el sistema después de cada cambio de aceite"),
     t("Without a reset, the next reminder is wrong", "Sin reiniciarlo, el siguiente aviso será incorrecto")),
]
GM_HEAD = (t("GM's guidance", "Indicación de GM"), t("What it means for you", "Qué significa para usted"))

# ------------------------------------------------------------------ pages
BRAND_PAGES = [
    # ============================================================ FORD
    {"key": "brand_ford", "slug": "brands/ford", "name": "Ford",
     "page": {
         "title": t("Ford Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Ford en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Ford truck, SUV and car repair in Phoenixville, PA: oil-life monitor service, brakes, engine repair and fleet work by ASE-certified technicians.",
                   "Reparación de camionetas, SUV y autos Ford en Phoenixville, PA: monitor de vida del aceite, frenos, motor y flotas, con técnicos certificados por ASE."),
         "h1": t("Ford Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Ford en Phoenixville, PA"),
         "lead": t("Ford builds the F-Series, the best-selling truck line in the US for decades, along with the Ranger, Maverick, Bronco, Explorer, Escape, Expedition, Mustang and Transit van. Our ASE-certified technicians service Ford trucks, SUVs, cars and vans.",
                   "Ford fabrica la Serie F, la línea de camionetas más vendida en EE. UU. desde hace décadas, además de la Ranger, Maverick, Bronco, Explorer, Escape, Expedition, Mustang y la van Transit. Nuestros técnicos certificados por ASE dan servicio a camionetas, SUV, autos y vans Ford."),
         "crumb": t("Ford", "Ford")},
     "service_type": t("Ford repair and maintenance", "Reparación y mantenimiento de vehículos Ford"),
     "search": ("ford f-150 f-series super duty ranger maverick bronco explorer escape expedition mustang transit oil life monitor",
                "ford f-150 serie f super duty ranger maverick bronco explorer escape expedition mustang transit monitor vida aceite"),
     "blocks": [
         ("h2", t("Ford service in Phoenixville, PA", "Servicio Ford en Phoenixville, PA")),
         ("p", t("Trucks and SUVs that tow, haul or idle for long stretches wear faster than the same vehicle driven gently. Ford's oil-life monitor accounts for that, and the rest of your maintenance should too.",
                 "Las camionetas y SUV que remolcan, cargan peso o pasan mucho tiempo en ralentí se desgastan más rápido que el mismo vehículo manejado con suavidad. El monitor de vida del aceite de Ford lo toma en cuenta, y el resto del mantenimiento también debe hacerlo.")),
         ("p", t("Running Fords for a business? See our [fleet repairs](fleet).", "¿Usa vehículos Ford en su negocio? Vea nuestras [reparaciones para flotas](fleet).")),
         ("p", WARRANTY),
         ("h2", t("Ford maintenance schedule: the Intelligent Oil-Life Monitor", "Calendario de mantenimiento Ford: el monitor inteligente de vida del aceite")),
         ("p", t("Most newer Fords use the Intelligent Oil-Life Monitor. It calculates oil life from how you drive and shows a message when an oil change is due.",
                 "La mayoría de los Ford recientes usan el Intelligent Oil-Life Monitor. Calcula la vida del aceite según cómo maneja y muestra un mensaje cuando toca el cambio de aceite.")),
         ("table", (t("Situation", "Situación"), t("Ford's guidance", "Indicación de Ford")), [
             (t("Normal driving", "Manejo normal"), t("Oil change when the message appears, up to 1 year or 10,000 miles", "Cambio de aceite cuando aparece el mensaje, hasta 1 año o 10,000 millas")),
             (t("After the message appears", "Después de que aparece el mensaje"), t("Change the oil within 2 weeks or 500 miles", "Cambie el aceite dentro de 2 semanas o 500 millas")),
             (t("Towing, heavy idling, short trips, cold weather", "Remolque, mucho ralentí, viajes cortos, clima frío"), t("The monitor shortens the interval on its own", "El monitor acorta el intervalo por sí solo")),
             (t("Monitor reset incorrectly or not working", "Monitor mal reiniciado o sin funcionar"), t("Fall back to every 6 months or 5,000 miles", "Vuelva a cada 6 meses o 5,000 millas")),
         ]),
         ("h3", t("The monitor must be reset", "El monitor debe reiniciarse")),
         ("p", t("The monitor has to be reset after every oil change so the next reminder is accurate.",
                 "El monitor debe reiniciarse después de cada cambio de aceite para que el siguiente aviso sea correcto.")),
         ("h3", PA_H3), ("p", PA_P_TRUCK),
         ("h2", t("Ford repair in Phoenixville, PA", "Reparación Ford en Phoenixville, PA")),
         ("p", t("Ford work we do:", "Trabajos que hacemos en vehículos Ford:")),
         ("ul", [t("Check engine light diagnosis and engine repair, including EcoBoost engines", "Diagnóstico de la luz de revisión del motor y reparación del motor, incluidos los motores EcoBoost"),
                 I_OIL, I_DRIVE, t("CV axles and joints", "Ejes CV y juntas"), I_BRAKES,
                 t("Steering and suspension, ball joints, power steering and wheel bearings", "Dirección y suspensión, rótulas, dirección asistida y baleros de rueda"),
                 I_TIRES, I_ELEC, I_COOL, I_EXHAUST]),
         ("p", t("Ford hybrids, such as the Maverick Hybrid and F-150 PowerBoost: we do basic work, such as state inspections, tires, alignments, brakes and suspension. We don't repair hybrid batteries or high-voltage systems.",
                 "Híbridos Ford, como la Maverick Hybrid y la F-150 PowerBoost: hacemos trabajos básicos, como inspecciones estatales, llantas, alineación, frenos y suspensión. No reparamos baterías híbridas ni sistemas de alto voltaje.")),
         ("p", t("Lincoln is Ford's luxury brand; see [Lincoln repair](brand_lincoln). See all our [auto repair services](services).",
                 "Lincoln es la marca de lujo de Ford; vea [reparación Lincoln](brand_lincoln). Vea todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Ford maintenance", "Costo promedio del mantenimiento Ford")),
         ("p", t("Fords average about $775 a year in repair and maintenance costs, according to RepairPal, compared with an industry average of about $652.",
                 "Los Ford promedian unos $775 al año en costos de reparación y mantenimiento, según RepairPal, frente a un promedio de la industria de unos $652.")),
         ("p", t("Costs vary widely by model. RepairPal lists the Focus at $569 a year and the F-150 at $788.",
                 "Los costos varían mucho según el modelo. RepairPal indica $569 al año para el Focus y $788 para la F-150.")),
         ("p", t("For work trucks, downtime can cost more than the repair itself. Following the oil-life monitor and inspecting brakes and cooling systems on schedule lowers the risk of a breakdown on the job.",
                 "En las camionetas de trabajo, el tiempo fuera de servicio puede costar más que la propia reparación. Seguir el monitor de vida del aceite y revisar a tiempo los frenos y el sistema de enfriamiento reduce el riesgo de una avería en el trabajo.")),
         ("h2", t("How reliable are Fords?", "¿Qué tan confiables son los Ford?")),
         ("p", t("RepairPal rates Ford 3.5 out of 5 for reliability, 21st out of 32 car brands, based on the cost, frequency and severity of real repairs.",
                 "RepairPal califica a Ford con 3.5 de 5 en confiabilidad, en el lugar 21 de 32 marcas, según el costo, la frecuencia y la gravedad de reparaciones reales.")),
         ("p", t("How you drive matters. Towing and heavy idling shorten oil life, and the oil-life monitor adjusts for it.",
                 "Su forma de manejar importa. Remolcar y dejar el motor mucho tiempo en ralentí acortan la vida del aceite, y el monitor se ajusta a eso.")),
     ], "cta": cta("Ford"),
     "faq": [
         (t("How often does my Ford need an oil change?", "¿Cada cuánto necesita mi Ford un cambio de aceite?"),
          t("When the Intelligent Oil-Life Monitor says so. Under normal driving, Ford's maximum is 1 year or 10,000 miles, whichever comes first.",
            "Cuando lo indique el Intelligent Oil-Life Monitor. Con manejo normal, el máximo de Ford es 1 año o 10,000 millas, lo que ocurra primero.")),
         (t("What should I do when the oil change message appears?", "¿Qué hago cuando aparece el aviso de cambio de aceite?"),
          t("Ford says to change the oil within 2 weeks or 500 miles of the message appearing.",
            "Ford indica cambiar el aceite dentro de 2 semanas o 500 millas después de que aparece el mensaje.")),
         (t("What happens if the oil-life monitor isn't reset?", "¿Qué pasa si no se reinicia el monitor de vida del aceite?"),
          t("Ford says the monitor falls back to a 6-month or 5,000-mile interval if it was reset early, wasn't reset at an oil change, or isn't working.",
            "Según Ford, el monitor vuelve a un intervalo de 6 meses o 5,000 millas si se reinició antes de tiempo, no se reinició en un cambio de aceite o no funciona.")),
         (t("Do you work on Ford work trucks and fleet vehicles?", "¿Trabajan en camionetas de trabajo y vehículos de flota Ford?"),
          t("Yes. We service Ford trucks and vans, and we offer fleet repairs for businesses.",
            "Sí. Damos servicio a camionetas y vans Ford, y ofrecemos reparaciones para flotas.")),
         faq_warranty("Ford"),
     ]},

    # ============================================================ LINCOLN
    {"key": "brand_lincoln", "slug": "brands/lincoln", "name": "Lincoln",
     "page": {
         "title": t("Lincoln Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Lincoln en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Lincoln service in Phoenixville, PA: oil-life monitor maintenance, brakes, suspension and engine repair for Corsair, Nautilus, Aviator and Navigator.",
                   "Servicio Lincoln en Phoenixville, PA: monitor de vida del aceite, frenos, suspensión y motor para Corsair, Nautilus, Aviator y Navigator."),
         "h1": t("Lincoln Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Lincoln en Phoenixville, PA"),
         "lead": t("Lincoln is Ford's luxury brand, building the Corsair, Nautilus, Aviator and Navigator, and before them the MKZ and Continental sedans. Our ASE-certified technicians service Lincoln SUVs and sedans.",
                   "Lincoln es la marca de lujo de Ford y fabrica los Corsair, Nautilus, Aviator y Navigator, y antes los sedanes MKZ y Continental. Nuestros técnicos certificados por ASE dan servicio a SUV y sedanes Lincoln."),
         "crumb": t("Lincoln", "Lincoln")},
     "service_type": t("Lincoln repair and maintenance", "Reparación y mantenimiento de vehículos Lincoln"),
     "search": ("lincoln corsair nautilus aviator navigator mkz continental oil life monitor",
                "lincoln corsair nautilus aviator navigator mkz continental monitor vida aceite"),
     "blocks": [
         ("h2", t("Lincoln service in Phoenixville, PA", "Servicio Lincoln en Phoenixville, PA")),
         ("p", t("Lincolns share much of their engineering with Ford, including the Intelligent Oil-Life Monitor that sets your oil change schedule.",
                 "Los Lincoln comparten gran parte de su ingeniería con Ford, incluido el Intelligent Oil-Life Monitor que fija su calendario de cambios de aceite.")),
         ("p", WARRANTY),
         ("h2", t("Lincoln maintenance schedule: the Intelligent Oil-Life Monitor", "Calendario de mantenimiento Lincoln: el monitor inteligente de vida del aceite")),
         ("table", (t("Situation", "Situación"), t("Lincoln's guidance", "Indicación de Lincoln")), [
             (t("Normal driving", "Manejo normal"), t("Change the oil when the message appears; never exceed 1 year or 10,000 miles", "Cambie el aceite cuando aparezca el mensaje; nunca más de 1 año o 10,000 millas")),
             (t("After the message appears", "Después de que aparece el mensaje"), t("Change the oil within 2 weeks or 500 miles", "Cambie el aceite dentro de 2 semanas o 500 millas")),
             (t("Towing, idling, short trips, cold weather", "Remolque, ralentí, viajes cortos, clima frío"), t("The monitor shortens the interval on its own", "El monitor acorta el intervalo por sí solo")),
         ]),
         ("h3", t("Reset after every oil change", "Reinicio después de cada cambio de aceite")),
         ("p", t("The monitor has to be reset after each oil change, or the next reminder will be wrong.",
                 "El monitor debe reiniciarse después de cada cambio de aceite; si no, el siguiente aviso será incorrecto.")),
         ("h3", PA_H3), ("p", PA_P),
         ("h2", t("Lincoln repair in Phoenixville, PA", "Reparación Lincoln en Phoenixville, PA")),
         ("p", t("Lincoln work we do:", "Trabajos que hacemos en vehículos Lincoln:")),
         ("ul", [I_ENGINE, I_OIL, I_BRAKES,
                 t("Steering and suspension: shocks, struts, control arms and ball joints", "Dirección y suspensión: amortiguadores, puntales, brazos de control y rótulas"),
                 t("Wheel bearings and hubs", "Baleros y mazas de rueda"),
                 t("Transmission maintenance and CV axles", "Mantenimiento de la transmisión y ejes CV"),
                 I_CLIMATE, I_ELEC, I_EXHAUST]),
         ("p", t("Lincoln shares many parts with Ford; see [Ford repair](brand_ford). See all our [auto repair services](services).",
                 "Lincoln comparte muchas piezas con Ford; vea [reparación Ford](brand_ford). Vea todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Lincoln maintenance", "Costo promedio del mantenimiento Lincoln")),
         ("p", t("Lincolns average about $879 a year in repair and maintenance costs, according to RepairPal, compared with an industry average of about $652.",
                 "Los Lincoln promedian unos $879 al año en costos de reparación y mantenimiento, según RepairPal, frente a un promedio de la industria de unos $652.")),
         ("p", t("Following the oil-life monitor and keeping up with brakes, tires and fluids keeps those costs predictable.",
                 "Seguir el monitor de vida del aceite y mantener al día frenos, llantas y líquidos hace que esos costos sean más predecibles.")),
         ("h2", t("How reliable are Lincolns?", "¿Qué tan confiables son los Lincoln?")),
         ("p", t("RepairPal rates Lincoln 3.0 out of 5 for reliability, 24th out of 32 car brands. Lincolns average 0.4 unscheduled shop visits a year, and 15% of repairs are severe.",
                 "RepairPal califica a Lincoln con 3.0 de 5 en confiabilidad, en el lugar 24 de 32 marcas. Los Lincoln promedian 0.4 visitas no programadas al taller por año, y el 15% de las reparaciones son graves.")),
     ], "cta": cta("Lincoln"),
     "faq": [
         (t("How often does a Lincoln need an oil change?", "¿Cada cuánto necesita un Lincoln un cambio de aceite?"),
          t("When the Intelligent Oil-Life Monitor shows the message. Lincoln says never to go more than 1 year or 10,000 miles between oil changes.",
            "Cuando el Intelligent Oil-Life Monitor muestre el mensaje. Lincoln indica no pasar nunca de 1 año o 10,000 millas entre cambios de aceite.")),
         (t("What happens if the oil-life monitor isn't reset?", "¿Qué pasa si no se reinicia el monitor de vida del aceite?"),
          t("The monitor won't know the oil was changed, so the next reminder comes at the wrong time.",
            "El monitor no sabrá que se cambió el aceite, así que el siguiente aviso llegará en el momento equivocado.")),
         (t("Is a Lincoln the same as a Ford underneath?", "¿Un Lincoln es igual a un Ford por dentro?"),
          t("Many Lincolns share platforms and parts with Ford models, such as the Navigator and the Ford Expedition. Trim, equipment and some parts differ.",
            "Muchos Lincoln comparten plataformas y piezas con modelos Ford, como el Navigator y la Ford Expedition. Los acabados, el equipamiento y algunas piezas son distintos.")),
         (t("Do you service the Lincoln Navigator?", "¿Dan servicio al Lincoln Navigator?"),
          t("Yes. We service Lincoln SUVs, including the Navigator, Aviator, Nautilus and Corsair.",
            "Sí. Damos servicio a las SUV Lincoln, incluidos los Navigator, Aviator, Nautilus y Corsair.")),
         faq_warranty("Lincoln"),
     ]},

    # ============================================================ CHEVROLET
    {"key": "brand_chevrolet", "slug": "brands/chevrolet", "name": "Chevrolet",
     "page": {
         "title": t("Chevrolet Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Chevrolet en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Chevy truck, SUV and car repair in Phoenixville, PA: oil life system service, brakes, suspension, engine repair and fleet work by ASE-certified techs.",
                   "Reparación de camionetas, SUV y autos Chevrolet en Phoenixville, PA: sistema de vida del aceite, frenos, suspensión, motor y flotas."),
         "h1": t("Chevrolet Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Chevrolet en Phoenixville, PA"),
         "lead": t("Chevrolet builds the Silverado and Colorado pickups, the Trax, Equinox, Blazer, Traverse, Tahoe and Suburban SUVs, and, until recently, the Malibu sedan. Our ASE-certified technicians service Chevrolet trucks, SUVs and cars, including work and fleet vehicles.",
                   "Chevrolet fabrica las camionetas Silverado y Colorado, las SUV Trax, Equinox, Blazer, Traverse, Tahoe y Suburban y, hasta hace poco, el sedán Malibu. Nuestros técnicos certificados por ASE dan servicio a camionetas, SUV y autos Chevrolet, incluidos vehículos de trabajo y de flota."),
         "crumb": t("Chevrolet", "Chevrolet")},
     "service_type": t("Chevrolet repair and maintenance", "Reparación y mantenimiento de vehículos Chevrolet"),
     "search": ("chevrolet chevy silverado colorado equinox traverse tahoe suburban trax blazer malibu oil life",
                "chevrolet chevy silverado colorado equinox traverse tahoe suburban trax blazer malibu vida aceite"),
     "blocks": [
         ("h2", t("Chevrolet service in Phoenixville, PA", "Servicio Chevrolet en Phoenixville, PA")),
         ("p", t("Most Chevrolets use the Engine Oil Life System. Chevrolet says it factors in speed, engine temperature, driving style and local weather to decide when your oil needs changing.",
                 "La mayoría de los Chevrolet usan el sistema de vida del aceite del motor (Engine Oil Life System). Según Chevrolet, toma en cuenta la velocidad, la temperatura del motor, su forma de manejar y el clima local para decidir cuándo cambiar el aceite.")),
         ("p", WARRANTY),
         ("h2", t("Chevrolet maintenance schedule: the Oil Life System", "Calendario de mantenimiento Chevrolet: el sistema de vida del aceite")),
         ("table", (t("What Chevrolet says", "Lo que indica Chevrolet"), t("What it means for you", "Qué significa para usted")), [
             (t("The Oil Life System tells you when an oil change is due", "El sistema le avisa cuándo toca el cambio de aceite"), t("Change the oil when the reminder appears", "Cambie el aceite cuando aparezca el aviso")),
             (t("Oil and filter must be changed at least once a year", "El aceite y el filtro deben cambiarse al menos una vez al año"), t("Even with low mileage, change it yearly", "Aunque maneje poco, cámbielo cada año")),
             (t("The system must be reset after each change", "El sistema debe reiniciarse después de cada cambio"), t("Without a reset, the next reminder is wrong", "Sin reiniciarlo, el siguiente aviso será incorrecto")),
         ]),
         ("p", t("Under easy driving, the system may not call for service for more than a year, which is why the once-a-year rule matters. Your owner's manual lists the tire rotation and other intervals for your model.",
                 "Con un manejo suave, el sistema puede no pedir servicio en más de un año; por eso importa la regla de una vez al año. El manual del propietario indica la rotación de llantas y los demás intervalos de su modelo.")),
         ("h3", PA_H3), ("p", PA_P_TRUCK),
         ("h2", t("Chevrolet repair in Phoenixville, PA", "Reparación Chevrolet en Phoenixville, PA")),
         ("p", t("Chevrolet work we do:", "Trabajos que hacemos en vehículos Chevrolet:")),
         ("ul", [I_ENGINE, I_OIL, I_BRAKES, I_TIRES,
                 t("Steering and suspension, ball joints and wheel bearings", "Dirección y suspensión, rótulas y baleros de rueda"),
                 I_DRIVE, I_COOL, I_ELEC, I_EXHAUST]),
         ("p", t("Running Chevy trucks or vans for a business? See our [fleet repairs](fleet). GMC trucks share much of their engineering; see [GMC repair](brand_gmc). See all our [auto repair services](services).",
                 "¿Usa camionetas o vans Chevrolet en su negocio? Vea nuestras [reparaciones para flotas](fleet). Las camionetas GMC comparten gran parte de su ingeniería; vea [reparación GMC](brand_gmc). Vea todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Chevrolet maintenance", "Costo promedio del mantenimiento Chevrolet")),
         ("p", t("Chevrolets average about $649 a year in repair and maintenance costs, according to RepairPal, right at the industry average of about $652.",
                 "Los Chevrolet promedian unos $649 al año en costos de reparación y mantenimiento, según RepairPal, casi igual al promedio de la industria de unos $652.")),
         ("p", t("Trucks and full-size SUVs that tow or haul usually cost more to maintain than smaller crossovers.",
                 "Las camionetas y SUV grandes que remolcan o cargan peso suelen costar más de mantener que las SUV pequeñas.")),
         ("h2", t("How reliable are Chevrolets?", "¿Qué tan confiables son los Chevrolet?")),
         ("p", t("RepairPal rates Chevrolet 3.5 out of 5 for reliability, 20th out of 32 car brands. The average Chevy visits a shop about 0.3 times a year for unscheduled repairs, and 15% of repairs are severe.",
                 "RepairPal califica a Chevrolet con 3.5 de 5 en confiabilidad, en el lugar 20 de 32 marcas. El Chevrolet promedio va al taller unas 0.3 veces al año por reparaciones no programadas, y el 15% de las reparaciones son graves.")),
     ], "cta": cta("Chevrolet"),
     "faq": [
         (t("How often does a Chevy need an oil change?", "¿Cada cuánto necesita un Chevrolet un cambio de aceite?"),
          t("When the Oil Life System says so, and at least once a year, according to Chevrolet.",
            "Cuando lo indique el sistema de vida del aceite, y al menos una vez al año, según Chevrolet.")),
         (t("My Chevy's oil life still shows a high percentage after a year. Do I still need an oil change?",
            "Mi Chevrolet todavía muestra un porcentaje alto de vida del aceite después de un año. ¿Igual necesito el cambio?"),
          t("Yes. Chevrolet says the oil and filter must be changed at least once a year, even if the system hasn't called for it.",
            "Sí. Chevrolet indica que el aceite y el filtro deben cambiarse al menos una vez al año, aunque el sistema no lo haya pedido.")),
         (t("What does the Chevrolet Oil Life System look at?", "¿Qué toma en cuenta el sistema de vida del aceite de Chevrolet?"),
          t("Chevrolet says it factors in speed, engine temperature, driving style and local weather.",
            "Según Chevrolet, toma en cuenta la velocidad, la temperatura del motor, su forma de manejar y el clima local.")),
         (t("Do you work on Silverado and Colorado pickups?", "¿Trabajan en camionetas Silverado y Colorado?"),
          t("Yes. We service Chevy pickups, including brakes, suspension, differential repair and transmission maintenance.",
            "Sí. Damos servicio a camionetas Chevrolet, incluidos frenos, suspensión, reparación del diferencial y mantenimiento de la transmisión.")),
         (t("Do you repair Chevy work trucks and fleet vehicles?", "¿Reparan camionetas de trabajo y vehículos de flota Chevrolet?"),
          t("Yes. We offer fleet repairs for businesses running Chevrolet trucks and vans.",
            "Sí. Ofrecemos reparaciones para flotas a negocios con camionetas y vans Chevrolet.")),
     ]},

    # ============================================================ GMC
    {"key": "brand_gmc", "slug": "brands/gmc", "name": "GMC",
     "page": {
         "title": t("GMC Repair in Phoenixville, PA | Diverse Autoworks", "Reparación GMC en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("GMC Sierra, Canyon, Yukon, Acadia and Terrain repair in Phoenixville, PA: oil life service, brakes, suspension and differential work.",
                   "Reparación GMC Sierra, Canyon, Yukon, Acadia y Terrain en Phoenixville, PA: vida del aceite, frenos, suspensión y diferenciales."),
         "h1": t("GMC Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento GMC en Phoenixville, PA"),
         "lead": t("GMC builds trucks and SUVs: the Sierra and Canyon pickups and the Yukon, Acadia and Terrain. Many of them tow and haul. Our ASE-certified technicians service GMC trucks and SUVs.",
                   "GMC fabrica camionetas y SUV: las pickups Sierra y Canyon y las Yukon, Acadia y Terrain. Muchas remolcan y cargan peso. Nuestros técnicos certificados por ASE dan servicio a camionetas y SUV GMC."),
         "crumb": t("GMC", "GMC")},
     "service_type": t("GMC repair and maintenance", "Reparación y mantenimiento de vehículos GMC"),
     "search": ("gmc sierra canyon yukon acadia terrain truck towing oil life brakes differential",
                "gmc sierra canyon yukon acadia terrain camioneta remolque vida aceite frenos diferencial"),
     "blocks": [
         ("h2", t("GMC service in Phoenixville, PA", "Servicio GMC en Phoenixville, PA")),
         ("p", t("GMC is part of General Motors, and most GMCs use GM's Engine Oil Life System to set the oil change schedule. Towing, heavy loads and idling shorten oil life, and the system adjusts for it.",
                 "GMC es parte de General Motors, y la mayoría de los GMC usan el sistema de vida del aceite de GM para fijar los cambios de aceite. Remolcar, cargar peso y el ralentí acortan la vida del aceite, y el sistema se ajusta a eso.")),
         ("p", WARRANTY),
         ("h2", t("GMC maintenance schedule", "Calendario de mantenimiento GMC")),
         ("table", GM_HEAD, GM_ROWS),
         ("p", t("Your owner's manual lists tire rotation, transmission and differential fluid intervals for your truck. Towing and plowing usually call for the shorter, severe-service intervals.",
                 "El manual del propietario indica los intervalos de rotación de llantas y de líquidos de transmisión y diferencial de su camioneta. Remolcar y quitar nieve suelen requerir los intervalos más cortos de servicio severo.")),
         ("h3", PA_H3), ("p", PA_P_TRUCK),
         ("h2", t("GMC repair in Phoenixville, PA", "Reparación GMC en Phoenixville, PA")),
         ("p", t("GMC work we do:", "Trabajos que hacemos en vehículos GMC:")),
         ("ul", [I_ENGINE, I_BRAKES, I_DRIVE,
                 t("Transmission maintenance and CV axles", "Mantenimiento de la transmisión y ejes CV"),
                 t("Steering and suspension: shocks, struts, ball joints and tie rods", "Dirección y suspensión: amortiguadores, puntales, rótulas y terminales"),
                 I_TIRES, I_COOL, I_ELEC, I_EXHAUST]),
         ("p", t("GMC and Chevrolet trucks share much of their engineering; see [Chevrolet repair](brand_chevrolet), or our [fleet repairs](fleet) for business trucks.",
                 "Las camionetas GMC y Chevrolet comparten gran parte de su ingeniería; vea [reparación Chevrolet](brand_chevrolet), o nuestras [reparaciones para flotas](fleet) para camionetas de negocio.")),
         ("h2", t("Average cost of GMC maintenance", "Costo promedio del mantenimiento GMC")),
         ("p", t("GMCs average about $744 a year in repair and maintenance costs, according to RepairPal, compared with an industry average of about $652. A lineup of trucks and large SUVs explains much of that.",
                 "Los GMC promedian unos $744 al año en costos de reparación y mantenimiento, según RepairPal, frente a un promedio de la industria de unos $652. Una línea de camionetas y SUV grandes explica buena parte de eso.")),
         ("h2", t("How reliable are GMCs?", "¿Qué tan confiables son los GMC?")),
         ("p", t("RepairPal rates GMC 3.0 out of 5 for reliability, 22nd out of 32 car brands. GMCs average 0.3 unscheduled shop visits a year, and 17% of repairs are severe, so catching problems early matters.",
                 "RepairPal califica a GMC con 3.0 de 5 en confiabilidad, en el lugar 22 de 32 marcas. Los GMC promedian 0.3 visitas no programadas al taller por año, y el 17% de las reparaciones son graves; por eso importa detectar los problemas a tiempo.")),
     ], "cta": cta("GMC"),
     "faq": [
         (t("How often does a GMC need an oil change?", "¿Cada cuánto necesita un GMC un cambio de aceite?"),
          t("When the Oil Life System calls for it, and at least once a year.",
            "Cuando lo indique el sistema de vida del aceite, y al menos una vez al año.")),
         (t("Does towing change my GMC's maintenance schedule?", "¿Remolcar cambia el calendario de mantenimiento de mi GMC?"),
          t("Yes. Towing and heavy loads shorten oil life, and the Oil Life System adjusts. Your owner's manual lists shorter intervals for other fluids under severe use.",
            "Sí. Remolcar y cargar peso acortan la vida del aceite, y el sistema se ajusta. El manual del propietario indica intervalos más cortos para otros líquidos con uso severo.")),
         (t("Do you repair GMC differentials?", "¿Reparan diferenciales GMC?"),
          t("Yes. We repair differentials and do related axle work, including rear-axle bearings and seals.",
            "Sí. Reparamos diferenciales y hacemos trabajos de ejes relacionados, incluidos baleros y sellos del eje trasero.")),
         (t("Are GMC and Chevy trucks the same?", "¿Las camionetas GMC y Chevrolet son iguales?"),
          t("The GMC Sierra and Chevrolet Silverado share much of their engineering, but trim, styling and some equipment differ.",
            "La GMC Sierra y la Chevrolet Silverado comparten gran parte de su ingeniería, pero los acabados, el diseño y parte del equipamiento son distintos.")),
         (t("Do you service GMC fleet trucks?", "¿Dan servicio a camionetas GMC de flota?"),
          t("Yes. We offer fleet repairs for business vehicles.", "Sí. Ofrecemos reparaciones para flotas de vehículos de negocio.")),
     ]},

    # ============================================================ BUICK
    {"key": "brand_buick", "slug": "brands/buick", "name": "Buick",
     "page": {
         "title": t("Buick Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Buick en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Buick Encore GX, Envista, Envision and Enclave repair in Phoenixville, PA: oil life service, brakes, A/C and engine repair by ASE-certified techs.",
                   "Reparación Buick Encore GX, Envista, Envision y Enclave en Phoenixville, PA: vida del aceite, frenos, aire acondicionado y motor."),
         "h1": t("Buick Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Buick en Phoenixville, PA"),
         "lead": t("Buick's lineup today is SUVs: the Envista, Encore GX, Envision and Enclave, plus older LaCrosse and Regal sedans still on the road. Our ASE-certified technicians service Buick SUVs and sedans.",
                   "Hoy la línea de Buick son SUV: Envista, Encore GX, Envision y Enclave, además de sedanes LaCrosse y Regal más antiguos que siguen en circulación. Nuestros técnicos certificados por ASE dan servicio a SUV y sedanes Buick."),
         "crumb": t("Buick", "Buick")},
     "service_type": t("Buick repair and maintenance", "Reparación y mantenimiento de vehículos Buick"),
     "search": ("buick encore gx envista envision enclave lacrosse regal oil life",
                "buick encore gx envista envision enclave lacrosse regal vida aceite"),
     "blocks": [
         ("h2", t("Buick service in Phoenixville, PA", "Servicio Buick en Phoenixville, PA")),
         ("p", t("Buick is part of General Motors, and most Buicks use GM's Engine Oil Life System. It sets your oil change schedule based on how you drive, and it needs resetting after every change.",
                 "Buick es parte de General Motors, y la mayoría de los Buick usan el sistema de vida del aceite de GM. Fija sus cambios de aceite según cómo maneja y debe reiniciarse después de cada cambio.")),
         ("p", WARRANTY),
         ("h2", t("Buick maintenance schedule", "Calendario de mantenimiento Buick")),
         ("table", GM_HEAD, GM_ROWS),
         ("p", t("Your owner's manual lists tire rotation, cabin filter and other intervals for your model.",
                 "El manual del propietario indica la rotación de llantas, el filtro de cabina y los demás intervalos de su modelo.")),
         ("h3", PA_H3), ("p", PA_P),
         ("h2", t("Buick repair in Phoenixville, PA", "Reparación Buick en Phoenixville, PA")),
         ("p", t("Buick work we do:", "Trabajos que hacemos en vehículos Buick:")),
         ("ul", [I_ENGINE, t("Oil changes, cabin air filters and belts", "Cambios de aceite, filtros de aire de cabina y correas"), I_BRAKES,
                 t("Steering and suspension, shocks and struts", "Dirección y suspensión, amortiguadores y puntales"),
                 I_CLIMATE, I_ELEC, I_TIRES, I_EXHAUST]),
         ("p", t("Buick shares engineering with other GM brands; see [Chevrolet repair](brand_chevrolet) and all our [auto repair services](services).",
                 "Buick comparte ingeniería con otras marcas de GM; vea [reparación Chevrolet](brand_chevrolet) y todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Buick maintenance", "Costo promedio del mantenimiento Buick")),
         ("p", t("Buicks average about $608 a year in repair and maintenance costs, according to RepairPal, below the industry average of about $652.",
                 "Los Buick promedian unos $608 al año en costos de reparación y mantenimiento, según RepairPal, por debajo del promedio de la industria de unos $652.")),
         ("h2", t("How reliable are Buicks?", "¿Qué tan confiables son los Buick?")),
         ("p", t("RepairPal rates Buick 3.5 out of 5 for reliability, 13th out of 32 car brands, the highest of the GM brands. Buicks average 0.3 unscheduled shop visits a year, and 13% of repairs are severe.",
                 "RepairPal califica a Buick con 3.5 de 5 en confiabilidad, en el lugar 13 de 32 marcas, el mejor de las marcas de GM. Los Buick promedian 0.3 visitas no programadas al taller por año, y el 13% de las reparaciones son graves.")),
     ], "cta": cta("Buick"),
     "faq": [
         (t("How often does a Buick need an oil change?", "¿Cada cuánto necesita un Buick un cambio de aceite?"),
          t("When the Oil Life System calls for it, and at least once a year, per GM's guidance.",
            "Cuando lo indique el sistema de vida del aceite, y al menos una vez al año, según GM.")),
         (t("How reliable are Buicks compared with other GM brands?", "¿Qué tan confiables son los Buick frente a otras marcas de GM?"),
          t("RepairPal ranks Buick 13th out of 32 brands, ahead of Chevrolet (20th), GMC (22nd) and Cadillac (26th).",
            "RepairPal coloca a Buick en el lugar 13 de 32 marcas, por delante de Chevrolet (20), GMC (22) y Cadillac (26).")),
         (t("Do you fix Buick A/C and heat?", "¿Reparan el aire acondicionado y la calefacción de Buick?"),
          t("Yes. We service A/C, heaters and cooling systems.", "Sí. Damos servicio al aire acondicionado, la calefacción y los sistemas de enfriamiento.")),
         (t("Do you work on older Buick sedans like the LaCrosse?", "¿Trabajan en sedanes Buick más antiguos, como el LaCrosse?"),
          t("Yes. We service Buick sedans as well as SUVs.", "Sí. Damos servicio a sedanes Buick y también a SUV.")),
         faq_warranty("Buick"),
     ]},

    # ============================================================ CADILLAC
    {"key": "brand_cadillac", "slug": "brands/cadillac", "name": "Cadillac",
     "page": {
         "title": t("Cadillac Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Cadillac en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Cadillac Escalade, XT4, XT5, XT6, CT4 and CT5 service in Phoenixville, PA: oil life system service, brakes, suspension and engine repair.",
                   "Servicio Cadillac Escalade, XT4, XT5, XT6, CT4 y CT5 en Phoenixville, PA: vida del aceite, frenos, suspensión y reparación del motor."),
         "h1": t("Cadillac Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Cadillac en Phoenixville, PA"),
         "lead": t("Cadillac is General Motors' luxury brand: the Escalade, the XT4, XT5 and XT6 SUVs and the CT4 and CT5 sedans. Our ASE-certified technicians service Cadillac SUVs and sedans.",
                   "Cadillac es la marca de lujo de General Motors: la Escalade, las SUV XT4, XT5 y XT6 y los sedanes CT4 y CT5. Nuestros técnicos certificados por ASE dan servicio a SUV y sedanes Cadillac."),
         "crumb": t("Cadillac", "Cadillac")},
     "service_type": t("Cadillac repair and maintenance", "Reparación y mantenimiento de vehículos Cadillac"),
     "search": ("cadillac escalade xt4 xt5 xt6 ct4 ct5 cts ats srx oil life",
                "cadillac escalade xt4 xt5 xt6 ct4 ct5 cts ats srx vida aceite"),
     "blocks": [
         ("h2", t("Cadillac service in Phoenixville, PA", "Servicio Cadillac en Phoenixville, PA")),
         ("p", t("Cadillacs use GM's oil life monitoring system to set the oil change schedule, with a firm 12-month limit.",
                 "Los Cadillac usan el sistema de vida del aceite de GM para fijar los cambios de aceite, con un límite firme de 12 meses.")),
         ("p", WARRANTY),
         ("h2", t("Cadillac maintenance schedule", "Calendario de mantenimiento Cadillac")),
         ("table", (t("Item", "Concepto"), t("Cadillac's guidance", "Indicación de Cadillac")), [
             (t("Oil and filter", "Aceite y filtro"), t("When the oil life monitor calls for it; never more than 12 months", "Cuando lo indique el monitor de vida del aceite; nunca más de 12 meses")),
             (t("Tire rotation", "Rotación de llantas"), t("About every 7,500 miles", "Aproximadamente cada 7,500 millas")),
             (t("Monitor reset", "Reinicio del monitor"), t("Required after every oil change", "Obligatorio después de cada cambio de aceite")),
         ]),
         ("p", t("Under easy driving, the monitor may not call for service for up to a year, so the 12-month limit is the one to watch.",
                 "Con un manejo suave, el monitor puede no pedir servicio hasta por un año, así que el límite de 12 meses es el que hay que vigilar.")),
         ("h3", PA_H3), ("p", PA_P),
         ("h2", t("Cadillac repair in Phoenixville, PA", "Reparación Cadillac en Phoenixville, PA")),
         ("p", t("Cadillac work we do:", "Trabajos que hacemos en vehículos Cadillac:")),
         ("ul", [t("Check engine and warning light diagnosis, engine repair", "Diagnóstico de la luz de revisión del motor y otras luces de advertencia, reparación del motor"),
                 t("Oil changes and filters", "Cambios de aceite y filtros"), I_BRAKES,
                 t("Steering and suspension, shocks, struts and wheel bearings", "Dirección y suspensión, amortiguadores, puntales y baleros de rueda"),
                 I_TIRES, t("Transmission maintenance and differential repair", "Mantenimiento de la transmisión y reparación del diferencial"),
                 I_CLIMATE, I_ELEC, I_EXHAUST]),
         ("p", t("See all our [auto repair services](services).", "Vea todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Cadillac maintenance", "Costo promedio del mantenimiento Cadillac")),
         ("p", t("Cadillacs average about $783 a year in repair and maintenance costs, according to RepairPal, compared with an industry average of about $652. Larger models like the Escalade usually cost more to maintain than the smaller sedans.",
                 "Los Cadillac promedian unos $783 al año en costos de reparación y mantenimiento, según RepairPal, frente a un promedio de la industria de unos $652. Los modelos más grandes, como la Escalade, suelen costar más de mantener que los sedanes pequeños.")),
         ("h2", t("How reliable are Cadillacs?", "¿Qué tan confiables son los Cadillac?")),
         ("p", t("RepairPal rates Cadillac 3.0 out of 5 for reliability, 26th out of 32 car brands. Cadillacs average 0.4 unscheduled shop visits a year, and 17% of repairs are severe.",
                 "RepairPal califica a Cadillac con 3.0 de 5 en confiabilidad, en el lugar 26 de 32 marcas. Los Cadillac promedian 0.4 visitas no programadas al taller por año, y el 17% de las reparaciones son graves.")),
     ], "cta": cta("Cadillac"),
     "faq": [
         (t("How often does a Cadillac need an oil change?", "¿Cada cuánto necesita un Cadillac un cambio de aceite?"),
          t("When the oil life monitor calls for it, and never more than 12 months apart.",
            "Cuando lo indique el monitor de vida del aceite, y nunca con más de 12 meses entre cambios.")),
         (t("How often should Cadillac tires be rotated?", "¿Cada cuánto se deben rotar las llantas de un Cadillac?"),
          t("About every 7,500 miles, according to Cadillac's maintenance guidance.",
            "Aproximadamente cada 7,500 millas, según las indicaciones de mantenimiento de Cadillac.")),
         (t("Do you service the Cadillac Escalade?", "¿Dan servicio a la Cadillac Escalade?"),
          t("Yes. We service the Escalade and Cadillac's other SUVs and sedans.",
            "Sí. Damos servicio a la Escalade y a las demás SUV y sedanes Cadillac.")),
         (t("Why do Cadillacs cost more to maintain than Chevrolets?", "¿Por qué un Cadillac cuesta más de mantener que un Chevrolet?"),
          t("RepairPal puts Cadillac at about $783 a year and Chevrolet at about $649. Larger engines, more equipment and luxury parts can add cost.",
            "RepairPal calcula unos $783 al año para Cadillac y unos $649 para Chevrolet. Los motores más grandes, el mayor equipamiento y las piezas de lujo pueden subir el costo.")),
         faq_warranty("Cadillac"),
     ]},

    # ============================================================ TESLA
    {"key": "brand_tesla", "slug": "brands/tesla", "name": "Tesla",
     "page": {
         "title": t("Tesla Service in Phoenixville, PA | Diverse Autoworks", "Servicio Tesla en Phoenixville, PA | Diverse Autoworks"),
         "desc": t("Tesla tires, brakes, suspension and PA state inspections in Phoenixville, PA. Model 3, Model Y, Model S and Model X. No high-voltage repairs.",
                   "Llantas, frenos, suspensión e inspección estatal para Tesla en Phoenixville, PA. Model 3, Model Y, Model S y Model X. Sin reparaciones de alto voltaje."),
         "h1": t("Tesla Tires, Brakes, Suspension & Inspections in Phoenixville, PA", "Llantas, frenos, suspensión e inspecciones Tesla en Phoenixville, PA"),
         "lead": t("Teslas don't need oil changes, but they still need tires, brakes, suspension work and a Pennsylvania state inspection. We handle those for the Model 3, Model Y, Model S and Model X. We don't do high-voltage battery or software repairs; those go to Tesla.",
                   "Los Tesla no necesitan cambios de aceite, pero sí llantas, frenos, trabajos de suspensión y la inspección estatal de Pennsylvania. Nos encargamos de eso para los Model 3, Model Y, Model S y Model X. No hacemos reparaciones de la batería de alto voltaje ni de software; esas van a Tesla."),
         "crumb": t("Tesla", "Tesla")},
     "service_type": t("Tesla tire, brake, suspension and inspection service", "Servicio de llantas, frenos, suspensión e inspección para Tesla"),
     "search": ("tesla model 3 model y model s model x tire rotation brakes suspension alignment inspection",
                "tesla model 3 model y model s model x rotación llantas frenos suspensión alineación inspección"),
     "blocks": [
         ("h2", t("Tesla service in Phoenixville, PA", "Servicio Tesla en Phoenixville, PA")),
         ("p", t("Electric cars are heavier than most gas cars of the same size, which adds wear to tires and suspension. Our ASE-certified technicians handle that work.",
                 "Los autos eléctricos pesan más que la mayoría de los autos de gasolina del mismo tamaño, lo que desgasta más las llantas y la suspensión. Nuestros técnicos certificados por ASE se encargan de ese trabajo.")),
         ("h3", t("What we don't do", "Lo que no hacemos")),
         ("p", t("We don't repair Tesla high-voltage batteries or software. Those need Tesla's tools and training.",
                 "No reparamos baterías de alto voltaje ni software de Tesla. Eso requiere las herramientas y la capacitación de Tesla.")),
         ("h2", t("Tesla maintenance schedule", "Calendario de mantenimiento Tesla")),
         ("table", (t("Item", "Concepto"), t("Tesla's interval", "Intervalo de Tesla")), [
             (t("Tire rotation", "Rotación de llantas"), t("Every 6,250 miles, or when tread depth differs by 2/32 in. or more", "Cada 6,250 millas, o cuando la profundidad del dibujo difiere en 2/32 de pulgada o más")),
             (t("Clean and lubricate brake calipers", "Limpiar y lubricar las mordazas de freno"), t("Every year or 12,500 miles where roads are salted in winter", "Cada año o 12,500 millas donde se usa sal en las calles en invierno")),
             (t("Brake fluid check", "Revisión del líquido de frenos"), t("Every 4 years (replace if needed)", "Cada 4 años (se reemplaza si hace falta)")),
             (t("Cabin air filter", "Filtro de aire de cabina"), t("Every 2 years", "Cada 2 años")),
             (t("Wiper blades", "Plumillas del limpiaparabrisas"), t("Every year", "Cada año")),
         ]),
         ("p", t("Intervals vary by model and year. Your Tesla app and owner's manual list yours.",
                 "Los intervalos varían según el modelo y el año. La app de Tesla y el manual del propietario indican los suyos.")),
         ("h3", t("Why caliper service matters in Pennsylvania", "Por qué importa el servicio de las mordazas en Pennsylvania")),
         ("p", t("Teslas use regenerative braking, so the brake pads do less work and calipers can stick from road salt. Tesla calls for yearly caliper cleaning where roads are salted.",
                 "Los Tesla usan frenado regenerativo, así que las pastillas trabajan menos y las mordazas pueden trabarse por la sal de las calles. Tesla indica limpiarlas cada año donde se usa sal en las calles.")),
         ("h3", PA_H3),
         ("p", t("Teslas need Pennsylvania's annual safety inspection. As electric vehicles, they're outside the emissions test, which covers gas vehicles. See [state inspections](inspections).",
                 "Los Tesla necesitan la inspección de seguridad anual de Pennsylvania. Como son eléctricos, no pasan la prueba de emisiones, que aplica a vehículos de gasolina. Vea [inspecciones estatales](inspections).")),
         ("h2", t("Tesla work we do in Phoenixville, PA", "Trabajos que hacemos en Tesla en Phoenixville, PA")),
         ("ul", [t("Pennsylvania state safety inspection", "Inspección estatal de seguridad de Pennsylvania"),
                 t("Tire rotation, balancing and replacement", "Rotación, balanceo y reemplazo de llantas"),
                 t("Wheel alignments", "Alineación de ruedas"),
                 t("Brake service, including caliper cleaning and brake fluid", "Servicio de frenos, incluida la limpieza de mordazas y el líquido de frenos"),
                 t("Steering and suspension: shocks, struts, control arms and tie rods", "Dirección y suspensión: amortiguadores, puntales, brazos de control y terminales")]),
         ("p", t("See all our [auto repair services](services).", "Vea todos nuestros [servicios de reparación](services).")),
         ("h2", t("Average cost of Tesla maintenance", "Costo promedio del mantenimiento Tesla")),
         ("p", t("RepairPal puts the annual maintenance cost of a Tesla at about $832. RepairPal doesn't publish a Tesla reliability rating.",
                 "RepairPal calcula el costo anual de mantenimiento de un Tesla en unos $832. RepairPal no publica una calificación de confiabilidad para Tesla.")),
     ], "cta": cta("Tesla", "tire, brake, suspension or inspection visit", "servicio de llantas, frenos, suspensión o inspección para su"),
     "faq": [
         (t("Do Teslas need oil changes?", "¿Los Tesla necesitan cambios de aceite?"),
          t("No. Teslas have no engine oil to change. They still need tires, brakes, cabin filters and other maintenance on Tesla's schedule.",
            "No. Los Tesla no tienen aceite de motor que cambiar. Sí necesitan llantas, frenos, filtros de cabina y otro mantenimiento según el calendario de Tesla.")),
         (t("How often should Tesla tires be rotated?", "¿Cada cuánto se deben rotar las llantas de un Tesla?"),
          t("Every 6,250 miles, or sooner if tread depth differs by 2/32 of an inch or more, according to Tesla.",
            "Cada 6,250 millas, o antes si la profundidad del dibujo difiere en 2/32 de pulgada o más, según Tesla.")),
         (t("Can you inspect my Tesla for Pennsylvania?", "¿Pueden hacer la inspección de Pennsylvania a mi Tesla?"),
          t("Yes. We do the annual state safety inspection. Electric vehicles don't need the emissions test.",
            "Sí. Hacemos la inspección estatal de seguridad anual. Los vehículos eléctricos no necesitan la prueba de emisiones.")),
         (t("Do you repair Tesla batteries?", "¿Reparan baterías de Tesla?"),
          t("No. We don't do high-voltage battery or software repairs. We handle inspections, tires, brakes and suspension.",
            "No. No hacemos reparaciones de la batería de alto voltaje ni de software. Nos encargamos de inspecciones, llantas, frenos y suspensión.")),
         (t("Why do Tesla brake calipers need cleaning?", "¿Por qué hay que limpiar las mordazas de freno de un Tesla?"),
          t("Regenerative braking means the friction brakes are used less, so calipers can stick, especially with road salt. Tesla calls for cleaning and lubricating them every year or 12,500 miles in salted regions.",
            "Con el frenado regenerativo, los frenos de fricción se usan menos y las mordazas pueden trabarse, sobre todo con la sal de las calles. Tesla indica limpiarlas y lubricarlas cada año o 12,500 millas en zonas donde se usa sal.")),
     ]},
]

# Remaining hub groups live in their own modules (imported here, after the shared helpers exist).
from bp_stellantis import STELLANTIS_PAGES  # noqa: E402
from bp_mainstream import MAINSTREAM_PAGES  # noqa: E402
from bp_luxury import LUXURY_PAGES  # noqa: E402
from bp_italian import ITALIAN_PAGES  # noqa: E402

BRAND_PAGES += STELLANTIS_PAGES + MAINSTREAM_PAGES + LUXURY_PAGES + ITALIAN_PAGES

BRAND_PAGE_BY_NAME = {b["name"]: b for b in BRAND_PAGES}
BRAND_PAGE_BY_KEY = {b["key"]: b for b in BRAND_PAGES}
