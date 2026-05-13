import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 1. LOAD DATA
# -----------------------------
gdf = gpd.read_file(r"D:\Task\KritterAssignment\village boundaries\All_vlg\villages_merged.shp")
df = pd.read_csv(r"D:\Task\KritterAssignment\FINAL_VILLAGE_GROWTH_DATA.csv", low_memory=False)

# Clean column names
gdf.columns = gdf.columns.str.strip()
df.columns = df.columns.str.strip()

# -----------------------------
# 2. KEEP ONLY REQUIRED COLUMNS
# -----------------------------
required_cols = ["Vill_name", "NDBI_CHANGE", "NDVI_CHANGE", "NTL_CHANGE"]

df = df[required_cols].copy()

# -----------------------------
# 3. FIX DATA TYPES
# -----------------------------
for c in ["NDBI_CHANGE", "NDVI_CHANGE", "NTL_CHANGE"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Drop missing values
df = df.dropna(subset=["Vill_name", "NDBI_CHANGE", "NDVI_CHANGE", "NTL_CHANGE"])

# -----------------------------
# 4. NORMALIZATION (0–1)
# -----------------------------
for c in ["NDBI_CHANGE", "NDVI_CHANGE", "NTL_CHANGE"]:
    min_val = df[c].min()
    max_val = df[c].max()

    if max_val - min_val == 0:
        df[c + "_NORM"] = 0
    else:
        df[c + "_NORM"] = (df[c] - min_val) / (max_val - min_val)

# -----------------------------
# 5. EGI CALCULATION
# -----------------------------
df["EGI"] = (
    0.5 * df["NTL_CHANGE_NORM"] +
    0.3 * df["NDBI_CHANGE_NORM"] +
    0.2 * df["NDVI_CHANGE_NORM"]
)

# -----------------------------
# 6. MERGE (SAFE JOIN)
# -----------------------------
merged = gdf.merge(df, on="Vill_name", how="inner")

print("Merged shape:", merged.shape)

# Drop NaN geometries or values
merged = merged.dropna(subset=["EGI", "NDBI_CHANGE", "NTL_CHANGE"])

# -----------------------------
# 7. FUNCTION FOR SAFE PLOTTING
# -----------------------------
def plot_map(column, cmap, title, output_path):
    vmin = merged[column].quantile(0.05)
    vmax = merged[column].quantile(0.95)

    fig, ax = plt.subplots(figsize=(10, 8))

    merged.plot(
        column=column,
        cmap=cmap,
        legend=True,
        vmin=vmin,
        vmax=vmax,
        ax=ax
    )

    ax.set_title(title)
    ax.axis("off")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

# -----------------------------
# 8. MAP 1 — NDBI CHANGE
# -----------------------------
 plot_map(
  "NDBI_CHANGE",
    "RdYlBu",
     "NDBI Change (2019–2024)",
     r"D:\Task\KritterAssignment\NDBI_map.png"
 )

# -----------------------------
# 9. MAP 2 — NIGHT LIGHT CHANGE
# -----------------------------
 plot_map(
     "NTL_CHANGE",
     "hot",
     "Night Light Change (2019–2024)",
     r"D:\Task\KritterAssignment\NTL_map.png"
 )

# -----------------------------
# 10. MAP 3 — TOP 100 EGI
# -----------------------------
merged = merged.dropna(subset=["EGI"])
merged["EGI"] = pd.to_numeric(merged["EGI"], errors="coerce")
merged = merged.dropna(subset=["EGI"])

top100 = merged.nlargest(100, "EGI")

print("Top100 shape:", top100.shape)

fig, ax = plt.subplots(figsize=(10, 8))

top100.plot(
    column="EGI",
    cmap="viridis",
    legend=True,
    ax=ax,
    edgecolor="black",
    linewidth=0.2
)

ax.set_title("Top 100 Villages by EGI")
ax.axis("off")

plt.savefig(
    r"D:\Task\KritterAssignment\Top100_EGI_map.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("✅ ALL MAPS GENERATED SUCCESSFULLY")