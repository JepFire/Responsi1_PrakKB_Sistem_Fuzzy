from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from fuzzy_logic import FuzzyCS2
import os

app = Flask(__name__, static_folder='.')
CORS(app)
fuzzy_sys = FuzzyCS2()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        adr = float(data.get('adr', 0))
        kd = float(data.get('kd', 0))
        result = fuzzy_sys.calculate(adr, kd)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Membaca port dari environment variable (untuk hosting) atau default ke 5005 (lokal)
    port = int(os.environ.get('PORT', 5005))
    print(f"CS2 Fuzzy System Server running at http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
