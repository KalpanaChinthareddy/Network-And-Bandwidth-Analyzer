from flask import Flask, request, jsonify
from utils import measure_latency, measure_bandwidth #train_predictive_model
from flask_cors import CORS
from data_preprocessing import preprocess_data
import joblib, time , json 
from data_logger import log_network_data

app = Flask(__name__)
CORS(app)

model = joblib.load('latency_bandwidth_predictor_model.pkl')
@app.route('/latency', methods=['GET'])
def latency():
    target = request.args.get('target')
    latency = measure_latency(target)
    return jsonify({"latency": latency})

@app.route('/bandwidth', methods=['GET'])
def bandwidth():
    target = request.args.get('target')
    bandwidth = measure_bandwidth(target)
    return jsonify({"bandwidth": bandwidth})


@app.route('/predict_latency_bandwidth', methods=['GET'])
def predict_latency_bandwidth():
    target = request.args.get('target')
    log_network_data("network_data.json",target=target)
    # Get the most recent data for prediction 
    time.sleep(10)
    df = preprocess_data()  # Preprocess and get recent data
    recent_data = df[['latency_rollavg', 'bandwidth_rollavg']].iloc[-1].values.reshape(1, -1)
    
    # Make prediction
    predicted_values = model.predict(recent_data)
    predicted_latency = predicted_values[0][0]
    predicted_bandwidth = predicted_values[0][1]
    
    # Return the predictions as JSON
    return jsonify({
        'predicted_latency': predicted_latency,
        'predicted_bandwidth': predicted_bandwidth
    })

@app.route('/network_data', methods=['GET'])
def get_network_data():
    target = request.args.get('target')
    filename = "network_data.json"
    
    # Read the log file and filter data for the specific target
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Filter the data for the specified target
        network_data = []
        for line in lines:
            data = json.loads(line)
            if target in data['timestamp']:  # You could filter based on specific criteria
                network_data.append(data)
        
        return jsonify(network_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
