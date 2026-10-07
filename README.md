# PhishGuard 🛡️

PhishGuard is a full-stack cybersecurity web application that analyzes suspicious URLs and emails to identify potential phishing activity.

It combines machine-learning models with simple, interpretable security indicators to provide a risk score, security status, and scan history.

## 🚀 Live Demo

Frontend: https://YOUR-FRONTEND-URL.onrender.com

Backend API: https://phishguard-api-yib4.onrender.com

> Replace `YOUR-FRONTEND-URL` with your actual Render frontend URL.

---

## ✨ Features

### 🔗 URL Security Scanner

- Analyzes URLs using a Random Forest machine-learning model.
- Extracts URL characteristics such as:
  - URL length
  - Domain length
  - HTTPS usage
  - IP-based domains
  - Subdomain count
  - Digit ratio
  - Special characters
  - URL entropy
  - Path and query length
- Detects common suspicious URL characteristics.
- Generates a risk score from 0–100.
- Classifies URLs as:
  - Safe
  - Suspicious
  - Malicious

### 📧 Email Phishing Scanner

- Uses TF-IDF text features.
- Uses Logistic Regression for classification.
- Detects suspicious language and common phishing indicators.
- Checks for patterns involving:
  - Urgent requests
  - Password information
  - Account verification
  - Suspicious links
  - Credit card information
  - Suspended accounts
- Generates a phishing risk score.

### 📊 Security Dashboard

- Total scans
- Safe scans
- Suspicious scans
- Phishing/Malicious scans
- Average risk score
- Visual statistics using charts

### 🗂️ Scan History

- Stores previous URL and email scans.
- Displays:
  - Scan type
  - Input
  - Risk score
  - Security status
  - ML probability
  - Timestamp

---

## 🧠 Machine Learning

### URL Detection

The URL detection system uses a Random Forest classifier trained on URL-based features.

The model uses features including:

- URL length
- Domain length
- TLD length
- Subdomain count
- IP address detection
- HTTPS usage
- Digit count
- Digit ratio
- Special character ratio
- Path length
- Query length
- URL entropy

### Email Detection

The email detection system uses:

**TF-IDF + Logistic Regression**

The email text is converted into numerical TF-IDF features and passed to the classification model.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      React UI        │
                    │  JavaScript/Tailwind │
                    └──────────┬───────────┘
                               │
                               │ HTTP REST API
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │   URL Scanner   │         │  Email Scanner  │
        │ Random Forest   │         │ TF-IDF + LR     │
        └────────┬────────┘         └────────┬────────┘
                 │                           │
                 └─────────────┬─────────────┘
                               ▼
                    ┌──────────────────────┐
                    │       SQLite         │
                    │    Scan History      │
                    └──────────────────────┘
🛠️ Tech Stack
Frontend
- React
- JavaScript
- Tailwind CSS
- Recharts
- Axios
- Vite
Backend
- Python
- FastAPI
- Pydantic
- SQLite
Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Random Forest
- Logistic Regression
- TF-IDF
Deployment
- GitHub
- Render
📁 Project Structure
PhishGuard/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   └── venv/
│
├── ml/
│   ├── models/
│   │   ├── url_phishing_model.pkl
│   │   └── email_phishing_model.pkl
│   │
│   ├── dataset/
│   ├── train_url_model.py
│   ├── train_email_model.py
│   ├── sanity_test.py
│   └── url_features.py
│
├── src/
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Dashboard.jsx
│   │   ├── URLScanner.jsx
│   │   ├── EmailScanner.jsx
│   │   └── History.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── .gitignore
├── package.json
├── package-lock.json
├── vite.config.js
└── README.md

⚙️ Running Locally
1. Clone the repository
git clone https://github.com/rajatsingh3719-lang/PhishGuard.git
cd PhishGuard

2. Install frontend dependencies
npm install

3. Start the frontend
npm run dev

The frontend will normally run at:
http://localhost:5173

4. Set up the backend
Open another terminal:
cd backend

Create a virtual environment:
python -m venv venv

Activate it on Windows:
.\venv\Scripts\Activate.ps1

Install dependencies:
pip install -r requirements.txt

Start FastAPI:
uvicorn main:app --reload

Backend:
http://127.0.0.1:8000

API documentation:
http://127.0.0.1:8000/docs

🔌 API Endpoints
Health Check
GET /health

URL Scanner
POST /api/url/scan

Example:
{
  "url": "https://github.com"
}

URL Features
POST /api/url/features

Email Scanner
POST /api/email/scan

Example:
{
  "email": "URGENT! Your account has been suspended. Click here to verify your password."
}

Scan History
GET /api/history

Dashboard Statistics
GET /api/dashboard/stats

📈 Risk Scoring
PhishGuard combines machine-learning predictions with interpretable security indicators.
For URLs, the final risk score combines:
ML Score       → 40%
Security Score → 60%

For emails, the score combines:
ML Probability → 40%
Indicators     → 60%

The purpose is to provide an understandable security assessment rather than relying only on a machine-learning prediction.
🔐 Security Note
PhishGuard is an educational and portfolio cybersecurity project.
It should not be treated as a guarantee that a website or email is safe.
The application uses URL characteristics, text classification, and heuristic indicators. It does not perform advanced threat intelligence, malware execution analysis, WHOIS investigation, or real-time external reputation checks.
🚀 Deployment
The application is deployed using Render.
Architecture:
GitHub
   │
   ├── React/Vite
   │       ↓
   │   Render Static Site
   │
   └── FastAPI
           ↓
       Render Web Service

The frontend communicates with the FastAPI backend through REST APIs.
🔮 Future Improvements
Possible future improvements include:
- Local LLM-based explanations
- More sophisticated URL analysis
- Additional phishing datasets
- Improved model validation
- User authentication
- Persistent production database
- More detailed security reports
- Improved model monitoring
👨‍💻 Author
Rajat Singh
GitHub:
https://github.com/rajatsingh3719-lang
⚠️ Disclaimer
PhishGuard is designed for educational, research, and portfolio purposes.
Security predictions are probabilistic and should not be considered a definitive security guarantee.

### Then commit it

After saving `README.md` in:

```text
PhishGuard/
├── README.md
├── backend/
├── ml/
└── src/

run:
git add README.md
git commit -m "Add professional project README"
git push origin main

One correction before you commit: replace this:
https://YOUR-FRONTEND-URL.onrender.com
