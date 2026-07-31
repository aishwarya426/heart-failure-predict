import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("dataset.csv")  # make sure this file is in the same folder
X = df.drop("DEATH_EVENT", axis=1)
y = df["DEATH_EVENT"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=150, max_depth=7, random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved successfully as model.pkl")
