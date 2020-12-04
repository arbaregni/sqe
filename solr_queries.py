import pip
import json
import urllib.parse
import urllib.request
import codecs

#Solr parameters
PORT = '8983'
COLLECTION = 'trec'
NUM_FILES = 100

#Trec parameter
IR_MODEL = 'DFR' 

def make_request(query):
    print(f'making request "{query}"...')
    query = urllib.parse.quote(query)
    url = f'http://localhost:{PORT}/solr/{COLLECTION}/select?fl=docno%2C%20score&q=doctext%3A({query})&rows={NUM_FILES}&sort=score%20desc'
    data = urllib.request.urlopen(url)
    return json.load(data)['response']['docs']

def run_test_queries(queries, expansions, expansion_weight, file):
    for qid, query_text in queries:
        expansion_terms = expansions[qid].split(' ')
        expansion = ' '.join([f'{term}^{expansion_weight}' for term in expansion_terms])
        results = make_request(f'{query_text} {expansion}')
        rank = 1
        for result in results:
            docno = str(result["docno"]).replace("'", '').replace(']', '').replace('[', '')
            file.write(f'{qid} Q0 {docno} {rank} {result["score"]} {IR_MODEL}\n')
            rank += 1            

# read in queries
queries = []  #pairs of (query id's, query texts)
with codecs.open('queries.txt', 'r', 'UTF-8') as file:
    for line in file:
        qid, query_text = line.split(':::')
        queries.append( (qid, query_text) )

# read in expansions
expansions = {} #maps qids -> new terms
with codecs.open('expansions.txt', 'r', 'UTF-8') as file:
    for line in file:
        qid, expansion = line.split(':::')
        expansions[qid] = expansion

# weights for the expansions takes values 0.0, 0.1, ... 0.9, 1.0
for w in map(lambda w: 0.1 * w, range(0, 11)):
    with codecs.open(f'solr-results-{w}.txt', 'w', 'UTF-8') as file:
        print(f'running test queries with w = {w}')
        run_test_queries(queries, expansions, w, file)

