from pathlib import Path
import pandas as pd
import folium

germany = pd.read_csv(
    Path(__file__).parent.parent.parent / "data" / "maps" / "GermanyMap.csv"
)
poland = pd.read_csv(
    Path(__file__).parent.parent.parent / "data" / "maps" / "PolandMap.csv"
)

stations_de = germany[
    [
        "Air Quality Station EoI Code",
        "Air Quality Station Name",
        "Latitude",
        "Longitude",
        "Country",
        "Air Quality Station Type",
    ]
].drop_duplicates(subset="Air Quality Station EoI Code")

stations_pl = poland[
    [
        "Air Quality Station EoI Code",
        "Air Quality Station Name",
        "Latitude",
        "Longitude",
        "Country",
        "Air Quality Station Type",
    ]
].drop_duplicates(subset="Air Quality Station EoI Code")

stations = pd.concat([stations_de, stations_pl])

stations.reset_index(drop=True, inplace=True)

# print(stations.head())


m = folium.Map(location=[51.5, 14.5], zoom_start=6)

for _, row in stations.iterrows():
    folium.Marker(
        [row["Latitude"], row["Longitude"]], popup=row["Air Quality Station Name"]
    ).add_to(m)

m.save("map.html")
