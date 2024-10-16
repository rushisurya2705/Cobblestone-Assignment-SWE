import math
import random
import time
from collections import deque
import matplotlib.pyplot as plt

# Function to simulate a continuous data stream
def data_stream():
    t = 0
    while True:
        # Seasonal pattern using a sine wave function
        seasonal = math.sin(2 * math.pi * (t % 100) / 100)
        
        # Adds random noise with a mean of 0 and a standard deviation of 0.1
        noise = random.gauss(0, 0.1)
        
        # Injects anomaly with a 20% probability (for testing purposes)
        anomaly = 0
        if random.random() < 0.2:  # Increased from 5% to 20%
            anomaly = random.uniform(1, 3)
        
        # Combine seasonal, noise, and anomaly into the final data point
        data_point = seasonal + noise + anomaly
        
        # Yield the data point, simulating a continuous stream
        yield data_point
        t += 1

# Class for detecting anomalies using EWMA and sliding window
class AnomalyDetector:
    def __init__(self, alpha=0.3, window_size=50):
        """
        Initializes the AnomalyDetector.
        Args:
        - alpha (float): Smoothing factor for EWMA, controls the weight given to recent data.
        - window_size (int): Size of the sliding window for real-time anomaly detection.
        """
        self.alpha = alpha
        self.ewma = None
        self.std_dev = 0
        self.window_size = window_size
        self.window = deque(maxlen=window_size)  # Buffer to store sliding window of data points

    def update(self, data_point):
        """
        Updates the sliding window, EWMA, and checks if the data point is an anomaly.
        Args:
        - data_point (float): The current value from the data stream.
        
        Returns:
        - bool: True if the data point is an anomaly, False otherwise.
        """
        # Add the new data point to the sliding window
        self.window.append(data_point)

        # Initialize EWMA with the first data point in the window
        if len(self.window) == 1:
            self.ewma = data_point
            self.std_dev = 0
            return False  # Cannot detect anomalies on the first point
        
        # Update EWMA using the sliding window
        prev_ewma = self.ewma
        self.ewma = self.alpha * data_point + (1 - self.alpha) * self.ewma

        # Calculate standard deviation for the window
        mean_diff = sum([(x - prev_ewma)**2 for x in self.window]) / len(self.window)
        self.std_dev = math.sqrt(mean_diff)
        
        # Threshold is set at 2 times the standard deviation (increased sensitivity)
        threshold = 2 * self.std_dev
        
        # If the difference between the data point and EWMA exceeds the threshold, it's an anomaly
        is_anomaly = abs(data_point - self.ewma) > threshold
        
        return is_anomaly

# Function to visualize the sliding window and detected anomalies using matplotlib
def visualize_stream(detector):
    """
    Visualizes the data stream and detected anomalies with a sliding window using matplotlib.
    Args:
    - detector (AnomalyDetector): The anomaly detector instance that checks for anomalies.
    """
    data_stream_gen = data_stream()  # Start data stream generation
    window_size = detector.window_size

    # Initialize the plot
    plt.ion()  # Interactive mode on
    fig, ax = plt.subplots()
    data_x = []
    data_y = []
    anomaly_x = []  # Store x-values of anomalies
    anomaly_y = []  # Store y-values of anomalies
    
    for i, data_point in enumerate(data_stream_gen):
        # Update the anomaly detector with each new data point
        is_anomaly = detector.update(data_point)
        
        # Get the current window of data
        current_window = list(detector.window)
        data_x.append(i)
        data_y.append(data_point)
        
        # Clear the plot
        ax.clear()

        # Plot the data points
        ax.plot(data_x, data_y, label="Data Stream", color='gray', alpha=0.6)
        
        # Highlight the sliding window data points in blue
        if len(data_x) > window_size:
            ax.plot(data_x[-window_size:], data_y[-window_size:], label="Sliding Window", color='blue')
        
        # Highlight the current data point if it's an anomaly
        if is_anomaly:
            anomaly_x.append(i)
            anomaly_y.append(data_point)
            print(f"Anomaly detected at time step {i}: {data_point}")
        
        # Plot all detected anomalies
        if anomaly_x:
            ax.plot(anomaly_x, anomaly_y, 'ro', label="Anomalies")
        
        # Set plot labels and title
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Data Value')
        ax.set_title('Real-Time Data Stream with Sliding Window and Anomaly Detection')

        # Add legend
        ax.legend()
        
        # Pause for a short interval to simulate real-time data streaming
        plt.pause(0.1)
        
        # Stop after 500 data points to limit the demo
        if i > 500:
            break

    plt.ioff()  # Interactive mode off
    plt.show()

# Create an instance of AnomalyDetector with alpha=0.3 and sliding window size of 50
detector = AnomalyDetector(alpha=0.3, window_size=50)

# Visualize the data stream and anomalies in real-time with sliding window
visualize_stream(detector)
