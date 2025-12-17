import os
import pefile
from src.malconv_nn import malconv

def check_sample(file):
    prob = model.predict("malwares/{}".format(f))
    print("p[{}] = {}".format(file, prob))

    pe = pefile.PE("malwares/{}".format(f), fast_load=True)

    # check if file is a valid PE
    if not pe.is_exe() and (pe.OPTIONAL_HEADER.DATA_DIRECTORY[14].VirtualAddress != 0 or pe.OPTIONAL_HEADER.DATA_DIRECTORY[14].Size != 0):
        pe.close()
        print("[!] File is not a valid PE...")
        return False

    # check if the probability is enough to be classified as malware
    if prob < 0.5:
        print("[!] File is not detected as malicious...")
        return False

    return True

# Main runner
files = os.listdir("malwares/")
model = malconv("src/malconv.h5")

# Remove every not valid files in malwares/ directory
for f in files:
    if not check_sample(f) :
        print("[!] Removing : {}".format(f))
        os.remove("malwares/{}".format(f))
