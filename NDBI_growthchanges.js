
// Lightweight study extent (IMPORTANT)
var bounds = villages.bounds();

// ---------- Function ----------
function getNDBI(start, end){

  var s2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterDate(start, end)
    .filterBounds(bounds)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
    .median();

  return s2.normalizedDifference(['B11','B8'])
           .rename('NDBI');
}
// ---------- 2019 ----------
var ndbi2019 = getNDBI('2019-01-01','2019-12-31');

// ---------- 2024 ----------
var ndbi2024 = getNDBI('2024-01-01','2024-12-31');

// ---------- Change ----------
var ndbiChange = ndbi2024.subtract(ndbi2019)
  .rename('NDBI_CHANGE');
// ---------- Display ----------
Map.centerObject(bounds,5);

Map.addLayer(ndbi2019, {min:-0.5,max:0.5}, 'NDBI 2019');
Map.addLayer(ndbi2024, {min:-0.5,max:0.5}, 'NDBI 2024');
Map.addLayer(ndbiChange, {min:-0.3,max:0.3}, 'NDBI Change');

// Village-wise extraction

var villageStats = ndbiChange.reduceRegions({
  collection: villages,
  reducer: ee.Reducer.mean(),
  scale: 30,
  tileScale: 4
});

var ndbiVis = {
  min: -0.3,
  max: 0.3,
  palette: ['blue', 'white', 'red']
};
Map.addLayer(
  ndbiChange.clip(bounds()),
  ndbiVis,
  "NDBI Change"
);
 Export.image.toDrive({
   image: ndbiChange.clip(villages),
   description: 'NDBI_Change_India_Clipped',
   scale: 30,
   region: ee.Geometry.Rectangle([68, 6, 98, 38]),  // full India bbox
   maxPixels: 1e13
 });

