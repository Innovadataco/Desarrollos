import { test, expect } from "@playwright/test";

const ADMIN_PASSWORD = process.env.ADMIN_ROOT_PASSWORD || "CHANGEME_ROOT_PASSWORD_2026";

function randomIp() {
  return `10.${Math.floor(Math.random() * 256)}.${Math.floor(
    Math.random() * 256
  )}.${Math.floor(Math.random() * 254) + 1}`;
}

async function seedReports(request) {
  // Genera un identificador único para evitar colisiones entre ejecuciones.
  const ident = `red-test-${Date.now()}@example.com`;
  // IP diferente por ejecución para evitar rate limits entre workers.
  const clientIp = randomIp();
  const reportHeaders = {
    "X-Forwarded-For": clientIp,
    "X-Client-City": "Bogotá",
    "X-Client-Country": "CO",
  };

  // Reportes desde 3 ciudades / 2 países para activar la red organizada.
  for (const [city, country] of [
    ["Bogotá", "CO"],
    ["Medellín", "CO"],
    ["Ciudad de México", "MX"],
  ]) {
    const resp = await request.post("/api/v1/reportes", {
      headers: {
        ...reportHeaders,
        "X-Client-City": city,
        "X-Client-Country": country,
      },
      data: {
        reported_identifier: ident,
        description:
          "Este contacto ha solicitado material sexual y coordina citas con menores en varias ciudades.",
        category: "CAT-03",
        consent_location: true,
      },
    });
    expect(resp.status()).toBe(201);
  }

  // Un perfil adicional que no es red.
  const single = await request.post("/api/v1/reportes", {
    headers: reportHeaders,
    data: {
      reported_identifier: `single-${Date.now()}@example.com`,
      description: "Contacto inapropiado reportado una sola vez.",
      category: "CAT-01",
      consent_location: true,
    },
  });
  expect(single.status()).toBe(201);

  return ident;
}

test("admin: inicia sesión, lista perfiles y detecta redes organizadas", async ({
  page,
  request,
}) => {
  await seedReports(request);

  await page.goto("/admin/login");
  await page.getByLabel(/Usuario/i).fill("root");
  await page.getByLabel(/Contraseña/i).fill(ADMIN_PASSWORD);
  await page.getByRole("button", { name: /Ingresar/i }).click();

  await expect(page.getByRole("heading", { name: /Perfiles de contacto/i })).toBeVisible();
  // La base de datos compartida puede tener otros perfiles; verificamos que haya al menos 2.
  const profileRows = await page.locator("table tbody tr").count();
  expect(profileRows).toBeGreaterThanOrEqual(2);
  await expect(
    page.locator("table tbody tr").filter({ hasText: "⚠️ Sí" }).first()
  ).toBeVisible();

  await page.getByRole("link", { name: /Ver redes/i }).click();
  await expect(page.getByRole("heading", { name: /Redes organizadas/i })).toBeVisible();
  await expect(page.locator("text=⚠️ Red").first()).toBeVisible();
});
