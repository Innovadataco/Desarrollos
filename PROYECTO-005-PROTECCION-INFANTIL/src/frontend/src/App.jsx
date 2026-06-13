import { useState } from "react";
import BottomNav from "./components/BottomNav";
import ReportForm from "./components/ReportForm";
import ResourcesView from "./components/ResourcesView";
import SearchView from "./components/SearchView";

function App() {
  const [tab, setTab] = useState("search");
  const [reportIdentifier, setReportIdentifier] = useState("");

  const handleReportFromSearch = (identifier) => {
    setReportIdentifier(identifier);
    setTab("report");
  };

  return (
    <div className="min-h-screen bg-gray-50 pb-24">
      <header className="bg-[#1A3A5C] px-4 py-5 text-center text-white">
        <h1 className="text-2xl font-bold">Semáforo de Confianza</h1>
        <p className="mt-1 text-sm opacity-90">
          Verifica contactos sospechosos en segundos. Sin registro.
        </p>
      </header>

      <main className="mx-auto max-w-md px-4 py-6">
        {tab === "search" && (
          <SearchView onReport={handleReportFromSearch} />
        )}
        {tab === "report" && <ReportForm prefillIdentifier={reportIdentifier} />}
        {tab === "resources" && <ResourcesView />}
      </main>

      <footer className="mx-auto max-w-md px-4 pb-4 text-center text-xs text-gray-500">
        🚫 Sin cookies, sin tracking. Conexión cifrada.
      </footer>

      <BottomNav active={tab} onChange={setTab} />
    </div>
  );
}

export default App;
