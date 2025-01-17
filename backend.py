from flask import Flask, request, jsonify
from flask_cors import CORS
import random

from model import FIR_model
import torch

random.seed(10)

app = Flask(__name__)

# Allow CORS only for localhost:3000
CORS(app, resources={r"/process": {"origins": "http://localhost:3000"}})
mTurk = FIR_model()
@app.route('/process', methods=['POST'])
def process_array():
    data = request.json
    data = data["array"]
    data = [data]
    data = torch.tensor(data)
    #print(data.shape)

    action = mTurk(data)
    print(action)
    action = action[0].argmax(0)
    action = action.item()
    print("mTurks action: ", action)

    #action = random.randint(1, 6)
    return jsonify({'result': action})

if __name__ == '__main__':
    app.run(debug=True)
