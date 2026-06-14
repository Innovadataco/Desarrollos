import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API_URL } from "../api";

const PLACEHOLDERS = {
  phone: "+57 300 123 4567",
  email: "correo@ejemplo.com",
  social: "@usuario",
  url: "https://sitio.com/perfil",
  text: "Escribe un nombre o identificador",
};

function detectType(value) {
  const v = value.trim();
  if (/^\+?\d[\d\s\-\(\)]{6,20}$/.test(v)) return "phone";
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return "email";
  if (v.startsWith("@")) return "social";
  if (/^https?:\/\//i.test(v)) return "url";
  return "text";
}

const CATEGORY_LABELS = {
  contacto_inapropiado: "Contacto inapropiado",
  solicitud_material: "Solicitud de material sexual",
  grooming: "Grooming / Engaño",
  cita_persona: "Cita en persona",
  extorsion: "Extorsión",
  desconocido: "Desconocido",
  otro: "Otro",
};

function formatDate(value) {
  if (!value) return null;
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleDateString("es-CO", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

const LEVEL_STYLES = {
  verde: {
    bg: "bg-green-50",
    border: "border-green-200",
    text: "text-green-800",
    badge: "bg-green-600",
    label: "Sin reportes previos",
    emoji: "🟢",
  },
  amarillo: {
    bg: "bg-yellow-50",
    border: "border-yellow-200",
    text: "text-yellow-800",
    badge: "bg-yellow-500",
    label: "Precaución: reportes previos",
    emoji: "🟡",
  },
  rojo: {
    bg: "bg-red-50",
    border: "border-red-200",
    text: "text-red-800",
    badge: "bg-red-600",
    label: "Riesgo alto",
    emoji: "🔴",
  },
  negro: {
    bg: "bg-gray-900",
    border: "border-gray-700",
    text: "text-white",
    badge: "bg-red-700",
    label: "Riesgo crítico: posible red organizada",
    emoji: "⚫",
  },
};

export default function SearchView() {
  const [identifier, setIdentifier] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [alertEmail, setAlertEmail] = useState("");
  const [alertSaved, setAlertSaved] = useState(false);
  const navigate = useNavigate();

  function loadAlertState(hash) {
    try {
      const raw = localStorage.getItem("alerts");
      const alerts = raw ? JSON.parse(raw) : {};
      return alerts[hash] || null;
    } catch {
      return null;
    }
  }

  function saveAlertState(hash, email) {
    try {
      const raw = localStorage.getItem("alerts");
      const alerts = raw ? JSON.parse(raw) : {};
      alerts[hash] = { email, createdAt: new Date().toISOString() };
      localStorage.setItem("alerts", JSON.stringify(alerts));
    } catch {
      // ignore
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);
    setAlertSaved(false);
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
        setAlertSaved(!!loadAlertState(data.identifier_hash));
      }
    } catch {
      setError("Error de conexión. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    const url = `${window.location.origin}${window.location.pathname}?ref=consulta`;
    const text = result
      ? `Semáforo de Confianza: ${style?.label || result.semaforo}. Consulta contactos sospechosos de forma anónima.`
      : "Consulta contactos sospechosos de forma anónima en el Semáforo de Confianza.";

    if (navigator.share) {
      try {
        await navigator.share({ title: "Semáforo de Confianza", text, url });
        return;
      } catch (err) {
        if (err.name === "AbortError") return;
      }
    }

    try {
      await navigator.clipboard.writeText(`${text} ${url}`);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // ignore
    }
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
              placeholder={PLACEHOLDERS[detectType(identifier)]}
              className="w-full rounded-lg border border-gray-300 pl-10 pr-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
              aria-describedby="search-help"
            />
            {identifier.trim() && (
              <span className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-[#1A3A5C]/10 px-2 py-0.5 text-xs font-medium text-[#1A3A5C]">
                {detectType(identifier) === "phone" && "📱 Teléfono"}
                {detectType(identifier) === "email" && "📧 Email"}
                {detectType(identifier) === "social" && "💬 Red social"}
                {detectType(identifier) === "url" && "🌐 URL"}
                {detectType(identifier) === "text" && "📝 Texto"}
              </span>
            )}
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
            <span className="text-2xl" aria-hidden="true">
              {style.emoji}
            </span>
            <h3 className="text-lg font-bold">{style.label}</h3>
          </div>
          <p className="text-base mb-4">{result.message}</p>
          {result.report_count > 0 && (
            <div className="mb-4 space-y-4 text-sm">
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-lg bg-white/60 p-3 text-center">
                  <p className="text-2xl font-bold">{result.report_count}</p>
                  <p className="text-xs opacity-80">reportes</p>
                </div>
                <div className="rounded-lg bg-white/60 p-3 text-center">
                  <p className="text-2xl font-bold">
                    {result.score_average != null
                      ? Number(result.score_average).toFixed(2)
                      : "—"}
                  </p>
                  <p className="text-xs opacity-80">score promedio</p>
                </div>
                <div className="rounded-lg bg-white/60 p-3 text-center">
                  <p className="text-2xl font-bold">{result.cities_count ?? 0}</p>
                  <p className="text-xs opacity-80">ciudades</p>
                </div>
                <div className="rounded-lg bg-white/60 p-3 text-center">
                  <p className="text-2xl font-bold">{result.countries_count ?? 0}</p>
                  <p className="text-xs opacity-80">países</p>
                </div>
              </div>

              {result.categories?.length > 0 && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide opacity-70">
                    Categorías reportadas
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {result.categories.map((cat) => (
                      <span
                        key={cat}
                        className="rounded-full bg-white/70 px-3 py-1 text-xs font-medium"
                      >
                        {CATEGORY_LABELS[cat] || cat}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div>
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide opacity-70">
                  Línea de tiempo
                </p>
                <div className="space-y-2">
                  <div className="flex justify-between rounded-lg bg-white/50 px-3 py-2">
                    <span>Primera vez reportado</span>
                    <span className="font-medium">
                      {formatDate(result.first_reported_at) || "—"}
                    </span>
                  </div>
                  <div className="flex justify-between rounded-lg bg-white/50 px-3 py-2">
                    <span>Última vez reportado</span>
                    <span className="font-medium">
                      {formatDate(result.last_reported_at) || "—"}
                    </span>
                  </div>
                </div>
              </div>

              {result.is_network && (
                <p className="rounded-lg bg-red-100/50 p-2 text-center font-semibold">
                  ⚠️ Posible red de contacto
                </p>
              )}
            </div>
          )}
          <div className="flex flex-col gap-2">
            <button
              onClick={() => navigate(`/report?identifier=${encodeURIComponent(identifier)}`)}
              className="w-full rounded-lg bg-[#E74C3C] py-3 text-white font-semibold transition-transform duration-200 hover:scale-[1.02] active:scale-95"
            >
              📣 Reportar este {detectType(identifier) === "email" ? "correo" : "identificador"}
            </button>
            <button
              onClick={handleShare}
              className="w-full rounded-lg border border-current bg-transparent py-2 text-sm font-medium transition-colors duration-200 hover:bg-white/30"
            >
              {copied ? "✓ Enlace copiado" : "Compartir resultado"}
            </button>
          </div>

          {result.report_count > 0 && (
            <div className="mt-4 rounded-lg bg-white/50 p-3">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wide opacity-70">
                🔔 Alertarme si cambia
              </p>
              {alertSaved ? (
                <p className="text-sm font-medium">✓ Alerta activada para este identificador.</p>
              ) : (
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    if (!alertEmail.trim() || !result.identifier_hash) return;
                    saveAlertState(result.identifier_hash, alertEmail.trim());
                    setAlertSaved(true);
                    setAlertEmail("");
                  }}
                  className="flex flex-col gap-2"
                >
                  <input
                    type="email"
                    value={alertEmail}
                    onChange={(e) => setAlertEmail(e.target.value)}
                    placeholder="tu@email.com"
                    required
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
                  />
                  <button
                    type="submit"
                    className="w-full rounded-lg bg-[#1A3A5C] py-2 text-sm font-semibold text-white transition-transform duration-200 hover:scale-[1.02] active:scale-95"
                  >
                    Activar alerta Premium
                  </button>
                  <p className="text-xs opacity-70">
                    Gratis durante el lanzamiento. Luego $2.99/mes.
                  </p>
                </form>
              )}
            </div>
          )}
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
