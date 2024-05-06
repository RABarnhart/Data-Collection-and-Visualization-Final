import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load data from JSON lines file
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        record = json.loads(line)
        data.append(record)

# Create DataFrame
df = pd.DataFrame(data)

# Filter data for "DRIVING WHILE IMPAIRED" charge
df = df[df['charges'].apply(lambda x: 'DRIVING WHILE IMPAIRED' in x)]

# Convert arrest date to datetime format
df['arrest date'] = pd.to_datetime(df['arrest date'], format='%m-%d-%Y')


'''
correlation between day of the week and charge
word cloud of words that show up
clustering descriptions based on words, count vectorizer, isomap, color based on offense
'''