import { test, expect } from "@playwright/test";

test.use({
  launchOptions: { slowMo: 1500 },
  viewport: { width: 390, height: 844 },
});

test("recorrido visual de todas las tasks del Módulo 002", async ({ page }) => {
  const greenId = `@verde_${Date.now()}`;
  const reportId = `@reporte_${Date.now()}`;

  // 1. Página principal como buscador
  await page.context().grantPermissions(["clipboard-read", "clipboard-write"]);
  await page.goto("/");
  await page.evaluate(() => {
    navigator.share = undefined;
  });
  await expect(page.getByText("Buscar contacto")).toBeVisible();
  await expect(page.getByPlaceholder(/Escribe un nombre o identificador/i)).toBeVisible();

  // 2. Placeholder dinámico y detección de tipo
  const input = page.getByRole("textbox", { name: /número o identificador/i });
  await input.fill(greenId);
  await expect(page.getByText("💬 Red social")).toBeVisible();
  await expect(input).toHaveAttribute("placeholder", "@usuario");

  // 3. Card verde (sin reportes)
  await page.getByRole("button", { name: /Buscar/i }).click();
  await expect(page.getByText("🟢")).toBeVisible();
  await expect(page.getByText("Sin reportes previos")).toBeVisible();

  // 4. Compartir resultado (URL sin identificador)
  await page.getByRole("button", { name: /Compartir resultado/i }).click();
  await expect(page.getByText(/Enlace copiado/i)).toBeVisible();

  // 5. Reportar este identificador → pre-llena Módulo 001
  await page.getByRole("button", { name: /Reportar este/i }).click();
  await expect(page.getByText(/Paso 2: Identificador y descripción/i)).toBeVisible();
  await expect(page.locator("#identifier")).toHaveValue(greenId);

  // Cambiamos el identificador para evitar el cache verde y mostrar el detalle luego
  await page.locator("#identifier").fill(reportId);

  await page.getByLabel(/¿Qué te pareció sospechoso/i).fill(
    "Este perfil contactó a un menor de forma inapropiada."
  );
  await page.getByRole("button", { name: /Siguiente/i }).click();
  await page.getByRole("button", { name: /Siguiente/i }).click();
  await page.getByRole("checkbox").check();
  await page.getByRole("button", { name: /Enviar reporte anónimo/i }).click();

  await expect(page.getByText(/Protección activada/i)).toBeVisible();

  // 6. Volver a consultar: card con detalle
  await page.getByRole("link", { name: /^Buscar$/i }).click();
  await input.fill(reportId);
  await page.getByRole("button", { name: /Buscar/i }).click();

  // Puede ser amarillo o rojo según el score de análisis
  await expect(page.getByText(/Precaución|Riesgo alto/)).toBeVisible();
  await expect(page.getByText("reportes", { exact: true })).toBeVisible();
  await expect(page.getByText(/Categorías reportadas/i)).toBeVisible();
  await expect(page.getByText(/Línea de tiempo/i)).toBeVisible();

  // 7. Alertarme si cambia
  await page.getByPlaceholder("tu@email.com").fill("demo@ejemplo.com");
  await page.getByRole("button", { name: /Activar alerta Premium/i }).click();
  await expect(page.getByText(/Alerta activada/i)).toBeVisible();
});
