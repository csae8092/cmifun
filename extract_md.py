import glob
import os
import pandas as pd
from tqdm import tqdm
from acdh_tei_pyutils.tei import TeiReader
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

from config import CMI_MD_FILE, NAMESPACES


ns = NAMESPACES
files = glob.glob('./data/cmi/*.xml')


def get_coords(url):
    item = {
        "url": url,
        "lat": None,
        "long": None,
        "name": None,
        "country_code": None
    }
    try:
        doc = TeiReader(f"{url}about.rdf")
        lat = doc.tree.xpath('.//wsg:lat/text()', namespaces=ns)[0]
        long = doc.tree.xpath('.//wsg:long/text()', namespaces=ns)[0]
        name = doc.tree.xpath('.//gn:name/text()', namespaces=ns)[0]
        country_code = doc.tree.xpath('.//gn:countryCode/text()', namespaces=ns)[0]
    except:
        item
    return {
        "url": url,
        "lat": lat,
        "long": long,
        "name": name,
        "country_code": country_code
    }

data = []
for x in tqdm(sorted(files), total=len(files)):
    _, file_name = os.path.split(x)
    hash_id = file_name.replace('cmi__', '').replace('.xml', '')
    try:
        doc = TeiReader(x)
    except Exception as e:
        continue
    cor_title = " ".join(" ".join(doc.any_xpath(
            './/tei:sourceDesc/tei:bibl//text()'
        )).split())
    for cur_num, c in enumerate(doc.any_xpath('.//tei:correspDesc')):
        item = {}
        item['key'] = f"gen_id__{cur_num}"
        item['hash_id'] = hash_id
        item['cor_title'] = cor_title
        try:
            item['place_sender_name'] = c.xpath(
                './/tei:correspAction[@type="sent"]/tei:placeName[1]/text()',
                namespaces=ns
            )[0]
        except IndexError:
            item['place_sender_name'] = "unbekannt"
        try:
            item['place_sender_ref'] = get_normalized_uri(
                    c.xpath(
                    './/tei:correspAction[@type="sent"]/tei:placeName[1]/@ref',
                    namespaces=ns
                )[0]
            )
        except IndexError:
            item['place_sender_ref'] = "unbekannt"
        try:
            item['sender_name'] = c.xpath(
                './/tei:correspAction[@type="sent"]/tei:persName[1]/text()',
                namespaces=ns
            )[0]
        except IndexError:
            item['sender_name'] = "unbekannt"
        try:
            item['sender_ref'] = get_normalized_uri(
                    c.xpath(
                    './/tei:correspAction[@type="sent"]/tei:persName[1]/@ref',
                    namespaces=ns
                )[0]
            )
        except IndexError:
            item['sender_ref'] = "unbekannt"
        try:
            item['place_receiver_name'] = c.xpath(
                './/tei:correspAction[@type="received"]/tei:placeName[1]/text()',
                namespaces=ns
            )[0]
        except IndexError:
            item['place_receiver_name'] = "unbekannt"
        try:
            item['place_receiver_ref'] = get_normalized_uri(
                    c.xpath(
                    './/tei:correspAction[@type="received"]/tei:placeName[1]/@ref',
                    namespaces=ns
                )[0]
            )
        except IndexError:
            item['place_receiver_ref'] = "unbekannt"
        try:
            item['receiver_name'] = c.xpath(
                './/tei:correspAction[@type="received"]/tei:persName[1]/text()',
                namespaces=ns
            )[0]
        except IndexError:
            item['receiver_name'] = "unbekannt"
        try:
            item['receiver_ref'] = get_normalized_uri(
                    c.xpath(
                    './/tei:correspAction[@type="received"]/tei:persName[1]/@ref',
                    namespaces=ns
                )[0]
            )
        except IndexError:
            item['receiver_ref'] = "unbekannt"
        try:
            date = c.xpath('.//tei:date[1]', namespaces=ns)[0]
            dates = []
            for key, value in date.attrib.items():
                dates.append(value[:4])
            item['year'] = dates[0]
        except:
            item['year'] = "0000"
        data.append(item)

df = pd.DataFrame(data)
df.to_csv(CMI_MD_FILE, index=False, compression='zip')
