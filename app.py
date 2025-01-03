from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_system_metrics')
def get_system_metrics():
    # Read the metrics data from the JSON file
    file_path = "/home/vishnuvrd/project/metrics_data.json"
    with open(file_path, 'r') as f:
        metrics_data = json.load(f)
    
    # Get the last metrics data (if available)
    if metrics_data:
        latest_data = metrics_data[-1]
        return jsonify(latest_data)
    else:
        return jsonify({"error": "No data available"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
