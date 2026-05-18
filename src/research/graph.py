from pathlib import Path
import pandas as pd
import folium
from geopy.distance import geodesic
import networkx as nx
import matplotlib.pyplot as plt

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

# m.save("map.html")


G = nx.Graph()
for _, row in stations.iterrows():
    G.add_node(
        row["Air Quality Station EoI Code"],
        name=row["Air Quality Station Name"],
        pos=(row["Latitude"], row["Longitude"]),
        country=row["Country"],
    )

MAX_DISTANCE = 80  # km

for i, row1 in stations.iterrows():
    for j, row2 in stations.iterrows():
        if i >= j:
            continue

        coord1 = (row1["Latitude"], row1["Longitude"])
        coord2 = (row2["Latitude"], row2["Longitude"])

        dist = geodesic(coord1, coord2).km

        if dist <= MAX_DISTANCE:
            G.add_edge(
                row1["Air Quality Station EoI Code"],
                row2["Air Quality Station EoI Code"],
                weight=dist,
            )

print("Vertices:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
print(nx.is_connected(G))
print(nx.density(G))
cycles = nx.cycle_basis(G)

print("LEN CYCLES:", len(cycles))
bfs_nodes = list(nx.bfs_tree(G, source=list(G.nodes)[0]))
print("BFS Nodes:", len(bfs_nodes))

dfs_nodes = list(nx.dfs_tree(G, source=list(G.nodes)[0]))

print("DFS Nodes:", len(dfs_nodes))
print(dfs_nodes)

source = list(G.nodes)[0]
target = list(G.nodes)[10]

path = nx.dijkstra_path(G, source, target, weight="weight")
print("Shortest path from", source, "to", target, ":", path)


articulation_points = list(nx.articulation_points(G))

print("Articulation Points:", len(articulation_points))


bridges = list(nx.bridges(G))

print("Bridges:", len(bridges))
print(bridges)
