import csv

import geodatasets
import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
from shapely.geometry import Point

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


def plot_graph(G: nx.Graph):
    gdf = gpd.GeoDataFrame(
        G.nodes,
        geometry=[Point(d.longitude, d.latitude) for d in G.nodes],
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
