// ==============================
// SENTINEL-2 NDVI 
// ==============================
// Imported asset:
// var states
var stateExtent = states.geometry();

// NDVI function
function getNDVI(startDate, endDate){

  var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate(startDate, endDate)
    .filterBounds(stateExtent)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
    .median();

  // Use 20m NIR band
  var ndvi = s2.normalizedDifference(['B8A','B4']);

  // Force coarser visualization
  return ndvi.reproject({
    crs: 'EPSG:4326',
    scale: 60
  });
}
// Years
var ndvi2019 = getNDVI('2019-01-01','2019-12-31');

var ndvi2024 = getNDVI('2024-01-01','2024-12-31');
// Change
var ndviChange = ndvi2024.subtract(ndvi2019);

// Display
Map.setCenter(78,18,5);
Map.addLayer(
  ndviChange.clip(stateExtent),
  {
    min:-0.3,
    max:0.3,
    palette:['brown','white','green']
  },
  "NDVI Change"
);
Map.addLayer(
  states.style({
    color:'black',
    fillColor:'00000000',
    width:1
  }),
  {},
  "States"
);
