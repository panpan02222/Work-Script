from uie_predictor import UIEPredictor
from flask import Flask, request, jsonify
import json
import numpy as np

app = Flask(__name__)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        return super().default(obj)


@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    text = data.get('text')
    schema = data.get('schema')  # Define the schema for entity extraction
    ie = UIEPredictor(model='uie-base', schema=schema)
    result = ie(text)

    json_str = json.dumps(result, cls=NumpyEncoder, ensure_ascii=False)
    print(type(json_str))
    return jsonify(json_str)

# ----------------------------------------------------------------------------------------


@app.route('/pr', methods=['POST'])
def proc():
    data = request.get_json()
    text = data.get('text')
    schema = data.get('schema')  # Define the schema for entity extraction
    schema = eval(schema)
    ie = UIEPredictor(model='uie-base', schema=schema)
    ie.set_schema(schema)
    result = ie(text)
    json_str = json.dumps(result, cls=NumpyEncoder, ensure_ascii=False)
    return jsonify(json_str)


if __name__ == '__main__':
    app.run('0.0.0.0', port=6666, debug=True)
