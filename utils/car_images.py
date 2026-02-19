"""
Car Images Utility - Maps car brands/models to high-quality images
URLs scraped fresh from CarWale (February 2026)
"""

# High-quality car images mapping by brand and model
CAR_IMAGES = {
    # Maruti Suzuki
    "Maruti Suzuki": {
        "Swift": "https://imgd.aeplcdn.com/664x374/n/cw/ec/159099/swift-exterior-left-front-three-quarter-28.jpeg",
        "Dzire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-2024-exterior-right-front-three-quarter-26.jpeg",
        "Alto": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127563/alto-k10-exterior-right-front-three-quarter-60.jpeg",
        "WagonR": "https://imgd.aeplcdn.com/664x374/n/cw/ec/112947/wagon-r-exterior-right-front-three-quarter-4.jpeg",
        "Baleno": "https://imgd.aeplcdn.com/664x374/n/cw/ec/102663/baleno-exterior-right-front-three-quarter-64.jpeg",
        "Celerio": "https://imgd.aeplcdn.com/664x374/n/cw/ec/53695/new-gen-celerio-exterior-right-front-three-quarter-3.jpeg",
        "Ciaz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48542/ciaz-exterior-left-front-three-quarter.jpeg",
        "Ertiga": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115777/ertiga-exterior-right-front-three-quarter-9.jpeg",
        "Grand Vitara": "https://imgd.aeplcdn.com/664x374/n/cw/ec/123185/grand-vitara-exterior-right-front-three-quarter-3.jpeg",
        "Fronx": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130591/fronx-exterior-right-front-three-quarter-108.jpeg",
        "Brezza": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107543/brezza-exterior-right-front-three-quarter-6.jpeg",
        "Jimny": "https://imgd.aeplcdn.com/664x374/n/cw/ec/45299/jimny-exterior-right-front-three-quarter-4.jpeg",
        "Ignis": "https://imgd.aeplcdn.com/664x374/n/cw/ec/142921/ignis-exterior-right-front-three-quarter-14.jpeg",
        "S-Presso": "https://imgd.aeplcdn.com/664x374/n/cw/ec/126463/s-presso-exterior-right-front-three-quarter-4.jpeg",
        "XL6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115601/2022-xl6-exterior-right-front-three-quarter-3.jpeg",
        "Invicto": "https://imgd.aeplcdn.com/664x374/n/cw/ec/147201/invicto-exterior-right-front-three-quarter-67.jpeg",
        "Grand i10 Nios": "https://imgd.aeplcdn.com/664x374/n/cw/ec/136183/grand-i10-nios-exterior-left-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/159099/swift-exterior-left-front-three-quarter-28.jpeg"
    },

    # Hyundai
    "Hyundai": {
        "i20": "https://imgd.aeplcdn.com/664x374/n/cw/ec/150603/i20-exterior-right-front-three-quarter-6.jpeg",
        "i10": "https://imgd.aeplcdn.com/664x374/n/cw/ec/136183/grand-i10-nios-exterior-left-front-three-quarter.jpeg",
        "Grand i10": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26859/grand-i10-exterior-right-front-three-quarter.jpeg",
        "Grand i10 Nios": "https://imgd.aeplcdn.com/664x374/n/cw/ec/136183/grand-i10-nios-exterior-left-front-three-quarter.jpeg",
        "Verna": "https://imgd.aeplcdn.com/664x374/n/cw/ec/121943/verna-facelift-exterior-right-front-three-quarter-100.jpeg",
        "Creta": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-2.jpeg",
        "Venue": "https://imgd.aeplcdn.com/664x374/n/cw/ec/197163/venue-exterior-right-front-three-quarter-37.jpeg",
        "Alcazar": "https://imgd.aeplcdn.com/664x374/n/cw/ec/157825/alcazar-facelift-exterior-right-front-three-quarter-22.jpeg",
        "Aura": "https://imgd.aeplcdn.com/664x374/n/cw/ec/139133/aura-exterior-right-front-three-quarter-4.jpeg",
        "Tucson": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106821/tucson-exterior-right-front-three-quarter-6.jpeg",
        "Exter": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144851/exter-exterior-right-front-three-quarter-62.jpeg",
        "Kona Electric": "https://imgd.aeplcdn.com/664x374/n/cw/ec/29580/kona-electric-exterior-right-front-three-quarter-162254.jpeg",
        "Santro": "https://imgd.aeplcdn.com/664x374/n/cw/ec/32940/santro-exterior-right-front-three-quarter-138782.jpeg",
        "Ioniq 5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40854/ioniq-5-exterior-right-front-three-quarter-16.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/150603/i20-exterior-right-front-three-quarter-6.jpeg"
    },

    # Tata
    "Tata": {
        "Nexon": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-facelift-exterior-right-front-three-quarter-69.jpeg",
        "Punch": "https://imgd.aeplcdn.com/664x374/n/cw/ec/172825/punch-facelift-exterior-left-front-three-quarter-3.jpeg",
        "Harrier": "https://imgd.aeplcdn.com/664x374/n/cw/ec/139139/harrier-facelift-exterior-right-front-three-quarter-2.jpeg",
        "Safari": "https://imgd.aeplcdn.com/664x374/n/cw/ec/138895/safari-facelift-exterior-right-front-three-quarter-38.jpeg",
        "Altroz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/199863/altroz-facelift-exterior-left-front-three-quarter-5.jpeg",
        "Tiago": "https://imgd.aeplcdn.com/664x374/n/cw/ec/39345/tiago-exterior-left-front-three-quarter-3.jpeg",
        "Tigor": "https://imgd.aeplcdn.com/664x374/n/cw/ec/41160/tigor-exterior-left-front-three-quarter-5.jpeg",
        "Curvv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/166413/curvv-exterior-right-front-three-quarter-6.jpeg",
        "Nexon EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/149123/nexon-ev-exterior-right-rear-three-quarter.jpeg",
        "Tiago EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40453/tiago-ev-exterior-right-side-view-4.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-facelift-exterior-right-front-three-quarter-69.jpeg"
    },

    # Mahindra
    "Mahindra": {
        "Thar": "https://imgd.aeplcdn.com/664x374/n/cw/ec/124839/thar-roxx-exterior-left-front-three-quarter-3.jpeg",
        "Scorpio N": "https://imgd.aeplcdn.com/664x374/n/cw/ec/205104/xuv-7xo-exterior-right-front-three-quarter-3.jpeg",
        "Scorpio": "https://imgd.aeplcdn.com/664x374/n/cw/ec/205104/xuv-7xo-exterior-right-front-three-quarter-3.jpeg",
        "XUV700": "https://imgd.aeplcdn.com/664x374/n/cw/ec/205104/xuv-7xo-exterior-right-front-three-quarter-3.jpeg",
        "XUV500": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34024/xuv500-exterior-right-front-three-quarter-3.jpeg",
        "XUV300": "https://imgd.aeplcdn.com/664x374/n/cw/ec/156405/xuv-3xo-exterior-right-front-three-quarter-32.jpeg",
        "XUV400": "https://imgd.aeplcdn.com/664x374/n/cw/ec/45278/xuv400-exterior-right-rear-three-quarter.jpeg",
        "Bolero": "https://imgd.aeplcdn.com/664x374/n/cw/ec/200003/gravite-exterior-right-front-three-quarter-6.jpeg",
        "Bolero Neo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/210989/bolero-neo-exterior-right-front-three-quarter.jpeg",
        "Marazzo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/49114/marazzo-exterior-left-front-three-quarter.jpeg",
        "XUV3XO": "https://imgd.aeplcdn.com/664x374/n/cw/ec/156405/xuv-3xo-exterior-right-front-three-quarter-32.jpeg",
        "BE 6e": "https://imgd.aeplcdn.com/664x374/n/cw/ec/178333/be-6e-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/205104/xuv-7xo-exterior-right-front-three-quarter-3.jpeg"
    },

    # Toyota
    "Toyota": {
        "Innova": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/innova-hycross-exterior-right-front-three-quarter-72.jpeg",
        "Innova Hycross": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/innova-hycross-exterior-right-front-three-quarter-72.jpeg",
        "Innova Crysta": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140809/innova-crysta-exterior-left-front-three-quarter.jpeg",
        "Fortuner": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44709/fortuner-exterior-right-front-three-quarter-7.jpeg",
        "Glanza": "https://imgd.aeplcdn.com/664x374/n/cw/ec/112839/glanza-exterior-right-front-three-quarter-2.jpeg",
        "Urban Cruiser": "https://imgd.aeplcdn.com/664x374/n/cw/ec/132427/taisor-exterior-right-front-three-quarter-38.jpeg",
        "Urban Cruiser Hyryder": "https://imgd.aeplcdn.com/664x374/n/cw/ec/105261/urban-cruiser-hyryder-exterior-right-front-three-quarter-6.jpeg",
        "Camry": "https://imgd.aeplcdn.com/664x374/n/cw/ec/192443/camry-exterior-right-front-three-quarter-13.jpeg",
        "Hilux": "https://imgd.aeplcdn.com/664x374/n/cw/ec/109265/hilux-exterior-right-front-three-quarter-42.jpeg",
        "Land Cruiser": "https://imgd.aeplcdn.com/664x374/n/cw/ec/109787/land-cruiser-300-exterior-right-front-three-quarter.jpeg",
        "Vellfire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/157893/vellfire-exterior-right-front-three-quarter-2.jpeg",
        "Rumion": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127565/rumion-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/innova-hycross-exterior-right-front-three-quarter-72.jpeg"
    },

    # Honda
    "Honda": {
        "City": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-rear-three-quarter.jpeg",
        "Amaze": "https://imgd.aeplcdn.com/664x374/n/cw/ec/184377/amaze-2024-exterior-left-front-three-quarter.jpeg",
        "Elevate": "https://imgd.aeplcdn.com/664x374/n/cw/ec/142515/elevate-exterior-right-front-three-quarter-26.jpeg",
        "Jazz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/46891/jazz-exterior-right-front-three-quarter.jpeg",
        "WR-V": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27627/wr-v-exterior-right-front-three-quarter.jpeg",
        "CR-V": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34457/cr-v-exterior-right-front-three-quarter.jpeg",
        "Civic": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27074/civic-exterior-right-front-three-quarter-148156.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-rear-three-quarter.jpeg"
    },

    # Kia
    "Kia": {
        "Seltos": "https://imgd.aeplcdn.com/664x374/n/cw/ec/192817/new-seltos-exterior-right-front-three-quarter-47.jpeg",
        "Sonet": "https://imgd.aeplcdn.com/664x374/n/cw/ec/174423/sonet-exterior-left-front-three-quarter.jpeg",
        "Carens": "https://imgd.aeplcdn.com/664x374/n/cw/ec/174325/carens-exterior-right-side-view-2.jpeg",
        "Carnival": "https://imgd.aeplcdn.com/664x374/n/cw/ec/138947/carnival-exterior-right-front-three-quarter-16.jpeg",
        "EV6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/196251/ev6-facelift-exterior-right-front-three-quarter.jpeg",
        "EV9": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144485/ev9-exterior-right-front-three-quarter-5.jpeg",
        "Syros": "https://imgd.aeplcdn.com/664x374/n/cw/ec/168707/syros-exterior-right-front-three-quarter-10.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/192817/new-seltos-exterior-right-front-three-quarter-47.jpeg"
    },

    # Ford
    "Ford": {
        "EcoSport": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40369/ecosport-exterior-left-front-three-quarter.jpeg",
        "Figo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/35463/figo-exterior-right-front-three-quarter-151689.jpeg",
        "Aspire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/35583/aspire-exterior-right-front-three-quarter-2.jpeg",
        "Endeavour": "https://imgd.aeplcdn.com/664x374/n/cw/ec/37640/endeavour-exterior-right-front-three-quarter-149473.jpeg",
        "Freestyle": "https://imgd.aeplcdn.com/664x374/n/cw/ec/32698/freestyle-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40369/ecosport-exterior-left-front-three-quarter.jpeg"
    },

    # Renault
    "Renault": {
        "Kwid": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141125/kwid-exterior-right-front-three-quarter-36.jpeg",
        "Triber": "https://imgd.aeplcdn.com/664x374/n/cw/ec/199767/triber-exterior-right-front-three-quarter-18.jpeg",
        "Kiger": "https://imgd.aeplcdn.com/664x374/n/cw/ec/208550/kiger-facelift-exterior-right-front-three-quarter-11.jpeg",
        "Duster": "https://imgd.aeplcdn.com/664x374/n/cw/ec/163801/duster-exterior-right-front-three-quarter-5.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/208550/kiger-facelift-exterior-right-front-three-quarter-11.jpeg"
    },

    # Nissan
    "Nissan": {
        "Magnite": "https://imgd.aeplcdn.com/664x374/n/cw/ec/171777/kylaq-exterior-right-front-three-quarter-10.jpeg",
        "X-Trail": "https://imgd.aeplcdn.com/664x374/n/cw/ec/133165/x-trail-exterior-right-front-three-quarter-2.jpeg",
        "Kicks": "https://imgd.aeplcdn.com/664x374/n/cw/ec/32596/kicks-exterior-left-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/32596/kicks-exterior-left-front-three-quarter.jpeg"
    },

    # Volkswagen
    "Volkswagen": {
        "Polo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/29628/polo-exterior-right-front-three-quarter-2.jpeg",
        "Vento": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26563/vento-exterior-right-front-three-quarter-169147.jpeg",
        "Taigun": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144689/taigun-exterior-right-front-three-quarter-5.jpeg",
        "Virtus": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144681/virtus-exterior-right-front-three-quarter-6.jpeg",
        "Tiguan": "https://imgd.aeplcdn.com/664x374/n/cw/ec/53123/tiguan-exterior-right-front-three-quarter-4.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144689/taigun-exterior-right-front-three-quarter-5.jpeg"
    },

    # Skoda
    "Skoda": {
        "Slavia": "https://imgd.aeplcdn.com/664x374/n/cw/ec/175951/slavia-exterior-right-front-three-quarter-8.jpeg",
        "Kushaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/175993/kushaq-exterior-right-front-three-quarter.jpeg",
        "Superb": "https://imgd.aeplcdn.com/664x374/n/cw/ec/195997/new-superb-exterior-right-front-three-quarter.jpeg",
        "Kodiaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/158729/kodiaq-exterior-right-front-three-quarter-12.jpeg",
        "Kylaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/171777/kylaq-exterior-right-front-three-quarter-10.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/175993/kushaq-exterior-right-front-three-quarter.jpeg"
    },

    # Jeep
    "Jeep": {
        "Compass": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47051/compass-exterior-right-front-three-quarter-83.jpeg",
        "Meridian": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47139/meridian-exterior-right-front-three-quarter-10.jpeg",
        "Wrangler": "https://imgd.aeplcdn.com/664x374/n/cw/ec/174975/wrangler-facelift-exterior-left-front-three-quarter.jpeg",
        "Grand Cherokee": "https://imgd.aeplcdn.com/664x374/n/cw/ec/110647/grand-cherokee-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47051/compass-exterior-right-front-three-quarter-83.jpeg"
    },

    # MG
    "MG": {
        "Hector": "https://imgd.aeplcdn.com/664x374/n/cw/ec/212881/hector-facelift-exterior-left-front-three-quarter.jpeg",
        "Hector Plus": "https://imgd.aeplcdn.com/664x374/n/cw/ec/214253/hector-plus-exterior-left-front-three-quarter.jpeg",
        "Astor": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51940/astor-exterior-right-front-three-quarter-6.jpeg",
        "ZS EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/110437/zs-ev-exterior-right-front-three-quarter-68.jpeg",
        "Gloster": "https://imgd.aeplcdn.com/664x374/n/cw/ec/129689/gloster-exterior-right-front-three-quarter-3.jpeg",
        "Comet EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/125193/comet-ev-exterior-right-front-three-quarter-4.jpeg",
        "Windsor EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/174611/windsor-ev-exterior-right-front-three-quarter-76.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/212881/hector-facelift-exterior-left-front-three-quarter.jpeg"
    },

    # BMW
    "BMW": {
        "3 Series": "https://imgd.aeplcdn.com/664x374/n/cw/ec/198567/3-series-exterior-left-front-three-quarter.jpeg",
        "5 Series": "https://imgd.aeplcdn.com/664x374/n/cw/ec/175183/new-5-series-exterior-right-front-three-quarter-94.jpeg",
        "X1": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140591/x1-exterior-left-front-three-quarter-4.jpeg",
        "X3": "https://imgd.aeplcdn.com/664x374/n/cw/ec/179903/x3-exterior-right-front-three-quarter-27.jpeg",
        "X5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/152681/x5-exterior-right-front-three-quarter-6.jpeg",
        "X7": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127037/x7-exterior-right-front-three-quarter.jpeg",
        "i4": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107483/i4-exterior-right-front-three-quarter-3.jpeg",
        "iX": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107485/ix-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/198567/3-series-exterior-left-front-three-quarter.jpeg"
    },

    # Mercedes-Benz
    "Mercedes-Benz": {
        "C-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/178535/c-class-exterior-right-front-three-quarter-2.jpeg",
        "E-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/162929/e-class-exterior-right-front-three-quarter-33.jpeg",
        "GLC": "https://imgd.aeplcdn.com/664x374/n/cw/ec/178525/glc-exterior-right-rear-three-quarter-2.jpeg",
        "GLE": "https://imgd.aeplcdn.com/664x374/n/cw/ec/161381/gle-exterior-right-front-three-quarter-25.jpeg",
        "A-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44839/a-class-limousine-exterior-right-front-three-quarter.jpeg",
        "S-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47403/s-class-exterior-right-front-three-quarter-4.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/178535/c-class-exterior-right-front-three-quarter-2.jpeg"
    },

    # Audi
    "Audi": {
        "A4": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/a4-exterior-right-front-three-quarter-79.jpeg",
        "A6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/39472/a6-exterior-left-front-three-quarter-2.jpeg",
        "Q3": "https://imgd.aeplcdn.com/664x374/n/cw/ec/28379/q3-exterior-right-front-three-quarter-93480.jpeg",
        "Q5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/53591/q5-facelift-exterior-right-front-three-quarter-35.jpeg",
        "Q7": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/audi-q7-right-front-three-quarter4.jpeg",
        "Q8": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44831/q8-exterior-right-front-three-quarter-3.jpeg",
        "e-tron": "https://imgd.aeplcdn.com/664x374/n/cw/ec/56377/e-tron-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/a4-exterior-right-front-three-quarter-79.jpeg"
    }
}

# Body type based fallback images
BODY_TYPE_IMAGES = {
    "hatchback": "https://imgd.aeplcdn.com/664x374/n/cw/ec/159099/swift-exterior-left-front-three-quarter-28.jpeg",
    "sedan": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-rear-three-quarter.jpeg",
    "suv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-2.jpeg",
    "mpv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/innova-hycross-exterior-right-front-three-quarter-72.jpeg",
    "muv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115777/ertiga-exterior-right-front-three-quarter-9.jpeg",
    "crossover": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-facelift-exterior-right-front-three-quarter-69.jpeg",
    "coupe": "https://imgd.aeplcdn.com/664x374/n/cw/ec/166413/curvv-exterior-right-front-three-quarter-6.jpeg",
    "convertible": "https://imgd.aeplcdn.com/664x374/n/cw/ec/198567/3-series-exterior-left-front-three-quarter.jpeg",
    "pickup": "https://imgd.aeplcdn.com/664x374/n/cw/ec/109265/hilux-exterior-right-front-three-quarter-42.jpeg",
    "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-2.jpeg"
}

# Default placeholder
DEFAULT_CAR_IMAGE = "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-2.jpeg"


def get_car_image(brand: str, model: str = None, body_type: str = None) -> str:
    """
    Get the image URL for a specific car

    Args:
        brand: Car brand (e.g., 'Hyundai', 'Tata')
        model: Car model (e.g., 'Creta', 'Nexon')
        body_type: Body type as fallback (e.g., 'suv', 'sedan')

    Returns:
        URL of the car image
    """
    # Clean inputs
    brand = brand.strip() if brand else ""
    model = model.strip() if model else ""
    body_type = body_type.lower().strip() if body_type else ""

    # Try to find exact brand + model match
    if brand in CAR_IMAGES:
        brand_images = CAR_IMAGES[brand]

        # Try exact model match
        if model in brand_images:
            return brand_images[model]

        # Try partial model match
        for key in brand_images:
            if key != "default" and (key.lower() in model.lower() or model.lower() in key.lower()):
                return brand_images[key]

        # Return brand default
        if "default" in brand_images:
            return brand_images["default"]

    # Try body type fallback
    if body_type in BODY_TYPE_IMAGES:
        return BODY_TYPE_IMAGES[body_type]

    # Return absolute default
    return DEFAULT_CAR_IMAGE


def get_thumbnail_url(image_url: str) -> str:
    """
    Convert full image URL to thumbnail (smaller) version

    Args:
        image_url: Full size image URL

    Returns:
        Thumbnail version of the URL
    """
    if "aeplcdn.com" in image_url:
        return image_url.replace("664x374", "370x208")
    return image_url


def get_large_url(image_url: str) -> str:
    """
    Convert image URL to larger version

    Args:
        image_url: Image URL

    Returns:
        Larger version of the URL
    """
    if "aeplcdn.com" in image_url:
        return image_url.replace("664x374", "1056x594").replace("370x208", "1056x594")
    return image_url


# Template filter function
def car_image_filter(brand, model=None, body_type=None):
    """Jinja2 template filter for getting car images"""
    return get_car_image(brand, model, body_type)
