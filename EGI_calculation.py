import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv(
    r"D:\Task\KritterAssignment\FINAL_VILLAGE_GROWTH_DATA.csv"
)

print(df.head())
print(df.columns)

# Required columns
cols = ['NDBI_CHANGE', 'NDVI_CHANGE', 'NTL_CHANGE']

# Convert to numeric
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove missing values
df = df.dropna(subset=cols)

# Normalize values (0–1)
for col in cols:
    df[col + '_NORM'] = (
        (df[col] - df[col].min()) /
        (df[col].max() - df[col].min())
    )

# Calculate EGI
df['EGI'] = (
    0.5 * df['NTL_CHANGE_NORM'] +
    0.3 * df['NDBI_CHANGE_NORM'] +
    0.2 * df['NDVI_CHANGE_NORM']
)

# Rank villages
df = df.sort_values(by='EGI', ascending=False)
df['RANK'] = range(1, len(df)+1)

# Top 100
top100 = df.head(100)

# Save
top100.to_csv(
    r"D:\Task\KritterAssignment\Top_100_Villages.csv",
    index=False
)

print(top100[['Vill_name', 'STATE_UT', 'EGI', 'RANK']])

# 1. Top 20 Villages by EGI
import matplotlib.pyplot as plt

top20 = top100.head(20).sort_values("EGI")

plt.figure(figsize=(12,7))

bars = plt.barh(top20['Vill_name'], top20['EGI'], color='teal')

plt.xlabel("Economic Growth Index (EGI)")
plt.title("Top 20 Fastest Growing Villages (2019–2024)")

plt.grid(axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()

# 2. EGI Distribution Histogram
plt.figure(figsize=(10,6))

plt.hist(df['EGI'], bins=30, color='orange', edgecolor='black')

plt.title("Distribution of Economic Growth Index (EGI)")
plt.xlabel("EGI Score")
plt.ylabel("Number of Villages")

plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()

# 3. State-wise Average EGI
state_avg = df.groupby('STATE_UT')['EGI'].mean().sort_values()

plt.figure(figsize=(12,6))

state_avg.plot(kind='barh', color='steelblue')

plt.title("State-wise Average Economic Growth (EGI)")
plt.xlabel("Average EGI")

plt.grid(axis='x', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()