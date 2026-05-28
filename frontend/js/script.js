
const mapContainer = document.getElementById('map');

// Ініціалізуємо карту тільки якщо контейнер існує на цій сторінці
if (mapContainer) {
    const map = L.map('map').setView([50.45, 30.52], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    async function loadShapes() {
        try {
            console.log("API request sent...");
            const response = await fetch('/api/v1/shapes');
            const data = await response.json();
            console.log("Data received:", data);

            const geoLayer = L.geoJSON(data, {
                style: {
                    color: "#ff7800",
                    weight: 5,
                    opacity: 0.65
                },
                onEachFeature: function (feature, layer) {
                    if (feature.properties && feature.properties.name_r) {
                        layer.bindPopup("District: " + feature.properties.name_r);
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

    loadShapes();
}