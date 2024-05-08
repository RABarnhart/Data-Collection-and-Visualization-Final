import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load JSONL file and parse data
data = []
with open('bookings.jsonl', 'r') as file:
    for line in file:
        data.append(json.loads(line))

# Extract relevant information and preprocess data
df = pd.DataFrame(data)
df['arrest date'] = pd.to_datetime(df['arrest date'], format='%m-%d-%Y')
df['day_of_week'] = df['arrest date'].dt.day_name()

# Encode categorical variables
label_encoder = LabelEncoder()
df['charges'] = df['charges'].apply(lambda x: ','.join(x))
df['charge_driving_impaired'] = df['charges'].str.contains('DRIVING WHILE IMPAIRED', case=False)
df['day_of_week_encoded'] = label_encoder.fit_transform(df['day_of_week'])
df['charge_driving_impaired'] = label_encoder.fit_transform(df['charge_driving_impaired'])

# Assign a single label for "Driving while impaired" charge
df.loc[df['charge_driving_impaired'] == 1, 'charges'] = 'DRIVING WHILE IMPAIRED'

# Split data into features (X) and target (y)
X = df[['charge_driving_impaired']]
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

# Create classification report
class_report = classification_report(y_test, y_pred)
print("Classification Report:\n", class_report)

# Filter dataframe for instances with "Driving while impaired" charge
df_filtered = df[df['charges'].str.contains('DRIVING WHILE IMPAIRED', case=False)]

# Count occurrences of arrests for "Driving while impaired" by day of the week
arrests_by_day = df_filtered['day_of_week'].value_counts().sort_index()

# Dark mode styling
plt.style.use('dark_background')

# Red color palette
colors = sns.color_palette('Reds', len(arrests_by_day))

# Define the order of days
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot the line plot
plt.figure(figsize=(10, 6))
arrests_by_day.loc[days_order].plot(kind='line', marker='o', color='red')
plt.title('Arrests for "Driving while impaired" by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Number of Occurrences')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()