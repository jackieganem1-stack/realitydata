import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
# Replace 'test.csv' with the path to your CSV file
df = pd.read_csv('test.csv', parse_dates=['timestamp'], index_col='timestamp')
num_data_points = df.shape[0]  # df.shape[0] gives the number of rows
print(f'Number of data points: {num_data_points}')
# Step 2: Check the first few rows to ensure the data is loaded correctly
print(df.head())

# Step 3: Plot the data
plt.figure(figsize=(10, 6))  # Set the size of the plot
plt.plot(df.index, df['sentiment_score'], label='sentiment_score')  # Replace 'Value' with the column you're interested in

# Step 4: Customize the plot
plt.title('Data Over Time')  # Title of the plot
plt.xlabel('Date')  # Label for the x-axis
plt.ylabel('Value')  # Label for the y-axis
plt.grid(True)  # Show grid
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Step 5: Show the plot
plt.legend()
plt.tight_layout()  # Adjust the layout to avoid clipping
plt.show()

