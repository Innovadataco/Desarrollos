import { test, expect } from "@playwright/test";

test("el usuario puede enviar un reporte anónimo y recibir un hash", async ({
  page,
}) => {
  await page.goto("/");

  await expect(page.locator("h1")).toContainText(
    "Protección Infantil Comunitaria"
  );

  await page
    .getByLabel("Identificador reportado")
    .fill("@usuario_sospechoso");
  await page
    .getByLabel("Descripción")
    .fill("Recibí mensajes inapropiados de esta cuenta");

  await page.getByRole("button", { name: "Enviar reporte anónimo" }).click();

  await expect(page.locator("text=Reporte enviado con éxito")).toBeVisible({
    timeout: 10000,
  });

  const hashLocator = page.locator("div.font-mono");
  await expect(hashLocator).toBeVisible();
  const hash = await hashLocator.textContent();
  expect(hash).toMatch(/^[a-f0-9]{64}$/);
});

test("el sistema no permite enviar sin campos requeridos", async ({ page }) => {
  await page.goto("/");

  await page.getByRole("button", { name: "Enviar reporte anónimo" }).click();

  // El navegador bloquea el submit por required; verificamos que seguimos en el formulario
  await expect(page.getByLabel("Identificador reportado")).toBeVisible();
});
