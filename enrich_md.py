import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader
from config import CMI_MD_FILE, NAMESPACES, ENRICHED_PLACES, ENRICHED_CMI_MD_FILE

from utils import get_distance


df = pd.read_csv(CMI_MD_FILE, compression='zip')
place_ids = list(set(list(df.place_sender_ref.unique()) + list(df.place_receiver_ref.unique())))
done_places_df = pd.read_csv(ENRICHED_PLACES)
done_places = list(done_places_df.url.unique())
to_do_places = [x for x in place_ids if x not in done_places]

def parse_geonames(url, ns=NAMESPACES):
    if "https://sws.geonames.org/" in url:
        doc = TeiReader(f"{url}about.rdf")
        lat = doc.tree.xpath('.//wsg:lat/text()', namespaces=ns)[0]
        long = doc.tree.xpath('.//wsg:long/text()', namespaces=ns)[0]
        name = doc.tree.xpath('.//gn:name/text()', namespaces=ns)[0]
        country_code = doc.tree.xpath('.//gn:countryCode/text()', namespaces=ns)[0]
        return {
            "url": url,
            "lat": lat,
            "long": long,
            "name": name,
            "country_code": country_code
        }
    else:
        return None


processed = []
failed = []
for x in tqdm(to_do_places, total=len(to_do_places)):
    url = f"{x}"
    item = None
    try:
        item = parse_geonames(url)
    except:
        failed.append(x)
        continue
    if item is not None:
        processed.append(item)

enriched_places = pd.DataFrame(processed)
to_save_df = pd.concat([done_places_df, enriched_places])
to_save_df.to_csv(ENRICHED_PLACES, index=False)
print(len(failed))
print(failed[0])

print(f'writing coords into {ENRICHED_CMI_MD_FILE}')
enriched = df.merge(to_save_df, how='left', left_on='place_sender_ref', right_on="url")
enriched = enriched.merge(to_save_df, how='left', left_on='place_receiver_ref', right_on="url")
enriched = enriched.drop(['url_x', 'url_y'], axis=1)
enriched['distance'] = enriched.apply(lambda row : get_distance(row), axis = 1)
enriched['path'] = enriched.apply(lambda row: "__".join([row['place_sender_ref'], row['place_receiver_ref']]), axis=1)
enriched['path_count'] = enriched.groupby('path')['path'].transform('count')
enriched['path_norm'] = (enriched['path_count'] - enriched['path_count'].min()) / (enriched['path_count'].max() - enriched['path_count'].min())
enriched.to_csv(ENRICHED_CMI_MD_FILE, index=False, compression='zip')