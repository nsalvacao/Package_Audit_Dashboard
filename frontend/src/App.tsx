import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Dashboard from './pages/Dashboard'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-900">
              📦 Package Audit Dashboard
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              Centralized package manager auditing and management
            </p>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Dashboard />
        </main>

        <footer className="mt-12 py-6 text-center text-sm text-gray-500 border-t">
          <p>Package Audit Dashboard v0.2.0 - Phase 2 Complete</p>
        </footer>
      </div>
    </QueryClientProvider>
  )
}

export default App
