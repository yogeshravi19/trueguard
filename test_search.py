import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time

def query_arxiv(query_str):
    url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query_str)}&start=0&max_results=1'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        xml_data = resp.read()
        root = ET.fromstring(xml_data)
        opensearch_ns = '{http://a9.com/-/spec/opensearch/1.1/}'
        total = root.find(f'{opensearch_ns}totalResults')
        return total.text if total is not None else '0'

queries = [
    ('ti:"hallucination" AND ti:"detection"', 'ti:"hallucination" AND ti:"detection"'),
    ('ti:"hallucination" AND (ti:"detection" OR ti:"mitigation")', 'ti:"hallucination" AND (ti:"detection" OR ti:"mitigation")'),
    ('ti:"hallucination" AND ti:"LLM"', 'ti:"hallucination" AND ti:"LLM"'),
    ('ti:"hallucination" AND ti:"large language models"', 'ti:"hallucination" AND ti:"large language models"'),
    ('ti:"hallucination" AND (ti:"detection" OR ti:"mitigation" OR ti:"uncertainty" OR ti:"entropy")', 'ti:"hallucination" AND (ti:"detection" OR ti:"mitigation" OR ti:"uncertainty" OR ti:"entropy")'),
]

for desc, q in queries:
    try:
        count = query_arxiv(q)
        print(f'{desc} -> {count} hits')
        time.sleep(1)
    except Exception as e:
        print(f'{desc} -> Error: {e}')
