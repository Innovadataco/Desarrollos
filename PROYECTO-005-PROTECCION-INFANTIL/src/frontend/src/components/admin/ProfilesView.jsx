import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { API_URL } from "../../api";

const authHeaders = () => {
  const token = localStorage.getItem("admin_token");
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
};

export default function ProfilesView() {
  const [profiles, setProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reportCountMin, setReportCountMin] = useState("");
  const [scoreMin, setScoreMin] = useState("");
  const [isNetwork, setIsNetwork] = useState("");
  const navigate = useNavigate();

  const fetchProfiles = async () => {
    setLoading(true);
    setError(null);
    const params = new URLSearchParams();
    if (reportCountMin) params.set("report_count_min", reportCountMin);
    if (scoreMin) params.set("score_min", scoreMin);
    if (isNetwork !== "") params.set("is_network", isNetwork);

    try {
      const res = await fetch(`${API_URL}/api/v1/admin/profiles?${params.toString()}`, {
        headers: authHeaders(),
      });
      if (res.status === 401) {
        localStorage.removeItem("admin_token");
        navigate("/admin/login");
        return;
      }
      if (!res.ok) throw new Error("No se pudieron cargar los perfiles");
      const data = await res.json();
      setProfiles(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfiles();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-[#1A3A5C]">Perfiles de contacto</h2>
        <Link
          to="/admin/networks"
          className="rounded-lg bg-[#E74C3C] px-4 py-2 text-sm font-semibold text-white"
        >
          Ver redes
        </Link>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <div className="grid gap-3 sm:grid-cols-4">
          <div>
            <label className="block text-xs font-medium text-gray-600">Reportes mín.</label>
            <input
              type="number"
              min={0}
              value={reportCountMin}
              onChange={(e) => setReportCountMin(e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
              placeholder="0"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600">Score mín.</label>
            <input
              type="number"
              min={0}
              max={1}
              step={0.01}
              value={scoreMin}
              onChange={(e) => setScoreMin(e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
              placeholder="0.0 - 1.0"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-gray-600">Red organizada</label>
            <select
              value={isNetwork}
              onChange={(e) => setIsNetwork(e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm bg-white"
            >
              <option value="">Todos</option>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={fetchProfiles}
              className="w-full rounded-lg bg-[#1A3A5C] py-2 text-sm font-semibold text-white"
            >
              Filtrar
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          {error}
        </div>
      )}

      {loading ? (
        <p className="text-center text-sm text-gray-500">Cargando...</p>
      ) : profiles.length === 0 ? (
        <p className="text-center text-sm text-gray-500">No hay perfiles que coincidan.</p>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-gray-50 text-xs uppercase text-gray-600">
              <tr>
                <th className="px-4 py-3">Hash</th>
                <th className="px-4 py-3">Tipo</th>
                <th className="px-4 py-3">Reportes</th>
                <th className="px-4 py-3">Score avg</th>
                <th className="px-4 py-3">Ciudades</th>
                <th className="px-4 py-3">Países</th>
                <th className="px-4 py-3">Red</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {profiles.map((p) => (
                <tr
                  key={p.identifier_hash}
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => navigate(`/admin/profiles/${p.identifier_hash}`)}
                >
                  <td className="px-4 py-3 font-mono text-xs">{p.identifier_hash.slice(0, 16)}…</td>
                  <td className="px-4 py-3">{p.identifier_type}</td>
                  <td className="px-4 py-3">{p.report_count}</td>
                  <td className="px-4 py-3">
                    {p.score_average != null ? p.score_average.toFixed(2) : "—"}
                  </td>
                  <td className="px-4 py-3">{p.cities_count}</td>
                  <td className="px-4 py-3">{p.countries_count}</td>
                  <td className="px-4 py-3">
                    {p.is_network ? (
                      <span className="rounded-full bg-red-100 px-2 py-1 text-xs font-medium text-red-800">
                        ⚠️ Sí
                      </span>
                    ) : (
                      <span className="text-gray-400">No</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
