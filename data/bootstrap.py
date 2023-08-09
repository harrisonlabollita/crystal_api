import json
import time
import os
import requests
import zipfile
import shutil

import sqlite3

PATH = __file__.split('/')[0]

DATA_PATH: str = PATH + "/cif/cifdata.txt" # encoded in latin1
URL : str = "http://rruff.geo.arizona.edu/AMS/zipped_files/cif_archive_2023_07_30.zip"

def fetch_data() -> None:
    print('fetching data...')
    response = requests.get(URL)
    if response.status_code == 200:
        print('fetch successful...writing zip file')
        with open(PATH+'/data.zip', 'wb') as file: file.write(response.content)
    print('unzipping data to dir cif')
    with zipfile.ZipFile(PATH+'/data.zip',  'r') as zipref: zipref.extractall(PATH+'/cif')

def cleanup() -> None:
    print('cleaning up from bootstrap...')
    if os.path.isfile(PATH+'/data.zip'): os.remove(PATH+'/data.zip')
    if os.path.isdir(PATH+'/cif'): shutil.rmtree(PATH+'/cif')


def build_database() -> None:

    print('building sql database...')

    file = open(DATA_PATH, "r", encoding="latin1")
    lines = file.readlines()
    file.close()

    conn = sqlite3.connect(PATH+'/database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY,
        name TEXT,
        lattice TEXT,
        volume REAL,
        atoms TEXT,
        sgroup TEXT,
        source TEXT
        )
    ''')

    ciffile = []
    for (il, line) in enumerate(lines):
        if "END" not in line:
            ciffile.append(line)
            if "chemical_name_mineral" in line: name = line.split("_chemical_name_mineral")[-1].replace("'", "").strip()
            if "cell_length_a" in line: a = float(line.split()[-1].replace(",", ""))
            if "cell_length_b" in line: b = float(line.split()[-1].replace(",", ""))
            if "cell_length_c" in line: c = float(line.split()[-1].replace(",", ""))
            if "cell_angle_alpha" in line: alpha = float(line.split()[-1])
            if "cell_angle_beta" in line: beta = float(line.split()[-1])
            if "cell_angle_gamma" in line: gamma = float(line.split()[-1])
            if "cell_volume" in line: volume = float(line.split()[-1])
            if "symmetry_space_group_name" in line: 
                sgroup = line.split("symmetry_space_group_name_H-M")[-1].strip().replace(",", "").replace("'", "")
                sgroup = "".join(sgroup.split())
            if "chemical_formula_sum" in line:
                line = line.replace("(", "").replace(")", "").replace("'", "")
                atoms = list(map(lambda x : "".join([s.replace('.', '') for s in x if not s.isnumeric() ]), line.split()[1:]))
                atoms = " ".join(atoms)
        else:
            ciffile.append(line)
            lattice = json.dumps([a,b,c, alpha, beta, gamma])
            source    = "".join(ciffile)
            # write to database
            cursor.execute('''
                INSERT INTO materials (name, lattice, volume, atoms, sgroup, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, lattice, volume, atoms, sgroup, source)
            )
            ciffile = []
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fetch_data()
    build_database()
    cleanup()


