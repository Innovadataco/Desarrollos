import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ReportForm() {
  const [form, setForm] = useState({
    reported_identifier: "",
    description: "",
    evidence_type: "",
    evidence_content: "",
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const payload = {
      reported_identifier: form.reported_identifier,
      description: form.description,
      evidence:
        form.evidence_type && form.evidence_content
          ? { type: form.evidence_type, content: form.evidence_content }
          : null,
    };

    try {
      const res = await fetch(`${API_URL}/api/reportes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        let message = data.detail || `Error ${res.status}`;
        if (res.status === 422 && Array.isArray(data.detail)) {
          const field = data.detail[0]?.loc?.slice(-1)[0] || "campo";
          message = `Campo inválido: ${field}`;
        }
        if (res.status === 429) {
          message = "Límite alcanzado. Intenta más tarde.";
        }
        throw new Error(message);
      }

      const data = await res.json();
      setResult(data);
      setForm({
        reported_identifier: "",
        description: "",
        evidence_type: "",
        evidence_content: "",
      });
    } catch (err) {
      setError(err.message || "Error de conexión con el servidor");
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <div className="text-5xl mb-4">✅</div>
        <h2 className="text-xl font-semibold text-green-700 mb-2">
          Reporte enviado con éxito
        </h2>
        <p className="text-sm text-gray-600 mb-4">
          Guarda este hash de confirmación. Es tu única prueba de envío.
        </p>
        <div className="bg-gray-100 rounded p-3 font-mono text-sm break-all mb-4">
          {result.report_hash}
        </div>
        <button
          onClick={() => setResult(null)}
          className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded transition"
        >
          Enviar otro reporte
        </button>
      </div>
    );
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-lg shadow-md p-6 space-y-4"
    >
      {error && (
        <div className="bg-red-50 text-red-700 text-sm p-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="reported_identifier" className="block text-sm font-medium text-gray-700 mb-1">
          Identificador reportado
        </label>
        <input
          id="reported_identifier"
          name="reported_identifier"
          value={form.reported_identifier}
          onChange={handleChange}
          required
          minLength={3}
          maxLength={100}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="Ej: usuario sospechoso, URL, etc."
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Descripción
        </label>
        <textarea
          id="description"
          name="description"
          value={form.description}
          onChange={handleChange}
          required
          minLength={10}
          maxLength={2000}
          rows={4}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="Describe lo ocurrido con el mayor detalle posible..."
        />
      </div>

      <div>
        <label htmlFor="evidence_type" className="block text-sm font-medium text-gray-700 mb-1">
          Tipo de evidencia (opcional)
        </label>
        <select
          id="evidence_type"
          name="evidence_type"
          value={form.evidence_type}
          onChange={handleChange}
          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">Sin evidencia</option>
          <option value="text">Texto / Captura</option>
          <option value="image">Imagen / URL</option>
        </select>
      </div>

      {form.evidence_type && (
        <div>
          <label htmlFor="evidence_content" className="block text-sm font-medium text-gray-700 mb-1">
            Contenido de evidencia
          </label>
          <textarea
            id="evidence_content"
            name="evidence_content"
            value={form.evidence_content}
            onChange={handleChange}
            required={!!form.evidence_type}
            maxLength={10000}
            rows={3}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            placeholder="Pega el texto, URL o descripción de la imagen..."
          />
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-primary hover:bg-primary-dark text-white font-medium py-2 px-4 rounded transition disabled:opacity-50"
      >
        {loading ? "Enviando..." : "Enviar reporte anónimo"}
      </button>
    </form>
  );
}