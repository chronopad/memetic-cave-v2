import ember
import lightgbm as lgb
import sys
import os

lgbm_model = lgb.Booster(model_file="weight-ember.txt")
MALWARE_DIR = "malwares"

if len(sys.argv) == 2:
    sha256 = sys.argv[1]
    putty_data = open(f"{MALWARE_DIR}/{sha256}.exe", "rb").read()
    print(f"{sha256}: {ember.predict_sample(lgbm_model, putty_data)}")
else:
    files = [f for f in os.listdir(MALWARE_DIR) if f.endswith(".exe")]
    for filename in files:
        file_path = os.path.join(MALWARE_DIR, filename)
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            prediction = ember.predict_sample(lgbm_model, file_data)
            print(f"{filename}: {prediction}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
