const RESOURCES = [
  {
    name: "CyberTipline",
    url: "https://www.cybertipline.org/",
    description: "Línea de reporte de explotación infantil en EE.UU.",
  },
  {
    name: "Missing Kids",
    url: "https://www.missingkids.org/ES",
    description: "Recursos de búsqueda y prevención.",
  },
  {
    name: "Internet Matters",
    url: "https://www.internetmatters.org/",
    description: "Guías para padres sobre seguridad digital.",
  },
  {
    name: "Línea 116 111 (Europa)",
    phone: "116 111",
    description: "Línea de ayuda para niños y adolescentes.",
  },
];

export default function ResourcesView() {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold text-[#1A3A5C]">Recursos de apoyo</h2>
        <p className="text-sm text-gray-600 mt-1">
          Líneas de ayuda y guías para padres y cuidadores.
        </p>
      </div>
      <ul className="space-y-3">
        {RESOURCES.map((r, idx) => (
          <li
            key={idx}
            className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
          >
            <h3 className="font-semibold text-[#1A3A5C]">{r.name}</h3>
            <p className="text-sm text-gray-600 mt-1">{r.description}</p>
            {r.url && (
              <a
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 inline-block text-sm text-[#4A90D9] underline"
              >
                Visitar sitio
              </a>
            )}
            {r.phone && (
              <p className="mt-2 text-sm font-medium text-gray-800">
                Teléfono: {r.phone}
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
