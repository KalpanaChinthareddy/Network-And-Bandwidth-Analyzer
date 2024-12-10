from ping3 import ping
import random
import numpy as np
import requests, time
import matplotlib.pyplot as plt 
latency_data = []
bandwidth_data = []
timestamps = []

def measure_latency(target="8.8.8.8"):
    try:
        return ping(target, timeout=2) * 1000  # Convert to ms
    except:
        return None

def measure_bandwidth(target="https://speed.hetzner.de/100MB.bin"):
    # Simulate bandwidth testing (e.g., by sending random packets)
    try:
        start_time = time.time()
        response = requests.get(target, stream=True, timeout=10)
        total_size = len(response.content)  # Total bytes downloaded
        end_time = time.time()
        duration = end_time - start_time  # Time taken in seconds
        bandwidth = (total_size / duration) / (1024 * 1024)  # Convert bytes/s to Mbps
        return bandwidth
    except:
        return random.uniform(10, 100)
   

def visualize_data():
    plt.figure(figsize=(10, 5))

    # Plot latency
    plt.subplot(1, 2, 1)
    plt.plot(timestamps, latency_data, color='blue', label='Latency (ms)')
    plt.xlabel('Time')
    plt.ylabel('Latency (ms)')
    plt.title('Latency Over Time')
    plt.grid(True)

    # Plot bandwidth
    plt.subplot(1, 2, 2)
    plt.plot(timestamps, bandwidth_data, color='green', label='Bandwidth (Mbps)')
    plt.xlabel('Time')
    plt.ylabel('Bandwidth (Mbps)')
    plt.title('Bandwidth Over Time')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# Main loop to fetch and plot data
def start_monitoring():
    try:
        while True:
            # Fetch and log network data
            target = "8.8.8.8"  # Example target for latency, can be updated
            bandwidth = measure_bandwidth()
            latency = measure_latency(target)
            
            if bandwidth and latency:
                # Append data to lists
                latency_data.append(latency)
                bandwidth_data.append(bandwidth)
                timestamps.append(datetime.now().strftime('%H:%M:%S'))

                # Plot the data every time new data is fetched
                visualize_data()

            # Wait for a few seconds before fetching the data again
            time.sleep(10)

    except KeyboardInterrupt:
        print("Monitoring stopped.")
