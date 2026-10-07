import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# SIMPLE EMAIL DATASET
# 0 = Legitimate
# 1 = Phishing
# =========================================================

emails = [

    # -------------------------
    # LEGITIMATE EMAILS
    # -------------------------

    "Hi John, your meeting is scheduled for tomorrow at 10 AM. Regards, HR.",
    "Your Amazon order has been shipped and will arrive tomorrow.",
    "Thank you for attending our meeting today. Please find the notes attached.",
    "Your monthly bank statement is now available in your account.",
    "Your electricity bill for this month is ready to view.",
    "Reminder: your appointment is scheduled for Monday at 3 PM.",
    "Your password was successfully changed.",
    "Welcome to our newsletter. Here are this week's updates.",
    "Your payment of 500 rupees was successfully received.",
    "Your flight booking has been confirmed.",
    "The project meeting has been moved to Friday afternoon.",
    "Your college examination timetable has been published.",
    "Please find attached the report you requested.",
    "Your subscription has been renewed successfully.",
    "Your package is ready for pickup.",
    "Thank you for contacting customer support.",
    "Your application has been received successfully.",
    "The requested document has been uploaded to your account.",
    "Your interview is scheduled for tomorrow.",
    "Your monthly salary has been credited to your account.",

    # -------------------------
    # PHISHING EMAILS
    # -------------------------

    "URGENT! Your account will be suspended. Click here immediately to verify your password.",
    "Your bank account has been locked. Verify your account now to avoid permanent suspension.",
    "Congratulations! You have won a cash prize. Click the link to claim your reward.",
    "Your PayPal account has been limited. Confirm your login details immediately.",
    "Security alert! We detected suspicious activity. Verify your account now.",
    "Your password will expire today. Click here to update your password.",
    "URGENT ACTION REQUIRED: Confirm your banking information immediately.",
    "You have received a refund. Click here and provide your card details to receive it.",
    "Your account has been compromised. Login now to secure your account.",
    "Final warning! Your account will be deleted unless you verify your information.",
    "You have won a lottery prize. Send your bank information to claim the money.",
    "Your payment failed. Click the link and enter your credit card information.",
    "We detected unusual login activity. Confirm your username and password now.",
    "Your email account will be closed today. Verify your identity immediately.",
    "Click here to receive your exclusive reward before the offer expires.",
    "URGENT: Your bank account requires verification. Login immediately.",
    "You are eligible for a free gift. Enter your personal information to claim it.",
    "Your account security has been compromised. Click here to verify your identity.",
    "Important security notification. Confirm your account credentials immediately.",
    "Your online banking access is suspended. Verify your account to restore access.",
]


# =========================================================
# SPLIT DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    emails,
    [0] * 20 + [1] * 20,
    test_size=0.25,
    random_state=42,
    stratify=[0] * 20 + [1] * 20
)


# =========================================================
# TF-IDF
# =========================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=3000
)


X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)


# =========================================================
# LOGISTIC REGRESSION
# =========================================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(
    X_train_tfidf,
    y_train
)


# =========================================================
# EVALUATION
# =========================================================

predictions = model.predict(
    X_test_tfidf
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nEmail Phishing Model")
print("--------------------")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
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


# =========================================================
# SAVE MODEL
# =========================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    {
        "model": model,
        "vectorizer": vectorizer
    },
    "models/email_phishing_model.pkl"
)

print(
    "\nModel saved to:"
)

print(
    "models/email_phishing_model.pkl"
)