import os
import sys
import joblib
import pandas as pd

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, save_scan, get_scan_history


# =========================================================
# PATHS
# =========================================================

ML_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../ml"
    )
)

sys.path.append(ML_PATH)


# =========================================================
# IMPORT URL FEATURE EXTRACTOR
# =========================================================

from url_features import extract_url_features


# =========================================================
# PHISHGUARD FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="PhishGuard API",
    description="AI-powered phishing detection backend",
    version="1.0.0",
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_db()


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# LOAD URL MODEL
# =========================================================

URL_MODEL_PATH = os.path.join(
    ML_PATH,
    "models",
    "url_phishing_model.pkl"
)

url_model_data = joblib.load(
    URL_MODEL_PATH
)

url_model = url_model_data["model"]

model_features = url_model_data["features"]


# =========================================================
# LOAD EMAIL MODEL
# =========================================================

EMAIL_MODEL_PATH = os.path.join(
    ML_PATH,
    "models",
    "email_phishing_model.pkl"
)

email_model_data = joblib.load(
    EMAIL_MODEL_PATH
)

email_model = email_model_data["model"]

email_vectorizer = email_model_data["vectorizer"]


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/")
def root():

    return {
        "message": "PhishGuard API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# =========================================================
# REQUEST MODELS
# =========================================================

class URLScanRequest(BaseModel):

    url: str


class EmailScanRequest(BaseModel):

    email: str


# =========================================================
# URL FEATURE API
# =========================================================

@app.post("/api/url/features")
def get_url_features(
    request: URLScanRequest
):

    features = extract_url_features(
        request.url
    )

    return {

        "url": request.url,

        "features": features,
    }


# =========================================================
# URL SCANNER
# =========================================================

@app.post("/api/url/scan")
def scan_url(
    request: URLScanRequest
):

    try:

        url = request.url.strip()


        # -------------------------------------------------
        # EMPTY URL CHECK
        # -------------------------------------------------

        if not url:

            return {

                "success": False,

                "message": "URL cannot be empty"
            }


        # -------------------------------------------------
        # EXTRACT URL FEATURES
        # -------------------------------------------------

        features = extract_url_features(
            url
        )


        # -------------------------------------------------
        # PREPARE ML INPUT
        # -------------------------------------------------

        feature_df = pd.DataFrame(
            [features],
            columns=model_features
        )


        # -------------------------------------------------
        # ML PREDICTION
        #
        # 0 = Legitimate
        # 1 = Phishing
        # -------------------------------------------------

        prediction = int(
            url_model.predict(
                feature_df
            )[0]
        )


        # -------------------------------------------------
        # ML PHISHING PROBABILITY
        # -------------------------------------------------

        phishing_probability = float(
            url_model.predict_proba(
                feature_df
            )[0][1]
        )

        ml_score = phishing_probability * 100


        # -------------------------------------------------
        # SECURITY INDICATORS
        # -------------------------------------------------

        indicators = []

        security_score = 0


        # HTTPS
        if features["uses_https"] == 0:

            indicators.append(
                "URL does not use HTTPS"
            )

            security_score += 20


        # IP ADDRESS
        if features["is_domain_ip"] == 1:

            indicators.append(
                "URL uses an IP address instead of a domain"
            )

            security_score += 30


        # LONG URL
        if features["url_length"] > 75:

            indicators.append(
                "Unusually long URL"
            )

            security_score += 15


        # SUBDOMAINS
        if features["subdomain_count"] >= 3:

            indicators.append(
                "Multiple subdomains detected"
            )

            security_score += 15


        # DIGITS
        if features["digit_count"] > 5:

            indicators.append(
                "High number of digits in URL"
            )

            security_score += 10


        # ENTROPY
        if features["url_entropy"] > 4.5:

            indicators.append(
                "High URL character entropy"
            )

            security_score += 10


        # -------------------------------------------------
        # SUSPICIOUS KEYWORDS
        # -------------------------------------------------

        suspicious_words = [

            "login",
            "signin",
            "sign-in",
            "verify",
            "verification",
            "account",
            "password",
            "secure",
            "confirm",
            "update",
        ]


        url_lower = url.lower()


        found_words = [

            word

            for word in suspicious_words

            if word in url_lower

        ]


        if found_words:

            indicators.append(
                "Contains suspicious security-related keywords"
            )

            security_score += min(
                len(found_words) * 10,
                20
            )


        # -------------------------------------------------
        # LIMIT SECURITY SCORE
        # -------------------------------------------------

        security_score = min(
            security_score,
            100
        )


        # -------------------------------------------------
        # HYBRID URL RISK SCORE
        # -------------------------------------------------

        risk_score = int(
            round(
                (ml_score * 0.4)
                +
                (security_score * 0.6)
            )
        )


        risk_score = max(
            0,
            min(
                risk_score,
                100
            )
        )


        # -------------------------------------------------
        # URL STATUS
        # -------------------------------------------------

        if (

            security_score == 0

            and features["uses_https"] == 1

        ):

            status = "Safe"


        elif risk_score < 70:

            status = "Suspicious"


        else:

            status = "Malicious"


        # -------------------------------------------------
        # URL MESSAGE
        # -------------------------------------------------

        if status == "Safe":

            message = (
                "The URL appears to have a low security risk."
            )

        elif status == "Suspicious":

            message = (
                "The URL contains characteristics "
                "that may indicate suspicious activity."
            )

        else:

            message = (
                "The URL contains multiple characteristics "
                "associated with phishing or malicious links."
            )


        # -------------------------------------------------
        # SAVE URL SCAN TO DATABASE
        # -------------------------------------------------

        save_scan(

            scan_type="URL",

            input_data=url,

            risk_score=risk_score,

            status=status,

            phishing_probability=round(
                phishing_probability * 100,
                2
            )
        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "success": True,

            "url": url,

            "risk_score": risk_score,

            "status": status,

            "prediction": prediction,

            "phishing_probability": round(
                phishing_probability * 100,
                2
            ),

            "security_score": security_score,

            "indicators": indicators,

            "message": message,
        }


    except Exception as error:

        return {

            "success": False,

            "error_type": type(error).__name__,

            "error": str(error),
        }


# =========================================================
# EMAIL SCANNER
# =========================================================

@app.post("/api/email/scan")
def scan_email(
    request: EmailScanRequest
):

    try:

        email_text = request.email.strip()


        # -------------------------------------------------
        # EMPTY EMAIL CHECK
        # -------------------------------------------------

        if not email_text:

            return {

                "success": False,

                "message": "Email cannot be empty"
            }


        # -------------------------------------------------
        # TF-IDF FEATURES
        # -------------------------------------------------

        email_features = email_vectorizer.transform(
            [email_text]
        )


        # -------------------------------------------------
        # ML PREDICTION
        #
        # 0 = Legitimate
        # 1 = Phishing
        # -------------------------------------------------

        prediction = int(
            email_model.predict(
                email_features
            )[0]
        )


        # -------------------------------------------------
        # PHISHING PROBABILITY
        # -------------------------------------------------

        phishing_probability = float(
            email_model.predict_proba(
                email_features
            )[0][1]
        )


        # -------------------------------------------------
        # EMAIL SECURITY INDICATORS
        # -------------------------------------------------

        indicators = []

        email_lower = email_text.lower()


        suspicious_words = [

            "urgent",
            "verify",
            "verification",
            "password",
            "account",
            "login",
            "click here",
            "confirm",
            "suspended",
            "winner",
            "prize",
            "refund",
            "security alert",
            "credit card",
        ]


        found_words = [

            word

            for word in suspicious_words

            if word in email_lower

        ]


        if found_words:

            indicators.append(
                "Contains suspicious or urgent language"
            )


        if "click here" in email_lower:

            indicators.append(
                "Contains a request to click a link"
            )


        if "password" in email_lower:

            indicators.append(
                "Requests or mentions password information"
            )


        if "credit card" in email_lower:

            indicators.append(
                "Mentions credit card information"
            )


        if "urgent" in email_lower:

            indicators.append(
                "Uses urgent language"
            )


        # -------------------------------------------------
        # EMAIL RISK SCORE
        # -------------------------------------------------

        indicator_score = min(
            len(indicators) * 20,
            60
        )


        risk_score = int(
            round(
                (phishing_probability * 100 * 0.4)
                +
                (indicator_score * 0.6)
            )
        )


        risk_score = max(
            0,
            min(
                risk_score,
                100
            )
        )


        # -------------------------------------------------
        # EMAIL STATUS
        # -------------------------------------------------

        if (

            len(indicators) == 0

            and prediction == 0

        ):

            status = "Safe"


        elif len(indicators) >= 3:

            status = "Phishing"


        elif risk_score < 70:

            status = "Suspicious"


        else:

            status = "Phishing"


        # -------------------------------------------------
        # EMAIL MESSAGE
        # -------------------------------------------------

        if status == "Safe":

            message = (
                "The email appears to have a low phishing risk."
            )

        elif status == "Suspicious":

            message = (
                "The email contains some characteristics "
                "commonly associated with phishing."
            )

        else:

            message = (
                "The email contains characteristics "
                "commonly associated with phishing attempts."
            )


        # -------------------------------------------------
        # SAVE EMAIL SCAN TO DATABASE
        # -------------------------------------------------

        save_scan(

            scan_type="EMAIL",

            input_data=email_text,

            risk_score=risk_score,

            status=status,

            phishing_probability=round(
                phishing_probability * 100,
                2
            )
        )


        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "success": True,

            "risk_score": risk_score,

            "status": status,

            "prediction": prediction,

            "phishing_probability": round(
                phishing_probability * 100,
                2
            ),

            "indicators": indicators,

            "message": message,
        }


    except Exception as error:

        return {

            "success": False,

            "error_type": type(error).__name__,

            "error": str(error),
        }


# =========================================================
# SCAN HISTORY API
# =========================================================

@app.get("/api/history")
def history():

    return {

        "success": True,

        "history": get_scan_history()
    }
# =========================================================
# DASHBOARD STATISTICS API
# =========================================================

@app.get("/api/dashboard/stats")
def dashboard_stats():

    history = get_scan_history()

    total_scans = len(history)

    safe_scans = sum(
        1
        for scan in history
        if scan["status"] == "Safe"
    )

    suspicious_scans = sum(
        1
        for scan in history
        if scan["status"] == "Suspicious"
    )

    phishing_scans = sum(
        1
        for scan in history
        if scan["status"] in ["Phishing", "Malicious"]
    )

    if total_scans > 0:
        average_risk = round(
            sum(
                scan["risk_score"]
                for scan in history
            ) / total_scans,
            2
        )
    else:
        average_risk = 0

    return {
        "success": True,
        "total_scans": total_scans,
        "safe_scans": safe_scans,
        "suspicious_scans": suspicious_scans,
        "phishing_scans": phishing_scans,
        "average_risk": average_risk,
    }