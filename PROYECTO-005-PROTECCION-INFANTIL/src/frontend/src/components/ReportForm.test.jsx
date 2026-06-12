import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ReportForm from "./ReportForm";

const API_URL = "http://localhost:8000";

describe("ReportForm", () => {
  beforeEach(() => {
    import.meta.env.VITE_API_URL = API_URL;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renderiza el formulario con campos requeridos", () => {
    render(<ReportForm />);
    expect(screen.getByLabelText(/Identificador reportado/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Descripción/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /Enviar reporte anónimo/i })
    ).toBeInTheDocument();
  });

  it("muestra error si falla la conexión con el servidor", async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error());

    render(<ReportForm />);
    fireEvent.change(screen.getByLabelText(/Identificador reportado/i), {
      target: { value: "@sospechoso" },
    });
    fireEvent.change(screen.getByLabelText(/Descripción/i), {
      target: { value: "Descripción del incidente" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Enviar reporte anónimo/i }));

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
    fireEvent.change(screen.getByLabelText(/Identificador reportado/i), {
      target: { value: "@sospechoso" },
    });
    fireEvent.change(screen.getByLabelText(/Descripción/i), {
      target: { value: "Descripción del incidente" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Enviar reporte anónimo/i }));

    await waitFor(() => {
      expect(screen.getByText(/Reporte enviado con éxito/i)).toBeInTheDocument();
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
    fireEvent.change(screen.getByLabelText(/Identificador reportado/i), {
      target: { value: "@sospechoso" },
    });
    fireEvent.change(screen.getByLabelText(/Descripción/i), {
      target: { value: "Descripción del incidente" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Enviar reporte anónimo/i }));

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
    fireEvent.change(screen.getByLabelText(/Identificador reportado/i), {
      target: { value: "@sospechoso" },
    });
    fireEvent.change(screen.getByLabelText(/Descripción/i), {
      target: { value: "Descripción del incidente" },
    });
    fireEvent.click(screen.getByRole("button", { name: /Enviar reporte anónimo/i }));

    await waitFor(() => {
      expect(screen.getByText(/campo inválido/i)).toBeInTheDocument();
    });
  });
});
