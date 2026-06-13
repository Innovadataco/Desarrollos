import { useEffect, useState } from "react";
import { API_URL } from "../api";

const TYPES = [
  {
    id: "phone",
    label: "📱 Celular",
    category: "contacto_inapropiado",
    placeholder: "+57 300 123 4567",
    inputMode: "tel",
    identifierLabel: "Número de celular",
    help: "Incluye el código de país.",
    validate: (v) => /^\+?\d[\d\s\-()]{6,20}$/.test(v.trim()),
  },
  {
    id: "social",
    label: "💬 Red social",
    category: "contacto_inapropiado",
    placeholder: "@usuario",
    inputMode: "text",
    identifierLabel: "Usuario / @usuario",
    help: "Ej: @usuario_malo o el enlace al perfil.",
    validate: (v) => v.trim().length >= 2,
  },
  {
    id: "email",
    label: "📧 Email",
    category: "contacto_inapropiado",
    placeholder: "correo@ejemplo.com",
    inputMode: "email",
    identifierLabel: "Correo electrónico",
    help: "Dirección de correo usada para contactar.",
    validate: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()),
  },
  {
    id: "url",
    label: "🌐 Sitio web",
    category: "solicitud_material",
    placeholder: "https://sitio-sospechoso.com/perfil",
    inputMode: "url",
    identifierLabel: "URL del sitio o perfil",
    help: "Pega el enlace completo.",
    validate: (v) => /^https?:\/\/.+/i.test(v.trim()),
  },
  {
    id: "content",
    label: "📸 Contenido inapropiado",
    category: "solicitud_material",
    placeholder: "Describe o adjunta el contenido",
    inputMode: "text",
    identifierLabel: "Descripción breve del contenido",
    help: "Puedes dejar esto y contar más abajo.",
    validate: () => true,
  },
  {
    id: "other",
    label: "📝 Otro",
    category: "otro",
    placeholder: "Escribe el identificador",
    inputMode: "text",
    identifierLabel: "Identificador",
    help: "Cualquier otro dato que identifique el contacto.",
    validate: (v) => v.trim().length >= 1,
  },
];

const ALLOWED_TYPES = [
  "image/png",
  "image/jpeg",
  "image/jpg",
  "image/gif",
  "image/webp",
  "application/pdf",
  "text/plain",
  "audio/mpeg",
  "audio/wav",
  "audio/webm",
  "video/mp4",
  "video/webm",
];

const MAX_SIZE_MB = 10;

const CATEGORY_OPTIONS = [
  { code: "CAT-01", label: "Contacto inapropiado" },
  { code: "CAT-02", label: "Solicitud de material sexual" },
  { code: "CAT-03", label: "Grooming / Engaño" },
  { code: "CAT-04", label: "Cita en persona" },
  { code: "CAT-05", label: "Extorsión" },
  { code: "CAT-06", label: "Desconocido / Otro" },
];

export default function ReportForm({ prefillIdentifier = "" }) {
  const [step, setStep] = useState(1);
  const [type, setType] = useState("");
  const [identifier, setIdentifier] = useState(prefillIdentifier);
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [evidenceFile, setEvidenceFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [confirmed, setConfirmed] = useState(false);
  const [honeypot, setHoneypot] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIdentifier(prefillIdentifier);
  }, [prefillIdentifier]);

  const selected = TYPES.find((t) => t.id === type);

  useEffect(() => {
    if (selected?.category) {
      const code =
        {
          contacto_inapropiado: "CAT-01",
          solicitud_material: "CAT-02",
          grooming: "CAT-03",
          cita_persona: "CAT-04",
          extorsion: "CAT-05",
        }[selected.category] || "CAT-06";
      setCategory(code);
    }
  }, [selected]);

  const isIdentifierValid = selected ? selected.validate(identifier) : identifier.trim().length >= 1;
  const canNext =
    (step === 1 && type) ||
    (step === 2 && isIdentifierValid && description.trim().length >= 10) ||
    step === 3;

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setError(null);
    if (!file) {
      setEvidenceFile(null);
      setFilePreview(null);
      return;
    }
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError("Formato no permitido. Usa PNG, JPG, PDF, MP4, MP3 o TXT.");
      e.target.value = "";
      return;
    }
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`El archivo excede ${MAX_SIZE_MB} MB.`);
      e.target.value = "";
      return;
    }
    setEvidenceFile(file);
    if (file.type.startsWith("image/")) {
      setFilePreview(URL.createObjectURL(file));
    } else {
      setFilePreview(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!confirmed) return;
    setLoading(true);
    setError(null);

    const payload = {
      reported_identifier: identifier,
      description,
      category: category || "CAT-06",
      honeypot,
    };

    try {
      const res = await fetch(`${API_URL}/api/v1/reportes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) {
        handleError(res.status, data);
        setLoading(false);
        return;
      }

      // Subir archivo si existe
      if (evidenceFile) {
        const formData = new FormData();
        formData.append("file", evidenceFile);
        const uploadRes = await fetch(
          `${API_URL}/api/v1/reportes/${data.report_hash}/evidence`,
          { method: "POST", body: formData }
        );
        if (!uploadRes.ok) {
          const uploadData = await uploadRes.json();
          setError(
            `Reporte guardado, pero no se pudo adjuntar el archivo: ${uploadData.detail || ""}`
          );
        }
      }

      setResult(data);
    } catch {
      setError("Error de conexión. Verifica tu red e intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  const handleError = (status, data) => {
    if (status === 429) {
      setError(data.detail || "Has alcanzado el límite. Intenta más tarde.");
    } else if (status === 422) {
      setError("Verifica los campos e intenta de nuevo.");
    } else {
      setError(data.detail || "No se pudo enviar el reporte.");
    }
  };

  const reset = () => {
    setStep(1);
    setType("");
    setIdentifier("");
    setDescription("");
    setCategory("");
    setEvidenceFile(null);
    setFilePreview(null);
    setConfirmed(false);
    setHoneypot("");
    setCopied(false);
    setResult(null);
    setError(null);
  };

  const copyHash = async () => {
    if (!result?.report_hash) return;
    try {
      await navigator.clipboard.writeText(result.report_hash);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setError("No se pudo copiar el código. Escríbelo manualmente.");
    }
  };

  if (result) {
    return (
      <div className="text-center space-y-5 rounded-xl border border-green-200 bg-green-50 p-6 animate-fade-in">
        <div className="text-5xl">🛡️</div>
        <h2 className="text-xl font-bold text-green-800">Protección activada</h2>
        <p className="text-green-800">
          Hiciste lo correcto. Tu reporte fue recibido de forma anónima.
        </p>
        <div className="rounded-lg bg-white p-4 text-left">
          <p className="text-sm text-gray-600">Guarda este código:</p>
          <p
            data-testid="report-hash"
            className="break-all font-mono text-sm font-semibold text-gray-900"
          >
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

      {/* Honeypot oculto: los bots lo llenan, los humanos no. */}
      <input
        type="text"
        name="website"
        value={honeypot}
        onChange={(e) => setHoneypot(e.target.value)}
        tabIndex={-1}
        autoComplete="off"
        aria-hidden="true"
        className="absolute opacity-0 pointer-events-none h-0 w-0"
      />

      <div className="flex justify-center gap-2" aria-label="Progreso">
        {[1, 2, 3, 4].map((s) => (
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
                onClick={() => {
                  setType(t.id);
                  setIdentifier("");
                }}
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

      {step === 2 && selected && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 2: Identificador y descripción</p>
          <div>
            <label htmlFor="identifier" className="block text-sm font-medium text-gray-700">
              {selected.identifierLabel}
            </label>
            <input
              id="identifier"
              type={selected.id === "email" ? "email" : "text"}
              inputMode={selected.inputMode}
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder={selected.placeholder}
              className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
            />
            <p className="text-xs text-gray-500 mt-1">{selected.help}</p>
            {identifier && !isIdentifierValid && (
              <p className="text-xs text-red-600 mt-1">Revisa el formato.</p>
            )}
          </div>
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700">
              ¿Qué te pareció sospechoso?
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe lo que pasó con el mayor detalle posible..."
              rows={4}
              minLength={10}
              className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9]"
              required
            />
          </div>
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700">
              Categoría del incidente
            </label>
            <select
              id="category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="mt-1 w-full rounded-lg border border-gray-300 px-4 py-3 text-base focus:outline-none focus:ring-2 focus:ring-[#4A90D9] bg-white"
              required
            >
              {CATEGORY_OPTIONS.map((opt) => (
                <option key={opt.code} value={opt.code}>
                  {opt.code} — {opt.label}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Selecciona la opción que mejor describa lo ocurrido.
            </p>
          </div>
        </div>
      )}

      {step === 3 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 3: Evidencia (opcional)</p>
          <div>
            <label htmlFor="evidence" className="block text-sm font-medium text-gray-700">
              Adjuntar evidencia
            </label>
            <input
              id="evidence"
              type="file"
              accept=".png,.jpg,.jpeg,.gif,.webp,.pdf,.txt,.mp3,.wav,.mp4,.webm"
              onChange={handleFileChange}
              className="mt-1 block w-full text-sm text-gray-700 file:mr-4 file:rounded-lg file:border-0 file:bg-[#1A3A5C] file:px-4 file:py-2 file:text-white file:font-semibold hover:file:bg-[#4A90D9]"
            />
            <p className="text-xs text-gray-500 mt-1">
              Formatos: PNG, JPG, PDF, MP4, MP3, TXT. Máx. {MAX_SIZE_MB} MB.
            </p>
            {evidenceFile && (
              <div className="mt-3 rounded-lg border border-gray-200 bg-gray-50 p-3">
                <p className="text-sm font-medium text-gray-800">{evidenceFile.name}</p>
                <p className="text-xs text-gray-500">
                  {(evidenceFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
                {filePreview && (
                  <img
                    src={filePreview}
                    alt="Vista previa"
                    className="mt-2 max-h-40 rounded border border-gray-300"
                  />
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {step === 4 && (
        <div className="space-y-4">
          <p className="font-semibold text-gray-800">Paso 4: Revisa y envía</p>
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 space-y-3 text-sm text-gray-800">
            <div>
              <span className="font-semibold">Tipo:</span> {selected?.label || type}
            </div>
            <div>
              <span className="font-semibold">Categoría:</span>{" "}
              {CATEGORY_OPTIONS.find((c) => c.code === category)?.label || category}
            </div>
            <div>
              <span className="font-semibold">Identificador:</span>{" "}
              <span className="font-mono">{identifier}</span>
            </div>
            <div>
              <span className="font-semibold">Descripción:</span>
              <p className="mt-1 whitespace-pre-wrap">{description}</p>
            </div>
            {evidenceFile && (
              <div>
                <span className="font-semibold">Evidencia:</span> {evidenceFile.name} (
                {(evidenceFile.size / 1024 / 1024).toFixed(2)} MB)
              </div>
            )}
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
        {step < 4 ? (
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
