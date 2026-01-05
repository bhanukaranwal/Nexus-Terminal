import { useEffect, useState } from 'react'
import { useWebSocket } from '@/lib/websocket_nexus'
import { Clock, Filter } from 'lucide-react'

interface TimeSalesReconstructProps {
  symbol: string
}

interface Trade {
  time: string
  price: number
  size: number
  side: 'buy' | 'sell'
  aggressor: boolean
}

export function TimeSalesReconstruct({ symbol }: TimeSalesReconstructProps) {
  const [trades, setTrades] = useState<Trade[]>([])
  const { data: tradeData } = useWebSocket(`/ws/market/${symbol}`)

  useEffect(() => {
    const sampleTrades: Trade[] = []
    for (let i = 0; i < 50; i++) {
      const now = new Date()
      now.setSeconds(now.getSeconds() - i * 2)
      sampleTrades.push({
        time: now.toLocaleTimeString(),
        price: 100 + (Math.random() - 0.5) * 2,
        size: Math.floor(Math.random() * 500) + 100,
        side: Math.random() > 0.5 ? 'buy' : 'sell',
        aggressor: Math.random() > 0.7,
      })
    }
    setTrades(sampleTrades)
  }, [symbol])

  useEffect(() => {
    if (tradeData) {
      const newTrade: Trade = {
        time: new Date().toLocaleTimeString(),
        price: tradeData.price || 100,
        size: tradeData.size || 100,
        side: Math.random() > 0.5 ? 'buy' : 'sell',
        aggressor: Math.random() > 0.5,
      }
      setTrades((prev) => [newTrade, ...prev.slice(0, 49)])
    }
  }, [tradeData])

  return (
    <div className="h-full flex flex-col text-xs font-mono">
      <div className="h-10 border-b border-gray-800 flex items-center justify-between px-3">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4" />
          <span className="font-semibold">Time & Sales</span>
        </div>
        <button className="p-1 hover:bg-gray-800 rounded">
          <Filter className="w-3 h-3" />
        </button>
      </div>

      <div className="grid grid-cols-4 gap-1 px-2 py-1 border-b border-gray-800 text-gray-400">
        <div>Time</div>
        <div className="text-right">Price</div>
        <div className="text-right">Size</div>
        <div className="text-right">Side</div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {trades.map((trade, idx) => (
          <div
            key={idx}
            className={`grid grid-cols-4 gap-1 px-2 py-0.5 ${
              trade.aggressor ? 'bg-yellow-950 bg-opacity-20' : ''
            }`}
          >
            <div className="text-gray-400">{trade.time}</div>
            <div
              className={`text-right font-semibold ${
                trade.side === 'buy' ? 'text-green-400' : 'text-red-400'
              }`}
            >
              {trade.price.toFixed(2)}
            </div>
            <div className="text-right">{trade.size}</div>
            <div className={`text-right ${trade.side === 'buy' ? 'text-green-400' : 'text-red-400'}`}>
              {trade.side.toUpperCase()}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
