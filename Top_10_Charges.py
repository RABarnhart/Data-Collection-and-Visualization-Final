"Histogram of top ten charges commited"

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set dark mode theme
plt.style.use('dark_background')

# Read the JSON lines file into a DataFrame
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        data.append(eval(line))

df = pd.DataFrame(data)

# Extract all charges
all_charges = []
for charges in df['charges']:
    all_charges.extend(charges)

# Count the frequency of each charge
charge_counts = pd.Series(all_charges).value_counts()

# Select the top 20 charges
top_10_charges = charge_counts.head(10)

# Plot histogram
plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_charges.values, y=top_10_charges.index, palette='YlOrRd')
# top_10_charges.plot(kind='bar', color='coral', edgecolor='black')

plt.xlabel('Charges')
plt.ylabel('Frequency')
plt.title('Top 20 Charges')
plt.tight_layout()
plt.show()
