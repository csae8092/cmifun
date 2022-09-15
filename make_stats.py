import pandas as pd
import json
from tqdm import tqdm
from config import ENRICHED_CMI_MD_FILE, HTML_DATA
from utils import place_sender_stats, place_receiver_stats, sender_stats, receiver_stats

df = pd.read_csv(ENRICHED_CMI_MD_FILE)

stats_df = place_sender_stats(df)
stats_df.to_csv(f"{HTML_DATA}/sender_place.csv", index=False)

stats_df = place_receiver_stats(df)
stats_df.to_csv(f"{HTML_DATA}/receiver_place.csv", index=False)

stats_df = sender_stats(df)
stats_df.to_csv(f"{HTML_DATA}/sender.csv", index=False)

stats_df = receiver_stats(df)
stats_df.to_csv(f"{HTML_DATA}/receiver.csv", index=False)

df = df[df['lat_x'].notna()]
df = df[df['lat_y'].notna()]

df = df.drop(df[(df.place_receiver_ref == "unbekannt")].index)
df.drop_duplicates(subset=["path"]).to_csv(f"{HTML_DATA}/paths.csv", index=False)
data = []
for i, row in tqdm(df.iterrows(), total=len(df)):
    item = {}
    item['from'] = {
        "name": row['place_sender_name'],
        "name_sender": row['sender_name'],
        "cor_title": row['cor_title'],
        "year": row['year'],
        "coordinates": [
            row['long_x'],
            row['lat_x']
        ]
    }
    item['to'] = {
        "name": row['place_receiver_name'],
        "name_receiver": row['receiver_name'],
        "coordinates": [
            row['long_y'],
            row['lat_y']
        ]
    }
    data.append(item)
with open ('./html/data/arc-data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)

