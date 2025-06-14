import pandas as pd
import networkx as nx
from networkx.algorithms.community import louvain_communities
import json
import os

class DarkGraphAnalyzer:
    def __init__(self, edges_csv, events_csv):
        self.edges_df = pd.read_csv(edges_csv)
        self.events_df = pd.read_csv(events_csv)
        self._prepare_graph()

    def _prepare_graph(self):
        self.edges_df.dropna(subset=["Source", "Target"], inplace=True)
        self.edges_df["Source"] = self.edges_df["Source"].astype(int)
        self.edges_df["Target"] = self.edges_df["Target"].astype(int)

        self.G = nx.DiGraph()
        for _, row in self.edges_df.iterrows():
            self.G.add_edge(row["Source"], row["Target"], type=row["Type"], description=row["Description"])

    def is_planar(self):
        return nx.check_planarity(self.G.to_undirected())[0]

    def connected_components(self):
        comps = list(nx.weakly_connected_components(self.G))
        sizes = [len(c) for c in comps]
        return comps, sizes

    def source_and_sink_nodes(self):
        sources = [n for n in self.G.nodes if self.G.in_degree(n) == 0]
        sinks = [n for n in self.G.nodes if self.G.out_degree(n) == 0]
        return sources, sinks

    def top_degree_nodes(self):
        in_degrees = dict(self.G.in_degree())
        out_degrees = dict(self.G.out_degree())
        max_in = max(in_degrees.values())
        max_out = max(out_degrees.values())
        top_in = [n for n, d in in_degrees.items() if d == max_in]
        top_out = [n for n, d in out_degrees.items() if d == max_out]
        return top_in, max_in, top_out, max_out

    def edge_type_distribution(self):
        types = nx.get_edge_attributes(self.G, "type").values()
        return pd.Series(types).value_counts()

    def analyze_characters(self):
        all_chars = self.events_df["Characters"].dropna().str.split(", ").explode()
        char_counts = all_chars.value_counts()
        unique_chars = char_counts.index.tolist()
        char_appearances = {
            char: self.events_df[self.events_df["Characters"].str.contains(char, na=False, regex=False)]["ID"].tolist()
            for char in unique_chars
        }

        full_stats = []
        for char, ids in char_appearances.items():
            subgraph = self.G.subgraph(ids)
            components = list(nx.weakly_connected_components(subgraph))
            n_components = len(components)
            sizes = [len(c) for c in components]
            full_stats.append((char, len(ids), n_components, sizes))

        complete_paths = [char for char, _, comps, _ in full_stats if comps == 1]
        complete_path_details = [(char, count) for char, count, comps, _ in full_stats if comps == 1]

        return {
            "total_characters": len(unique_chars),
            "multi_event_characters": char_counts[char_counts > 1].to_dict(),
            "complete_paths_characters": complete_paths,
            "complete_paths_details": complete_path_details,
            "all_characters_stats": full_stats
        }

    def events_per_year(self):
        self.events_df["Year"] = pd.to_datetime(self.events_df["Date"], format="%d-%m-%Y", errors="coerce").dt.year
        return self.events_df.groupby("Year")["ID"].count().to_dict()

    def analyze_cycles(self):
        cycles = list(nx.simple_cycles(self.G))
        cycle_lengths = [len(c) for c in cycles]
        return  len(cycles),
            

    def graph_density(self):
        return nx.density(self.G)

    def detect_communities(self):
        G_und = self.G.to_undirected()
        communities = louvain_communities(G_und, resolution=1)
        modularity = nx.algorithms.community.modularity(G_und, communities)
        return communities, modularity

    def export_analysis_to_json(self, path):
        is_planar = self.is_planar()
        components, comp_sizes = self.connected_components()
        sources, sinks = self.source_and_sink_nodes()
        top_in, in_deg, top_out, out_deg = self.top_degree_nodes()
        edge_types = self.edge_type_distribution().to_dict()
        char_data = self.analyze_characters()
        yearly_events = self.events_per_year()
        density = self.graph_density()
        cycles = self.analyze_cycles()
        communities, modularity = self.detect_communities()

        data = {
            "is_planar": is_planar,
            "num_connected_components": len(components),
            "component_sizes": comp_sizes,
            "sources": sources,
            "sinks": sinks,
            "top_in_degree_nodes": top_in,
            "max_in_degree": in_deg,
            "top_out_degree_nodes": top_out,
            "max_out_degree": out_deg,
            "edge_type_distribution": edge_types,
            "character_analysis": char_data,
            "events_per_year": yearly_events,
            "graph_density": density,
            "cycles": cycles,
            "community_analysis": {
                "num_communities": len(communities),
                "modularity": round(modularity, 4),
                "community_sizes": [len(c) for c in communities]
            }
        }

        with open(path, "w") as f:
            json.dump(data, f, indent=2, separators=(',', ': '), ensure_ascii=False, default=str)

        html_path = os.path.splitext(path)[0] + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <title>Graph Analysis Report</title>
  <style>
    body {{ font-family: sans-serif; margin: 2em; background: #f9f9f9; }}
    pre {{ background: #fff; padding: 1em; border: 1px solid #ccc; overflow-x: auto; white-space: pre-wrap; word-break: break-word; }}
  </style>
</head>
<body>
  <h1>Graph Analysis Summary</h1>
  <pre id="output"></pre>
  <script>
    fetch('{os.path.basename(path)}')
      .then(res => res.json())
      .then(data => {{
        document.getElementById('output').textContent = JSON.stringify(data, null, 1);
      }});
  </script>
</body>
</html>
""")

if __name__ == "__main__":
    analyzer = DarkGraphAnalyzer("Dark_GD_Contest_Edges.csv", "Dark_GD_Contest_Events.csv")
    analyzer.export_analysis_to_json("graph_community_analysis.json")
    print("Analisi esportata in graph_community_analysis.json e graph_community_analysis.html")
