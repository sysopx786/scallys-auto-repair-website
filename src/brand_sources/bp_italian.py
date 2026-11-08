# -*- coding: utf-8 -*-
"""Brand pages: Italian brands (Fiat, Alfa Romeo, Maserati). See brand_pages.py for rules."""
from brand_pages import (t, WARRANTY, PA_H3, PA_P, faq_warranty, cta, I_ENGINE, I_OIL, I_BRAKES, I_COOL, I_ELEC,
                         I_EXHAUST)
from bp_stellantis import page

I_WARN = t("Check engine and warning light diagnosis, engine repair", "Diagnóstico de la luz de revisión del motor y luces de advertencia, reparación del motor")
I_LEAKS = t("Oil leaks and gaskets", "Fugas de aceite y juntas")
I_STEER = t("Steering and suspension, control arms and wheel bearings", "Dirección y suspensión, brazos de control y baleros de rueda")
I_TRANS = t("Transmission maintenance", "Mantenimiento de la transmisión")

ITALIAN_PAGES = []

# ============================================================ FIAT
p = page("brand_fiat", "Fiat",
         t("Fiat Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Fiat en Phoenixville, PA | Diverse Autoworks"),
         t("Fiat 500, 500X and 500L repair in Phoenixville, PA: oil change indicator service, brakes, clutch, suspension and engine repair.",
           "Reparación Fiat 500, 500X y 500L en Phoenixville, PA: indicador de cambio de aceite, frenos, embrague, suspensión y motor."),
         t("Fiat Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Fiat en Phoenixville, PA"),
         t("Fiat brought the 500, 500X and 500L to the US, and many are still daily drivers. Our ASE-certified technicians service Fiat engines, clutches, brakes and suspensions.",
           "Fiat trajo el 500, el 500X y el 500L a EE. UU., y muchos todavía se usan a diario. Nuestros técnicos certificados por ASE dan servicio a motores, embragues, frenos y suspensiones Fiat."),
         t("Fiat repair and maintenance", "Reparación y mantenimiento de vehículos Fiat"),
         ("fiat 500 500x 500l abarth oil change indicator clutch",
          "fiat 500 500x 500l abarth indicador cambio aceite embrague"))
p["blocks"] = [
    ("h2", t("Fiat service in Phoenixville, PA", "Servicio Fiat en Phoenixville, PA")),
    ("p", t("Fiats use an automatic oil change indicator that adapts to how you drive. It can call for an oil change as early as 3,500 miles or as late as 10,000.",
            "Los Fiat usan un indicador automático de cambio de aceite que se adapta a su forma de manejar. Puede pedir el cambio desde las 3,500 hasta las 10,000 millas.")),
    ("p", WARRANTY),
    ("h2", t("Fiat maintenance schedule", "Calendario de mantenimiento Fiat")),
    ("table", (t("Situation", "Situación"), t("Fiat's guidance", "Indicación de Fiat")), [
        (t("Oil change indicator", "Indicador de cambio de aceite"), t("Can come on anywhere from 3,500 to 10,000 miles, depending on driving", "Puede encenderse entre las 3,500 y las 10,000 millas, según su manejo")),
        (t("Maximum interval", "Intervalo máximo"), t("10,000 miles, 12 months or 350 hours of engine run time, whichever comes first", "10,000 millas, 12 meses o 350 horas de funcionamiento del motor, lo que ocurra primero")),
        (t("Severe duty", "Uso severo"), t("The indicator doesn't account for it; follow the severe schedule in your manual", "El indicador no lo toma en cuenta; siga el calendario severo de su manual")),
    ]),
    ("h3", PA_H3), ("p", PA_P),
    ("h2", t("Fiat repair in Phoenixville, PA", "Reparación Fiat en Phoenixville, PA")),
    ("p", t("Fiat work we do:", "Trabajos que hacemos en vehículos Fiat:")),
    ("ul", [I_ENGINE, I_OIL, t("Clutch service on manual models", "Servicio de embrague en modelos manuales"), I_BRAKES,
            t("Steering and suspension, control arms and tie rods", "Dirección y suspensión, brazos de control y terminales"),
            I_COOL, I_ELEC, I_EXHAUST]),
    ("p", t("Fiat is a Stellantis brand, like [Alfa Romeo](brand_alfa_romeo), [Jeep](brand_jeep) and [Chrysler](brand_chrysler). See all our [auto repair services](services).",
            "Fiat es una marca de Stellantis, igual que [Alfa Romeo](brand_alfa_romeo), [Jeep](brand_jeep) y [Chrysler](brand_chrysler). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Fiat maintenance", "Costo promedio del mantenimiento Fiat")),
    ("p", t("Fiats average about $538 a year in repair and maintenance costs, according to RepairPal, below the industry average of about $652.",
            "Los Fiat promedian unos $538 al año en costos de reparación y mantenimiento, según RepairPal, por debajo del promedio de la industria de unos $652.")),
    ("h2", t("How reliable are Fiats?", "¿Qué tan confiables son los Fiat?")),
    ("p", t("RepairPal rates Fiat 3.5 out of 5 for reliability, 18th out of 32 car brands.",
            "RepairPal califica a Fiat con 3.5 de 5 en confiabilidad, en el lugar 18 de 32 marcas.")),
]
p["cta"] = cta("Fiat")
p["faq"] = [
    (t("How often does a Fiat 500 need an oil change?", "¿Cada cuánto necesita un Fiat 500 un cambio de aceite?"),
     t("When the oil change indicator comes on, which can be anywhere from 3,500 to 10,000 miles, and no later than 10,000 miles or 12 months.",
       "Cuando se encienda el indicador de cambio de aceite, que puede ser entre las 3,500 y las 10,000 millas, y a más tardar a las 10,000 millas o 12 meses.")),
    (t("Why doesn't my Fiat's oil change light account for severe driving?", "¿Por qué el indicador de aceite de mi Fiat no toma en cuenta el manejo severo?"),
     t("Fiat's manual says the indicator doesn't cover severe duty use. If you drive under severe conditions, follow the severe schedule in your manual.",
       "El manual de Fiat indica que el indicador no cubre el uso severo. Si maneja en condiciones severas, siga el calendario severo de su manual.")),
    (t("Do you replace Fiat clutches?", "¿Cambian embragues Fiat?"),
     t("Yes. We do clutch service on manual-transmission Fiats.", "Sí. Damos servicio de embrague a los Fiat de transmisión manual.")),
    (t("Can I still get my Fiat serviced near Phoenixville?", "¿Todavía puedo darle servicio a mi Fiat cerca de Phoenixville?"),
     t("Yes. We service Fiat 500, 500X and 500L models.", "Sí. Damos servicio a los modelos Fiat 500, 500X y 500L.")),
    faq_warranty("Fiat"),
]
ITALIAN_PAGES.append(p)

# ============================================================ ALFA ROMEO
p = page("brand_alfa_romeo", "Alfa Romeo",
         t("Alfa Romeo Repair in Phoenixville, PA | Diverse Autoworks", "Servicio Alfa Romeo en Phoenixville, PA | Diverse Autoworks"),
         t("Alfa Romeo Giulia and Stelvio service in Phoenixville, PA: oil change indicator service, brakes, suspension, cooling and engine repair.",
           "Servicio Alfa Romeo Giulia y Stelvio en Phoenixville, PA: indicador de cambio de aceite, frenos, suspensión, enfriamiento y motor."),
         t("Alfa Romeo Repair & Maintenance in Phoenixville, PA", "Reparación y mantenimiento Alfa Romeo en Phoenixville, PA"),
         t("Alfa Romeo's Giulia sedan and Stelvio SUV both come in high-performance Quadrifoglio versions. Our ASE-certified technicians work on Alfa Romeo engines, brakes and suspensions.",
           "El sedán Giulia y la SUV Stelvio de Alfa Romeo tienen versiones de alto rendimiento Quadrifoglio. Nuestros técnicos certificados por ASE trabajan en motores, frenos y suspensiones Alfa Romeo."),
         t("Alfa Romeo repair and maintenance", "Reparación y mantenimiento de vehículos Alfa Romeo"),
         ("alfa romeo giulia stelvio 4c quadrifoglio oil change indicator service",
          "alfa romeo giulia stelvio 4c quadrifoglio indicador cambio aceite servicio"))
p["blocks"] = [
    ("h2", t("Alfa Romeo service in Phoenixville, PA", "Servicio Alfa Romeo en Phoenixville, PA")),
    ("p", t("Alfa Romeos use an automatic oil change indicator that adapts to how you drive, with a firm maximum interval.",
            "Los Alfa Romeo usan un indicador automático de cambio de aceite que se adapta a su forma de manejar, con un intervalo máximo fijo.")),
    ("p", WARRANTY),
    ("h2", t("Alfa Romeo maintenance schedule", "Calendario de mantenimiento Alfa Romeo")),
    ("table", (t("Situation", "Situación"), t("Alfa Romeo guidance", "Indicación de Alfa Romeo")), [
        (t("Oil change indicator", "Indicador de cambio de aceite"), t("Can come on anywhere from 3,500 to 10,000 miles, depending on driving", "Puede encenderse entre las 3,500 y las 10,000 millas, según su manejo")),
        (t("Maximum interval", "Intervalo máximo"), t("Synthetic oil and filter no later than 10,000 miles or 12 months", "Aceite sintético y filtro a más tardar a las 10,000 millas o 12 meses")),
    ]),
    ("h3", PA_H3), ("p", PA_P),
    ("h2", t("Alfa Romeo repair in Phoenixville, PA", "Reparación Alfa Romeo en Phoenixville, PA")),
    ("p", t("Alfa Romeo work we do:", "Trabajos que hacemos en vehículos Alfa Romeo:")),
    ("ul", [I_WARN, t("Synthetic oil changes", "Cambios de aceite sintético"), I_BRAKES, I_STEER, I_COOL, I_LEAKS, I_TRANS, I_ELEC]),
    ("p", t("Alfa Romeo is a Stellantis brand, like [Fiat](brand_fiat) and [Maserati](brand_maserati). See all our [auto repair services](services).",
            "Alfa Romeo es una marca de Stellantis, igual que [Fiat](brand_fiat) y [Maserati](brand_maserati). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Alfa Romeo maintenance", "Costo promedio del mantenimiento Alfa Romeo")),
    ("p", t("RepairPal puts the annual repair and maintenance cost of an Alfa Romeo at about $834, above the industry average of about $652. RepairPal doesn't publish an Alfa Romeo reliability rating.",
            "RepairPal calcula el costo anual de reparación y mantenimiento de un Alfa Romeo en unos $834, por encima del promedio de la industria de unos $652. RepairPal no publica una calificación de confiabilidad para Alfa Romeo.")),
]
p["cta"] = cta("Alfa Romeo")
p["faq"] = [
    (t("How often does an Alfa Romeo Giulia need an oil change?", "¿Cada cuánto necesita un Alfa Romeo Giulia un cambio de aceite?"),
     t("When the oil change indicator comes on, and no later than 10,000 miles or 12 months.",
       "Cuando se encienda el indicador de cambio de aceite, y a más tardar a las 10,000 millas o 12 meses.")),
    (t("Why did my Stelvio's oil change light come on early?", "¿Por qué el indicador de aceite de mi Stelvio se encendió antes?"),
     t("The indicator adapts to how you drive and can come on as early as 3,500 miles under hard use.",
       "El indicador se adapta a su forma de manejar y puede encenderse desde las 3,500 millas con uso exigente.")),
    (t("Do you work on Quadrifoglio models?", "¿Trabajan en modelos Quadrifoglio?"),
     t("Yes. We service the Giulia and Stelvio, including Quadrifoglio versions.", "Sí. Damos servicio al Giulia y al Stelvio, incluidas las versiones Quadrifoglio.")),
    (t("Is Alfa Romeo owned by Stellantis?", "¿Alfa Romeo es propiedad de Stellantis?"),
     t("Yes. Alfa Romeo is a Stellantis brand, along with Fiat, Maserati, Jeep, Chrysler, Dodge and Ram.",
       "Sí. Alfa Romeo es una marca de Stellantis, junto con Fiat, Maserati, Jeep, Chrysler, Dodge y Ram.")),
    faq_warranty("Alfa Romeo"),
]
ITALIAN_PAGES.append(p)

# ============================================================ MASERATI
p = page("brand_maserati", "Maserati",
         t("Maserati Repair in Phoenixville, PA | Diverse Autoworks", "Reparación Maserati en Phoenixville, PA | Diverse Autoworks"),
         t("Maserati Ghibli, Levante, Quattroporte and Grecale service in Phoenixville, PA: yearly oil service, brakes, suspension and engine repair.",
           "Servicio Maserati Ghibli, Levante, Quattroporte y Grecale en Phoenixville, PA: aceite anual, frenos, suspensión y reparación del motor."),
         t("Maserati Repair & Service in Phoenixville, PA", "Reparación y servicio Maserati en Phoenixville, PA"),
         t("Maserati owners drive the Ghibli and Quattroporte sedans, the Levante and Grecale SUVs and the GranTurismo. Our ASE-certified technicians work on Maserati engines, brakes and suspensions.",
           "Los dueños de Maserati manejan los sedanes Ghibli y Quattroporte, las SUV Levante y Grecale y el GranTurismo. Nuestros técnicos certificados por ASE trabajan en motores, frenos y suspensiones Maserati."),
         t("Maserati repair and maintenance", "Reparación y mantenimiento de vehículos Maserati"),
         ("maserati ghibli levante quattroporte grecale granturismo oil change due service",
          "maserati ghibli levante quattroporte grecale granturismo cambio aceite servicio"))
p["blocks"] = [
    ("h2", t("Maserati service in Phoenixville, PA", "Servicio Maserati en Phoenixville, PA")),
    ("p", t("Maserati service is due by mileage or by time, whichever comes first. The oil change indicator only counts miles, so a low-mileage Maserati still needs its yearly oil change even if the message never appears.",
            "El servicio Maserati toca por millaje o por tiempo, lo que ocurra primero. El indicador de cambio de aceite solo cuenta millas, así que un Maserati con poco millaje necesita su cambio de aceite anual aunque el mensaje nunca aparezca.")),
    ("p", WARRANTY),
    ("h2", t("Maserati maintenance schedule", "Calendario de mantenimiento Maserati")),
    ("table", (t("Item", "Punto"), t("Maserati's guidance (Ghibli owner's manual)", "Indicación de Maserati (manual del Ghibli)")), [
        (t("Scheduled service", "Servicio programado"), t("At 12,500 miles or 1 year, then on the same pattern", "A las 12,500 millas o 1 año, y luego con el mismo patrón")),
        (t("Oil change message", "Mensaje de cambio de aceite"), t("Appears at about 11,900 miles since the last change; service within 500 miles", "Aparece a unas 11,900 millas desde el último cambio; servicio dentro de 500 millas")),
        (t("Low mileage", "Poco millaje"), t("Change the oil after 1 year even if no message appears", "Cambie el aceite al año aunque no aparezca el mensaje")),
    ]),
    ("p", t("Intervals vary by model. Your owner's manual lists yours.", "Los intervalos varían según el modelo. El manual del propietario indica los suyos.")),
    ("h3", PA_H3), ("p", PA_P),
    ("h2", t("Maserati repair in Phoenixville, PA", "Reparación Maserati en Phoenixville, PA")),
    ("p", t("Maserati work we do:", "Trabajos que hacemos en vehículos Maserati:")),
    ("ul", [I_WARN, t("Yearly oil service", "Servicio anual de aceite"), I_BRAKES, I_STEER, I_COOL, I_LEAKS, I_TRANS, I_ELEC]),
    ("p", t("Maserati is a Stellantis brand, like [Alfa Romeo](brand_alfa_romeo) and [Fiat](brand_fiat). See all our [auto repair services](services).",
            "Maserati es una marca de Stellantis, igual que [Alfa Romeo](brand_alfa_romeo) y [Fiat](brand_fiat). Vea todos nuestros [servicios de reparación](services).")),
    ("h2", t("Average cost of Maserati maintenance", "Costo promedio del mantenimiento Maserati")),
    ("p", t("Maseratis cost an average of about $1,500 a year to maintain during the first four years of ownership, according to MIE Corp., the commercial arm of Maserati Club International, as reported by ConsumerAffairs. RepairPal doesn't publish a Maserati rating.",
            "Los Maserati cuestan en promedio unos $1,500 al año de mantenimiento durante los primeros cuatro años, según MIE Corp., el brazo comercial de Maserati Club International, citado por ConsumerAffairs. RepairPal no publica una calificación para Maserati.")),
]
p["cta"] = cta("Maserati")
p["faq"] = [
    (t("How often does a Maserati need an oil change?", "¿Cada cuánto necesita un Maserati un cambio de aceite?"),
     t("At 12,500 miles or once a year, whichever comes first, per the Ghibli owner's manual. Check your manual for your model.",
       "A las 12,500 millas o una vez al año, lo que ocurra primero, según el manual del Ghibli. Revise el manual de su modelo.")),
    (t("My Maserati's oil message hasn't come on. Do I still need service?", "El mensaje de aceite de mi Maserati no ha aparecido. ¿Igual necesito servicio?"),
     t("Yes, if it's been a year. The oil change indicator only tracks mileage, so time-based service is up to you.",
       "Sí, si ya pasó un año. El indicador de cambio de aceite solo sigue el millaje, así que el servicio por tiempo depende de usted.")),
    (t("When does the Maserati oil change message appear?", "¿Cuándo aparece el mensaje de cambio de aceite de Maserati?"),
     t("At about 11,900 miles since the last oil change on the Ghibli. Have the car serviced within the next 500 miles.",
       "A unas 11,900 millas desde el último cambio de aceite en el Ghibli. Llévelo a servicio dentro de las siguientes 500 millas.")),
    (t("Is Maserati owned by Stellantis?", "¿Maserati es propiedad de Stellantis?"),
     t("Yes. Maserati is a Stellantis brand, along with Alfa Romeo and Fiat.", "Sí. Maserati es una marca de Stellantis, junto con Alfa Romeo y Fiat.")),
    faq_warranty("Maserati"),
]
ITALIAN_PAGES.append(p)
