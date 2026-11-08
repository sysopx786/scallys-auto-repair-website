# -*- coding: utf-8 -*-
"""Brand pages: US brands owned by Stellantis (Chrysler, Dodge, Jeep, Ram). See brand_pages.py for rules."""
from brand_pages import (t, WARRANTY, PA_H3, PA_P, faq_warranty, cta, I_ENGINE, I_OIL, I_BRAKES, I_TIRES, I_COOL,
                         I_CLIMATE, I_ELEC, I_EXHAUST, I_DRIVE)


def page(key, name, title, desc, h1, lead, stype, search):
    return {"key": key, "slug": "brands/" + key.split("_", 1)[1].replace("_", "-"), "name": name,
            "page": {"title": title, "desc": desc, "h1": h1, "lead": lead, "crumb": t(name, name)},
            "service_type": stype, "search": search}


STELLANTIS_INDICATOR_ROWS = [
    (t("The oil change message appears", "Aparece el mensaje de cambio de aceite"), t("Have the vehicle serviced within the next 500 miles", "Lleve el vehículo a servicio dentro de las siguientes 500 millas")),
    (t("Maximum interval", "Intervalo máximo"), t("Never more than 10,000 miles or 12 months", "Nunca más de 10,000 millas o 12 meses")),
    (t("Short trips, towing, extreme heat or cold", "Viajes cortos, remolque, calor o frío extremos"), t("The message can come on sooner", "El mensaje puede aparecer antes")),
]

STELLANTIS_PAGES = []

# ============================================================ CHRYSLER
p = page("brand_chrysler", "Chrysler",
         t("Chrysler Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Chrysler en Phoenixville, PA | Diverse Autoworks"),
         t("Chrysler Pacifica, Voyager and 300 repair in Phoenixville, PA: oil change indicator service, brakes, A/C and engine repair by ASE-certified techs.",
           "Reparación Chrysler Pacifica, Voyager y 300 en Phoenixville, PA: indicador de cambio de aceite, frenos, aire acondicionado y motor."),
         t("Chrysler Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Chrysler en Phoenixville, PA"),
         t("Chrysler's Pacifica and Voyager minivans carry a lot of families, and plenty of Chrysler 300 sedans are still on the road. Our ASE-certified technicians service Chrysler minivans and sedans.",
           "Las minivans Pacifica y Voyager de Chrysler llevan a muchas familias, y todavía circulan muchos sedanes Chrysler 300. Nuestros técnicos certificados por ASE dan servicio a minivans y sedanes Chrysler."),
         t("Chrysler repair and maintenance", "Reparación y mantenimiento de vehículos Chrysler"),
         ("chrysler pacifica voyager 300 town and country minivan oil change indicator pentastar",
          "chrysler pacifica voyager 300 town and country minivan indicador cambio aceite"))
p["blocks"] = [
    ("h2", t("Chrysler service in Phoenixville, PA", "Servicio Chrysler en Phoenixville, PA")),
    ("p", t("Chryslers use an automatic oil change indicator. It shows an oil change message when engine conditions call for service. Short trips, towing and extreme temperatures bring that message on sooner.",
            "Los Chrysler usan un indicador automático de cambio de aceite. Muestra un mensaje cuando las condiciones del motor piden servicio. Los viajes cortos, el remolque y las temperaturas extremas hacen que aparezca antes.")),
    ("p", WARRANTY),
    ("h2", t("Chrysler maintenance schedule", "Calendario de mantenimiento Chrysler")),
    ("table", (t("Situation", "Situación"), t("Chrysler's guidance", "Indicación de Chrysler")), STELLANTIS_INDICATOR_ROWS),
    ("p", t("These limits come from the Chrysler Pacifica owner's manual. Check your manual for your model's exact schedule.",
            "Estos límites vienen del manual del propietario de la Chrysler Pacifica. Revise su manual para el calendario exacto de su modelo.")),
    ("h3", PA_H3), ("p", PA_P),
    ("h2", t("Chrysler repair in Phoenixville, PA", "Reparación Chrysler en Phoenixville, PA")),
    ("p", t("Chrysler work we do:", "Trabajos que hacemos en vehículos Chrysler:")),
    ("ul", [I_ENGINE, I_OIL, I_BRAKES, I_CLIMATE, t("Water pump and thermostat", "Bomba de agua y termostato"),
            t("Transmission maintenance and CV axles", "Mantenimiento de la transmisión y ejes CV"),
            t("Steering and suspension, wheel bearings", "Dirección y suspensión, baleros de rueda"), I_ELEC, I_EXHAUST]),
    ("p", t("Chrysler is a Stellantis brand, like [Dodge](brand_dodge), [Jeep](brand_jeep) and [Ram](brand_ram). See all our [auto repair services](services).",
            "Chrysler es una marca de Stellantis, igual que [Dodge](brand_dodge), [Jeep](brand_jeep) y [Ram](brand_ram). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Chrysler maintenance", "Costo promedio del mantenimiento Chrysler")),
    ("p", t("Chryslers average about $608 a year in repair and maintenance costs, according to RepairPal, below the industry average of about $652.",
            "Los Chrysler promedian unos $608 al año en costos de reparación y mantenimiento, según RepairPal, por debajo del promedio de la industria de unos $652.")),
    ("h2", t("How reliable are Chryslers?", "¿Qué tan confiables son los Chrysler?")),
    ("p", t("RepairPal rates Chrysler 3.5 out of 5 for reliability, 11th out of 32 car brands. Chryslers average 0.3 unscheduled shop visits a year, and 12% of repairs are severe.",
            "RepairPal califica a Chrysler con 3.5 de 5 en confiabilidad, en el lugar 11 de 32 marcas. Los Chrysler promedian 0.3 visitas no programadas al taller por año, y el 12% de las reparaciones son graves.")),
]
p["cta"] = cta("Chrysler")
p["faq"] = [
    (t("How often does a Chrysler Pacifica need an oil change?", "¿Cada cuánto necesita una Chrysler Pacifica un cambio de aceite?"),
     t("When the oil change message appears, and never more than 10,000 miles or 12 months, per the Pacifica owner's manual.",
       "Cuando aparezca el mensaje de cambio de aceite, y nunca más de 10,000 millas o 12 meses, según el manual de la Pacifica.")),
    (t("How soon after the oil change message should I get service?", "¿Qué tan pronto debo ir a servicio después del mensaje de cambio de aceite?"),
     t("Within the next 500 miles, according to Chrysler.", "Dentro de las siguientes 500 millas, según Chrysler.")),
    (t("Do you fix minivan A/C?", "¿Reparan el aire acondicionado de minivans?"),
     t("Yes. We service A/C, heaters and cooling systems.", "Sí. Damos servicio al aire acondicionado, la calefacción y los sistemas de enfriamiento.")),
    (t("Do you work on the Chrysler 300?", "¿Trabajan en el Chrysler 300?"),
     t("Yes. We service Chrysler sedans as well as minivans.", "Sí. Damos servicio a sedanes Chrysler y también a minivans.")),
    faq_warranty("Chrysler"),
]
STELLANTIS_PAGES.append(p)

# ============================================================ DODGE
p = page("brand_dodge", "Dodge",
         t("Dodge Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Dodge en Phoenixville, PA | Diverse Autoworks"),
         t("Dodge Durango, Charger, Challenger and Hornet repair in Phoenixville, PA: oil change indicator service, brakes, suspension and HEMI engine repair.",
           "Reparación Dodge Durango, Charger, Challenger y Hornet en Phoenixville, PA: indicador de cambio de aceite, frenos, suspensión y motores HEMI."),
         t("Dodge Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Dodge en Phoenixville, PA"),
         t("Dodge builds the Durango SUV and the Charger and Hornet, and plenty of Challengers, Journeys and Grand Caravans are still on local roads. Our ASE-certified technicians work on Dodge V6 and HEMI V8 engines, brakes and suspensions.",
           "Dodge fabrica la SUV Durango, el Charger y el Hornet, y todavía circulan muchos Challenger, Journey y Grand Caravan. Nuestros técnicos certificados por ASE trabajan en motores Dodge V6 y HEMI V8, frenos y suspensiones."),
         t("Dodge repair and maintenance", "Reparación y mantenimiento de vehículos Dodge"),
         ("dodge durango charger challenger hornet journey grand caravan hemi oil change indicator",
          "dodge durango charger challenger hornet journey grand caravan hemi indicador cambio aceite"))
p["blocks"] = [
    ("h2", t("Dodge service in Phoenixville, PA", "Servicio Dodge en Phoenixville, PA")),
    ("p", t("Dodges use an automatic oil change indicator that adapts to how you drive. Hard driving, short trips and towing bring the reminder sooner.",
            "Los Dodge usan un indicador automático de cambio de aceite que se adapta a su forma de manejar. Manejar fuerte, los viajes cortos y el remolque adelantan el aviso.")),
    ("p", WARRANTY),
    ("h2", t("Dodge maintenance schedule", "Calendario de mantenimiento Dodge")),
    ("table", (t("Situation", "Situación"), t("Dodge guidance", "Indicación de Dodge")), [
        (t("Oil change indicator", "Indicador de cambio de aceite"), t("Can come on as early as 3,500 miles or as late as 10,000, depending on driving", "Puede encenderse desde las 3,500 hasta las 10,000 millas, según su manejo")),
        (t("Maximum interval", "Intervalo máximo"), t("10,000 miles or 12 months, whichever comes first, regardless of the indicator", "10,000 millas o 12 meses, lo que ocurra primero, sin importar el indicador")),
        (t("Severe use", "Uso severo"), t("Shorter intervals; check your owner's manual", "Intervalos más cortos; revise el manual del propietario")),
    ]),
    ("h3", PA_H3), ("p", PA_P),
    ("h2", t("Dodge repair in Phoenixville, PA", "Reparación Dodge en Phoenixville, PA")),
    ("p", t("Dodge work we do:", "Trabajos que hacemos en vehículos Dodge:")),
    ("ul", [t("Check engine light diagnosis and engine repair, including HEMI V8s", "Diagnóstico de la luz de revisión del motor y reparación del motor, incluidos los HEMI V8"),
            I_OIL, I_BRAKES, t("Steering and suspension, shocks, struts and ball joints", "Dirección y suspensión, amortiguadores, puntales y rótulas"),
            I_TIRES, t("Transmission maintenance and differential repair", "Mantenimiento de la transmisión y reparación del diferencial"), I_COOL, I_EXHAUST]),
    ("p", t("Dodge is a Stellantis brand, like [Chrysler](brand_chrysler), [Jeep](brand_jeep) and [Ram](brand_ram). See all our [auto repair services](services).",
            "Dodge es una marca de Stellantis, igual que [Chrysler](brand_chrysler), [Jeep](brand_jeep) y [Ram](brand_ram). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Dodge maintenance", "Costo promedio del mantenimiento Dodge")),
    ("p", t("Dodges average about $634 a year in repair and maintenance costs, according to RepairPal, close to the industry average of about $652. High-performance models can cost more in brakes and tires.",
            "Los Dodge promedian unos $634 al año en costos de reparación y mantenimiento, según RepairPal, cerca del promedio de la industria de unos $652. Los modelos de alto rendimiento pueden costar más en frenos y llantas.")),
    ("h2", t("How reliable are Dodges?", "¿Qué tan confiables son los Dodge?")),
    ("p", t("RepairPal rates Dodge 3.5 out of 5 for reliability, 19th out of 32 car brands. Dodges average 0.2 unscheduled shop visits a year, and 15% of repairs are severe.",
            "RepairPal califica a Dodge con 3.5 de 5 en confiabilidad, en el lugar 19 de 32 marcas. Los Dodge promedian 0.2 visitas no programadas al taller por año, y el 15% de las reparaciones son graves.")),
]
p["cta"] = cta("Dodge")
p["faq"] = [
    (t("How often does a Dodge need an oil change?", "¿Cada cuánto necesita un Dodge un cambio de aceite?"),
     t("When the oil change indicator says so, and no later than 10,000 miles or 12 months.",
       "Cuando lo indique el indicador de cambio de aceite, y a más tardar a las 10,000 millas o 12 meses.")),
    (t("Why did my oil change reminder come on early?", "¿Por qué el aviso de cambio de aceite apareció antes?"),
     t("The indicator adapts to how you drive. Short trips, towing and hard driving can bring it on as early as 3,500 miles.",
       "El indicador se adapta a su forma de manejar. Los viajes cortos, el remolque y manejar fuerte pueden adelantarlo hasta las 3,500 millas.")),
    (t("Do you work on HEMI engines?", "¿Trabajan en motores HEMI?"),
     t("Yes. We diagnose and repair Dodge engines, including HEMI V8s.", "Sí. Diagnosticamos y reparamos motores Dodge, incluidos los HEMI V8.")),
    (t("Do you service the Durango?", "¿Dan servicio a la Durango?"),
     t("Yes. We service the Durango, including brakes, suspension, transmission maintenance and differential repair.",
       "Sí. Damos servicio a la Durango, incluidos frenos, suspensión, mantenimiento de la transmisión y reparación del diferencial.")),
    faq_warranty("Dodge"),
]
STELLANTIS_PAGES.append(p)

# ============================================================ JEEP
p = page("brand_jeep", "Jeep",
         t("Jeep Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Jeep en Phoenixville, PA | Diverse Autoworks"),
         t("Jeep repair in Phoenixville, PA: oil changes, steering and suspension, brakes, engine repair and PA inspections by ASE-certified technicians.",
           "Reparación Jeep en Phoenixville, PA: cambios de aceite, dirección y suspensión, frenos, motor e inspecciones de PA con técnicos certificados por ASE."),
         t("Jeep Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Jeep en Phoenixville, PA"),
         t("Jeep owners use their vehicles differently. A Wrangler, Gladiator, Grand Cherokee, Cherokee, Compass or Wagoneer might commute all week and hit a trail on Saturday. Our ASE-certified technicians work on Jeep engines, steering, suspension and drivetrains.",
           "Los dueños de Jeep usan sus vehículos de forma distinta. Un Wrangler, Gladiator, Grand Cherokee, Cherokee, Compass o Wagoneer puede ir al trabajo toda la semana y salir a un sendero el sábado. Nuestros técnicos certificados por ASE trabajan en motores, dirección, suspensión y tren motriz de Jeep."),
         t("Jeep repair and maintenance", "Reparación y mantenimiento de vehículos Jeep"),
         ("jeep wrangler gladiator grand cherokee cherokee compass wagoneer suspension steering oil change off-road",
          "jeep wrangler gladiator grand cherokee cherokee compass wagoneer suspensión dirección cambio aceite todoterreno"))
p["blocks"] = [
    ("h2", t("Jeep service in Phoenixville, PA", "Servicio Jeep en Phoenixville, PA")),
    ("p", t("Off-road driving, mud, water crossings and dust are hard on a vehicle. Jeep treats dusty and off-road driving as severe duty, with shorter service intervals.",
            "Manejar fuera de camino, el lodo, cruzar agua y el polvo desgastan un vehículo. Jeep considera el manejo con polvo y fuera de camino como uso severo, con intervalos de servicio más cortos.")),
    ("p", WARRANTY),
    ("h2", t("Jeep maintenance schedule", "Calendario de mantenimiento Jeep")),
    ("p", t("Most Jeeps use an automatic oil change indicator. It tracks your driving and shows a message on the dash when an oil change is due.",
            "La mayoría de los Jeep usan un indicador automático de cambio de aceite. Sigue su forma de manejar y muestra un mensaje en el tablero cuando toca el cambio.")),
    ("table", (t("Situation", "Situación"), t("Jeep's guidance", "Indicación de Jeep")), [
        (t("Normal driving", "Manejo normal"), t("Oil change when the indicator says so; on most gas models, never more than 10,000 miles or 12 months", "Cambio de aceite cuando lo indique; en la mayoría de los modelos de gasolina, nunca más de 10,000 millas o 12 meses")),
        (t("Severe conditions (short trips, towing, extreme heat or cold)", "Condiciones severas (viajes cortos, remolque, calor o frío extremos)"), t("The indicator can come on as early as 3,500 miles", "El indicador puede encenderse desde las 3,500 millas")),
        (t("Dusty or off-road driving", "Manejo con polvo o fuera de camino"), t("Change oil as often as every 4,000 miles (check your owner's manual)", "Cambie el aceite hasta cada 4,000 millas (revise el manual del propietario)")),
        (t("After the indicator appears", "Después de que aparece el indicador"), t("Service within the next 500 miles", "Servicio dentro de las siguientes 500 millas")),
    ]),
    ("h3", t("After the trail", "Después del sendero")),
    ("p", t("After off-road trips, have the steering and suspension checked. Trail damage isn't always visible right away.",
            "Después de salir fuera de camino, haga revisar la dirección y la suspensión. El daño del sendero no siempre se ve de inmediato.")),
    ("h3", PA_H3),
    ("p", t("Pennsylvania requires an annual safety inspection. Vehicles registered in Chester and Montgomery counties also need an emissions test, done at the same visit. Lifted and modified Jeeps still have to pass. See [state inspections](inspections).",
            "Pennsylvania exige una inspección de seguridad anual. Los vehículos registrados en los condados de Chester y Montgomery también necesitan una prueba de emisiones, que se hace en la misma visita. Los Jeep levantados o modificados también deben aprobarla. Vea [inspecciones estatales](inspections).")),
    ("h2", t("Jeep repair in Phoenixville, PA", "Reparación Jeep en Phoenixville, PA")),
    ("p", t("Jeep work we do:", "Trabajos que hacemos en vehículos Jeep:")),
    ("ul", [I_ENGINE, I_OIL,
            t("Steering and suspension: shocks, struts, control arms, tie rods, ball joints and sway bar links", "Dirección y suspensión: amortiguadores, puntales, brazos de control, terminales, rótulas y bieletas"),
            t("Power steering service", "Servicio de dirección asistida"), I_BRAKES, I_DRIVE, t("CV axles and joints", "Ejes CV y juntas"),
            I_TIRES, t("Corrosion and rust control", "Control de corrosión y óxido"), I_COOL, I_EXHAUST]),
    ("p", t("Jeep is a Stellantis brand, like [Chrysler](brand_chrysler), [Dodge](brand_dodge) and [Ram](brand_ram). See all our [auto repair services](services).",
            "Jeep es una marca de Stellantis, igual que [Chrysler](brand_chrysler), [Dodge](brand_dodge) y [Ram](brand_ram). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Jeep maintenance", "Costo promedio del mantenimiento Jeep")),
    ("p", t("Jeeps average about $634 a year in repair and maintenance costs, according to RepairPal, close to the industry average of about $652. RepairPal lists the Compass at $526 a year and the 2020 Wrangler at $694.",
            "Los Jeep promedian unos $634 al año en costos de reparación y mantenimiento, según RepairPal, cerca del promedio de la industria de unos $652. RepairPal indica $526 al año para el Compass y $694 para el Wrangler 2020.")),
    ("p", t("Your own costs depend on how you drive. Trail use, lifts and larger tires add wear to steering, suspension and drivetrain parts.",
            "Sus costos dependen de cómo maneja. El uso en senderos, las suspensiones levantadas y las llantas más grandes desgastan más la dirección, la suspensión y el tren motriz.")),
    ("h2", t("How reliable are Jeeps?", "¿Qué tan confiables son los Jeep?")),
    ("p", t("RepairPal rates Jeep 3.5 out of 5 for reliability, 15th out of 32 car brands. Model matters: RepairPal rates the Compass 4.0 out of 5 and the Wrangler 3.0.",
            "RepairPal califica a Jeep con 3.5 de 5 en confiabilidad, en el lugar 15 de 32 marcas. El modelo importa: RepairPal califica al Compass con 4.0 de 5 y al Wrangler con 3.0.")),
]
p["cta"] = cta("Jeep")
p["faq"] = [
    (t("How often should I change my Jeep's oil?", "¿Cada cuánto debo cambiar el aceite de mi Jeep?"),
     t("When the oil change indicator says so. On most gas models, Jeep's maximum is 10,000 miles or 12 months. Dusty or off-road driving can bring it down to about every 4,000 miles; check your owner's manual.",
       "Cuando lo indique el indicador de cambio de aceite. En la mayoría de los modelos de gasolina, el máximo de Jeep es 10,000 millas o 12 meses. Con polvo o manejo fuera de camino puede bajar a unas 4,000 millas; revise su manual.")),
    (t("Does off-roading count as severe duty?", "¿Manejar fuera de camino cuenta como uso severo?"),
     t("Yes. Jeep's owner's manuals treat dusty and off-road driving as severe duty, which calls for more frequent oil changes.",
       "Sí. Los manuales de Jeep consideran el manejo con polvo y fuera de camino como uso severo, que requiere cambios de aceite más frecuentes.")),
    (t("Do you repair Jeep steering and suspension?", "¿Reparan la dirección y la suspensión de Jeep?"),
     t("Yes. We service steering and suspension, including shocks, struts, control arms, tie rods, ball joints, sway bar links and power steering.",
       "Sí. Damos servicio a la dirección y la suspensión, incluidos amortiguadores, puntales, brazos de control, terminales, rótulas, bieletas y dirección asistida.")),
    (t("Do lifted Jeeps need to pass Pennsylvania inspection?", "¿Los Jeep levantados deben aprobar la inspección de Pennsylvania?"),
     t("Yes. Lifted and modified Jeeps need the same annual safety inspection, plus the emissions test in Chester and Montgomery counties.",
       "Sí. Los Jeep levantados o modificados necesitan la misma inspección de seguridad anual, además de la prueba de emisiones en los condados de Chester y Montgomery.")),
    faq_warranty("Jeep"),
]
STELLANTIS_PAGES.append(p)

# ============================================================ RAM
p = page("brand_ram", "Ram",
         t("Ram Truck Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Ram en Phoenixville, PA | Diverse Autoworks"),
         t("Ram 1500, 2500, 3500 and ProMaster repair in Phoenixville, PA: oil change indicator service, brakes, differentials, suspension and fleet work.",
           "Reparación Ram 1500, 2500, 3500 y ProMaster en Phoenixville, PA: indicador de cambio de aceite, frenos, diferenciales, suspensión y flotas."),
         t("Ram Truck Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento de camionetas Ram en Phoenixville, PA"),
         t("Ram builds the 1500, 2500 and 3500 pickups and the ProMaster van. Ram trucks were sold under the Dodge name before Ram became its own brand. Our ASE-certified technicians service Ram pickups and vans for owners and fleets.",
           "Ram fabrica las camionetas 1500, 2500 y 3500 y la van ProMaster. Las camionetas Ram se vendían con el nombre Dodge antes de que Ram fuera una marca propia. Nuestros técnicos certificados por ASE dan servicio a camionetas y vans Ram de particulares y flotas."),
         t("Ram truck repair and maintenance", "Reparación y mantenimiento de camionetas Ram"),
         ("ram 1500 2500 3500 promaster dodge ram hemi diesel truck towing oil change indicator",
          "ram 1500 2500 3500 promaster dodge ram hemi diésel camioneta remolque indicador cambio aceite"))
p["blocks"] = [
    ("h2", t("Ram service in Phoenixville, PA", "Servicio Ram en Phoenixville, PA")),
    ("p", t("Rams use an automatic oil change indicator. Towing, short trips and extreme temperatures bring the oil change message on sooner, so a truck that tows needs service more often than one that commutes.",
            "Las Ram usan un indicador automático de cambio de aceite. El remolque, los viajes cortos y las temperaturas extremas adelantan el mensaje, así que una camioneta que remolca necesita servicio más seguido que una que solo va al trabajo.")),
    ("p", t("Running Rams or ProMasters for a business? See our [fleet repairs](fleet).", "¿Usa Ram o ProMaster en su negocio? Vea nuestras [reparaciones para flotas](fleet).")),
    ("p", WARRANTY),
    ("h2", t("Ram maintenance schedule", "Calendario de mantenimiento Ram")),
    ("table", (t("Situation", "Situación"), t("Ram's guidance (2025 Ram 1500 manual)", "Indicación de Ram (manual de la Ram 1500 2025)")), [
        (t("The oil change message appears", "Aparece el mensaje de cambio de aceite"), t("Service within the next 500 miles", "Servicio dentro de las siguientes 500 millas")),
        (t("Maximum interval", "Intervalo máximo"), t("Never more than 10,000 miles, 12 months or 350 hours of engine run time", "Nunca más de 10,000 millas, 12 meses o 350 horas de funcionamiento del motor")),
        (t("Dusty areas, very short trips, towing", "Zonas con polvo, viajes muy cortos, remolque"), t("More frequent maintenance may be needed", "Puede requerir mantenimiento más frecuente")),
    ]),
    ("p", t("The 350-hour limit matters most for fleet trucks that idle a lot.",
            "El límite de 350 horas importa sobre todo en camionetas de flota que pasan mucho tiempo en ralentí.")),
    ("h3", PA_H3),
    ("p", t("Pennsylvania requires an annual safety inspection. Gas trucks with a gross vehicle weight rating (GVWR) of 9,000 lb or less that are registered in Chester and Montgomery counties also need an emissions test. Diesel trucks and heavier gas trucks, including many 2500 and 3500 models, need only the safety inspection. See [state inspections](inspections).",
            "Pennsylvania exige una inspección de seguridad anual. Las camionetas de gasolina con un peso bruto vehicular nominal (GVWR) de 9,000 lb o menos registradas en los condados de Chester y Montgomery también necesitan una prueba de emisiones. Las diésel y las de gasolina más pesadas, incluidas muchas 2500 y 3500, solo necesitan la inspección de seguridad. Vea [inspecciones estatales](inspections).")),
    ("h2", t("Ram truck repair in Phoenixville, PA", "Reparación de camionetas Ram en Phoenixville, PA")),
    ("p", t("Ram work we do:", "Trabajos que hacemos en vehículos Ram:")),
    ("ul", [t("Check engine light diagnosis and engine repair, including HEMI V8s", "Diagnóstico de la luz de revisión del motor y reparación del motor, incluidos los HEMI V8"),
            I_OIL, I_BRAKES, I_DRIVE, t("Transmission maintenance and CV axles", "Mantenimiento de la transmisión y ejes CV"),
            t("Steering and suspension: shocks, ball joints, tie rods and control arms", "Dirección y suspensión: amortiguadores, rótulas, terminales y brazos de control"),
            I_TIRES, I_COOL, I_ELEC]),
    ("p", t("Ram is a Stellantis brand, like [Dodge](brand_dodge), [Jeep](brand_jeep) and [Chrysler](brand_chrysler). See all our [auto repair services](services).",
            "Ram es una marca de Stellantis, igual que [Dodge](brand_dodge), [Jeep](brand_jeep) y [Chrysler](brand_chrysler). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Ram maintenance", "Costo promedio del mantenimiento Ram")),
    ("p", t("Rams average about $858 a year in repair and maintenance costs, according to RepairPal, compared with an industry average of about $652. Heavy-duty trucks and towing add wear to brakes, suspension and drivetrain parts.",
            "Las Ram promedian unos $858 al año en costos de reparación y mantenimiento, según RepairPal, frente a un promedio de la industria de unos $652. Las camionetas de trabajo pesado y el remolque desgastan más frenos, suspensión y tren motriz.")),
    ("h2", t("How reliable are Ram trucks?", "¿Qué tan confiables son las camionetas Ram?")),
    ("p", t("RepairPal rates Ram 3.0 out of 5 for reliability, 23rd out of 32 car brands. Rams average 0.3 unscheduled shop visits a year, and 15% of repairs are severe.",
            "RepairPal califica a Ram con 3.0 de 5 en confiabilidad, en el lugar 23 de 32 marcas. Las Ram promedian 0.3 visitas no programadas al taller por año, y el 15% de las reparaciones son graves.")),
]
p["cta"] = cta("Ram")
p["faq"] = [
    (t("How often does a Ram 1500 need an oil change?", "¿Cada cuánto necesita una Ram 1500 un cambio de aceite?"),
     t("When the oil change message appears, and never more than 10,000 miles, 12 months or 350 engine hours, per the 2025 Ram 1500 manual.",
       "Cuando aparezca el mensaje de cambio de aceite, y nunca más de 10,000 millas, 12 meses o 350 horas de motor, según el manual de la Ram 1500 2025.")),
    (t("What are the 350 engine hours in the Ram oil change rule?", "¿Qué son las 350 horas de motor en la regla de cambio de aceite de Ram?"),
     t("Ram counts engine run time as well as miles. Trucks that idle a lot, like fleet and work trucks, can hit 350 hours before 10,000 miles.",
       "Ram cuenta el tiempo de funcionamiento del motor además de las millas. Las camionetas que pasan mucho tiempo en ralentí, como las de flota o de trabajo, pueden llegar a 350 horas antes de las 10,000 millas.")),
    (t("Does a diesel Ram need a Pennsylvania emissions test?", "¿Una Ram diésel necesita la prueba de emisiones de Pennsylvania?"),
     t("No. Diesel vehicles are exempt from Pennsylvania's emissions test, but they still need the annual safety inspection.",
       "No. Los vehículos diésel están exentos de la prueba de emisiones de Pennsylvania, pero sí necesitan la inspección de seguridad anual.")),
    (t("Do you repair Ram differentials?", "¿Reparan diferenciales Ram?"),
     t("Yes. We repair differentials and do related axle work, including rear-axle bearings and seals.",
       "Sí. Reparamos diferenciales y hacemos trabajos de ejes relacionados, incluidos baleros y sellos del eje trasero.")),
    (t("Do you service Ram fleet trucks and ProMaster vans?", "¿Dan servicio a camionetas Ram de flota y vans ProMaster?"),
     t("Yes. We offer fleet repairs for business vehicles.", "Sí. Ofrecemos reparaciones para flotas de vehículos de negocio.")),
]
STELLANTIS_PAGES.append(p)
