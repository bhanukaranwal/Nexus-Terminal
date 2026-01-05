import { useState } from 'react'
import { Plus, Star, TrendingUp } from 'lucide-react'

interface WatchlistPanelProps {
  onSelectSymbol: (symbol: string) => void
}

export function WatchlistPanel({ onSelectSymbol }: WatchlistPanelProps) {
  const [watchlist, setWatchlist] = useState([
    { symbol: 'AAPL', price: 185.50, change: 2.45 },
    { symbol: 'TSLA', price: 245.30, change: -1.23 },
    { symbol: 'NVDA', price: 520.80, change: 3.87 },
    { symbol: 'SPY', price: 485.20, change: 0.65 },
    { symbol: 'QQQ', price: 395.40, change: 1.12 },
  ])

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="p-3 border-b border-gray-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm">Watchlist</h3>
        <button className="p-1 hover:bg-gray-800 rounded">
          <Plus className="w-4 h-4" />
        </button>
      </div>
      
      <div className="p-2 space-y-1">
        {watchlist.map((item) => (
          <div
            key={item.symbol}
            onClick={() => onSelectSymbol(item.symbol)}
            className="bg-gray-900 rounded p-2 cursor-pointer hover:bg-gray-800"
          >
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                <Star className="w-3 h-3 text-yellow-500" />
                <span className="font-semibold text-sm">{item.symbol}</span>
              </div>
              <span className="text-sm">${item.price.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-end">
              <span className={`text-xs flex items-center gap-1 ${item.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                <TrendingUp className="w-3 h-3" />
                {item.change > 0 ? '+' : ''}{item.change.toFixed(2)}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
