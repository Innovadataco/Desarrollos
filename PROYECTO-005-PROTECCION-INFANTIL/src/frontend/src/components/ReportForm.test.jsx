import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ReportForm from "./ReportForm";

const API_URL = "http://localhost:8000";

async function fillAndSubmit() {
  // Step 1: select type
  fireEvent.click(screen.getByText(/Celular/i));
  fireEvent.click(screen.getByRole("button", { name: /Siguiente/i }));
  // Step 2: fill identifier and description
  fireEvent.change(screen.getByLabelText(/Número de celular/i), {
    target: { value: "+573001234567" },
  });
  fireEvent.change(screen.getByLabelText(/¿Qué te pareció sospechoso?/i), {
    target: { value: "Descripción del incidente suficiente" },
  });
  fireEvent.click(screen.getByRole("button", { name: /Siguiente/i }));
  // Step 3: confirm and submit
  fireEvent.click(screen.getByLabelText(/Confirmo que esta información es veraz/i));
  fireEvent.click(screen.getByRole("button", { name: /Enviar reporte anónimo/i }));
}

describe("ReportForm", () => {
  beforeEach(() => {
    import.meta.env.VITE_API_URL = API_URL;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renderiza el wizard inicial en el paso 1", () => {
    render(<ReportForm />);
    expect(screen.getByText(/Paso 1/i)).toBeInTheDocument();
    expect(screen.getByText(/Celular/i)).toBeInTheDocument();
  });

  it("muestra error si falla la conexión con el servidor", async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error());

    render(<ReportForm />);
    await fillAndSubmit();

    await waitFor(() => {
      expect(screen.getByText(/Error de conexión/i)).toBeInTheDocument();
    });
  });

  it("muestra hash de confirmación tras envío exitoso", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        report_hash:
          "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef",
        reported_at: "2026-06-12T10:00:00Z",
      }),
    });

    render(<ReportForm />);
    await fillAndSubmit();

    await waitFor(() => {
      expect(screen.getByText(/Protección activada/i)).toBeInTheDocument();
    });
    expect(screen.getByText(/abcdefabcdef/i)).toBeInTheDocument();
  });

  it("muestra mensaje de límite alcanzado cuando el backend responde 429", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 429,
      json: async () => ({
        detail: "Has alcanzado el límite de reportes. Intenta más tarde.",
      }),
    });

    render(<ReportForm />);
    await fillAndSubmit();

    await waitFor(() => {
      expect(screen.getByText(/límite/i)).toBeInTheDocument();
    });
  });

  it("muestra mensaje de campo inválido cuando el backend responde 422", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({
        detail: [
          { loc: ["body", "description"], msg: "field required", type: "value_error.missing" },
        ],
      }),
    });

    render(<ReportForm />);
    await fillAndSubmit();

    await waitFor(() => {
      expect(screen.getByText(/Verifica los campos/i)).toBeInTheDocument();
    });
  });

  it("muestra error si el formato de teléfono es inválido", async () => {
    render(<ReportForm />);
    fireEvent.click(screen.getByText(/Celular/i));
    fireEvent.click(screen.getByRole("button", { name: /Siguiente/i }));
    fireEvent.change(screen.getByLabelText(/Número de celular/i), {
      target: { value: "no-es-numero" },
    });
    fireEvent.change(screen.getByLabelText(/¿Qué te pareció sospechoso?/i), {
      target: { value: "Descripción del incidente suficiente" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Siguiente/i }));
    expect(screen.getByText(/Revisa el formato/i)).toBeInTheDocument();
  });
});
