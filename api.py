import logging
from flask import Flask, request, jsonify
import sqlite3

from sgroup  import SG_NUM_TO_NAME, SG_NAME_TO_NUM


# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

DATABASE = 'data/database.db'


def error_response(message, status_code):
    response = jsonify({'error': message})
    response.status_code = status_code
    return response


def write_json(response):
    keys = ['id', 'name', 'lattice', 'volume', 'atoms', 'sgroup', 'source']
    return {k : v for (k,v) in zip(keys, response) }

@app.route('/material/<int:material_id>', methods=['GET'])
def get_material_by_id(material_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materials WHERE id = ?', (material_id,))
    material = cursor.fetchone()
    conn.close()

    if material:
        return jsonify(write_json(material))
    else:
        logging.debug('Material not found')
        return error_response('Material not found', 404)

@app.route('/material/<name>', methods=['GET'])
def get_material_by_name(name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materials WHERE name = ?', (name,))
    material = cursor.fetchone()
    conn.close()

    if material:
        return jsonify(write_json(material))
    else:
        logging.debug('Material not found')
        return error_response('Material not found', 404)

@app.route('/materials/', methods=['GET'])
def query_materials():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = 'SELECT * FROM materials where 1=1'
    params = []

    volume = request.args.get('volume')
    if volume:
        query += ' AND volume >= ?'
        params.append(float(volume))

    atom  = request.args.get('atom')
    if atom:
        atom_symbols = atom.split(',')
        atom_conditions = ' OR '.join(['atoms LIKE ?' for _ in atom_symbols])
        query += f' AND ({atom_conditions})'
        for symbol in atom_symbols: params.append(f'%{symbol}%')

    cursor.execute(query, params)
    materials = cursor.fetchall()
    conn.close()

    result = []
    for material in materials:
        result.append(write_json(material))
    return jsonify(result)

    sgroup = request.args.get('sgroup')
    if sgroup:
        sgroup = int(sgroup)
        if sgroup < 1 or sgroup > 230:
            logging.debug('Invalid space group number')
            return error_response('Invalid space group number', 404)

        query += ' AND sgroup LIKE ?'
        params.append(f'%{SG_NUM_TO_NAME[sgroup]}%')

    cursor.execute(query, params)
    materials = cursor.fetchall()
    conn.close()

    result = []
    for material in materials:
        result.append(write_json(material))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
