import os 
import sys 
import shutil
import json
import signal
import subprocess
import time
from src.malconv_nn import malconv
from hashlib import sha256
from tqdm import trange

OG_DIR = "malwares"
GA_DIR = "ga_dir"
MA_DIR = "ma_dir"

files = os.listdir(OG_DIR)
model = malconv("src/malconv.h5")

for i in trange(len(files)):
    src_path = os.path.join(OG_DIR, files[i])
    if os.path.isfile(src_path):
        shutil.copy(src_path, GA_DIR)
        shutil.copy(src_path, MA_DIR)
    print("[+] Running GA...")
    start_time = time.time()
    subprocess.run(f"cd src; python original.py -b {files[i]} -p ../{GA_DIR}", shell=True)
    end_time = time.time()

    time_ga = end_time - start_time

    print("[+] Running MA...")
    start_time = time.time()
    subprocess.run(f"cd src; python memetic-cave.py -b {files[i]} -p ../{MA_DIR}", shell=True)
    end_time = time.time()

    time_ma = end_time - start_time

    pred_og = model.predict(f"{OG_DIR}/{files[i]}")
    pred_ga = model.predict(f"{GA_DIR}/{files[i]}")
    pred_ma = model.predict(f"{MA_DIR}/{files[i]}")

    result = {
            "file" : files[i],
            "original" : float(pred_og),
            "genetic" : {
                "probability" : float(pred_ga),
                "time" : time_ga,
            },
            "memetic" : 
            {
                "probability" : float(pred_ma),
                "time" : time_ma,
            },
        }

    print(f"File: {files[i]}")
    print(f"  Original: {pred_og:.8f} -", sha256(open(f"{OG_DIR}/{files[i]}", "rb").read()).hexdigest())
    print(f"  GA:       {pred_ga:.8f} -", sha256(open(f"{GA_DIR}/{files[i]}", "rb").read()).hexdigest(), f"- {time_ga}")
    print(f"  MA:       {pred_ma:.8f} -", sha256(open(f"{MA_DIR}/{files[i]}", "rb").read()).hexdigest(), f"- {time_ma}")
    print("-" * 30)

    with open("results.json", "a", encoding="utf-8") as fout:
        json.dump(result, fout, indent=2)

