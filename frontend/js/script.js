
// Ініціалізація карти (залишається як була)
const map = L.map('map').setView([50.45, 30.52], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

async function loadShapes() {
    try {
        console.log("Запит до API відправлено..."); // Додай для перевірки
        const response = await fetch('/api/shapes');
        const data = await response.json();
        console.log("Дані отримано:", data); // Додай для перевірки

        const geoLayer = L.geoJSON(data, {
            style: {
                color: "#ff7800",
                weight: 5,
                opacity: 0.65
            },
            onEachFeature: function (feature, layer) {
                if (feature.properties && feature.properties.name_r) {
                    layer.bindPopup("Район: " + feature.properties.name_r);
                }
            }
        }).addTo(map);

        if (data.features && data.features.length > 0) {
            map.fitBounds(geoLayer.getBounds());
        }

    } catch (error) {
        console.error("Error loading shapes:", error);
    }
}

// ОСЬ ЦЬОГО РЯДКА НЕ ВИСТАЧАЛО:
loadShapes();

