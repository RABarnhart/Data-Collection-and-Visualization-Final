import json
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Read the JSON lines file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Filter data for individuals charged with "DRIVING WHILE IMPAIRED"
impaired_driving_data = [record for record in data if "DRIVING WHILE IMPAIRED" in record["charges"]]

# Create a DataFrame from the filtered data
df = pd.DataFrame(impaired_driving_data)

# Convert 'age' column to numeric for correct sorting
df['age'] = pd.to_numeric(df['age'])

# Sort DataFrame by age in ascending order
df.sort_values(by='age', inplace=True)

# Plotting in dark mode
plt.style.use('dark_background')

# Plotting
plt.figure(figsize=(10, 6))

# Use Seaborn to create a grouped violin plot
sns.violinplot(x='sex', y='age', data=df, hue='sex', split=True, inner="quartile", palette='hls')

plt.xlabel('Gender')
plt.ylabel('Age')
plt.title('Distribution of Age for "DRIVING WHILE IMPAIRED" by Gender')

# Manually adjust y-axis ticks
plt.yticks(range(10, max(df['age'].astype(int))+1, 10))

plt.grid(True)
plt.show()
