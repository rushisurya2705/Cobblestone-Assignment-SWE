
# Problem Statement:
### Project Title:
Efficient Data Stream Anomaly Detection

### Project Description:
Your task is to develop a Python script capable of detecting anomalies in a continuous data stream. This stream, simulating real-time sequences of floating-point numbers, could represent various metrics such as financial transactions or system metrics. Your focus will be on identifying unusual patterns, such as exceptionally high values or deviations from the norm.

### Objectives:
1) Algorithm Selection: Identify and implement a suitable algorithm for anomaly detection, capable of adapting to concept drift and seasonal variations.
2) Data Stream Simulation: Design a function to emulate a data stream, incorporating regular patterns, seasonal elements, and random noise.
3) Anomaly Detection: Develop a real-time mechanism to accurately flag anomalies as the data is streamed.
4) Optimization: Ensure the algorithm is optimized for both speed and efficiency.
5) Visualization: Create a straightforward real-time visualization tool to display both the data stream and any detected anomalies.

### Requirements:
1) The project must be implemented using Python 3.x.
2) Your code should be thoroughly documented, with comments to explain key sections.
3) Include a concise explanation of your chosen algorithm and its effectiveness.
4) Ensure robust error handling and data validation.
5) Limit the use of external libraries. If necessary, include a requirements.txt file.


# Solution Explaination:

### Algorithm Explanation:
The Exponential Weighted Moving Average (EWMA) algorithm is used for anomaly detection in the streaming data. It updates a smoothed average (EWMA) based on a smoothing factor (alpha), giving more weight to recent data points. The algorithm compares the difference between the current data point and the EWMA to the standard deviation. If the difference exceeds a set threshold (3 times the standard deviation), the point is flagged as an anomaly.

#### Why EWMA is Effective:
1) Adapts to Concept Drift: EWMA adapts to changes in data patterns by adjusting the average based on recent trends.
2) Handles Noise: The standard deviation helps differentiate anomalies from random noise.
3) Efficient for Streaming: EWMA is computationally light and works well for continuous data streams.
#### Key Points:
1) Data Stream Simulation: Generates data with seasonal patterns, noise, and random anomalies.
2) Anomaly Detection: Detects anomalies in real-time using EWMA.
3) Text-Based Visualization: A simple real-time display of data points, highlighting anomalies.

### Error Handling and Validation:
The code uses basic error handling by ensuring that ewma is initialized correctly when the first data point is processed.
Data validation could be added to ensure that incoming data points are valid numbers (e.g., not None or non-numeric values).

### No External Libraries Used:
Since the project limits external libraries, the code avoids using matplotlib and instead provides a text-based output, which works for the project's purpose of detecting anomalies in a streaming environment.
