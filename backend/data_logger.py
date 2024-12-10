# backend/data_logger.py

import time
import json
from datetime import datetime
from utils import measure_latency  # Assume this function measures latency
from utils import measure_bandwidth  # Assume this function measures bandwidth

def log_network_data(filename="network_data.json",target='8.8.8.8'):
    # Measure network performance
    latency = measure_latency(target)
    bandwidth = measure_bandwidth(target)

    # Get current timestamp
    timestamp = datetime.now().isoformat()

    # Create a log entry
    log_entry = {
        "timestamp": timestamp,
        "latency": latency,
        "bandwidth": bandwidth
    }

    # Append log entry to a JSON file
    try:
        with open(filename, 'a') as file:
            file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Error logging data: {e}")

if __name__ == "__main__":
    start_time = time.time()  # Start the timer
    duration = 10  # Stop after 10 seconds

    while True:
        log_network_data()  # Log data

        # Check if 10 seconds have passed
        if time.time() - start_time >= duration:
            print("Stopping data logging after 10 seconds")
            break  # Exit the loop after 10 seconds
        
        time.sleep(1)
