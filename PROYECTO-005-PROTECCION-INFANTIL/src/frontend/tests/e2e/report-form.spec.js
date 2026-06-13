import { test, expect } from "@playwright/test";

test("el wizard de reporte avanza por los 3 pasos", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /^Reportar$/i }).click();

  await expect(page.getByText(/Reportar anónimo/i)).toBeVisible();
  await expect(page.getByText(/Paso 1/i)).toBeVisible();

  // Paso 1
  await page.getByRole("button", { name: /Red social/i }).click();
  await page.getByRole("button", { name: /Siguiente/i }).click();

  // Paso 2
  await expect(page.getByText(/Paso 2/i)).toBeVisible();
  await page.getByPlaceholder(/\+57 300 123 4567/i).fill("@usuario_sospechoso");
  await page.getByPlaceholder(/Describe lo que pasó/i).fill(
    "Recibí mensajes inapropiados de esta cuenta"
  );
  await page.getByRole("button", { name: /Siguiente/i }).click();

  // Paso 3
  await expect(page.getByText(/Paso 3/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /Enviar reporte/i })).toBeDisabled();

  await page.getByRole("checkbox").check();
  await expect(page.getByRole("button", { name: /Enviar reporte/i })).toBeEnabled();
});
