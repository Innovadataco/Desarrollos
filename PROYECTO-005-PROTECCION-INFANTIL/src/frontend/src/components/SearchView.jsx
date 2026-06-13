import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../api";

const LEVEL_STYLES = {
  verde: {
    bg: "bg-green-50",
    border: "border-green-200",
    text: "text-green-800",
    badge: "bg-green-600",
    label: "Sin reportes previos",
  },
  amarillo: {
    bg: "bg-yellow-50",
    border: "border-yellow-200",
    text: "text-yellow-800",
    badge: "bg-yellow-500",
    label: "Precaución: reportes previos",
  },
  rojo: {
    bg: "bg-red-50",
    border: "border-red-200",
    text: "text-red-800",
    badge: "bg-red-600",
    label: "Riesgo alto",
  },
  negro: {
    bg: "bg-gray-900",
    border: "border-gray-700",
    text: "text-white",
    badge: "bg-red-700",
    label: "Riesgo crítico: posible red organizada",
  },
};

export default function SearchView() {
  const [identifier, setIdentifier] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const encoded = encodeURIComponent(identifier.trim());
      const res = await fetch(`${API_URL}/api/v1/validate/${encoded}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "No pudimos completar la búsqueda.");
      } else {
        setResult(data);
      }
    } catch {
      setError("Error de conexión. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleShare = () => {
    const url = `${window.location.origin}${window.location.pathname}?ref=consulta`;
    navigator.clipboard.writeText(url).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  const style = result ? LEVEL_STYLES[result.semaforo] || LEVEL_STYLES.verde : null;

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#1A3A5C]">Buscar contacto</h2>
        <p className="text-sm text-gray-600 mt-1">
          Verifica si un número, usuario, email o sitio tiene reportes previos.
        </p>
      </div>

      <form onSubmit={handleSearch} className="space-y-4" role="search" aria-label="Buscar contacto">
        <label htmlFor="search-identifier" className="sr-only">
          Número o identificador
        </label>
        <div className="flex gap-2">
          <div className="relative flex-1">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" aria-hidden="true">
              🔍
            </span>
            <input
              id="search-identifier"
              type="text"
              inputMode="search"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="+57 300 123 4567, @usuario, email o URL"
              className="w-full rounded-lg border border-gray-300 pl-10 pr-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
              aria-describedby="search-help"
            />
          </div>
          <button
            type="submit"
            disabled={loading || !identifier.trim()}
            className="rounded-lg bg-[#1A3A5C] px-5 py-3 text-white font-semibold disabled:opacity-50"
          >
            {loading ? "..." : "Buscar"}
          </button>
        </div>
      </form>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800">
          {error}
        </div>
      )}

      {result && style && (
        <div
          className={`rounded-xl border p-5 shadow-md transition-all duration-500 ease-out animate-fade-in ${style.bg} ${style.border} ${style.text}`}
        >
          <div className="flex items-center gap-3 mb-3">
            <span
              className={`inline-block h-4 w-4 rounded-full ${style.badge}`}
              aria-hidden="true"
            />
            <h3 className="text-lg font-bold">{style.label}</h3>
          </div>
          <p className="text-base mb-4">{result.message}</p>
          {result.report_count > 0 && (
            <ul className="text-sm space-y-1 mb-4">
              <li>Reportes asociados: {result.report_count}</li>
              <li>Categorías: {result.categories?.join(", ") || "—"}</li>
              <li>
                Score: promedio {result.score_average ?? "—"}, máximo{" "}
                {result.score_max ?? "—"}
              </li>
              <li>
                Geografía: {result.cities_count} ciudad(es),{" "}
                {result.countries_count} país(es)
              </li>
              {result.is_network && (
                <li className="font-semibold">⚠️ Posible red de contacto</li>
              )}
            </ul>
          )}
          <div className="flex flex-col gap-2">
            <button
              onClick={() => navigate(`/report?identifier=${encodeURIComponent(identifier)}`)}
              className="w-full rounded-lg bg-[#E74C3C] py-3 text-white font-semibold transition-transform duration-200 hover:scale-[1.02] active:scale-95"
            >
              📣 Reportar este {result.identifier_type === "email" ? "correo" : "identificador"}
            </button>
            <button
              onClick={handleShare}
              className="w-full rounded-lg border border-current bg-transparent py-2 text-sm font-medium transition-colors duration-200 hover:bg-white/30"
            >
              {copied ? "✓ Enlace copiado" : "Compartir resultado"}
            </button>
          </div>
        </div>
      )}

      <p id="search-help" className="text-xs text-gray-500">
        Busca números de teléfono, usuarios de redes sociales, emails o URLs.
      </p>

      <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 text-sm text-gray-600">
        🔒 No guardamos tu búsqueda ni tu identidad.
      </div>
    </div>
  );
}
