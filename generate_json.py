import pandas as pd
import json

# === CONFIG ===
EVENTS_CSV = "Dark_GD_Contest_Events.csv"
EDGES_CSV = "Dark_GD_Contest_Edges.csv"
OUTPUT_JSON = "dark_graph_data_cleaned.json"

# === LOAD DATA ===
events_df = pd.read_csv(EVENTS_CSV)
edges_df = pd.read_csv(EDGES_CSV)

# === RENAME COLUMNS ===
events_df = events_df.rename(columns={
    "ID": "id",
    "World": "world",
    "Date": "date",
    "Important Trigger": "important_trigger",
    "Death": "death",
    "Description": "event",
    "Characters": "characters"
})

edges_df = edges_df.rename(columns={
    "ID": "id",
    "Source": "source",
    "Target": "target",
    "Type": "type",
    "Description": "description"
})
# Rimuove righe con Source o Target mancanti
edges_df = edges_df.dropna(subset=["source", "target"])


# === FORMAT FIELDS ===
events_df['characters'] = events_df['characters'].fillna('').apply(
    lambda x: [c.strip() for c in x.split(',')] if x else [])
events_df['important_trigger'] = events_df['important_trigger'].fillna('')
events_df['death'] = events_df['death'].fillna('')

# === BUILD NODES ===
nodes = []
for _, row in events_df.iterrows():
    node = {
        "id": int(row["id"]),
        "label": row["event"],
        "world": row["world"],
        "date": row["date"],
        "characters": row["characters"],
        "important_trigger": row["important_trigger"] or None,
        "death": row["death"] or None
    }
    nodes.append(node)

# === BUILD EDGES ===
edges = []
for _, row in edges_df.iterrows():
    edge = {
        "id": int(row["id"]),
        "source": int(row["source"]),
        "target": int(row["target"]),
        "type": row["type"]
    }
    edges.append(edge)

# === UNIQUE CHARACTERS ===
all_characters = sorted({
    char
    for characters in events_df['characters']
    for char in characters
})

# === UNIQUE DATES ===
event_dates = sorted(events_df['date'].unique())

# === EXPORT JSON ===
graph_data = {
    "nodes": nodes,
    "edges": edges,
    "characters": all_characters,
    "event_dates": event_dates
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(graph_data, f, indent=2, ensure_ascii=False)

print(f"✅ JSON file generated: {OUTPUT_JSON}")
