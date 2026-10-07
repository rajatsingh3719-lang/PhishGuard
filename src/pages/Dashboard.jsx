import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/dashboard/stats`
      );

      setStats(response.data);
    } catch (error) {
      console.error("Failed to load dashboard:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
        <div className="max-w-6xl mx-auto">
          <p className="text-slate-400">
            Loading dashboard...
          </p>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
        <div className="max-w-6xl mx-auto">
          <div className="bg-red-500/10 border border-red-500/30 text-red-300 rounded-xl p-4">
            Unable to load dashboard statistics.
          </div>
        </div>
      </div>
    );
  }

  const chartData = [
    {
      name: "Safe",
      value: stats.safe_scans,
    },
    {
      name: "Suspicious",
      value: stats.suspicious_scans,
    },
    {
      name: "Phishing",
      value: stats.phishing_scans,
    },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">

      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="mb-8">

          <h1 className="text-3xl font-bold">
            Security Dashboard
          </h1>

          <p className="text-slate-400 mt-2">
            Overview of your PhishGuard security scans.
          </p>

        </div>


        {/* Statistics */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">

          {/* Total */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Total Scans
            </p>

            <p className="text-3xl font-bold mt-2">
              {stats.total_scans}
            </p>

          </div>


          {/* Safe */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Safe Scans
            </p>

            <p className="text-3xl font-bold text-green-400 mt-2">
              {stats.safe_scans}
            </p>

          </div>


          {/* Suspicious */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Suspicious
            </p>

            <p className="text-3xl font-bold text-yellow-400 mt-2">
              {stats.suspicious_scans}
            </p>

          </div>


          {/* Phishing */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Phishing / Malicious
            </p>

            <p className="text-3xl font-bold text-red-400 mt-2">
              {stats.phishing_scans}
            </p>

          </div>

        </div>


        {/* Average Risk */}
        <div className="mt-5">

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">

            <p className="text-slate-400 text-sm">
              Average Risk Score
            </p>

            <div className="flex items-end gap-2 mt-2">

              <p className="text-4xl font-bold">
                {stats.average_risk}
              </p>

              <p className="text-slate-500 mb-1">
                / 100
              </p>

            </div>

          </div>

        </div>


        {/* Chart */}
        <div className="mt-8 bg-slate-900 border border-slate-800 rounded-2xl p-6">

          <h2 className="text-xl font-semibold mb-6">
            Scan Distribution
          </h2>

          {stats.total_scans === 0 ? (

            <div className="h-72 flex items-center justify-center text-slate-400">
              No scan data available yet.
            </div>

          ) : (

            <div className="h-72">

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <PieChart>

                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >

                    <Cell />
                    <Cell />
                    <Cell />

                  </Pie>

                  <Tooltip />

                </PieChart>

              </ResponsiveContainer>

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

export default Dashboard;