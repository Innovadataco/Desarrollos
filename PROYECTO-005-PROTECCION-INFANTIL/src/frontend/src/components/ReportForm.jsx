import { useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const EVIDENCE_TYPES = [
  { value: '', label: 'Sin evidencia' },
  { value: 'text', label: 'Texto' },
  { value: 'image', label: 'Imagen' },
]

export default function ReportForm() {
  const [identifier, setIdentifier] = useState('')
  const [description, setDescription] = useState('')
  const [evidenceType, setEvidenceType] = useState('')
  const [evidenceContent, setEvidenceContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const reset = () => {
    setIdentifier('')
    setDescription('')
    setEvidenceType('')
    setEvidenceContent('')
    setResult(null)
    setError(null)
  }

  const validate = () => {
    if (!identifier.trim()) return 'El identificador reportado es obligatorio.'
    if (!description.trim()) return 'La descripción es obligatoria.'
    if (evidenceType && !evidenceContent.trim()) {
      return 'Debes incluir el contenido de la evidencia.'
    }
    return null
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null)
    setResult(null)

    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }

    const payload = {
      reported_identifier: identifier.trim(),
      description: description.trim(),
    }
    if (evidenceType) {
      payload.evidence = {
        type: evidenceType,
        content: evidenceContent.trim(),
      }
    }

    setLoading(true)
    try {
      const response = await fetch(`${API_URL}/api/reportes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await response.json().catch(() => ({}))
      if (!response.ok) {
        throw new Error(data.detail || `Error ${response.status}`)
      }
      setResult(data)
    } catch (err) {
      setError(err.message || 'No se pudo enviar el reporte. Intenta más tarde.')
    } finally {
      setLoading(false)
    }
  }

  if (result) {
    return (
      <div className="rounded-lg bg-white p-6 shadow-md" role="status" aria-live="polite">
        <h2 className="text-lg font-semibold text-teal-800">Reporte recibido</h2>
        <p className="mt-2 text-sm text-slate-600">
          Guarda este código de forma segura. No lo usamos para rastrearte.
        </p>
        <div className="mt-4 break-all rounded bg-slate-100 p-3 font-mono text-sm text-slate-800">
          {result.report_hash}
        </div>
        <button
          onClick={reset}
          className="mt-6 w-full rounded-md bg-teal-700 px-4 py-2 text-white hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
        >
          Hacer otro reporte
        </button>
      </div>
    )
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-5 rounded-lg bg-white p-6 shadow-md"
      noValidate
    >
      <div>
        <label htmlFor="identifier" className="block text-sm font-medium text-slate-700">
          Identificador reportado
        </label>
        <input
          id="identifier"
          type="text"
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="Número telefónico, usuario o correo"
          className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
          required
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-slate-700">
          Descripción
        </label>
        <textarea
          id="description"
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe lo ocurrido"
          className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
          required
        />
      </div>

      <div>
        <label htmlFor="evidenceType" className="block text-sm font-medium text-slate-700">
          Tipo de evidencia (opcional)
        </label>
        <select
          id="evidenceType"
          value={evidenceType}
          onChange={(e) => setEvidenceType(e.target.value)}
          className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
        >
          {EVIDENCE_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

      {evidenceType && (
        <div>
          <label htmlFor="evidenceContent" className="block text-sm font-medium text-slate-700">
            Contenido de la evidencia
          </label>
          <textarea
            id="evidenceContent"
            rows={3}
            value={evidenceContent}
            onChange={(e) => setEvidenceContent(e.target.value)}
            placeholder={evidenceType === 'image' ? 'Describe o pega la imagen' : 'Texto de la evidencia'}
            className="mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
          />
        </div>
      )}

      {error && (
        <div className="rounded-md bg-red-50 p-3 text-sm text-red-700" role="alert">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full rounded-md bg-teal-700 px-4 py-2 text-sm font-medium text-white hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? 'Enviando...' : 'Enviar reporte anónimo'}
      </button>
    </form>
  )
}
