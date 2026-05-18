import csv

import geodatasets
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from shapely.geometry import (
    LineString,
    MultiLineString,
    MultiPoint,
    Point,
)
from sklearn.neighbors import NearestNeighbors

from research.node import Node


def graph_from_csv(csv_file_path):
    """
    Reads a CSV file with columns 'Air Quality Station EoI Code', 'Longitude', 'Latitude', 'Country'
    and returns a NetworkX graph with nodes as Node objects.
    """
    G = nx.Graph()
    with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get("Air Quality Station EoI Code")
            longitude = row.get("Longitude")
            latitude = row.get("Latitude")
            country = row.get("Country")
            if name and longitude and latitude and country:
                node = Node(name, longitude, latitude, country)
                G.add_node(node)
    return G


def connect_knn(graph: nx.Graph, k=5):
    """
    Connects nodes in the given graph using the k-nearest neighbors algorithm.
    Assumes each node has 'x' and 'y' attributes for coordinates.
    """
    nodes: list[Node] = list(graph.nodes)
    coords = np.array([[node.longitude, node.latitude] for node in nodes], dtype=float)
    # for x, y in coords:
    #     print(type(x))
    #     assert type(x) is type(0.1)
    #     assert type(y) is type(0.1)
    nbrs = NearestNeighbors(n_neighbors=k + 1, algorithm="auto").fit(coords)
    distances, indices = nbrs.kneighbors(coords)
    for idx, node in enumerate(nodes):
        for neighbor_idx in indices[idx][1:]:  # skip self (first neighbor)
            neighbor = nodes[neighbor_idx]
            if not graph.has_edge(node, neighbor):
                graph.add_edge(node, neighbor)
    return graph


def plot_graph(G: nx.Graph):
    points = MultiPoint([Point(d.longitude, d.latitude) for d in G.nodes])
    edges = MultiLineString(
        [
            LineString([[n1.longitude, n1.latitude], [n2.longitude, n2.latitude]])
            for n1, n2 in G.edges
        ]
    )
    gdf = gpd.GeoDataFrame(
        # G.nodes,
        geometry=[points, edges],
        crs="EPSG:4326",
    )
    fig, ax = plt.subplots(figsize=(10, 8))
    gdf.plot(ax=ax, marker="o", color="red", markersize=50)

    world = gpd.read_file(geodatasets.get_path("naturalearth.land"))

    world.boundary.plot(ax=ax, linewidth=1, color="black")
    ax.set_xlim(-25, 45)
    ax.set_ylim(34, 72)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Sensor Locations")
    plt.show()
