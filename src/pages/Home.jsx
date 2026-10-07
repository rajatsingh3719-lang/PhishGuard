import { Link } from 'react-router-dom'

function Home() {
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


      {/* Hero */}
      <main className="mx-auto max-w-7xl px-8 py-24">

        <div className="max-w-3xl">

          <p className="mb-5 text-sm font-semibold tracking-wide text-cyan-400">
            AI-POWERED THREAT DETECTION
          </p>

          <h2 className="text-5xl font-bold leading-tight tracking-tight md:text-6xl">
            Detect phishing.
            <br />

            <span className="text-cyan-400">
              Stay protected.
            </span>
          </h2>

          <p className="mt-7 max-w-2xl text-lg leading-8 text-slate-400">
            PhishGuard uses machine learning and natural language
            processing to identify suspicious URLs and phishing emails
            before they become a threat.
          </p>


          {/* Buttons */}
          <div className="mt-10 flex flex-wrap gap-4">

            <Link
              to="/url-scanner"
              className="rounded-lg bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400"
            >
              Scan a URL
            </Link>

            <Link
              to="/email-scanner"
              className="rounded-lg border border-slate-700 px-6 py-3 font-semibold text-slate-200 transition hover:bg-slate-800"
            >
              Analyze Email
            </Link>

          </div>

        </div>


        {/* Features */}
        <div className="mt-24 grid gap-6 md:grid-cols-3">

          <FeatureCard
            icon="🔗"
            title="URL Detection"
            description="Analyze suspicious URLs using machine learning and identify phishing patterns."
          />

          <FeatureCard
            icon="📧"
            title="Email Analysis"
            description="Detect suspicious language and phishing patterns in emails using NLP."
          />

          <FeatureCard
            icon="🤖"
            title="AI Explanation"
            description="Understand why a URL or email has been classified as suspicious."
          />

        </div>

      </main>

    </div>
  )
}


function FeatureCard({ icon, title, description }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-7 transition hover:border-cyan-500/40">

      <div className="mb-6 text-3xl">
        {icon}
      </div>

      <h3 className="text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-3 text-sm leading-6 text-slate-400">
        {description}
      </p>

    </div>
  )
}


export default Home