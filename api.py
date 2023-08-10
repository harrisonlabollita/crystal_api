from flask import Flask, request, jsonify
import sqlite3

from sgroup  import SG_NUM_TO_NAME, SG_NAME_TO_NUM


app = Flask(__name__)

DATABASE = 'data/database.db'

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
    if material: return jsonify(write_json(material))
    else: return jsonify({'message' : 'Material not found' }), 404

@app.route('/material', methods=['GET'])
def get_material_by_name():
    name = request.args.get('name')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materials WHERE name = ?', (name,))
    material = cursor.fetchone()
    conn.close()
    if material: jsonify(write_json(material))
    else: return jsonify({'message' : 'Material not found' }), 404

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
        query += ' AND atoms LIKE ?'
        params.append(f'%{atom}%')

    sgroup = request.args.get('sgroup')
    if sgroup:
        sgroup = int(sgroup)
        if sgroup < 1 or sgroup > 230:
            return jsonify({'message' : 'Invalid space group number' }), 404
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
