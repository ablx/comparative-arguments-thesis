import requests
import spacy
import editdistance
from collections import defaultdict
from pprint import pprint
import json
import re

ES_ENDPOINT = "http://localhost:9222/fd2/freq"
url_pattern = 'http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws/api/trigram/jo/similar/{}?numberOfEntries=25&format=json'

groups = []
dups = set()
header = 'name,source,type,cleaned_name,freq\n'
pattern = '{},{},{},{},{}\n'

def get_words(term):
    req = requests.get(url_pattern.format(term)).json()['results']
    for word in req:
        term2 = word['key']
        h = hash(term) + hash(term2)
        if h not in dups and ( editdistance.eval(term,term2) >= 2 or editdistance.eval(term,term2) == 0):
            dups.add(h)
            freq = get_freq(term2)
            line = pattern.format(term2, 'jobimtext', 'seed=' + term, term2,
                                  freq)
            groups.append(line)


def get_freq(term):
    contains_word = re.compile(r'\w')
    try:
        query = '{{ "query": {{ "query_string": {{ "fields": ["word"], "query": "\\"{}\\"" }} }} ,  "sort" : {{"freq" : "desc"}} }}'.format(
            str(term).strip().encode('utf-8').decode('utf-8'))
        res = requests.post(
            url=ES_ENDPOINT + "/_search", data=query.encode('utf-8'))
        hits = res.json()['hits']
        if len(hits) > 0 and len(hits['hits']):
            hits_data = hits['hits'][0]['_source']
            return hits_data['freq']
        return 0
    except KeyError as e:
        print(e)
        return -1


get_words('apple')
get_words('prune')


with open('jbt.csv', 'w') as f:
    f.write(header)
    for line in groups:
        f.write(line)