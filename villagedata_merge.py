import geopandas as gpd
import pandas as pd
import os

folder = r"D:\Task\KritterAssignment\village boundaries\All_vlg"

states = [
    os.path.join(folder, "karnataka.shp"),
    os.path.join(folder, "maharashtra.shp"),
    os.path.join(folder, "tamilnadu.shp"),
    os.path.join(folder, "gujarat.shp"),
    os.path.join(folder, "telangana.shp")
]

# Read all shapefiles
gdfs = [gpd.read_file(i) for i in states]

# Use first shapefile CRS as reference
target_crs = gdfs[0].crs

print("Target CRS:", target_crs)

# Reproject all others
gdfs = [gdf.to_crs(target_crs) for gdf in gdfs]

# Merge
merged = pd.concat(gdfs, ignore_index=True)

# Save output
output_path = os.path.join(folder, "villages_merged.shp")
merged.to_file(output_path)

print("Merge completed successfully")