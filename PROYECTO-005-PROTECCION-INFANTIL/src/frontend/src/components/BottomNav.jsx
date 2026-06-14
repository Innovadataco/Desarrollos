import { Link, useLocation } from "react-router-dom";

export default function BottomNav() {
  const location = useLocation();
  const segment = location.pathname.split("/")[1] || "search";
  const active = segment === "" ? "search" : segment;

  const tabs = [
    { id: "search", label: "Buscar", icon: "🔍", to: "/" },
    { id: "report", label: "Reportar", icon: "📝", to: "/report" },
    { id: "resources", label: "Recursos", icon: "📚", to: "/resources" },
    { id: "admin", label: "Admin", icon: "🛡️", to: "/admin/login" },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 border-t bg-white pb-safe">
      <div className="mx-auto flex max-w-md">
        {tabs.map((tab) => (
          <Link
            key={tab.id}
            to={tab.to}
            className={`flex flex-1 flex-col items-center py-3 text-xs font-medium transition ${
              active === tab.id ? "text-[#1A3A5C]" : "text-gray-500"
            }`}
            aria-current={active === tab.id ? "page" : undefined}
          >
            <span className="text-xl" aria-hidden="true">
              {tab.icon}
            </span>
            <span>{tab.label}</span>
          </Link>
        ))}
      </div>
    </nav>
  );
}
