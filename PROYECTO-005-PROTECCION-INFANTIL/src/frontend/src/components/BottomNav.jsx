export default function BottomNav({ active, onChange }) {
  const tabs = [
    { id: "search", label: "Buscar", icon: "🔍" },
    { id: "report", label: "Reportar", icon: "📝" },
    { id: "resources", label: "Recursos", icon: "📚" },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 border-t bg-white pb-safe">
      <div className="mx-auto flex max-w-md">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={`flex flex-1 flex-col items-center py-3 text-xs font-medium transition ${
              active === tab.id
                ? "text-[#1A3A5C]"
                : "text-gray-500"
            }`}
            aria-current={active === tab.id ? "page" : undefined}
          >
            <span className="text-xl" aria-hidden="true">
              {tab.icon}
            </span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
}
