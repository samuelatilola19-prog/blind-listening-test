import json
import random
import soundfile as sf
import pyloudnorm as pyln
from pathlib import Path

files = {}
for path in Path("versions").glob("*.wav"):
    samples, rate = sf.read(path)
    meter = pyln.Meter(rate)
    files[path.name] = (samples, rate, meter.integrated_loudness(samples))

target = min(loud for _, _, loud in files.values())

names = list(files)
random.shuffle(names)

Path("output").mkdir(exist_ok=True)
key = {}

for label, name in zip("ABCDEFGH", names):
    samples, rate, loudness = files[name]
    matched = pyln.normalize.loudness(samples, loudness, target)
    sf.write(f"output/{label}.wav", matched, rate)
    key[label] = name

with open("key.json", "w") as f:
    json.dump(key, f, indent=2)

print("Created:", ", ".join(f"{label}.wav" for label in key))
print("Key saved to key.json - don't open it until you've scored everything.")
