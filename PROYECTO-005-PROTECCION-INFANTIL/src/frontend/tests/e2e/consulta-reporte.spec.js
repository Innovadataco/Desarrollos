import { test, expect } from "@playwright/test";

test.describe("Flujo consulta + reporte", () => {
  test("consulta un identificador sin reportes, lo reporta y muestra confirmación", async ({ page }) => {
    const uniqueId = `@e2e_${Date.now()}`;

    await page.goto("/");
    await page.getByRole("textbox", { name: /número o identificador/i }).fill(uniqueId);
    await page.getByRole("button", { name: /Buscar/i }).click();

    await expect(page.getByText("Sin reportes previos")).toBeVisible();
    await expect(page.getByText("Buscar contacto")).toBeVisible();

    await page.getByRole("button", { name: /Reportar este/i }).click();

    await expect(page.getByText(/Paso 2: Identificador y descripción/i)).toBeVisible();
    await expect(page.locator("#identifier")).toHaveValue(uniqueId);

    await page.getByLabel(/¿Qué te pareció sospechoso/i).fill(
      "Este usuario contactó a un menor de forma inapropiada solicitando fotos."
    );

    await page.getByRole("button", { name: /Siguiente/i }).click();
    await expect(page.getByText(/Paso 3: Evidencia/i)).toBeVisible();

    await page.getByRole("button", { name: /Siguiente/i }).click();
    await expect(page.getByText(/Paso 4: Revisa y envía/i)).toBeVisible();

    await page.getByRole("checkbox", { name: /Confirmo que esta información es veraz/i }).check();
    await page.getByRole("button", { name: /Enviar reporte anónimo/i }).click();

    await expect(page.getByText(/Protección activada/i)).toBeVisible();
    await expect(page.getByTestId("report-hash")).toBeVisible();
  });
});
