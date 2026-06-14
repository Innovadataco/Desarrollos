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

export default function NetworksView() {
  const [networks, setNetworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchNetworks = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_URL}/api/v1/admin/profiles/networks/list`, {
          headers: authHeaders(),
        });
        if (res.status === 401) {
          localStorage.removeItem("admin_token");
          navigate("/admin/login");
          return;
        }
        if (!res.ok) throw new Error("No se pudieron cargar las redes");
        const data = await res.json();
        setNetworks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchNetworks();
  }, [navigate]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-[#1A3A5C]">Redes organizadas</h2>
        <Link
          to="/admin/profiles"
          className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700"
        >
          ← Perfiles
        </Link>
      </div>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          {error}
        </div>
      )}

      {loading ? (
        <p className="text-center text-sm text-gray-500">Cargando...</p>
      ) : networks.length === 0 ? (
        <p className="text-center text-sm text-gray-500">No se detectaron redes organizadas.</p>
      ) : (
        <div className="grid gap-4">
          {networks.map((n) => (
            <div
              key={n.identifier_hash}
              onClick={() => navigate(`/admin/profiles/${n.identifier_hash}`)}
              className="cursor-pointer rounded-xl border border-red-200 bg-red-50 p-4 shadow-sm transition hover:shadow-md"
            >
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <p className="text-xs text-gray-500">Hash del identificador</p>
                  <p className="font-mono text-sm font-semibold text-gray-900">
                    {n.identifier_hash.slice(0, 24)}…
                  </p>
                </div>
                <span className="rounded-full bg-red-200 px-3 py-1 text-xs font-bold text-red-800">
                  ⚠️ Red
                </span>
              </div>
              <div className="mt-3 grid gap-2 text-sm sm:grid-cols-4">
                <div>
                  <span className="text-gray-500">Reportes:</span>{" "}
                  <span className="font-semibold">{n.report_count}</span>
                </div>
                <div>
                  <span className="text-gray-500">Score max:</span>{" "}
                  <span className="font-semibold">
                    {n.score_max != null ? n.score_max.toFixed(2) : "—"}
                  </span>
                </div>
                <div>
                  <span className="text-gray-500">Ciudades:</span>{" "}
                  <span className="font-semibold">{n.cities_count}</span>
                </div>
                <div>
                  <span className="text-gray-500">Países:</span>{" "}
                  <span className="font-semibold">{n.countries_count}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
