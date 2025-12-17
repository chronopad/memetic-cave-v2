import os 
import sys 
import shutil
from src.malconv_nn import malconv
from hashlib import sha256

OG_DIR = "malwares"
GA_DIR = "ga_dir"
MA_DIR = "ma_dir"

if len(sys.argv) == 1:  
    for f in os.listdir(OG_DIR):
        src_path = os.path.join(OG_DIR, f)
        if os.path.isfile(src_path) and f.lower().endswith(".exe"):
            shutil.copy(src_path, GA_DIR)
            shutil.copy(src_path, MA_DIR)

    os.system(f"cd src; python3 original.py -p ../{GA_DIR}")
    os.system(f"cd src; python3 memetic-cave.py -p ../{MA_DIR}")

files = [f for f in os.listdir(OG_DIR) if os.path.isfile(os.path.join(OG_DIR, f)) and f.lower().endswith(".exe")]
model = malconv("src/malconv.h5")

print("\n==== Predictions ====\n")
for f in files:
    pred_og = model.predict(f"{OG_DIR}/{f}")
    pred_ga = model.predict(f"{GA_DIR}/{f}")
    pred_ma = model.predict(f"{MA_DIR}/{f}")

    print(f"File: {f}")
    print(f"  Original: {pred_og:.8f} -", sha256(open(f"{OG_DIR}/{f}", "rb").read()).hexdigest())
    print(f"  GA:       {pred_ga:.8f} -", sha256(open(f"{GA_DIR}/{f}", "rb").read()).hexdigest())
    print(f"  MA:       {pred_ma:.8f} -", sha256(open(f"{MA_DIR}/{f}", "rb").read()).hexdigest())
    print("-" * 30)