from flask import Flask, request, jsonify
from flask_cors import CORS
import random

random.seed(1)

app = Flask(__name__)

# Allow CORS only for localhost:3000
CORS(app, resources={r"/process": {"origins": "http://localhost:3000"}})

@app.route('/process', methods=['POST'])
def process_array():
    data = request.json
    action = random.randint(1, 6)
    return jsonify({'result': action})

if __name__ == '__main__':
    app.run(debug=True)
