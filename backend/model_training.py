import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load and preprocess the data
df = pd.read_csv('processed_network_data.csv')
X = df[['latency_rollavg', 'bandwidth_rollavg']]  # Features (can add more)
y = df[['latency', 'bandwidth']]  # Target variables (latency and bandwidth)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse_latency = mean_squared_error(y_test['latency'], y_pred[:, 0])
mse_bandwidth = mean_squared_error(y_test['bandwidth'], y_pred[:, 1])

print(f"Mean Squared Error for Latency: {mse_latency}")
print(f"Mean Squared Error for Bandwidth: {mse_bandwidth}") 

# Save the trained model to a file
joblib.dump(model, 'latency_bandwidth_predictor_model.pkl')
