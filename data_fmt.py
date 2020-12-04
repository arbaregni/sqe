import sys

data = {}
with open(sys.argv[1], 'r') as file:
    for line in file:
        measure, qid, x = line.split()
        if qid not in data:
            data[qid] = {}
        data[qid][measure] = x

weight = float(sys.argv[2])
for qid in data:
    print(f'{weight},{qid},{data[qid]["map"]},{data[qid]["num_rel_ret"]}')

