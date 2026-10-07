import joblib
import pandas as pd

from url_features import extract_url_features


MODEL_PATH = "models/url_phishing_model.pkl"


TEST_URLS = [
    # Clearly legitimate / well-known domains
    ("https://google.com", 0),
    ("https://github.com", 0),
    ("https://microsoft.com", 0),
    ("https://apple.com", 0),
    ("https://amazon.com", 0),
    ("https://wikipedia.org", 0),
    ("https://youtube.com", 0),
    ("https://linkedin.com", 0),
    ("https://www.python.org", 0),
    ("https://www.mozilla.org", 0),

    # Suspicious URL patterns
    ("http://192.168.1.10/login", 1),
    ("http://example.com/login/verify-account", 1),
    ("http://secure-login-account.example.com/verify", 1),
    ("http://account-verification.example.com/login", 1),
    ("http://paypal-login.example.com/verify", 1),
    ("http://192.168.1.50/secure/login", 1),
]


print("Loading model...")

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
features = model_data["features"]


print("\nTesting URLs...\n")


urls = [item[0] for item in TEST_URLS]
expected = [item[1] for item in TEST_URLS]


X = pd.DataFrame(
    [
        extract_url_features(url)
        for url in urls
    ],
    columns=features
)


probabilities = model.predict_proba(X)[:, 1]
predictions = model.predict(X)


results = pd.DataFrame({
    "URL": urls,
    "Expected": expected,
    "Prediction": predictions,
    "PhishingProbability": (
        probabilities * 100
    ).round(2)
})


print(
    results.to_string(
        index=False
    )
)


print("\nSanity Test Summary")

correct = (
    results["Expected"]
    == results["Prediction"]
).sum()

total = len(results)

accuracy = (
    correct / total
) * 100


print(
    f"Correct: {correct}/{total}"
)

print(
    f"Sanity accuracy: {accuracy:.2f}%"
)