from flask import Flask, request, jsonify

import sqlite3

app = Flask(__name__)

DATABASE = 'data/database.db'

def write_json(response):
    keys = ['id', 'name', 'lattice', 'volume', 'atoms', 'sgroup', 'source']
    return jsonify( {k : v for (k,v) in zip(keys, response) } )

@app.route('/material/<int:material_id>', methods=['GET'])
def get_material_by_id(material_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materials WHERE id = ?', (material_id,))
    material = cursor.fetchone()
    conn.close()
    if material: return write_json(material)
    else: return jsonify({'message' : 'Material not found' }), 404


if __name__ == "__main__":
    app.run(debug=True)
