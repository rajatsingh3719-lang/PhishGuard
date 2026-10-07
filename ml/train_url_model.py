import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from url_features import extract_url_features, FEATURE_NAMES


DATASET_PATH = "dataset/PhiUSIIL_Phishing_URL_Dataset.csv"
MODEL_PATH = "models/url_phishing_model.pkl"


print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Dataset loaded: {len(df)} URLs")


print("\nExtracting URL features...")

features = []

for i, url in enumerate(df["URL"]):
    features.append(
        extract_url_features(url)
    )

    if (i + 1) % 25000 == 0:
        print(f"Processed {i + 1} URLs")


X = pd.DataFrame(
    features,
    columns=FEATURE_NAMES
)

# Dataset:
# 1 = legitimate
# 0 = phishing
#
# Our model:
# 0 = legitimate
# 1 = phishing

y = (df["label"] == 0).astype(int)


print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


print("\nModel trained successfully.")


print("\nEvaluating model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Legitimate",
            "Phishing"
        ]
    )
)


print("\nFeature Importance:")

importance = pd.DataFrame({
    "feature": FEATURE_NAMES,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    "importance",
    ascending=False
)

print(
    importance.to_string(index=False)
)


os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    {
        "model": model,
        "features": FEATURE_NAMES
    },
    MODEL_PATH
)

print(
    f"\nModel saved to: {MODEL_PATH}"
)