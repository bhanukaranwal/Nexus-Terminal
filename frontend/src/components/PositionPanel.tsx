import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/api_hooks'
import { TrendingUp, TrendingDown } from 'lucide-react'

export function PositionPanel() {
  const { data: positions } = useQuery({
    queryKey: ['positions'],
    queryFn: async () => {
      const response = await apiClient.get('/api/positions/')
      return response.data
    },
    refetchInterval: 5000,
  })

  return (
    <div className="flex-1 border-t border-gray-800 overflow-y-auto">
      <div className="p-3 border-b border-gray-800">
        <h3 className="font-semibold text-sm">Positions</h3>
      </div>
      
      <div className="p-2 space-y-1">
        {positions?.length === 0 ? (
          <div className="text-center text-gray-500 text-xs py-4">No positions</div>
        ) : (
          <div className="space-y-1">
            <PositionItem symbol="AAPL" qty={100} pnl={250} pnlPercent={2.5} />
            <PositionItem symbol="TSLA" qty={50} pnl={-125} pnlPercent={-1.2} />
            <PositionItem symbol="NVDA" qty={75} pnl={450} pnlPercent={3.8} />
          </div>
        )}
      </div>
    </div>
  )
}

function PositionItem({ symbol, qty, pnl, pnlPercent }: any) {
  const isProfit = pnl >= 0
  
  return (
    <div className="bg-gray-900 rounded p-2 text-xs hover:bg-gray-800 cursor-pointer">
      <div className="flex items-center justify-between mb-1">
        <span className="font-semibold">{symbol}</span>
        <span className="text-gray-400">{qty} shares</span>
      </div>
      <div className="flex items-center justify-between">
        <div className={`flex items-center gap-1 ${isProfit ? 'text-green-400' : 'text-red-400'}`}>
          {isProfit ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
          <span className="font-semibold">${Math.abs(pnl).toFixed(2)}</span>
        </div>
        <span className={isProfit ? 'text-green-400' : 'text-red-400'}>
          {pnlPercent > 0 ? '+' : ''}{pnlPercent.toFixed(2)}%
        </span>
      </div>
    </div>
  )
}
