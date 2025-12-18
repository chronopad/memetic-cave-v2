import os 
import sys 
import shutil
import json
import signal
from src.malconv_nn import malconv
from hashlib import sha256

OG_DIR = "malwares"
GA_DIR = "ga_dir"
MA_DIR = "ma_dir"

def save_and_exit(sig, frame):
    with open("temp_results.json", "w", encoding="utf-8") as fout:
        json.dump(results, fout, indent=2)

for f in os.listdir(OG_DIR):
    src_path = os.path.join(OG_DIR, f)
    if os.path.isfile(src_path):
        shutil.copy(src_path, GA_DIR)
        shutil.copy(src_path, MA_DIR)

print("[+] Running GA...")
os.system(f"cd src; python3 original.py -p ../{GA_DIR}")

print("[+] Running MA...")
os.system(f"cd src; python3 memetic-cave.py -p ../{MA_DIR}")

files = [f for f in os.listdir(OG_DIR) if os.path.isfile(os.path.join(OG_DIR, f))]
model = malconv("src/malconv.h5")

signal.signal(signal.signal.SIGINT, save_and_exit)

results = []
for f in files:
    pred_og = model.predict(f"{OG_DIR}/{f}")
    pred_ga = model.predict(f"{GA_DIR}/{f}")
    pred_ma = model.predict(f"{MA_DIR}/{f}")

    results.append(
        {
            "file" : f,
            "original" : float(pred_og),
            "genetic" : float(pred_ga),
            "memetic" : float(pred_ma),
        }
    )

    print(f"File: {f}")
    print(f"  Original: {pred_og:.8f} -", sha256(open(f"{OG_DIR}/{f}", "rb").read()).hexdigest())
    print(f"  GA:       {pred_ga:.8f} -", sha256(open(f"{GA_DIR}/{f}", "rb").read()).hexdigest())
    print(f"  MA:       {pred_ma:.8f} -", sha256(open(f"{MA_DIR}/{f}", "rb").read()).hexdigest())
    print("-" * 30)

with open("results.json", "w", encoding="utf-8") as fout:
    json.dump(results, fout, indent=2)

