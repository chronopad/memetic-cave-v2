import os 
from tqdm import trange

failureMessage = "json.decoder.JSONDecodeError: Expecting value: line 2 column 1 (char 1)"

for _ in trange(100):
    res = os.popen("python3 bazaar-interface.py 20 2>&1").read()
    print(res)
    if failureMessage not in res:
        break