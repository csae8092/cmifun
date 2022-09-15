const { DeckGL, ArcLayer, DataFilterExtension } = deck;

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
    controller: true,
});

let data = null;
const OPTIONS = ['getWidth', 'getHeight'];

OPTIONS.forEach(key => {
    document.getElementById(key).oninput = renderLayer;
});
document.getElementById('filter-min').oninput = renderLayer;
document.getElementById('filter-max').oninput = renderLayer;
document.getElementById('searchPlaceInput').oninput = renderLayer
document.getElementById('searchAdesseInput').oninput = renderLayer
document.getElementById('correspondenceInput').oninput = renderLayer



function renderLayer() {
    const options = {};
    const minVal = document.getElementById('filter-min').value;
    document.getElementById('filter-min-value').innerHTML = minVal;
    const maxVal = document.getElementById('filter-max').value;
    document.getElementById('filter-max-value').innerHTML = maxVal;
    const filterRangeValues = [Number(minVal), Number(maxVal)]
    options["filterRange"] = filterRangeValues
    OPTIONS.forEach(key => {
        const value = document.getElementById(key).value;
        document.getElementById(key + '-value').innerHTML = value;
        options[key] = Number(value);
    });
    const searchString = document.getElementById('searchPlaceInput').value;
    const myData = data.filter(function (el) {
        return el.from.name.includes(searchString) && el.from.name_sender.includes(document.getElementById('searchAdesseInput').value) && el.from.cor_title.includes(document.getElementById('correspondenceInput').value);
    });
    // myData = data.filter(function (el) {
    //     return el.from.name_sender.includes(document.getElementById('searchAdesseInput').value);
    // });

    const greatCircleLayer = new ArcLayer({
        id: 'great-circle',
        data: myData,
        greatCircle: true,
        getSourcePosition: d => d.from.coordinates,
        getTargetPosition: d => d.to.coordinates,
        getSourceColor: [64, 255, 0],
        getTargetColor: [0, 128, 200],
        widthMinPixels: 1,
        getTilt: 2,
        pickable: true,
        getFilterValue: d => Number(d.from.year),
        autoHighlight: true,
        // filterRange: [1500, 1600],
        extensions: [new DataFilterExtension({ filterSize: 1 })],
        ...options
    });

    deckgl.setProps({
        layers: [greatCircleLayer],
        getTooltip: ({ object }) => object && `Von ${object.from.name_sender} aus ${object.from.name} an ${object.to.name_receiver} nach ${object.to.name} im Jahr ${object.from.year}, in: ${object.from.cor_title}` 
    });
}

d3.json('data/arc-data.json')
    .then(response => {
        data = response;
        renderLayer();
    });




