"""Download the raw Météo-France files used by prepare_data.ipynb into data/raw/.

Usage:
    python download_data.py          # only downloads the missing files
    python download_data.py --force  # downloads everything again
"""
import gzip
import os
import shutil
import sys

import requests

# Météo-France, "Données climatologiques de base - quotidiennes" on data.gouv.fr
DATASET_API = "https://www.data.gouv.fr/api/1/datasets/6569b51ae64326786e4e8e1a/"
RAW_FOLDER = "data/raw/"

# The 5 Pyrenean departments, and the 4 files we need for each one
DEPARTMENTS = ["09", "31", "64", "65", "66"]
FILE_TYPES = [
    "previous-1950-2024_RR-T-Vent",
    "latest-2025-2026_RR-T-Vent",
    "previous-1950-2024_autres-parametres",
    "latest-2025-2026_autres-parametres",
]

# With "--force", the files are downloaded again even if they already exist
force = "--force" in sys.argv

os.makedirs(RAW_FOLDER, exist_ok=True)

# Names of the files we want, for example "Q_09_previous-1950-2024_RR-T-Vent.csv.gz"
wanted = []
for dept in DEPARTMENTS:
    for file_type in FILE_TYPES:
        wanted.append(f"Q_{dept}_{file_type}.csv.gz")

# Ask data.gouv.fr for the list of all the files of the dataset, with their download link
resources = requests.get(DATASET_API, timeout=60).json()["resources"]

for resource in resources:
    url = resource["url"]
    gz_name = url.split("/")[-1]
    if gz_name not in wanted:
        continue

    csv_path = RAW_FOLDER + gz_name.replace(".gz", "")
    gz_path = RAW_FOLDER + gz_name

    # Do not download a file we already have (unless --force)
    if os.path.exists(csv_path) and not force:
        print("Already there:", csv_path)
        continue

    # 1. Download the compressed file (.csv.gz), piece by piece
    print("Downloading:", gz_name)
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(gz_path, "wb") as file:
            for piece in response.iter_content(chunk_size=1024 * 1024):
                file.write(piece)

    # 2. Unzip it into a .csv file, then delete the .csv.gz
    with gzip.open(gz_path, "rb") as compressed, open(csv_path, "wb") as file:
        shutil.copyfileobj(compressed, file)
    os.remove(gz_path)
    print("Saved:", csv_path)

print("Done: the raw files are in", RAW_FOLDER)
