import os
from api_key import APIKEY
from mp_api.client import MPRester


setenv = lambda x, default : int(os.getenv(x)) if os.getenv(x) is not None else default
QUICK = setenv('QUICK', 0)

# Materials Project API
mpr = MPRester(APIKEY)

parse_mid = lambda x : x.json().split(",")[0].split(":")[-1].strip().replace("\"", "")


def build_key_database(fields=['material_id'], num_chunks=100, chunk_size=100):
    m_ids = None
    response = mpr.materials.search(fields=fields,
                                    num_chunks=num_chunks,
                                    chunk_size=chunk_size
                                    )
    if response:
        m_ids = list(map(parse_mid, response))
    else:
        raise Exception("ERROR: did not successfully retrieve data from the Materials Project API")
    return m_ids

def summarize_mag_data(data):
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
    for k, v in ordering.items():
        print(f"{k } = {v}")


def build_mag_data_from_keys(materials_ids):
    mag_by_id = lambda x : mpr.magnetism.get_data_by_id(x, fields=['is_magnetic', 'ordering'])
    dmag = list(map(mag_by_id, materials_ids))
    data = {}
    for mid, d in zip(materials_ids, dmag):
        data[mid] = d

    return data

if __name__ == "__main__":

    if QUICK: mids = build_key_database(num_chunks=10, chunk_size=10)
    else : mids = build_key_database(num_chunks=100, chunk_size=100)
    mag_info = build_mag_data_from_keys(mids)
    summarize_mag_data(mag_info)
