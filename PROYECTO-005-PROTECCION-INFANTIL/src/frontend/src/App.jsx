import ReportForm from './components/ReportForm'

function App() {
  return (
    <div className="min-h-screen bg-slate-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-md">
        <header className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-teal-800 sm:text-3xl">
            Protección Infantil Comunitaria
          </h1>
          <p className="mt-2 text-sm text-slate-600">
            Reporte anónimo y seguro. No guardamos IPs, cookies ni metadata.
          </p>
        </header>
        <main>
          <ReportForm />
        </main>
        <footer className="mt-8 text-center text-xs text-slate-500">
          Tu reporte es encriptado en reposo con AES-256-GCM.
        </footer>
      </div>
    </div>
  )
}

export default App
