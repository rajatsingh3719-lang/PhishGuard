import { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/history`
      );

      setHistory(response.data.history || []);
    } catch (error) {
      console.error("Failed to load history:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white px-6 py-10">
      <div className="max-w-6xl mx-auto">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold">
            Scan History
          </h1>

          <p className="text-slate-400 mt-2">
            View previous URL and email security scans.
          </p>
        </div>

        {/* Loading */}
        {loading && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center">
            <p className="text-slate-400">
              Loading scan history...
            </p>
          </div>
        )}

        {/* Empty */}
        {!loading && history.length === 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center">
            <p className="text-slate-400">
              No scans have been recorded yet.
            </p>
          </div>
        )}

        {/* History */}
        {!loading && history.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">

            <div className="overflow-x-auto">

              <table className="w-full">

                <thead className="bg-slate-800/70">

                  <tr>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      Type
                    </th>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      Input
                    </th>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      Risk
                    </th>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      Status
                    </th>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      ML Probability
                    </th>

                    <th className="text-left px-5 py-4 text-sm text-slate-300">
                      Date
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {history.map((item) => (

                    <tr
                      key={item.id}
                      className="border-t border-slate-800 hover:bg-slate-800/40"
                    >

                      {/* Type */}
                      <td className="px-5 py-4">

                        <span className="px-3 py-1 rounded-full bg-blue-500/10 text-blue-400 text-xs font-semibold">
                          {item.scan_type}
                        </span>

                      </td>

                      {/* Input */}
                      <td className="px-5 py-4 max-w-md">

                        <div
                          className="truncate text-slate-300"
                          title={item.input_data}
                        >
                          {item.input_data}
                        </div>

                      </td>

                      {/* Risk */}
                      <td className="px-5 py-4">

                        <span className="font-semibold">
                          {item.risk_score}/100
                        </span>

                      </td>

                      {/* Status */}
                      <td className="px-5 py-4">

                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            item.status === "Safe"
                              ? "bg-green-500/10 text-green-400"
                              : item.status === "Suspicious"
                              ? "bg-yellow-500/10 text-yellow-400"
                              : "bg-red-500/10 text-red-400"
                          }`}
                        >
                          {item.status}
                        </span>

                      </td>

                      {/* Probability */}
                      <td className="px-5 py-4 text-slate-300">
                        {item.phishing_probability}%
                      </td>

                      {/* Timestamp */}
                      <td className="px-5 py-4 text-slate-400 text-sm whitespace-nowrap">
                        {item.timestamp}
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default History;