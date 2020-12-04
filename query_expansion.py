import nltk
from nltk.corpus import wordnet
import itertools
import codecs

def wordnet_tag_from_penn(tag):
    """
    Converts a penn part of speech tag to a wordnet tag
    Example "NNS" (singular noun) becomes wordnet.NOUN
    """
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    elif tag.startswith('V'):
        return wordnet.VERB
    return None

def sim(synset1, synset2):
    """
    normalized similarity score in the interval [0,1]
    between two synsets
    """
    score = synset1.wup_similarity(synset2)
    if score is None:
        score = 0
    return score

def coherence(synsets):
    """
    total pair-wise similarity between every synset in `synsets`
    """
    total = 0
    synset_pairs = itertools.combinations_with_replacement(synsets, 2)
    for s1, s2 in synset_pairs:
        total += sim(s1, s2)
    return total

def main_synsets_of(tokens):
    """
    each noun or verb in this sentence could be a number of synsets
    return a list of those choices
    """
    tagged = nltk.pos_tag(tokens)
    tagged = [(tok, wordnet_tag_from_penn(tag)) for tok, tag in tagged]
    # synset choices is a sequence [S_1, S_2, ...]
    # where S_i is possible synsets for token i (including only nouns and verbs)
    synset_choices = [
        wordnet.synsets(tok, pos)
        for tok, pos in tagged
        if pos == wordnet.NOUN # or pos == wordnet.VERB
    ]
    # print(synset_choices)
    # we want to pick a synset for each noun/verb.
    # this is an element of the cartesian product S_1 × S_2 × ...
    feasible_solns = itertools.product(*synset_choices)
    try:
        soln = max(feasible_solns, key = coherence)
    except ValueError:
        soln = tuple() # no feasible solutions
    return soln
    
def expand_query(original_query):
    """
    append new word forms to the given query
    these are assigned a weight of `expansion_weight`

    returns a set of terms to add to the query
    """

    tokens = nltk.word_tokenize(original_query)
    # remove non words and duplicates
    tokens = set([tok.lower() for tok in tokens if tok.isalnum()])
    
    synsets = main_synsets_of(tokens)
    
    # find the new terms
    expansions = []
    for synset in synsets:
        for lemma in synset.lemmas():
            # some lemma names are separated by underscores, as in 'sea_bass'
            for t in lemma.name().split('_'):
                # original terms are already accounted for
                if t not in tokens:
                    # expansion terms (i.e. the synonyms) are not
                    expansions.append(t)
                    
    return expansions

##    original = input('Query TREC collection> ')
##    query = expand_query(original, 0.5)
##    print(f'Expanded query> {query}')


# list of (query id, query text) pairs
queries = []
with codecs.open('queries.txt','r','UTF-8') as file:
    for line in file:
        elements = line.split(":::")
        qid, qtext = elements[0], elements[1]
        queries.append((qid, qtext))

# find their expansions
with codecs.open('expansions.txt', 'w', 'UTF-8') as file:
    for qid, qtext in queries:
        print(f'Expanding query {qid}...')
        expansion = ' '.join(expand_query(qtext))
        file.write(f'{qid}:::{expansion}\n')
