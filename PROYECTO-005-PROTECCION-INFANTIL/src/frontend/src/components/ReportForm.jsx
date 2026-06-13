import { useEffect, useState } from "react";
import { API_URL } from "../api";

const TYPES = [
  { id: "phone", label: "📱 Celular", category: "contacto_inapropiado" },
  { id: "social", label: "💬 Red social", category: "contacto_inapropiado" },
  { id: "email", label: "📧 Email", category: "contacto_inapropiado" },
  { id: "url", label: "🌐 Sitio web", category: "solicitud_material" },
  { id: "content", label: "📸 Contenido inapropiado", category: "solicitud_material" },
  { id: "other", label: "📝 Otro", category: "otro" },
];

export default function ReportForm({ prefillIdentifier = "" }) {
  const [step, setStep] = useState(1);
  const [type, setType] = useState("");
  const [identifier, setIdentifier] = useState(prefillIdentifier);
  const [description, setDescription] = useState("");
  const [evidence, setEvidence] = useState("");
  const [evidenceType, setEvidenceType] = useState("text");
  const [confirmed, setConfirmed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIdentifier(prefillIdentifier);
  }, [prefillIdentifier]);

  const selected = TYPES.find((t) => t.id === type);

  const canNext =
    (step === 1 && type) ||
    (step === 2 && identifier.trim().length >= 1 && description.trim().length >= 10);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!confirmed) return;
    setLoading(true);
    setError(null);
    const payload = {
      reported_identifier: identifier,
      description,
      category: selected?.category || "otro",
      evidence: evidence
        ? { type: evidenceType, content: evidence }
        : undefined,
    };
    try {
      const res = await fetch(`${API_URL}/api/v1/reportes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) {
        if (res.status === 429) {
          setError(data.detail || "Has alcanzado el límite. Intenta más tarde.");
        } else if (res.status === 422) {
          setError("Verifica los campos e intenta de nuevo.");
        } else {
          setError(data.detail || "No se pudo enviar el reporte.");
        }
      } else {
        setResult(data);
      }
    } catch {
      setError("Error de conexión. Verifica tu red e intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setStep(1);
    setType("");
    setIdentifier("");
    setDescription("");
    setEvidence("");
    setConfirmed(false);
    setResult(null);
    setError(null);
  };

  if (result) {
    return (
      <div className="text-center space-y-5 rounded-xl border border-green-200 bg-green-50 p-6">
        <div className="text-5xl">🛡️</div>
        <h2 className="text-xl font-bold text-green-800">
          Protección activada
        </h2>
        <p className="text-green-800">
          Hiciste lo correcto. Tu reporte fue recibido de forma anónima.
        </p>
        <div className="rounded-lg bg-white p-4 text-left">
          <p className="text-sm text-gray-600">Guarda este código:</p>
          <p className="break-all font-mono text-sm font-semibold text-gray-900">
            {result.report_hash}
          </p>
        </div>
        <button
          onClick={reset}
          className="rounded-lg bg-[#1A3A5C] px-6 py-3 text-white font-semibold"
        >
          Reportar otro
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#1A3A5C]">Reportar anónimo</h2>
        <p className="text-sm text-gray-600 mt-1">
          Tu identidad no se guarda. Ni siquiera nosotros sabemos quién eres.
        </p>
      </div>

      <div className="flex justify-center gap-2" aria-label="Progreso">
        {[1, 2, 3].map((s) => (
          <span
            key={s}
            className={`h-3 w-3 rounded-full ${
              s < step
                ? "bg-[#1A3A5C]"
                : s === step
                ? "border-2 border-[#1A3A5C]"
                : "bg-gray-300"
            }`}
          />
        ))}
      </div>

      {step === 1 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 1: ¿Qué tipo de contacto es?</p>
          <div className="grid grid-cols-2 gap-3">
            {TYPES.map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setType(t.id)}
                className={`rounded-lg border px-3 py-4 text-sm font-medium text-center transition ${
                  type === t.id
                    ? "border-[#1A3A5C] bg-[#1A3A5C] text-white"
                    : "border-gray-300 bg-white text-gray-700 hover:bg-gray-50"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {step === 2 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 2: Identificador y descripción</p>
          <div>
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">
              Número o identificador reportado
            </label>
            <input
              id="identifier"
              type="text"
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="+57 300 123 4567"
              className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
            />
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              ¿Qué te pareció sospechoso?
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe lo que pasó..."
              rows={4}
              minLength={10}
              className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
            />
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 3: Evidencia y confirmación</p>
          <div>
            <label htmlFor="evidence" className="block text-sm font-medium text-gray-700">
              Evidencia (opcional)
            </label>
            <select
              id="evidence-type"
              value={evidenceType}
              onChange={(e) => setEvidenceType(e.target.value)}
              className="mt-1 mb-2 w-full rounded-lg border border-gray-300 px-3 py-2 text-base"
            >
              <option value="text">Texto / captura</option>
              <option value="image">Imagen</option>
              <option value="video">Video</option>
              <option value="audio">Audio</option>
              <option value="screenshot">Captura de pantalla</option>
            </select>
            <textarea
              id="evidence"
              value={evidence}
              onChange={(e) => setEvidence(e.target.value)}
              placeholder="Pega aquí el contenido de la evidencia..."
              rows={3}
              className="w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
            />
          </div>
          <label className="flex items-start gap-3">
            <input
              type="checkbox"
              checked={confirmed}
              onChange={(e) => setConfirmed(e.target.checked)}
              className="mt-1 h-5 w-5 accent-[#1A3A5C]"
            />
            <span className="text-sm text-gray-700">
              Confirmo que esta información es veraz y la comparto de forma anónima.
            </span>
          </label>
        </div>
      )}

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 text-sm">
          {error}
        </div>
      )}

      <div className="flex gap-3 pt-2">
        {step > 1 ? (
          <button
            type="button"
            onClick={() => setStep(step - 1)}
            className="flex-1 rounded-lg border border-gray-300 bg-white py-3 text-gray-700 font-semibold"
          >
            Atrás
          </button>
        ) : (
          <div className="flex-1" />
        )}
        {step < 3 ? (
          <button
            type="button"
            onClick={() => setStep(step + 1)}
            disabled={!canNext}
            className="flex-1 rounded-lg bg-[#1A3A5C] py-3 text-white font-semibold disabled:opacity-50"
          >
            Siguiente
          </button>
        ) : (
          <button
            type="submit"
            disabled={loading || !confirmed}
            className="flex-1 rounded-lg bg-[#E74C3C] py-3 text-white font-semibold disabled:opacity-50"
          >
            {loading ? "Enviando..." : "🛡️ Enviar reporte anónimo"}
          </button>
        )}
      </div>
    </form>
  );
}
