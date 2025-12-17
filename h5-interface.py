from src.malconv_nn import malconv
import sys, os

MALWARE_DIR = "malwares"
model = malconv("src/malconv.h5")

if len(sys.argv) == 2:
    sha256 = sys.argv[1]
    prediction = model.predict(f"{MALWARE_DIR}/{sha256}.exe")
    print(f"{sha256}: {prediction}")
# else:
#     files = [f for f in os.listdir(MALWARE_DIR) if f.endswith(".exe")]
#     for filename in files:
#         file_path = os.path.join(MALWARE_DIR, filename)
#         try:
#             with open(file_path, "rb") as f:
#                 file_data = f.read()
#             prediction = ember.predict_sample(lgbm_model, file_data)
#             print(f"{filename}: {prediction}")
#         except Exception as e:
#             print(f"Error processing {filename}: {e}")