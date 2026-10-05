import csv
from datetime import datetime
from pathlib import Path

labels = sorted(p.stem for p in Path("output").glob("*.wav"))

print("Score each file from 1 (worst) to 5 (best).")
print()

session = datetime.now().strftime("%Y-%m-%d %H:%M")
rows = []

for label in labels:
    while True:
        answer = input(f"Score for {label} (1-5): ")
        if answer.isdigit() and 1 <= int(answer) <= 5:
            score = int(answer)
            break
        print("Please enter a whole number from 1 to 5.")
    comment = input(f"Comment on {label} (optional): ")
    rows.append([session, label, score, comment])

new_file = not Path("results.csv").exists()
with open("results.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["session", "label", "score", "comment"])
    writer.writerows(rows)

print()
print("Saved", len(rows), "scores to results.csv")
