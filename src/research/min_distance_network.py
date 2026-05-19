from pathlib import Path
import pandas as pd
from research.utils import graph_from_csv, plot_graph
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


G = graph_from_csv(
    Path(__file__).parent.parent.parent / "data" / "maps" / "PolandMap.csv"
)
germany_g = graph_from_csv(
    Path(__file__).parent.parent.parent / "data" / "maps" / "GermanyMap.csv"
)
G.add_nodes_from(germany_g)
# G = nx.Graph()
# for _, row in stations.iterrows():
#     G.add_node(
#         row["Air Quality Station EoI Code"],
#         name=row["Air Quality Station Name"],
#         pos=(row["Latitude"], row["Longitude"]),
#         country=row["Country"],
#     )

MAX_DISTANCE = 60  # km

print("Calculation graph")
for i, node1 in enumerate(G.nodes):
    for j, node2 in enumerate(G.nodes):
        if i >= j:
            continue

        coord1 = (node1.latitude, node1.longitude)
        coord2 = (node2.latitude, node2.longitude)

        dist = geodesic(coord1, coord2).km

        if dist <= MAX_DISTANCE:
            G.add_edge(
                node1,
                node2,
                weight=dist,
            )
print("Graph completed")

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
# print(dfs_nodes)

# source = list(G.nodes)[0]
# target = list(G.nodes)[10]

# path = nx.dijkstra_path(G, source, target, weight="weight")
# print("Shortest path from", source, "to", target, ":", path)


articulation_points = list(nx.articulation_points(G))

print("Articulation Points:", len(articulation_points))


bridges = list(nx.bridges(G))

# print("Bridges:", len(bridges))
# print(bridges)

plot_graph(G)
