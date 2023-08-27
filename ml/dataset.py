import os
import glob

# materials project
from api_key import APIKEY
from mp_api.client import MPRester

# pymatgen
from pymatgen.core.structure import Structure


setenv = lambda x, default : int(os.getenv(x)) if os.getenv(x) is not None else default

INMP  = setenv('INMP', 0)
MAG   = setenv('MAG',  0)

QUICK = setenv('QUICK', 0)
VERB  = setenv('VERB',  0)



# Materials Project API
mpr = MPRester(APIKEY)

def find_overlap_of_databases() -> None:
    def find_struct(x):
        try:
            res = mpr.find_structure(x)
            return res
        except Exception as e:
            print(x)
            return None

    ciffiles = sorted(glob.glob("../data/*.cif"), key = lambda x : int(x.split('_')[1].split('.')[0]))
    mpids = []
    for cif in ciffiles:
        mid = find_struct(cif)
        if mid: mpids.append(mid)

    print(f"Total structures: {len(ciffiles)}")
    print(f"Total in MP:      {len(mpids)   } ({(len(mpids)*100/len(ciffiles)):.2f}%)")

parse_material_id = lambda x : x.json().split(",")[0].split(":")[-1].strip().replace("\"", "")

# fetch material ids
def build_key_database(fields=['material_id'], num_chunks=100, chunk_size=100) -> list[str]:
    m_ids = None
    response = mpr.materials.search(fields=fields,
                                    num_chunks=num_chunks,
                                    chunk_size=chunk_size
                                    )

    if response: m_ids = list(map(parse_material_id, response))
    else: raise Exception("ERROR: did not successfully retrieve data from the Materials Project API")

    return m_ids


# fetch the magnetism data from material ids
def build_mag_data_from_keys(materials_ids : list[str]) -> dict:
    mag_by_id = lambda x : mpr.magnetism.get_data_by_id(x, fields=['is_magnetic', 'ordering'])
    dmag = list(map(mag_by_id, materials_ids))

    data = {}
    for mid, d in zip(materials_ids, dmag): data[mid] = d

    return data

# summarize the number of magnetic materials
def summarize_mag_data(data : dict) -> None:
    is_magnetic, ordering = 0, {}
    for k, v in data.items():
        if v.is_magnetic: is_magnetic += 1
        if v.ordering in ordering.keys():
            ordering[v.ordering] += 1
        else:
            ordering[v.ordering] = 1
    print('mag data summary:')
    print('magnetic materials = ', is_magnetic)
    print('mag orderings : ')
    for k, v in ordering.items(): print(f"{k } = {v}")


# fetch crystal structure from material ids
def fetch_crystal_structure_from_id(material_ids : list[str]) -> dict[str, Structure]:
    structures = list(map(mpr.get_structure_by_material_id, material_ids))

    data = {}
    for mid, structure in zip(material_ids, structures): data[mid] = structure

    return data

if __name__ == "__main__":

    if INMP: find_overlap_of_databases()

    if MAG:
        if QUICK: mids = build_key_database(num_chunks=1, chunk_size=10)
        else : mids = build_key_database(num_chunks=100, chunk_size=100)
        mag_info = build_mag_data_from_keys(mids)
        if VERB: summarize_mag_data(mag_info)

        structures = fetch_crystal_structure_from_id(mids)

