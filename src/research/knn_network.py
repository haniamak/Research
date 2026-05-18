from pathlib import Path


from research.utils import graph_from_csv, plot_graph, connect_knn

MAP = Path(__file__).parent.parent.parent / "data" / "maps" / "PolandMap.csv"

G = graph_from_csv(MAP)


G = connect_knn(G, k=3)

plot_graph(G)
