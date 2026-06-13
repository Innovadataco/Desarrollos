import { test, expect } from "@playwright/test";

test.describe("Smoke tests", () => {
  test("la página carga y muestra el formulario de búsqueda", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("Buscar contacto")).toBeVisible();
    await expect(page.getByPlaceholder(/@usuario, email o URL/i)).toBeVisible();
    await expect(page.locator("form").getByRole("button", { name: /Buscar/i })).toBeVisible();
  });

  test("se puede navegar entre las tres pestañas", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /^Reportar$/i }).click();
    await expect(page.getByText(/Reportar anónimo/i)).toBeVisible();

    await page.getByRole("button", { name: /^Recursos$/i }).click();
    await expect(page.getByRole("heading", { name: /Recursos de apoyo/i })).toBeVisible();

    await page.getByRole("button", { name: /^Buscar$/i }).click();
    await expect(page.getByText("Buscar contacto")).toBeVisible();
  });
});
