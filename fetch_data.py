import requests
import glob
import os
import hashlib
import pandas as pd

from acdh_tei_pyutils.tei import TeiReader
from bs4 import BeautifulSoup

CMI_DIR = './data/cmi'
to_delete = glob.glob(f"{CMI_DIR}/cmi__*.xml")
print(f"delete {len(to_delete)} files")
for x in to_delete:
    os.remove(x)


r = requests.get('https://correspsearch.net/en/data.html?view=cmiFiles')

soup = BeautifulSoup(r.text, 'html.parser')
data_spans = soup.find_all("span", class_="dataLinks")
cmi_files = []
with open('./data/urls.txt', 'w') as fp:
    for x in data_spans:
        url = x.findChildren("a" , recursive=False)[0].get('href')
        if "https://correspsearch.net/en/search.html?c" in url:
            continue
        url = url.strip()
        cmi_files.append(url.replace(' ',''))
        fp.write(f"{url}\n")
cmi_files.append('https://thun-korrespondenz.acdh.oeaw.ac.at/cmif.xml')
cmi_files.append('https://raw.githubusercontent.com/QHOD/qhodCMIFxquery/main/QhoDCMIF.xml')

report = []
total_cmifs = len(cmi_files)
for n, url in enumerate(cmi_files):
    print(f"{n}/{total_cmifs}: {url}")
    item = {
        "url": url,
        "status": "all_good"
    }
    try:
        doc = TeiReader(url)
    except Exception as e:
        item["status"] = e
        report.append(item)
        continue
    try:
        hash_id = doc.any_xpath('.//tei:sourceDesc/tei:bibl/@xml:id')[0]
    except IndexError:
        hash_id = hashlib.md5(url.encode('utf-8')).hexdigest()
    filename = os.path.join(CMI_DIR, f"cmi__{hash_id}.xml")
    doc.tree_to_file(filename)

    report.append(item)

df = pd.DataFrame(report)
print("saving report to ./data/report.csv")
df.to_csv("./data/report.csv", index=False)