import os
import subprocess
import urllib.request
import tarfile

# Step 1: Create a working directory
os.makedirs("tmate_install", exist_ok=True)
os.chdir("tmate_install")

# Step 2: Download precompiled tmate (static build)
tmate_url = "https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-amd64.tar.xz"
tmate_tar = "tmate.tar.xz"

if not os.path.exists("tmate"):
    print("[*] Downloading tmate...")
    urllib.request.urlretrieve(tmate_url, tmate_tar)

    print("[*] Extracting tmate...")
    with tarfile.open(tmate_tar) as tar:
        tar.extractall()
    
    os.rename("tmate-2.4.0-static-linux-amd64", "tmate")

# Step 3: Run tmate (note: this opens an interactive session)
print("[*] Starting tmate...")
subprocess.run(["./tmate/tmate", "-F"], check=False)
