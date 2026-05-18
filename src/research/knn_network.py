from research.utils import graph_from_csv, plot_graph
from pathlib import Path

MAP = Path(__file__).parent.parent.parent / "data" / "maps" / "PolandMap.csv"

G = graph_from_csv(MAP)
plot_graph(G)
