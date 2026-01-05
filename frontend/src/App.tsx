import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import { NexusDashboard } from './pages/NexusDashboard'
import { TradingCosmos } from './pages/TradingCosmos'
import { ChartsEpic } from './pages/ChartsEpic'
import { OptionsGalaxy } from './pages/OptionsGalaxy'
import { PortfolioFortress } from './pages/PortfolioFortress'
import { StrategiesUniverse } from './pages/StrategiesUniverse'
import { ScannersOracle } from './pages/ScannersOracle'
import { SettingsNexus } from './pages/SettingsNexus'
import { MarketplaceCosmos } from './pages/MarketplaceCosmos'
import { AuthProvider } from './lib/auth_context'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="min-h-screen bg-background text-foreground">
            <Routes>
              <Route path="/" element={<NexusDashboard />} />
              <Route path="/trading" element={<TradingCosmos />} />
              <Route path="/charts" element={<ChartsEpic />} />
              <Route path="/options" element={<OptionsGalaxy />} />
              <Route path="/portfolio" element={<PortfolioFortress />} />
              <Route path="/strategies" element={<StrategiesUniverse />} />
              <Route path="/scanners" element={<ScannersOracle />} />
              <Route path="/settings" element={<SettingsNexus />} />
              <Route path="/marketplace" element={<MarketplaceCosmos />} />
            </Routes>
          </div>
          <Toaster position="top-right" />
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
