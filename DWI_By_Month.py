import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data from JSON lines file
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Filter data for "DRIVING WHILE IMPAIRED" charge
dui_df = df[df['charges'].apply(lambda x: 'DRIVING WHILE IMPAIRED' in x)]

# Convert arrest date to datetime format
dui_df['arrest date'] = pd.to_datetime(dui_df['arrest date'], format='%m-%d-%Y')

# Extract week number from arrest date
dui_df['week'] = dui_df['arrest date'].dt.isocalendar().week

# Count occurrences of DUI charges per week
weekly_counts = dui_df.groupby('week').size()

# Plot the number of occurrences per week
plt.figure(figsize=(10, 6))
plt.plot(weekly_counts.index, weekly_counts.values, marker='o', linestyle='-')
plt.title('Number of DUI Charges per Week')
plt.xlabel('Week')
plt.ylabel('Number of Occurrences')
plt.grid(True)
plt.show()

