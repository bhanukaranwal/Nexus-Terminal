import { Link } from 'react-router-dom'
import { TrendingUp, BarChart3, Target, Cpu, Coins, Settings } from 'lucide-react'

export function NexusDashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-blue-950 text-white">
      <header className="border-b border-gray-800 bg-gray-950 bg-opacity-80 backdrop-blur">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
            NEXUS
          </h1>
          <nav className="flex items-center gap-6">
            <Link to="/trading" className="hover:text-blue-400">Trading</Link>
            <Link to="/charts" className="hover:text-blue-400">Charts</Link>
            <Link to="/portfolio" className="hover:text-blue-400">Portfolio</Link>
            <Link to="/strategies" className="hover:text-blue-400">Strategies</Link>
            <Link to="/marketplace" className="hover:text-blue-400">Marketplace</Link>
          </nav>
        </div>
      </header>

      <main className="container mx-auto px-6 py-12">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold mb-4">The Ultimate Trading Terminal</h2>
          <p className="text-xl text-gray-400 mb-8">
            AI-Powered • Blockchain-Native • Quantum-Optimized
          </p>
          <Link
            to="/trading"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-8 py-3 rounded-lg text-lg"
          >
            Launch Terminal
          </Link>
        </div>

        <div className="grid grid-cols-3 gap-6 mb-16">
          <FeatureCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="Multi-Asset Trading"
            description="Trade equities, options, futures, forex, crypto, and tokenized assets from one platform"
          />
          <FeatureCard
            icon={<Cpu className="w-8 h-8" />}
            title="AI Agentic Execution"
            description="Deploy autonomous AI agents that analyze, strategize, and execute trades 24/7"
          />
          <FeatureCard
            icon={<Coins className="w-8 h-8" />}
            title="DeFi Integration"
            description="Access lending, borrowing, yield farming, and atomic swaps directly from the terminal"
          />
          <FeatureCard
            icon={<BarChart3 className="w-8 h-8" />}
            title="Advanced Order Flow"
            description="Reconstruct Time & Sales, footprint charts, delta divergence, absorbed volume analysis"
          />
          <FeatureCard
            icon={<Target className="w-8 h-8" />}
            title="Quantum Optimization"
            description="JAX-powered backtesting and strategy optimization with 10,000+ iterations"
          />
          <FeatureCard
            icon={<Settings className="w-8 h-8" />}
            title="Infinite Customization"
            description="Drag-drop workspaces, AR/VR support, cloud sync, collaborative trading rooms"
          />
        </div>
      </main>
    </div>
  )
}

function FeatureCard({ icon, title, description }: any) {
  return (
    <div className="bg-gray-900 bg-opacity-50 border border-gray-800 rounded-lg p-6 hover:border-blue-500 transition-colors">
      <div className="text-blue-500 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}
