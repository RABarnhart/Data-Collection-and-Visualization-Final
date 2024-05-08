'''
correlation between day of the week and charge
clustering descriptions based on words, count vectorizer, isomap, color based on offense
'''
import json
import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load JSONL file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Extract relevant information and preprocess data
df = pd.DataFrame(data)
df['arrest date'] = pd.to_datetime(df['arrest date'], format='%m-%d-%Y')
df['day_of_week'] = df['arrest date'].dt.day_name()
df['charges'] = df['charges'].apply(lambda x: ','.join(x))

# Encode categorical variables
label_encoder = LabelEncoder()
df['day_of_week_encoded'] = label_encoder.fit_transform(df['day_of_week'])
df['charges_encoded'] = label_encoder.fit_transform(df['charges'])

# Swap X and y
X = df[['charges_encoded']]
y = df['day_of_week_encoded']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)