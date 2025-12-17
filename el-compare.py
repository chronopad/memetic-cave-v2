import os 
import sys 

sha256 = sys.argv[1]
OG_DIR = "malwares/"
GA_DIR = "ga_dir/"
MA_DIR = "ma_dir/"

os.system(f"cp {OG_DIR}/{sha256}.exe {GA_DIR}/{sha256}.exe")
os.system(f"cp {OG_DIR}/{sha256}.exe {MA_DIR}/{sha256}.exe")

os.system(f"cd src; python3 original.py -b {sha256}.exe -p ../{GA_DIR}")
os.system(f"cd src; python3 memetic-cave.py -b {sha256}.exe -p ../{MA_DIR}")

print()
print("==== Checksums ====")
print(f"SHA256: {sha256}")
print("OG:", os.popen(f"sha256sum {OG_DIR}/{sha256}.exe").read())
print("GA:", os.popen(f"sha256sum {GA_DIR}/{sha256}.exe").read())
print("MA:", os.popen(f"sha256sum {MA_DIR}/{sha256}.exe").read())

print()
print("==== Predicts ====")
print("OG:", os.popen(f"python3 h5-interface.py {sha256} malwares").read())
print("GA:", os.popen(f"python3 h5-interface.py {sha256} ga_dir").read())
print("MA:", os.popen(f"python3 h5-interface.py {sha256} ma_dir").read())