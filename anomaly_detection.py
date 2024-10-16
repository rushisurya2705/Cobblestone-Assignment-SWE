import math
import random
import time

# Function to simulate a continuous data stream
def data_stream():
    t = 0
    while True:
        # Introduces a seasonal pattern using a sine wave function
        seasonal = math.sin(2 * math.pi * (t % 100) / 100)
        
        # Adds random noise with a mean of 0 and a standard deviation of 0.1
        noise = random.gauss(0, 0.1)
        
        # Initially, no anomaly
        anomaly = 0
        
        # With a 5% probability, inject an anomaly between 1 and 3
        if random.random() < 0.05:
            anomaly = random.uniform(1, 3)
        
        # The final data point combines seasonal, noise, and anomaly
        data_point = seasonal + noise + anomaly
        
        # Yield the data point, simulating a continuous stream
        yield data_point
        
        # Increment time step
        t += 1

# Class for detecting anomalies using Exponential Weighted Moving Average (EWMA)
class AnomalyDetector:
    def __init__(self, alpha=0.3):
        """
        Initializes the AnomalyDetector.
        Args:
        - alpha (float): Smoothing factor for EWMA, controls the weight given to the most recent data.
        """
        self.alpha = alpha  # Smoothing factor
        self.ewma = None    # Initial EWMA is set to None
        self.std_dev = 0    # Initial standard deviation
        self.n = 0          # Counter for the number of data points processed

    def update(self, data_point):
        """
        Updates the EWMA and checks if the data point is an anomaly.
        Args:
        - data_point (float): The current value from the data stream.
        
        Returns:
        - bool: True if the data point is an anomaly, False otherwise.
        """
        if self.ewma is None:
            # Initialize EWMA with the first data point
            self.ewma = data_point
            self.std_dev = 0
        else:
            self.n += 1
            prev_ewma = self.ewma
            
            # Update the EWMA using the exponential smoothing formula
            self.ewma = self.alpha * data_point + (1 - self.alpha) * self.ewma
            
            # Update the standard deviation using an incremental formula
            self.std_dev = math.sqrt(((self.n - 1) * self.std_dev**2 + (data_point - prev_ewma)**2) / self.n)
        
        # Threshold is set at 3 times the standard deviation
        threshold = 3 * self.std_dev
        
        # If the difference between data point and EWMA exceeds the threshold, it's an anomaly
        is_anomaly = abs(data_point - self.ewma) > threshold
        return is_anomaly

# Function to visualize the data stream in a text-based manner
def visualize_stream(detector):
    """
    Visualizes the data stream and detected anomalies.
    Args:
    - detector (AnomalyDetector): The anomaly detector instance that checks for anomalies.
    """
    data_stream_gen = data_stream()  # Start data stream generation
    
    print("Data Stream (Anomalies marked with '*'):")
    for i, data_point in enumerate(data_stream_gen):
        # Update the anomaly detector with each new data point
        is_anomaly = detector.update(data_point)
        
        # Print data point, flagging anomalies with an asterisk (*)
        if is_anomaly:
            print(f"{i:3}: {data_point:.5f}  * Anomaly")
        else:
            print(f"{i:3}: {data_point:.5f}")
        
        # Simulate real-time streaming with a slight delay
        time.sleep(0.05)
        
        # Stop after 500 data points to limit the demonstration
        if i > 500:
            break

# Create an instance of AnomalyDetector with alpha=0.3
detector = AnomalyDetector(alpha=0.3)

# Visualize the data stream and detect anomalies in real-time
visualize_stream(detector)
