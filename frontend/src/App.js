import React, { useState, useEffect } from "react";
import axios from "axios";
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);
const App = () => {
  const [latency, setLatency] = useState(null);
  const [bandwidth, setBandwidth] = useState(null);
  const [target, setTarget] = useState("");
  const [predictedLatency, setPredictedLatency] = useState(null);
    const [predictedBandwidth, setPredictedBandwidth] = useState(null);
    const [networkData, setNetworkData] = useState([]);

    const fetchNetworkData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/network_data?target=`);
        setNetworkData(response.data);
      } catch (error) {
        console.error("Error fetching network data:", error);
      }
    };
  
   
  const fetchPrediction = async () => {
      const response = await axios.get(`http://127.0.0.1:5000/predict_latency_bandwidth?target=${target}`);
      //const data = await response.json();
      setPredictedLatency(response.data.predicted_latency);
      setPredictedBandwidth(response.data.predicted_bandwidth);
  };

      

  const fetchLatency = async () => {
    const res = await axios.get(`http://127.0.0.1:5000/latency?target=${target}`);
    setLatency(res.data.latency);
  };

  const fetchBandwidth = async () => {
    const res = await axios.get(`http://127.0.0.1:5000/bandwidth?target=${target}`);
    setBandwidth(res.data.bandwidth);
  };
  const graphdata = {
    labels: networkData.map(item => item.timestamp), // X-axis: timestamps
    datasets: [
      {
        label: 'Latency (ms)',
        data: networkData.map(item => item.latency),
        borderColor: 'blue',
        fill: false,
        tension: 0.1,
      },
      {
        label: 'Bandwidth (Mbps)',
        data: networkData.map(item => item.bandwidth),
        borderColor: 'green',
        fill: false,
        tension: 0.1,
      }
    ]
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Network Analyzer</h1>
      <input
        type="text"
        placeholder="Enter target"
        value={target}
        onChange={(e) => setTarget(e.target.value)}
      />
      <button onClick={fetchLatency}>Check Latency</button>
      <button onClick={fetchBandwidth}>Check Bandwidth</button>
      <div>
        <h3>Latency: {latency ? `${latency} ms` : "N/A"}</h3>
        <h3>Bandwidth: {bandwidth ? `${bandwidth} Mbps` : "N/A"}</h3>
      </div>
      <button onClick={fetchPrediction}>Get Predictions</button>
      <div>
            <h3>Predicted Latency:</h3>
            <p>{predictedLatency ? `${predictedLatency} ms` : 'Loading prediction...'}</p>

            <h3>Predicted Bandwidth:</h3>
            <p>{predictedBandwidth ? `${predictedBandwidth} Mbps` : 'Loading prediction...'}</p>
        </div>
        
      <button onClick={fetchNetworkData}>Fetch Data</button>
      <div style={{ width: "80%", margin: "0 auto", marginTop: "20px" }}>
        {/* Graph Component */}
        <h3>Network Performance Over Time</h3>
        <Line data={graphdata} options={{ responsive: true, scales: { x: { type: 'category' }, y: { beginAtZero: true } } }} />
      </div>
    </div>
  );
};

export default App;
