from flask import Flask, request, jsonify
from btree import BTree, BTreeNode
import os

app = Flask(__name__)
   

@app.route('/health', methods=['GET'])
def check() :
    return { "success" : True }

@app.route('/search', methods=['GET'])
def search():
    key = request.args.get('id') 
    b_tree = BTree.load_from_file('/app/bin_files/btree_data.bin')
    if b_tree is None:
        return {'error': f'File not found.'}

    result = b_tree.search(key)  # Assuming the search function returns a tuple (node, position)
    try : 
        result_node, index = result

        if result_node is not None:
            found_value = result_node.values[index]
            print(f"Found {key} in the B-tree with value : {found_value}")
            return { 'id' : key, 'survived' : found_value }

    except:
        return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()  # Retrieving JSON data from the request body
    b_tree = BTree.load_from_file('/app/bin_files/btree_data.bin')
    if b_tree is None:
        return {'error': f'File not found.'}

    if 'id' in data and 'survived' in data:
        id_value = data['id']
        survived_value = data['survived']

        # Assuming 'id' is the key and 'survived' is the value in the B-tree
        b_tree.insert(id_value, survived_value)
        
        # Saving the B-tree to a file after every insertion
        b_tree.save_to_file('/app/bin_files/btree_data.bin')

        return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200
    else:
        return jsonify({'error': 'Please provide both "id" and "survived" in the request body.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)