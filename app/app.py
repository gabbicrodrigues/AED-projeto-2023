from flask import Flask, request, jsonify
from btree import BTree, BTreeNode
import requests
import json

app = Flask(__name__)

def load_b_tree(file_url):
    response = requests.get(file_url)
    b_tree = BTree.load_from_file(response.content)

    # Carrega a B-tree em chunks
    # response = requests.get(file_url, stream=True)
    # response.raise_for_status()
    # b_tree = BTree.load_from_file_in_chunks(response.iter_content(chunk_size=1240))

    return b_tree

@app.route('/health', methods=['GET'])
def check() :
    return { "success" : True }

@app.route('/user/search', methods=['GET'])
def user_search():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://user-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    result = b_tree.search(key)  # Assuming the search function returns a tuple (node, position)

    try : 
        result_node, index = result

        if result_node is not None:
            found_value = result_node.values[index]
            print(f"Found {key} in the B-tree with value : {found_value}")
            return found_value

    except:
        return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/user/insert', methods=['POST'])
def user_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

    b_tree = load_b_tree('http://user-storage:80/')

    if b_tree is None:
        return {'error': f'Btree not loaded.'}

    id_value = data['id']

        # Assuming 'id' is the key and 'survived' is the value in the B-tree
    b_tree.insert(id_value, data)
        
     # Saving the B-tree to the storage server
    save_response = requests.post('http://user-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/user/delete', methods=['DELETE'])
def user_delete():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://user-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    b_tree.remove(key)  # Assuming the search function returns a tuple (node, position)
    
         # Saving the B-tree to the storage server
    save_response = requests.post('http://user-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200


@app.route('/book/search', methods=['GET'])
def book_search():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://book-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    result = b_tree.search(key)  # Assuming the search function returns a tuple (node, position)
    try : 
        result_node, index = result

        if result_node is not None:
            found_value = result_node.values[index]
            print(f"Found {key} in the B-tree with value : {found_value}")
            return found_value

    except:
        return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/book/insert', methods=['POST'])
def book_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

    b_tree = load_b_tree('http://book-storage:80/')

    if b_tree is None:
        return {'error': f'Btree not loaded.'}

    id_value = data['id']

        # Assuming 'id' is the key and 'survived' is the value in the B-tree
    b_tree.insert(id_value, data)
        
     # Saving the B-tree to the storage server
    save_response = requests.post('http://book-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/book/delete', methods=['DELETE'])
def book_delete():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://book-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    b_tree.remove(key)  # Assuming the search function returns a tuple (node, position)
    
         # Saving the B-tree to the storage server
    save_response = requests.post('http://book-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200

@app.route('/rating/search', methods=['GET'])
def rating_search():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://rating-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    result = b_tree.search(key)  # Assuming the search function returns a tuple (node, position)
    try : 
        result_node, index = result

        if result_node is not None:
            found_value = result_node.values[index]
            print(f"Found {key} in the B-tree with value : {found_value}")
            return found_value

    except:
        return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/rating/insert', methods=['POST'])
def rating_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

    b_tree = load_b_tree('http://rating-storage:80/')

    if b_tree is None:
        return {'error': f'Btree not loaded.'}

    id_value = data['id']

        # Assuming 'id' is the key and 'survived' is the value in the B-tree
    b_tree.insert(id_value, data)
        
     # Saving the B-tree to the storage server
    save_response = requests.post('http://rating-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/rating/delete', methods=['DELETE'])
def rating_delete():
    key = request.args.get('id') 

    b_tree = load_b_tree('http://rating-storage:80/')
    if b_tree is None:
        return {'error': f'Btree is not loaded.'}

    b_tree.remove(key)  # Assuming the search function returns a tuple (node, position)
    
         # Saving the B-tree to the storage server
    save_response = requests.post('http://rating-storage:80/save', json=b_tree.to_json())

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)