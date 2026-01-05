"""
Car Images Utility - Maps car brands/models to high-quality images
Uses publicly available car images from reliable sources
"""

# High-quality car images mapping by brand and model
# Using placeholder images that represent each car type/brand
CAR_IMAGES = {
    # Maruti Suzuki
    "Maruti Suzuki": {
        "Swift": "https://imgd.aeplcdn.com/664x374/n/cw/ec/54399/swift-exterior-right-front-three-quarter-64.jpeg",
        "Dzire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/55883/dzire-exterior-right-front-three-quarter-2.jpeg",
        "Alto": "https://imgd.aeplcdn.com/664x374/n/cw/ec/113501/alto-k10-exterior-right-front-three-quarter-2.jpeg",
        "WagonR": "https://imgd.aeplcdn.com/664x374/n/cw/ec/135591/wagon-r-exterior-right-front-three-quarter-5.jpeg",
        "Baleno": "https://imgd.aeplcdn.com/664x374/n/cw/ec/132427/baleno-exterior-right-front-three-quarter-28.jpeg",
        "Celerio": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51349/celerio-exterior-right-front-three-quarter.jpeg",
        "Ciaz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48542/ciaz-exterior-right-front-three-quarter-3.jpeg",
        "Ertiga": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/ertiga-exterior-right-front-three-quarter-2.jpeg",
        "Grand Vitara": "https://imgd.aeplcdn.com/664x374/n/cw/ec/100837/grand-vitara-exterior-right-front-three-quarter-4.jpeg",
        "Fronx": "https://imgd.aeplcdn.com/664x374/n/cw/ec/124027/fronx-exterior-right-front-three-quarter.jpeg",
        "Brezza": "https://imgd.aeplcdn.com/664x374/n/cw/ec/102433/brezza-exterior-right-front-three-quarter-5.jpeg",
        "Jimny": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115115/jimny-exterior-right-front-three-quarter-16.jpeg",
        "Ignis": "https://imgd.aeplcdn.com/664x374/n/cw/ec/46596/ignis-exterior-right-front-three-quarter.jpeg",
        "S-Presso": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115693/s-presso-exterior-right-front-three-quarter-4.jpeg",
        "XL6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/118073/xl6-exterior-right-front-three-quarter-8.jpeg",
        "Invicto": "https://imgd.aeplcdn.com/664x374/n/cw/ec/109113/invicto-exterior-right-front-three-quarter.jpeg",
        "Grand i10 Nios": "https://imgd.aeplcdn.com/664x374/n/cw/ec/132427/baleno-exterior-right-front-three-quarter-28.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/54399/swift-exterior-right-front-three-quarter-64.jpeg"
    },
    
    # Hyundai
    "Hyundai": {
        "i20": "https://imgd.aeplcdn.com/664x374/n/cw/ec/150579/i20-exterior-right-front-three-quarter-5.jpeg",
        "i10": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141113/grand-i10-nios-exterior-right-front-three-quarter-7.jpeg",
        "Grand i10": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26745/grand-i10-exterior-right-front-three-quarter-2.jpeg",
        "Grand i10 Nios": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141113/grand-i10-nios-exterior-right-front-three-quarter-7.jpeg",
        "Verna": "https://imgd.aeplcdn.com/664x374/n/cw/ec/121943/verna-exterior-right-front-three-quarter.jpeg",
        "Creta": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-4.jpeg",
        "Venue": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141115/venue-exterior-right-front-three-quarter-6.jpeg",
        "Tucson": "https://imgd.aeplcdn.com/664x374/n/cw/ec/97835/tucson-exterior-right-front-three-quarter-66.jpeg",
        "Alcazar": "https://imgd.aeplcdn.com/664x374/n/cw/ec/151281/alcazar-exterior-right-front-three-quarter-8.jpeg",
        "Aura": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48035/aura-exterior-right-front-three-quarter.jpeg",
        "Exter": "https://imgd.aeplcdn.com/664x374/n/cw/ec/114531/exter-exterior-right-front-three-quarter-6.jpeg",
        "Ioniq 5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40854/ioniq-5-exterior-right-front-three-quarter-16.jpeg",
        "Kona Electric": "https://imgd.aeplcdn.com/664x374/n/cw/ec/40432/hyundai-kona-electric-right-front-three-quarter1.jpeg",
        "Santro": "https://imgd.aeplcdn.com/664x374/n/cw/ec/24761/hyundai-santro-right-front-three-quarter5.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/150579/i20-exterior-right-front-three-quarter-5.jpeg"
    },
    
    # Tata
    "Tata": {
        "Nexon": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-exterior-right-front-three-quarter-69.jpeg",
        "Punch": "https://imgd.aeplcdn.com/664x374/n/cw/ec/114551/punch-exterior-right-front-three-quarter-20.jpeg",
        "Harrier": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140893/harrier-exterior-right-front-three-quarter-74.jpeg",
        "Safari": "https://imgd.aeplcdn.com/664x374/n/cw/ec/137507/safari-exterior-right-front-three-quarter-14.jpeg",
        "Altroz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/149035/altroz-exterior-right-front-three-quarter-5.jpeg",
        "Tiago": "https://imgd.aeplcdn.com/664x374/n/cw/ec/118925/tiago-exterior-right-front-three-quarter-4.jpeg",
        "Tigor": "https://imgd.aeplcdn.com/664x374/n/cw/ec/146699/tigor-exterior-right-front-three-quarter-4.jpeg",
        "Curvv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/166413/curvv-exterior-right-front-three-quarter-6.jpeg",
        "Nexon EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/131109/nexon-ev-exterior-right-front-three-quarter-5.jpeg",
        "Tiago EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/103883/tiago-ev-exterior-right-front-three-quarter-3.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-exterior-right-front-three-quarter-69.jpeg"
    },
    
    # Mahindra
    "Mahindra": {
        "Thar": "https://imgd.aeplcdn.com/664x374/n/cw/ec/159771/thar-roxx-exterior-right-front-three-quarter-12.jpeg",
        "Scorpio N": "https://imgd.aeplcdn.com/664x374/n/cw/ec/99009/scorpio-n-exterior-right-front-three-quarter-10.jpeg",
        "Scorpio": "https://imgd.aeplcdn.com/664x374/n/cw/ec/99009/scorpio-n-exterior-right-front-three-quarter-10.jpeg",
        "XUV700": "https://imgd.aeplcdn.com/664x374/n/cw/ec/42355/xuv700-exterior-right-front-three-quarter.jpeg",
        "XUV500": "https://imgd.aeplcdn.com/664x374/n/cw/ec/33197/xuv500-exterior-right-front-three-quarter-3.jpeg",
        "XUV300": "https://imgd.aeplcdn.com/664x374/n/cw/ec/102089/xuv300-exterior-right-front-three-quarter-5.jpeg",
        "XUV400": "https://imgd.aeplcdn.com/664x374/n/cw/ec/110119/xuv400-exterior-right-front-three-quarter.jpeg",
        "Bolero": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107605/bolero-exterior-right-front-three-quarter.jpeg",
        "Bolero Neo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/41250/bolero-neo-exterior-right-front-three-quarter.jpeg",
        "Marazzo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26280/marazzo-exterior-right-front-three-quarter.jpeg",
        "XUV3XO": "https://imgd.aeplcdn.com/664x374/n/cw/ec/153149/xuv-3xo-exterior-right-front-three-quarter-7.jpeg",
        "BE 6e": "https://imgd.aeplcdn.com/664x374/n/cw/ec/178333/be-6e-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/99009/scorpio-n-exterior-right-front-three-quarter-10.jpeg"
    },
    
    # Toyota
    "Toyota": {
        "Innova": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140809/innova-hycross-exterior-right-front-three-quarter-5.jpeg",
        "Innova Hycross": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140809/innova-hycross-exterior-right-front-three-quarter-5.jpeg",
        "Innova Crysta": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51435/innova-crysta-exterior-right-front-three-quarter.jpeg",
        "Fortuner": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44709/fortuner-exterior-right-front-three-quarter-19.jpeg",
        "Glanza": "https://imgd.aeplcdn.com/664x374/n/cw/ec/133649/glanza-exterior-right-front-three-quarter-3.jpeg",
        "Urban Cruiser": "https://imgd.aeplcdn.com/664x374/n/cw/ec/161409/urban-cruiser-taisor-exterior-right-front-three-quarter-3.jpeg",
        "Urban Cruiser Hyryder": "https://imgd.aeplcdn.com/664x374/n/cw/ec/105261/urban-cruiser-hyryder-exterior-right-front-three-quarter-6.jpeg",
        "Camry": "https://imgd.aeplcdn.com/664x374/n/cw/ec/167227/camry-exterior-right-front-three-quarter-14.jpeg",
        "Vellfire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/157893/vellfire-exterior-right-front-three-quarter-2.jpeg",
        "Hilux": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48043/hilux-exterior-right-front-three-quarter-24.jpeg",
        "Land Cruiser": "https://imgd.aeplcdn.com/664x374/n/cw/ec/109787/land-cruiser-300-exterior-right-front-three-quarter.jpeg",
        "Rumion": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127565/rumion-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140809/innova-hycross-exterior-right-front-three-quarter-5.jpeg"
    },
    
    # Honda
    "Honda": {
        "City": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-front-three-quarter-77.jpeg",
        "Amaze": "https://imgd.aeplcdn.com/664x374/n/cw/ec/161995/amaze-exterior-right-front-three-quarter-5.jpeg",
        "Elevate": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115115/elevate-exterior-right-front-three-quarter.jpeg",
        "Jazz": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27074/jazz-exterior-right-front-three-quarter-3.jpeg",
        "WR-V": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27627/wr-v-exterior-right-front-three-quarter.jpeg",
        "CR-V": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27063/cr-v-exterior-right-front-three-quarter.jpeg",
        "Civic": "https://imgd.aeplcdn.com/664x374/n/cw/ec/27054/civic-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-front-three-quarter-77.jpeg"
    },

    # Ford
    "Ford": {
        "EcoSport": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34033/ecosport-exterior-right-front-three-quarter-2.jpeg",
        "Figo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34036/figo-exterior-right-front-three-quarter-2.jpeg",
        "Aspire": "https://imgd.aeplcdn.com/664x374/n/cw/ec/33439/aspire-exterior-right-front-three-quarter.jpeg",
        "Endeavour": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34035/endeavour-exterior-right-front-three-quarter-3.jpeg",
        "Freestyle": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34037/freestyle-exterior-right-front-three-quarter-3.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/34033/ecosport-exterior-right-front-three-quarter-2.jpeg"
    },
    
    # Kia
    "Kia": {
        "Seltos": "https://imgd.aeplcdn.com/664x374/n/cw/ec/149839/seltos-exterior-right-front-three-quarter-13.jpeg",
        "Sonet": "https://imgd.aeplcdn.com/664x374/n/cw/ec/146271/sonet-exterior-right-front-three-quarter-22.jpeg",
        "Carens": "https://imgd.aeplcdn.com/664x374/n/cw/ec/143459/carens-exterior-right-front-three-quarter-11.jpeg",
        "Carnival": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127001/carnival-exterior-right-front-three-quarter-2.jpeg",
        "EV6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/136661/ev6-exterior-right-front-three-quarter-7.jpeg",
        "EV9": "https://imgd.aeplcdn.com/664x374/n/cw/ec/155485/ev9-exterior-right-front-three-quarter.jpeg",
        "Syros": "https://imgd.aeplcdn.com/664x374/n/cw/ec/176393/syros-exterior-right-front-three-quarter-7.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/149839/seltos-exterior-right-front-three-quarter-13.jpeg"
    },
    
    # MG
    "MG": {
        "Hector": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130583/hector-exterior-right-front-three-quarter-73.jpeg",
        "Hector Plus": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48047/hector-plus-exterior-right-front-three-quarter-3.jpeg",
        "Astor": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115139/astor-exterior-right-front-three-quarter-5.jpeg",
        "ZS EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/125529/zs-ev-exterior-right-front-three-quarter-3.jpeg",
        "Gloster": "https://imgd.aeplcdn.com/664x374/n/cw/ec/91487/gloster-exterior-right-front-three-quarter-3.jpeg",
        "Comet EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/108821/comet-ev-exterior-right-front-three-quarter.jpeg",
        "Windsor EV": "https://imgd.aeplcdn.com/664x374/n/cw/ec/153185/windsor-ev-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/130583/hector-exterior-right-front-three-quarter-73.jpeg"
    },
    
    # Renault
    "Renault": {
        "Kwid": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141863/kwid-exterior-right-front-three-quarter-2.jpeg",
        "Triber": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51811/triber-exterior-right-front-three-quarter.jpeg",
        "Kiger": "https://imgd.aeplcdn.com/664x374/n/cw/ec/118273/kiger-exterior-right-front-three-quarter-14.jpeg",
        "Duster": "https://imgd.aeplcdn.com/664x374/n/cw/ec/169133/duster-exterior-right-front-three-quarter-4.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/118273/kiger-exterior-right-front-three-quarter-14.jpeg"
    },
    
    # Nissan
    "Nissan": {
        "Magnite": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127597/magnite-exterior-right-front-three-quarter-42.jpeg",
        "X-Trail": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127595/x-trail-exterior-right-front-three-quarter.jpeg",
        "Kicks": "https://imgd.aeplcdn.com/664x374/n/cw/ec/26585/kicks-exterior-right-front-three-quarter-148702.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127597/magnite-exterior-right-front-three-quarter-42.jpeg"
    },
    
    # Volkswagen
    "Volkswagen": {
        "Polo": "https://imgd.aeplcdn.com/664x374/n/cw/ec/49042/polo-exterior-right-front-three-quarter-2.jpeg",
        "Vento": "https://imgd.aeplcdn.com/664x374/n/cw/ec/49046/vento-exterior-right-front-three-quarter.jpeg",
        "Taigun": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144681/taigun-exterior-right-front-three-quarter-41.jpeg",
        "Virtus": "https://imgd.aeplcdn.com/664x374/n/cw/ec/126891/virtus-exterior-right-front-three-quarter-74.jpeg",
        "Tiguan": "https://imgd.aeplcdn.com/664x374/n/cw/ec/95757/tiguan-exterior-right-front-three-quarter-31.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/144681/taigun-exterior-right-front-three-quarter-41.jpeg"
    },
    
    # Skoda
    "Skoda": {
        "Slavia": "https://imgd.aeplcdn.com/664x374/n/cw/ec/123185/slavia-exterior-right-front-three-quarter-7.jpeg",
        "Kushaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/143659/kushaq-exterior-right-front-three-quarter-16.jpeg",
        "Superb": "https://imgd.aeplcdn.com/664x374/n/cw/ec/129461/superb-exterior-right-front-three-quarter.jpeg",
        "Kodiaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/129457/kodiaq-exterior-right-front-three-quarter-74.jpeg",
        "Kylaq": "https://imgd.aeplcdn.com/664x374/n/cw/ec/176765/kylaq-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/143659/kushaq-exterior-right-front-three-quarter-16.jpeg"
    },
    
    # Jeep
    "Jeep": {
        "Compass": "https://imgd.aeplcdn.com/664x374/n/cw/ec/156673/compass-exterior-right-front-three-quarter-38.jpeg",
        "Meridian": "https://imgd.aeplcdn.com/664x374/n/cw/ec/103397/meridian-exterior-right-front-three-quarter-46.jpeg",
        "Wrangler": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47060/wrangler-exterior-right-front-three-quarter-3.jpeg",
        "Grand Cherokee": "https://imgd.aeplcdn.com/664x374/n/cw/ec/110647/grand-cherokee-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/156673/compass-exterior-right-front-three-quarter-38.jpeg"
    },
    
    # BMW
    "BMW": {
        "3 Series": "https://imgd.aeplcdn.com/664x374/n/cw/ec/153591/3-series-exterior-right-front-three-quarter-3.jpeg",
        "5 Series": "https://imgd.aeplcdn.com/664x374/n/cw/ec/157897/5-series-exterior-right-front-three-quarter-2.jpeg",
        "X1": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115101/x1-exterior-right-front-three-quarter-3.jpeg",
        "X3": "https://imgd.aeplcdn.com/664x374/n/cw/ec/155497/x3-exterior-right-front-three-quarter-30.jpeg",
        "X5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/119763/x5-exterior-right-front-three-quarter.jpeg",
        "X7": "https://imgd.aeplcdn.com/664x374/n/cw/ec/127037/x7-exterior-right-front-three-quarter.jpeg",
        "i4": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107483/i4-exterior-right-front-three-quarter-3.jpeg",
        "iX": "https://imgd.aeplcdn.com/664x374/n/cw/ec/107485/ix-exterior-right-front-three-quarter.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/153591/3-series-exterior-right-front-three-quarter-3.jpeg"
    },
    
    # Mercedes-Benz
    "Mercedes-Benz": {
        "C-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/143179/c-class-exterior-right-front-three-quarter-2.jpeg",
        "E-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/148998/e-class-exterior-right-front-three-quarter.jpeg",
        "GLC": "https://imgd.aeplcdn.com/664x374/n/cw/ec/126513/glc-exterior-right-front-three-quarter.jpeg",
        "GLE": "https://imgd.aeplcdn.com/664x374/n/cw/ec/161381/gle-exterior-right-front-three-quarter-25.jpeg",
        "A-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44839/a-class-limousine-exterior-right-front-three-quarter.jpeg",
        "S-Class": "https://imgd.aeplcdn.com/664x374/n/cw/ec/47403/s-class-exterior-right-front-three-quarter-4.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/143179/c-class-exterior-right-front-three-quarter-2.jpeg"
    },
    
    # Audi
    "Audi": {
        "A4": "https://imgd.aeplcdn.com/664x374/n/cw/ec/126511/a4-exterior-right-front-three-quarter.jpeg",
        "A6": "https://imgd.aeplcdn.com/664x374/n/cw/ec/149589/a6-exterior-right-front-three-quarter-24.jpeg",
        "Q3": "https://imgd.aeplcdn.com/664x374/n/cw/ec/108375/q3-exterior-right-front-three-quarter.jpeg",
        "Q5": "https://imgd.aeplcdn.com/664x374/n/cw/ec/152541/q5-exterior-right-front-three-quarter.jpeg",
        "Q7": "https://imgd.aeplcdn.com/664x374/n/cw/ec/51909/audi-q7-right-front-three-quarter4.jpeg",
        "Q8": "https://imgd.aeplcdn.com/664x374/n/cw/ec/44831/q8-exterior-right-front-three-quarter-3.jpeg",
        "e-tron": "https://imgd.aeplcdn.com/664x374/n/cw/ec/56377/e-tron-exterior-right-front-three-quarter-2.jpeg",
        "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/126511/a4-exterior-right-front-three-quarter.jpeg"
    }
}

# Body type based fallback images
BODY_TYPE_IMAGES = {
    "hatchback": "https://imgd.aeplcdn.com/664x374/n/cw/ec/54399/swift-exterior-right-front-three-quarter-64.jpeg",
    "sedan": "https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-front-three-quarter-77.jpeg",
    "suv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-4.jpeg",
    "mpv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/140809/innova-hycross-exterior-right-front-three-quarter-5.jpeg",
    "muv": "https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/ertiga-exterior-right-front-three-quarter-2.jpeg",
    "crossover": "https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-exterior-right-front-three-quarter-69.jpeg",
    "coupe": "https://imgd.aeplcdn.com/664x374/n/cw/ec/166413/curvv-exterior-right-front-three-quarter-6.jpeg",
    "convertible": "https://imgd.aeplcdn.com/664x374/n/cw/ec/153591/3-series-exterior-right-front-three-quarter-3.jpeg",
    "pickup": "https://imgd.aeplcdn.com/664x374/n/cw/ec/48043/hilux-exterior-right-front-three-quarter-24.jpeg",
    "default": "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-4.jpeg"
}

# Default placeholder
DEFAULT_CAR_IMAGE = "https://imgd.aeplcdn.com/664x374/n/cw/ec/106815/creta-exterior-right-front-three-quarter-4.jpeg"


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
    # For aeplcdn images, we can adjust size in URL
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
