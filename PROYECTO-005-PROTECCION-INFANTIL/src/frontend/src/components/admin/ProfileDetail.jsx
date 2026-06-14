import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { API_URL } from "../../api";

const authHeaders = () => {
  const token = localStorage.getItem("admin_token");
  return {
    "Content-Type": "application/json",
    Authorization: token ? `Bearer ${token}` : "",
  };
};

function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString("es-CO", { year: "numeric", month: "short", day: "numeric" });
}

export default function ProfileDetail() {
  const { hash } = useParams();
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_URL}/api/v1/admin/profiles/${hash}`, {
          headers: authHeaders(),
        });
        if (res.status === 401) {
          localStorage.removeItem("admin_token");
          navigate("/admin/login");
          return;
        }
        if (!res.ok) throw new Error("No se pudo cargar el perfil");
        const data = await res.json();
        setProfile(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [hash, navigate]);

  if (loading) return <p className="text-center text-sm text-gray-500">Cargando perfil...</p>;
  if (error)
    return <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">{error}</div>;
  if (!profile) return null;

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-[#1A3A5C]">Detalle del perfil</h2>
        <Link
          to="/admin/profiles"
          className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700"
        >
          ← Volver
        </Link>
      </div>

      {profile.alert && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm font-semibold text-red-800">
          {profile.alert}
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-xl border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-2xl font-bold text-[#1A3A5C]">{profile.report_count}</p>
          <p className="text-xs text-gray-500">reportes</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-2xl font-bold text-[#1A3A5C]">
            {profile.score_average != null ? profile.score_average.toFixed(2) : "—"}
          </p>
          <p className="text-xs text-gray-500">score promedio</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-2xl font-bold text-[#1A3A5C]">{profile.cities_count}</p>
          <p className="text-xs text-gray-500">ciudades</p>
        </div>
        <div className="rounded-xl border border-gray-200 bg-white p-4 text-center shadow-sm">
          <p className="text-2xl font-bold text-[#1A3A5C]">{profile.countries_count}</p>
          <p className="text-xs text-gray-500">países</p>
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">Resumen</h3>
        <div className="grid gap-4 text-sm sm:grid-cols-2">
          <div>
            <span className="font-medium text-gray-600">Tipo:</span> {profile.identifier_type}
          </div>
          <div>
            <span className="font-medium text-gray-600">Score máx:</span>{" "}
            {profile.score_max != null ? profile.score_max.toFixed(2) : "—"}
          </div>
          <div>
            <span className="font-medium text-gray-600">Primero reportado:</span>{" "}
            {formatDate(profile.first_reported)}
          </div>
          <div>
            <span className="font-medium text-gray-600">Último reportado:</span>{" "}
            {formatDate(profile.last_reported)}
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">Categorías</h3>
        {profile.categories?.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {profile.categories.map((cat) => (
              <span
                key={cat}
                className="rounded-full bg-[#1A3A5C]/10 px-3 py-1 text-xs font-medium text-[#1A3A5C]"
              >
                {cat}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">Sin categorías registradas.</p>
        )}
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">
          Tipos de evidencia
        </h3>
        {profile.evidence_types?.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {profile.evidence_types.map((t) => (
              <span
                key={t}
                className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700"
              >
                {t}
              </span>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">Sin evidencia registrada.</p>
        )}
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">
          Ciudades / Países
        </h3>
        <div className="grid gap-4 text-sm sm:grid-cols-2">
          <div>
            <p className="font-medium text-gray-600">Ciudades:</p>
            <p className="text-gray-800">{profile.cities?.join(", ") || "—"}</p>
          </div>
          <div>
            <p className="font-medium text-gray-600">Países:</p>
            <p className="text-gray-800">{profile.countries?.join(", ") || "—"}</p>
          </div>
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500">
          Línea de tiempo
        </h3>
        {profile.timeline?.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-gray-50 text-xs uppercase text-gray-600">
                <tr>
                  <th className="px-3 py-2">Mes</th>
                  <th className="px-3 py-2">Reportes</th>
                  <th className="px-3 py-2">Score avg</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {profile.timeline.map((entry) => (
                  <tr key={entry.month}>
                    <td className="px-3 py-2">{entry.month}</td>
                    <td className="px-3 py-2">{entry.count}</td>
                    <td className="px-3 py-2">{entry.score_avg?.toFixed(2) ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-sm text-gray-500">Sin datos de timeline.</p>
        )}
      </div>
    </div>
  );
}
