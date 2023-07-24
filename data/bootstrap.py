import json 
import random
import time
import os

raw_data : str = "cifdata.txt"

def buildDatabase() -> None:

    file = open("cifdata.txt", "r", encoding="latin1")
    lines = file.readlines()
    file.close()

    ciffile = []
    numid = 10000
    for (il, line) in enumerate(lines):

        if "END" not in line:

            ciffile.append(line)

            if "chemical_name_mineral" in line:
                name = line.split("_chemical_name_mineral")[-1].replace("'", "").strip()
            if "cell_length_a" in line:
                a = float(line.split()[-1].replace(",", ""))
            if "cell_length_b" in line:
                b = float(line.split()[-1].replace(",", ""))
            if "cell_length_c" in line:
                c = float(line.split()[-1].replace(",", ""))
            if "cell_angle_alpha" in line:
                alpha = float(line.split()[-1])
            if "cell_angle_beta" in line:
                beta = float(line.split()[-1])
            if "cell_angle_gamma" in line:
                gamma = float(line.split()[-1])
            if "cell_volume" in line:
                volume = float(line.split()[-1])
            if "symmetry_space_group_name" in line:
                sgroup = line.split("symmetry_space_group_name_H-M")[-1]
                sgroup = sgroup.replace(",", "").replace(" ", "").replace("'", "")
            if "chemical_formula_sum" in line:
                line = line.replace("(", "").replace(")", "").replace("'", "")
                species = list(map(lambda x : "".join([s.replace('.', '') for s in x if not s.isnumeric() ]), line.split()[1:]))
                species = " ".join(species)
        else:
            ciffile.append(line)
            Crystal = {}

            Crystal['id']      = numid
            assert name != '', f"Error parsing name {name}, check line numer = {il}"
            Crystal['name']    = name
            Crystal['lattice'] = [a,b,c, alpha, beta, gamma]
            Crystal['volume']  = volume
            Crystal['sgroup']  = sgroup
            Crystal['atoms']   = species
            Crystal['file']    = "".join(ciffile)
            with open(str(Crystal['id'])+'.json', 'w') as file:
                json.dump(Crystal, file)
            numid += 1
            ciffile = []

if __name__ == "__main__":

    BUILD = int(os.getenv("BUILD")) if os.getenv("BUILD") is not None else 0

    if BUILD:
        print("You have elected to build the json representation of the database.\nWaiting 5 seconds before starting...")
        time.sleep(5)
        start = time.time()
        buildDatabase()
        stop = time.time()
        print(f"Finished building database in {(stop-start)} seconds")
