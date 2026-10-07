import { useState } from "react";
import axios from "axios";

function EmailScanner() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const scanEmail = async () => {
    if (!email.trim()) {
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/email/scan",
        {
          email: email,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);

      setResult({
        success: false,
        message: "Unable to connect to the PhishGuard backend.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="max-w-4xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Email Scanner
          </h1>

          <p className="text-slate-400 mt-2">
            Analyze an email for phishing indicators using machine learning.
          </p>
        </div>

        {/* Input */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

          <label className="block text-sm font-medium text-slate-300 mb-3">
            Email Content
          </label>

          <textarea
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Paste the email content here..."
            rows={10}
            className="w-full rounded-xl bg-slate-950 border border-slate-700 px-4 py-3 text-white outline-none focus:border-blue-500 resize-none"
          />

          <button
            onClick={scanEmail}
            disabled={loading || !email.trim()}
            className="mt-4 px-6 py-3 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-400 font-semibold transition"
          >
            {loading ? "Scanning..." : "Scan Email"}
          </button>
        </div>

        {/* Result */}
        {result && result.success && (
          <div className="mt-8 bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <div className="flex items-center justify-between mb-6">

              <h2 className="text-xl font-semibold">
                Scan Result
              </h2>

              <span
                className={`px-4 py-2 rounded-full text-sm font-semibold ${
                  result.status === "Safe"
                    ? "bg-green-500/20 text-green-400"
                    : result.status === "Suspicious"
                    ? "bg-yellow-500/20 text-yellow-400"
                    : "bg-red-500/20 text-red-400"
                }`}
              >
                {result.status}
              </span>

            </div>

            {/* Risk Score */}
            <div className="mb-6">

              <div className="flex justify-between mb-2">
                <span className="text-slate-400">
                  Risk Score
                </span>

                <span className="font-bold">
                  {result.risk_score}/100
                </span>
              </div>

              <div className="w-full h-3 bg-slate-800 rounded-full overflow-hidden">

                <div
                  className={`h-full rounded-full ${
                    result.status === "Safe"
                      ? "bg-green-500"
                      : result.status === "Suspicious"
                      ? "bg-yellow-500"
                      : "bg-red-500"
                  }`}
                  style={{
                    width: `${result.risk_score}%`,
                  }}
                />

              </div>

            </div>

            {/* ML Probability */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">

              <div className="bg-slate-950 rounded-xl p-4">
                <p className="text-sm text-slate-400">
                  ML Phishing Probability
                </p>

                <p className="text-2xl font-bold mt-1">
                  {result.phishing_probability}%
                </p>
              </div>

              <div className="bg-slate-950 rounded-xl p-4">
                <p className="text-sm text-slate-400">
                  ML Prediction
                </p>

                <p className="text-2xl font-bold mt-1">
                  {result.prediction === 1
                    ? "Phishing"
                    : "Legitimate"}
                </p>
              </div>

            </div>

            {/* Message */}
            <div className="bg-slate-950 rounded-xl p-4 mb-6">
              <p className="text-slate-300">
                {result.message}
              </p>
            </div>

            {/* Indicators */}
            {result.indicators &&
              result.indicators.length > 0 && (

                <div>

                  <h3 className="font-semibold mb-3">
                    Security Indicators
                  </h3>

                  <div className="space-y-2">

                    {result.indicators.map(
                      (indicator, index) => (
                        <div
                          key={index}
                          className="bg-red-500/10 border border-red-500/20 text-red-300 rounded-lg px-4 py-3"
                        >
                          ⚠ {indicator}
                        </div>
                      )
                    )}

                  </div>

                </div>

              )}

          </div>
        )}

        {/* Error */}
        {result && !result.success && (
          <div className="mt-8 bg-red-500/10 border border-red-500/30 text-red-300 rounded-xl p-4">
            {result.message || result.error}
          </div>
        )}

      </div>
    </div>
  );
}

export default EmailScanner;