# sqe
Information Retrieval 2020 Homework 2

## Expanding Queries
Running `query_expansion.py` will iterate through the queries in `queries.txt`, and put the corresponding expansions (all of the synonyms which were not present originally) in `expansions.txt` associated with the corresponding query id.

Thus, query expansion is actually performed *ahead of retrieval*. This is done just to avoid recalculating them during evaluation.
Why didn't I just structure it so I wouldn't have to do that? That's a good question, and one that defies all logic.

## Querying Solr
Running `solr_queries.py` will format each query by appending the downweighted expansions to the original query, and making the request to Solr.
If `0.4` is the current expansion_weight, the results are written to `solr-results-0.4.txt` (up to floating point imprecision).

This is done on each expansion weight from `0.0, 0.1, ... 0.9, 1.0`.

## Data Collection

Assuming you have a `groundTruth.txt` and `trec_eval`, you can evaluate the performance like so:
Run
```
 ./trec_eval -q -m map -m num_rel_ret groundTruth.txt solr-results-0.4.txt > out.txt
```
Then, to append the results to a csv file named `all-results.csv`, with the weight set to be `0.4`, run
```
python3 out.txt 0.4 >> all-results.txt
```

This assumes the header of `all-results.csv` is:
```
weight,qid,map,num_rel_ret
...
```
