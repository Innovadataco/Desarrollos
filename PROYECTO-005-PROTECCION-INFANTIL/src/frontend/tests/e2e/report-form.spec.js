import { test, expect } from "@playwright/test";

test("el wizard de reporte avanza por los 3 pasos", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /^Reportar$/i }).click();

  await expect(page.getByText(/Reportar anónimo/i)).toBeVisible();
  await expect(page.getByText(/Paso 1/i)).toBeVisible();

  // Paso 1: seleccionar email
  await page.getByRole("button", { name: /Email/i }).click();
  await page.getByRole("button", { name: /Siguiente/i }).click();

  // Paso 2: email y descripción
  await expect(page.getByText(/Paso 2/i)).toBeVisible();
  await page.getByLabel(/Correo electrónico/i).fill("abuso@example.com");
  await page.getByLabel(/¿Qué te pareció sospechoso?/i).fill(
    "Recibí mensajes inapropiados desde esta dirección"
  );
  await page.getByRole("button", { name: /Siguiente/i }).click();

  // Paso 3: adjuntar y enviar
  await expect(page.getByText(/Paso 3/i)).toBeVisible();
  await expect(page.getByRole("button", { name: /Enviar reporte/i })).toBeDisabled();

  await page.getByRole("checkbox").check();
  await expect(page.getByRole("button", { name: /Enviar reporte/i })).toBeEnabled();
});

test("se puede reportar un email y adjuntar una imagen", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /^Reportar$/i }).click();

  await page.getByRole("button", { name: /Email/i }).click();
  await page.getByRole("button", { name: /Siguiente/i }).click();

  await page.getByLabel(/Correo electrónico/i).fill("adjunto@test.org");
  await page.getByLabel(/¿Qué te pareció sospechoso?/i).fill(
    "Adjunto captura de pantalla como evidencia"
  );
  await page.getByRole("button", { name: /Siguiente/i }).click();

  await page.getByLabel(/Adjuntar evidencia/i).setInputFiles({
    name: "captura.png",
    mimeType: "image/png",
    buffer: Buffer.from("fake-image-content"),
  });

  await page.getByRole("checkbox").check();

  const [response] = await Promise.all([
    page.waitForResponse((resp) => resp.url().includes("/api/v1/reportes") && resp.request().method() === "POST"),
    page.getByRole("button", { name: /Enviar reporte/i }).click(),
  ]);

  expect(response.status()).toBe(201);
  await expect(page.getByText(/Protección activada/i)).toBeVisible({ timeout: 10000 });
});
