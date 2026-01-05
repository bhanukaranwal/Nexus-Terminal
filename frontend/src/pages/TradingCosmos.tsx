import { useState } from 'react'
import { ChartNexus } from '@/components/ChartNexus'
import { DOMSupreme } from '@/components/DOMSupreme'
import { TimeSalesReconstruct } from '@/components/TimeSalesReconstruct'
import { OrderOracle } from '@/components/OrderOracle'
import { WorkspaceEvolution } from '@/components/WorkspaceEvolution'
import { PositionPanel } from '@/components/PositionPanel'
import { WatchlistPanel } from '@/components/WatchlistPanel'

export function TradingCosmos() {
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL')
  const [layout, setLayout] = useState('standard')

  return (
    <div className="h-screen flex flex-col bg-gray-950">
      <header className="h-14 border-b border-gray-800 flex items-center px-4 justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent">
            NEXUS
          </h1>
          <input
            type="text"
            value={selectedSymbol}
            onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
            className="bg-gray-900 border border-gray-700 rounded px-3 py-1 text-sm w-32 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Symbol"
          />
        </div>
        <WorkspaceEvolution layout={layout} onLayoutChange={setLayout} />
      </header>

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-64 border-r border-gray-800 flex flex-col">
          <WatchlistPanel onSelectSymbol={setSelectedSymbol} />
          <PositionPanel />
        </aside>

        <main className="flex-1 grid grid-cols-3 gap-1 p-1">
          <div className="col-span-2 row-span-2 bg-gray-900 rounded">
            <ChartNexus symbol={selectedSymbol} />
          </div>
          
          <div className="bg-gray-900 rounded">
            <DOMSupreme symbol={selectedSymbol} />
          </div>
          
          <div className="bg-gray-900 rounded">
            <TimeSalesReconstruct symbol={selectedSymbol} />
          </div>
          
          <div className="col-span-3 bg-gray-900 rounded">
            <OrderOracle symbol={selectedSymbol} />
          </div>
        </main>
      </div>
    </div>
  )
}
