from flask import Flask, request, jsonify
from btree import BTree, BTreeNode
import requests
import json

app = Flask(__name__)

def load_b_tree(file_url):
    response = requests.get(file_url)
    print(response.content, flush=True)
    b_tree = BTree.load_from_file(response.content)
    return b_tree

@app.route('/health', methods=['GET'])
def check() :
    return { "success" : True }

@app.route('/user/search', methods=['GET'])
def user_search_page():
    try : 
        key = request.args.get('id') 
        response = requests.get(f'http://user-storage:80/get_page?id={key}')
        page = response.json()
        for user in page['data'] :
            if (user['id'] == key) :
                return user
        return jsonify({'error': f'Not found register with id : {key}'}), 404
    except:
        return jsonify({'error': f'Internal server error'}), 500
        

# @app.route('/user/search', methods=['GET'])
# def user_search():
#     key = request.args.get('id') 

#     b_tree = load_b_tree('http://user-storage:80/')
#     if b_tree is None:
#         return {'error': f'Btree is not loaded.'}

#     result = b_tree.search(int(key))  # Assuming the search function returns a tuple (node, position)

#     try : 
#         result_node, index = result

#         if result_node is not None:
#             found_value = result_node.values[index]
#             print(f"Found {key} in the B-tree with value : {found_value}")
#             return found_value

#     except:
#         return jsonify({'error': f'Not found register with id : {key}'}), 404

# @app.route('/user/insert', methods=['POST'])
# def user_insert_data():    
#     data = request.get_json()  # Retrieving JSON data from the request body

#     b_tree = load_b_tree('http://user-storage:80/')

#     if b_tree is None:
#         return {'error': f'Btree not loaded.'}

#     id_value = data['id']

#         # Assuming 'id' is the key and 'survived' is the value in the B-tree
#     b_tree.insert(int(id_value), data)
        
#      # Saving the B-tree to the storage server
#     save_response = requests.post('http://user-storage:80/save', json=b_tree.to_json())

#     if save_response.status_code != 200:
#         return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

#     return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200


@app.route('/user/insert', methods=['POST'])
def user_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

     # Saving the B-tree to the storage server
    save_response = requests.post('http://user-storage:80/insert', json=data)

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/user/insert-page', methods=['POST'])
def user_insert_page():    
    data = request.get_json()  # Retrieving JSON data from the request body
    id = int(data['id'])
    data['id'] = id

    response = requests.get(f'http://user-storage:80/get_insert_page?id={id}')
    page_to_insert = response.json()
    page_data = page_to_insert['data']
    page_keys = page_to_insert['keys']
    index_to_insert = 0
    
    for index, item in enumerate(page_to_insert['data']):
        current_key = int(item["id"])
        if id > current_key:
            index_to_insert = index + 1
        else:
            break
    
    page_data = page_data[:index_to_insert] + [data] + page_data[index_to_insert:]
    page_keys = page_keys[:index_to_insert] + [id] + page_keys[index_to_insert:]

    save_response = requests.put(f'http://user-storage:80/save_page', json=json.dumps({
        'keys' : page_keys,
        'values' : page_data
    }))
    
    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/user/delete', methods=['DELETE'])
def user_delete():
    key = request.args.get('id') 

     # Saving the B-tree to the storage server
    save_response = requests.delete(f'http://user-storage:80/delete?id={key}')

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200


@app.route('/book/search', methods=['GET'])
def book_search_page():
    try : 
        key = request.args.get('id') 
        response = requests.get(f'http://book-storage:80/get_page?id={key}')
        page = response.json()
        for book in page['data'] :
            if (book['id'] == key) :
                return book
        return jsonify({'error': f'Not found register with id : {key}'}), 404
    except:
        return jsonify({'error': f'Internal server error'}), 500

# @app.route('/book/search', methods=['GET'])
# def book_search():
#     key = request.args.get('id') 

#     b_tree = load_b_tree('http://book-storage:80/')
    
#     if b_tree is None:
#         return {'error': f'Btree is not loaded.'}

#     result = b_tree.search(int(key))  # Assuming the search function returns a tuple (node, position)
#     try : 
#         result_node, index = result

#         if result_node is not None:
#             found_value = result_node.values[index]
#             print(f"Found {key} in the B-tree with value : {found_value}")
#             return found_value

#     except:
#         return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/book/insert', methods=['POST'])
def book_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

     # Saving the B-tree to the storage server
    save_response = requests.post('http://book-storage:80/insert', json=data)

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/book/delete', methods=['DELETE'])
def book_delete():
    key = request.args.get('id') 

     # Saving the B-tree to the storage server
    save_response = requests.delete(f'http://book-storage:80/delete?id={key}')

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200


@app.route('/rating/search', methods=['GET'])
def rating_search_page():
    try : 
        key = request.args.get('id') 
        response = requests.get(f'http://rating-storage:80/get_page?id={key}')
        page = response.json()
        for rating in page['data'] :
            if (rating['id'] == key) :
                return rating
        return jsonify({'error': f'Not found register with id : {key}'}), 404
    except:
        return jsonify({'error': f'Internal server error'}), 500

# @app.route('/rating/search', methods=['GET'])
# def rating_search():
#     key = request.args.get('id') 

#     b_tree = load_b_tree('http://rating-storage:80/')
#     if b_tree is None:
#         return {'error': f'Btree is not loaded.'}

#     result = b_tree.search(int(key))  # Assuming the search function returns a tuple (node, position)
#     try : 
#         result_node, index = result

#         if result_node is not None:
#             found_value = result_node.values[index]
#             print(f"Found {key} in the B-tree with value : {found_value}")
#             return found_value

#     except:
#         return jsonify({'error': f'Not found register with id : {key}'}), 404

@app.route('/rating/insert', methods=['POST'])
def rating_insert_data():    
    data = request.get_json()  # Retrieving JSON data from the request body

     # Saving the B-tree to the storage server
    save_response = requests.post('http://rating-storage:80/insert', json=data)

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data inserted into B-tree successfully.'}), 200

@app.route('/rating/delete', methods=['DELETE'])
def rating_delete():
    key = request.args.get('id') 

     # Saving the B-tree to the storage server
    save_response = requests.delete(f'http://rating-storage:80/delete?id={key}')

    if save_response.status_code != 200:
        return jsonify({'error': f'Error saving B-tree to storage server: {save_response.text}'}), save_response.status_code

    return jsonify({'message': 'Data removed into B-tree successfully.'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)