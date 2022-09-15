const { DeckGL, ColumnLayer } = deck;

const deckgl = new DeckGL({
    container: 'viscontainer',
    mapStyle: 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json',
    initialViewState: {
        longitude: 10.4356549,
        latitude: 48.9833712,
        zoom: 5,
        minZoom: 1,
        maxZoom: 15,
        pitch: 45
    },
    controller: true
});

let data = null;
let receiverData = null;

const OPTIONS = ['radius', 'elevationScale'];
document.getElementById('sender-vis').oninput = renderLayer
document.getElementById('receiver-vis').oninput = renderLayer


OPTIONS.forEach(key => {
    document.getElementById(key).oninput = renderLayer;
});

function renderLayer() {
    const options = {};
    OPTIONS.forEach(key => {
        const value = document.getElementById(key).value;
        document.getElementById(key + '-value').innerHTML = value;
        options[key] = Number(value);
    });
    let optionsSender = {
        visible: document.getElementById('sender-vis').checked
    };

    let optionsReceiver = {
        visible: document.getElementById('receiver-vis').checked
    };

    const columnlayer = new ColumnLayer({
        id: 'column-layer',
        data,
        diskResolution: 6,
        radius: 3500,
        extruded: true,
        pickable: true,
        elevationScale: 50,
        getPosition: d => d.centroid,
        getFillColor: d => [d.value / 50, 128, d.value / 100, 255],
        getLineColor: [0, 0, 0],
        getElevation: d => d.value,
        autoHighlight: true,
        ...optionsSender,
        ...options
    });
    const receiverLayer = new ColumnLayer({
        id: 'receiver-layer',
        data: receiverData,
        diskResolution: 6,
        radius: 3500,
        extruded: true,
        pickable: true,
        elevationScale: 50,
        getPosition: d => d.centroid,
        getFillColor: d => [128, d.value / 50, d.value / 100, 255],
        getLineColor: [0, 0, 0],
        getElevation: d => d.value,
        autoHighlight: true,
        ...optionsReceiver,
        ...options
    });

    deckgl.setProps({
        layers: [columnlayer, receiverLayer],
        getTooltip: ({ object }) => object && `${object.name}: ${object.type} von ${object.value} Korrespondenzen`,
    });
}

d3.csv('data/sender_place.csv')
    .then(response => {
        data = response.map(
            d => ({
                "centroid": [
                    Number(d.long_x), Number(d.lat_x),
                ],
                "value": Number(d.amount),
                "name": d.name_x,
                "type": "Ausgangspunkt",
            })
        );
        renderLayer();
    });

d3.csv('data/receiver_place.csv')
    .then(response => {
        receiverData = response.map(
            d => ({
                "centroid": [
                    Number(d.long_y), Number(d.lat_y),
                ],
                "value": Number(d.amount),
                "name": d.name_y,
                "type": "Zielort",
            })
        );
        renderLayer();
    });