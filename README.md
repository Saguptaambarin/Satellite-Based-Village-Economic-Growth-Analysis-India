# Satellite-Based-Village-Economic-Growth-Analysis-India
# 🛰️ Village Economic Growth Intelligence System (2019–2024)


## 📌 Overview

This project builds a geospatial intelligence pipeline to estimate **village-level economic growth in India** using satellite-derived indicators.

The system identifies the **top 100 fastest-growing villages** based on changes in built-up intensity and night-time light activity over time.

The framework is designed to be:
- Scalable  
- Reproducible  
- Applicable for regional development analysis  


## 🎯 Objective

To develop a satellite-based analytical framework that:

- Extracts multi-year geospatial indicators  
- Measures economic growth proxies at village level  
- Constructs a composite Economic Growth Index (EGI)  
- Ranks villages based on growth potential  
- Visualizes spatial development patterns  


## 🛰️ Data Sources

- VIIRS Nighttime Lights (2019–2024)  
- Sentinel-2 multispectral imagery  
- Village boundary shapefiles (merged state-wise datasets)  


## ⚙️ Methodology

### 1. Data Processing
All satellite datasets were processed using **Google Earth Engine (GEE)** for temporal aggregation and spatial clipping.


### 2. Feature Extraction

Key indicators derived:

- 🌃 Night-time light intensity (proxy for economic activity)  
- 🏗️ Built-up index using NDBI  
- 🌿 Vegetation index (NDVI used for stability and validation)  

###**GEE scripts-** [https://code.earthengine.google.com/8030179aa06a74a9dd43f1b582f2b7c1]-Night-time_Light_Growth
[https://code.earthengine.google.com/050d95103ac7825965575999fec41fbc]-NDBI_change
[https://code.earthengine.google.com/41671f46f5de443ac27947f367549f10]-NDVI_change

### 3. Economic Growth Index (EGI)

The final growth score is computed as:

\[
EGI = 0.6 \times (NDBI_{2024} - NDBI_{2019}) + 0.4 \times (NTL_{2024} - NTL_{2019})
\]


### 4. Ranking System

- Each village is assigned an EGI score  
- Villages are ranked in descending order  
- Top 100 villages are selected for final analysis  


## 📊 Outputs

- 📄 Top 100 village ranking dataset (CSV)  
- 🗺️ NDBI change map (2019–2024)  
- 🌃 Night-time light change map  
- 📈 Histogram and state-wise growth charts  


## 🧰 Tools & Technologies

- Google Earth Engine (GEE)  
- Python (Pandas, NumPy, Matplotlib)  
- QGIS (spatial validation)  
- GeoJSON / Shapefile processing  


## 📌 Key Insights

Village-level economic growth is strongly associated with:

- Expansion of built-up areas  
- Increase in night-time light intensity  
- Development along urban corridors  


## ⚠️ Limitations

- Satellite proxies may not fully represent ground-level income  
- Cloud cover affects optical imagery consistency  
- Requires census or socio-economic data for validation  


## 🚀 Future Scope

- Integration with census and mobility datasets  
- Machine learning-based growth prediction  
- Automated pan-India scalability pipeline  

