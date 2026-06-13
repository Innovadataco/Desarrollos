import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import SearchView from "./SearchView";

describe("SearchView", () => {
  let storage = {};

  beforeEach(() => {
    storage = {};
    Object.defineProperty(global, "localStorage", {
      value: {
        getItem: (key) => storage[key] || null,
        setItem: (key, value) => { storage[key] = value; },
        clear: () => { storage = {}; },
      },
      writable: true,
    });
    global.fetch = vi.fn();
    Object.assign(navigator, {
      clipboard: { writeText: vi.fn(() => Promise.resolve()) },
      share: undefined,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  function setup() {
    return render(
      <BrowserRouter>
        <SearchView />
      </BrowserRouter>
    );
  }

  it("muestra el placeholder según el tipo de identificador", () => {
    setup();
    const input = screen.getByRole("textbox", { name: /número o identificador/i });
    expect(input).toHaveAttribute("placeholder", "Escribe un nombre o identificador");

    fireEvent.change(input, { target: { value: "@usuario" } });
    expect(input).toHaveAttribute("placeholder", "@usuario");
  });

  it("renderiza la card de semáforo con emoji y animación", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        identifier_hash: "abc123",
        semaforo: "rojo",
        report_count: 5,
        score_average: 7.5,
        score_max: 9,
        first_reported_at: "2024-01-01T00:00:00Z",
        last_reported_at: "2024-06-01T00:00:00Z",
        categories: ["grooming", "contacto directo"],
        cities_count: 3,
        countries_count: 2,
        is_network: true,
        message: "Este identificador tiene múltiples reportes.",
        report_button: true,
      }),
    });

    const { container } = setup();
    const input = screen.getByRole("textbox", { name: /número o identificador/i });
    fireEvent.change(input, { target: { value: "@delincuente" } });
    fireEvent.click(screen.getByRole("button", { name: /buscar/i }));

    await waitFor(() =>
      expect(screen.getByText("Riesgo alto")).toBeInTheDocument()
    );

    expect(container.querySelector(".animate-fade-in")).toBeInTheDocument();
    expect(screen.getByText("🔴")).toBeInTheDocument();
    expect(screen.getByText(/múltiples reportes/i)).toBeInTheDocument();
    expect(screen.getByText(/Posible red de contacto/i)).toBeInTheDocument();
  });

  it("comparte la URL sin incluir el identificador buscado", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        identifier_hash: "abc123",
        semaforo: "verde",
        report_count: 0,
        message: "Sin reportes.",
        report_button: true,
      }),
    });

    setup();
    const input = screen.getByRole("textbox", { name: /número o identificador/i });
    fireEvent.change(input, { target: { value: "+573001234567" } });
    fireEvent.click(screen.getByRole("button", { name: /buscar/i }));

    await waitFor(() =>
      expect(screen.getByText("Sin reportes previos")).toBeInTheDocument()
    );

    fireEvent.click(screen.getByRole("button", { name: /compartir resultado/i }));

    await waitFor(() => {
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith(
        expect.stringContaining("?ref=consulta")
      );
    });

    const written = navigator.clipboard.writeText.mock.calls[0][0];
    expect(written).not.toContain("+573001234567");
    expect(written).not.toContain("3001234567");
  });

  it("permite activar una alerta por email y la guarda localmente", async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        identifier_hash: "hash-alert",
        semaforo: "rojo",
        report_count: 2,
        score_average: 6.5,
        score_max: 8,
        first_reported_at: "2024-01-01T00:00:00Z",
        last_reported_at: "2024-06-01T00:00:00Z",
        categories: ["grooming"],
        cities_count: 1,
        countries_count: 1,
        is_network: false,
        message: "Reportes previos.",
        report_button: true,
      }),
    });

    setup();
    const input = screen.getByRole("textbox", { name: /número o identificador/i });
    fireEvent.change(input, { target: { value: "@alertame" } });
    fireEvent.click(screen.getByRole("button", { name: /buscar/i }));

    await waitFor(() =>
      expect(screen.getByText("Riesgo alto")).toBeInTheDocument()
    );

    const emailInput = screen.getByPlaceholderText("tu@email.com");
    fireEvent.change(emailInput, { target: { value: "usuario@ejemplo.com" } });
    fireEvent.click(screen.getByRole("button", { name: /activar alerta premium/i }));

    await waitFor(() =>
      expect(screen.getByText(/Alerta activada/i)).toBeInTheDocument()
    );

    const stored = JSON.parse(localStorage.getItem("alerts"));
    expect(stored["hash-alert"].email).toBe("usuario@ejemplo.com");
  });
});
