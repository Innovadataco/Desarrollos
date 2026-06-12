import ReportForm from "./components/ReportForm";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-md mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary-dark mb-2">
            Protección Infantil Comunitaria
          </h1>
          <p className="text-gray-600">
            Reporte anónimo y seguro. No guardamos IPs, cookies ni metadata.
          </p>
        </header>
        <ReportForm />
        <footer className="text-center mt-8 text-xs text-gray-500">
          Tu reporte es encriptado en reposo con AES-256-GCM.
        </footer>
      </div>
    </div>
  );
}

export default App;