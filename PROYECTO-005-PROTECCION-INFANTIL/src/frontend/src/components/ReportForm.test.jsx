import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ReportForm from './ReportForm'

describe('ReportForm', () => {
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the form fields', () => {
    render(<ReportForm />)
    expect(screen.getByLabelText(/identificador reportado/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/descripción/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /enviar reporte anónimo/i })).toBeInTheDocument()
  })

  it('shows validation error when fields are empty', async () => {
    render(<ReportForm />)
    const button = screen.getByRole('button', { name: /enviar reporte anónimo/i })
    await userEvent.click(button)
    expect(await screen.findByRole('alert')).toHaveTextContent(/obligatorio/i)
  })

  it('submits the report and displays the returned hash', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ report_hash: 'abcd1234'.repeat(8), reported_at: '2026-01-01T00:00:00Z' }),
    })

    render(<ReportForm />)
    await userEvent.type(screen.getByLabelText(/identificador reportado/i), '+573001234567')
    await userEvent.type(screen.getByLabelText(/descripción/i), 'Mensajes inapropiados')
    await userEvent.click(screen.getByRole('button', { name: /enviar reporte anónimo/i }))

    await waitFor(() => {
      expect(screen.getByText(/reporte recibido/i)).toBeInTheDocument()
    })
    expect(screen.getByText('abcd1234'.repeat(8))).toBeInTheDocument()
  })

  it('displays server error when submission fails', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 429,
      json: async () => ({ detail: 'Has alcanzado el límite de reportes.' }),
    })

    render(<ReportForm />)
    await userEvent.type(screen.getByLabelText(/identificador reportado/i), '+573001234567')
    await userEvent.type(screen.getByLabelText(/descripción/i), 'Mensajes inapropiados')
    await userEvent.click(screen.getByRole('button', { name: /enviar reporte anónimo/i }))

    expect(await screen.findByRole('alert')).toHaveTextContent(/límite/i)
  })
})
