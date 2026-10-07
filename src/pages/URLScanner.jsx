import { useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

function URLScanner() {
  const [url, setUrl] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleScan = async (e) => {
    e.preventDefault()

    if (!url.trim()) {
      setError('Please enter a URL.')
      setResult(null)
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/url/scan',
        {
          url: url.trim(),
        }
      )

      const data = response.data

      setResult({
        score: data.risk_score,
        status: data.status,
        message: data.message,
        indicators: data.indicators,
      })
    } catch (err) {
      console.error(err)

      setError(
        'Unable to connect to the PhishGuard backend. Make sure FastAPI is running.'
      )
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = () => {
    if (!result) return 'text-slate-400'

    if (result.status === 'Safe') {
      return 'text-emerald-400'
    }

    if (result.status === 'Suspicious') {
      return 'text-amber-400'
    }

    return 'text-red-400'
  }

  const getBorderColor = () => {
    if (!result) return 'border-slate-800'

    if (result.status === 'Safe') {
      return 'border-emerald-500/30'
    }

    if (result.status === 'Suspicious') {
      return 'border-amber-500/30'
    }

    return 'border-red-500/30'
  }

  const getBarColor = () => {
    if (!result) return 'bg-slate-500'

    if (result.status === 'Safe') {
      return 'bg-emerald-400'
    }

    if (result.status === 'Suspicious') {
      return 'bg-amber-400'
    }

    return 'bg-red-400'
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      {/* Navbar */}
      <nav className="border-b border-slate-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <Link to="/" className="flex items-center gap-3">

            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-xl">
              🛡️
            </div>

            <div>
              <h1 className="text-xl font-bold">
                PhishGuard
              </h1>

              <p className="text-xs text-slate-500">
                AI Security Platform
              </p>
            </div>

          </Link>

          <Link
            to="/dashboard"
            className="rounded-lg border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-200 transition hover:bg-slate-800"
          >
            Dashboard
          </Link>

        </div>
      </nav>


      {/* Main */}
      <main className="mx-auto max-w-4xl px-8 py-20">

        <div className="text-center">

          <p className="text-sm font-semibold tracking-wide text-cyan-400">
            URL SECURITY SCANNER
          </p>

          <h2 className="mt-4 text-4xl font-bold">
            Is this website safe?
          </h2>

          <p className="mx-auto mt-5 max-w-2xl text-slate-400">
            Enter a URL and PhishGuard will analyze its characteristics
            to identify potential phishing or malicious activity.
          </p>

        </div>


        {/* Scanner Card */}
        <div className="mt-12 rounded-2xl border border-slate-800 bg-slate-900/60 p-8">

          <form onSubmit={handleScan}>

            <label className="mb-3 block text-sm font-medium text-slate-300">
              Website URL
            </label>

            <div className="flex flex-col gap-4 sm:flex-row">

              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                className="flex-1 rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition placeholder:text-slate-600 focus:border-cyan-500"
              />

              <button
                type="submit"
                disabled={loading}
                className="rounded-lg bg-cyan-500 px-7 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? 'Scanning...' : 'Scan URL'}
              </button>

            </div>

          </form>


          {/* Error */}
          {error && (

            <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/5 p-4">

              <p className="text-sm text-red-400">
                {error}
              </p>

            </div>

          )}


          {/* Result */}
          {result && (

            <div
              className={`mt-8 rounded-xl border bg-slate-950/40 p-6 ${getBorderColor()}`}
            >

              <div className="flex items-center justify-between">

                <div>

                  <p className="text-sm text-slate-400">
                    Security Result
                  </p>

                  <h3 className={`mt-1 text-2xl font-bold ${getStatusColor()}`}>
                    {result.status}
                  </h3>

                </div>


                <div className="text-right">

                  <p className="text-sm text-slate-400">
                    Risk Score
                  </p>

                  <p className="text-3xl font-bold">

                    {result.score}

                    <span className="text-lg text-slate-500">
                      /100
                    </span>

                  </p>

                </div>

              </div>


              {/* Risk Bar */}
              <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-800">

                <div
                  className={`h-full rounded-full transition-all ${getBarColor()}`}
                  style={{
                    width: `${result.score}%`,
                  }}
                />

              </div>


              {/* Message */}
              <p className="mt-5 text-sm text-slate-400">
                {result.message}
              </p>


              {/* Indicators */}
              {result.indicators && result.indicators.length > 0 && (

                <div className="mt-6">

                  <p className="text-sm font-medium text-slate-300">
                    Detected Indicators
                  </p>

                  <div className="mt-3 space-y-2">

                    {result.indicators.map((indicator, index) => (

                      <div
                        key={index}
                        className="rounded-lg border border-slate-800 bg-slate-900 px-4 py-3 text-sm text-slate-400"
                      >
                        ⚠️ {indicator}
                      </div>

                    ))}

                  </div>

                </div>

              )}


              {/* AI Explanation */}
              <div className="mt-6 border-t border-slate-800 pt-5">

                <p className="text-sm font-medium text-slate-300">
                  AI Explanation
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  AI explanation will be added after the core URL
                  detection system is connected to the local LLM.
                </p>

              </div>

            </div>

          )}

        </div>


        {/* Disclaimer */}
        <p className="mt-6 text-center text-xs text-slate-600">
          PhishGuard provides automated security analysis and should
          not be considered a guarantee that a website is safe.
        </p>

      </main>

    </div>
  )
}

export default URLScanner