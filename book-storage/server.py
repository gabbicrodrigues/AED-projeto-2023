# server.py
from flask import Flask, send_file, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/')
def serve_binary_file():
    file_path = os.path.join(os.getcwd(), 'btree.json')
    return send_file(file_path, as_attachment=True)

@app.route('/save', methods=['POST'])
def upload_file():
    try:
        data = request.get_json()  # Retrieving JSON data from the request body

        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400

        with open('btree.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)

        return {'success': True}
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)