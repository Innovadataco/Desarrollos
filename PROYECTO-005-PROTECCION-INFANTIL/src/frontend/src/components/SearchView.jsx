import { useState } from "react";
import { API_URL } from "../api";

const LEVEL_STYLES = {
  low: {
    bg: "bg-green-50",
    border: "border-green-200",
    text: "text-green-800",
    badge: "bg-green-600",
    label: "Sin reportes previos",
  },
  medium: {
    bg: "bg-yellow-50",
    border: "border-yellow-200",
    text: "text-yellow-800",
    badge: "bg-yellow-500",
    label: "Precaución: reportes previos",
  },
  high: {
    bg: "bg-orange-50",
    border: "border-orange-200",
    text: "text-orange-800",
    badge: "bg-orange-500",
    label: "Riesgo alto",
  },
  critical: {
    bg: "bg-red-50",
    border: "border-red-200",
    text: "text-red-800",
    badge: "bg-red-600",
    label: "Riesgo crítico",
  },
  severe: {
    bg: "bg-red-100",
    border: "border-red-300",
    text: "text-red-900",
    badge: "bg-red-700",
    label: "Riesgo severo",
  },
};

export default function SearchView({ onReport }) {
  const [identifier, setIdentifier] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/api/v1/consultas`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ identifier }),
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

  const style = result ? LEVEL_STYLES[result.level] || LEVEL_STYLES.low : null;

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#1A3A5C]">Buscar contacto</h2>
        <p className="text-sm text-gray-600 mt-1">
          Verifica si un número o usuario tiene reportes previos.
        </p>
      </div>

      <form onSubmit={handleSearch} className="space-y-4">
        <label htmlFor="search-identifier" className="sr-only">
          Número o identificador
        </label>
        <div className="flex gap-2">
          <input
            id="search-identifier"
            type="tel"
            inputMode="tel"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="+57 300 123 4567"
            className="flex-1 rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
            required
          />
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
          className={`rounded-xl border p-5 ${style.bg} ${style.border} ${style.text}`}
        >
          <div className="flex items-center gap-3 mb-3">
            <span
              className={`inline-block h-4 w-4 rounded-full ${style.badge}`}
              aria-hidden="true"
            />
            <h3 className="text-lg font-bold">{style.label}</h3>
          </div>
          <p className="text-base mb-4">{result.message}</p>
          {result.status === "found" && (
            <ul className="text-sm space-y-1 mb-4">
              <li>Reportes asociados: {result.report_count}</li>
              <li>Nivel: {result.level}</li>
              {result.is_network && (
                <li className="font-semibold">⚠️ Posible red de contacto</li>
              )}
            </ul>
          )}
          <button
            onClick={() => onReport && onReport(identifier)}
            className="w-full rounded-lg bg-[#E74C3C] py-3 text-white font-semibold"
          >
            Reportar ahora
          </button>
          {result.resources?.length > 0 && (
            <div className="mt-4 pt-4 border-t border-current border-opacity-20">
              <p className="font-semibold mb-2">Recursos de apoyo:</p>
              <ul className="space-y-1">
                {result.resources.map((url, idx) => (
                  <li key={idx}>
                    <a
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="underline"
                    >
                      {url}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 text-sm text-gray-600">
        🔒 No guardamos tu búsqueda ni tu identidad.
      </div>
    </div>
  );
}
