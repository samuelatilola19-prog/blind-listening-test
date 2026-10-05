import csv
import json
from collections import defaultdict

with open("key.json") as f:
    key = json.load(f)

scores = defaultdict(list)
comments = defaultdict(list)

with open("results.csv", newline="") as f:
    for row in csv.DictReader(f):
        version = key[row["label"]]
        scores[version].append(int(row["score"]))
        if row["comment"]:
            comments[version].append(row["comment"])

print("RESULTS (best to worst)")
print()

ranked = sorted(scores, key=lambda v: sum(scores[v]) / len(scores[v]), reverse=True)
for version in ranked:
    avg = sum(scores[version]) / len(scores[version])
    print(f"{version}: {avg:.1f}  ({len(scores[version])} rating(s))")
    for c in comments[version]:
        print("   -", c)
