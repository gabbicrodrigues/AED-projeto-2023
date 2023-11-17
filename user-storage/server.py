# server.py
from btree import BTree
from flask import Flask, send_file, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/get_page', methods=['GET'])
def get_page():
    key_to_search = int(request.args.get('id', 0))  
    btree = BTree.load_from_file('user_btree.json')
    result, index = btree.search_page(key_to_search)

    if result:
        return jsonify({'data': result.values, 'page_index' : index })
    else:
        return jsonify({'error': 'Key not found'}), 404

@app.route('/get_insert_page', methods=['GET'])
def get_insert_page():
    key_to_search = int(request.args.get('id', 0))  
    btree = BTree.load_from_file('user_btree.json')
    result, index = btree.get_insert_page(key_to_search)

    if result:
        return jsonify({'data': result.values, 'keys' : result.keys })
    else:
        return jsonify({'error': 'Key not found'}), 404

@app.route('/save_page', methods=['PUT'])
def save_page():
    page = request.get_json()  # Retrieving JSON data from the request body
    btree = BTree.load_from_file('user_btree.json')
    page = json.loads(page)
    btree.insert_page(int(page['keys'][0]), page)
     # Saving the B-tree to the storage server
    btree.save_to_file('user_btree.json')

    return jsonify({'message': 'Data updated into B-tree successfully.'}), 200
    
@app.route('/insert', methods=['POST'])
def insert():    
    data = request.get_json()  # Retrieving JSON data from the request body

    btree = BTree.load_from_file('user_btree.json')

    if btree is None:
        return {'error': f'Btree not loaded.'}

    id_value = data['id']

        # Assuming 'id' is the key and 'survived' is the value in the B-tree
    btree.insert(int(id_value), data)
        
     # Saving the B-tree to the storage server
    btree.save_to_file('user_btree.json')

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/delete', methods=['DELETE'])
def delete():
    key = request.args.get('id') 

    btree = BTree.load_from_file('user_btree.json')

    if btree is None:
        return {'error': f'Btree is not loaded.'}

    btree.remove(int(key))  # Assuming the search function returns a tuple (node, position)
    
     # Saving the B-tree to the storage server
    btree.save_to_file('user_btree.json')

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200

@app.route('/')
def serve_binary_file():
    file_path = os.path.join(os.getcwd(), 'user_btree.json')
    return send_file(file_path)

@app.route('/save', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()  # Retrieving JSON data from the request body

        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400

        with open('user_btree.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)

        return {'success': True}
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)