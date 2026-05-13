// -------------------------
// USE UPLOADED 5-STATE BOUNDARY
// -------------------------
var bounds = states.geometry();
// -------------------------
// VIIRS NIGHT LIGHTS
// -------------------------
var viirs = ee.ImageCollection(
  "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG"
).select("avg_rad");

// -------------------------
// 2019 & 2024
// -------------------------
var ntl2019 = viirs
  .filterDate('2019-01-01', '2019-12-31')
  .filterBounds(bounds)
  .mean();

var ntl2024 = viirs
  .filterDate('2024-01-01', '2024-12-31')
  .filterBounds(bounds)
  .mean();
// -------------------------
// LIGHT CHANGE
// -------------------------
var ntlChange = ntl2024.subtract(ntl2019)
  .rename("NTL_CHANGE");
// -------------------------
// DISPLAY (ONLY 5 STATES)
// -------------------------
Map.centerObject(bounds, 6);

Map.addLayer(
  ntlChange.clip(bounds),
  {
    min: -3,
    max: 5,
    palette: ['0000FF','000000','FFFF00','FF0000']
  },
  "Night Light Change"
);
// Optional state boundary overlay for screenshot
Map.addLayer(
  states.style({
    color: 'white',
    fillColor: '00000000',
    width: 1
  }),
  {},
  "State Boundary"
);
// -------------------------
// VILLAGE-WISE COMPUTATION
// (using your merged village layer)
// -------------------------
var villageLights = ntlChange.reduceRegions({
  collection: villages,
  reducer: ee.Reducer.mean(),
  scale: 500,
  tileScale: 4
});

print("Village Light Change:", villageLights.limit(5));
// -------------------------
// EXPORT (SAFE REGION, NOT FULL COMPLEX GEOMETRY)
// -------------------------
 Export.table.toDrive({
  collection: villageLights,   // or 'growth' if you used growth variable
  description: 'Village_VIIRS_Growth_CSV',
  fileFormat: 'CSV',
   selectors: [
     'system:index',
    'ntl_2019',
    'ntl_2024',
     'mean',        // if reduceRegions output
    'growth_pct'
   ]
 });
