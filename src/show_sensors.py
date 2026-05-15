from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import geodatasets
import matplotlib.pyplot as plt

# Directory containing CSV files
maps_dir = Path(__file__).parent.parent / "data" / "maps"
print(f"Searching: {maps_dir.as_posix()}")

sensor_data = []

# Iterate over all CSV files in the directory
for csv_file in maps_dir.glob("*.csv"):
    print(f"Reading {csv_file.name}")
    df = pd.read_csv(csv_file)
    # Adjust column names as needed
    if {"Air Quality Station Name", "Latitude", "Longitude"}.issubset(df.columns):
        for _, row in df.iterrows():
            sensor_data.append(
                {
                    "sensor": row["Air Quality Station Name"],
                    "latitude": row["Latitude"],
                    "longitude": row["Longitude"],
                }
            )

if not sensor_data:
    print("No sensor data found.")
    exit(1)

# Create GeoDataFrame
gdf = gpd.GeoDataFrame(
    sensor_data,
    geometry=[Point(d["longitude"], d["latitude"]) for d in sensor_data],
    crs="EPSG:4326",
)

# Plot
fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, marker="o", color="red", markersize=50)
# Plot country borders using Natural Earth low resolution dataset
world = gpd.read_file(geodatasets.get_path("naturalearth.land"))

world.boundary.plot(ax=ax, linewidth=1, color="black")
ax.set_xlim(-25, 45)
ax.set_ylim(34, 72)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Sensor Locations")
plt.show()
