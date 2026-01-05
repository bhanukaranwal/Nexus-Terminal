import { useEffect, useState } from 'react'
import { useWebSocket } from '@/lib/websocket_nexus'
import { ArrowUp, ArrowDown } from 'lucide-react'

interface DOMSupremeProps {
  symbol: string
}

interface OrderBookLevel {
  price: number
  size: number
  orders: number
}

export function DOMSupreme({ symbol }: DOMSupremeProps) {
  const [orderBook, setOrderBook] = useState<{ bids: OrderBookLevel[]; asks: OrderBookLevel[] }>({
    bids: [],
    asks: [],
  })
  const [lastPrice, setLastPrice] = useState(100)
  
  useEffect(() => {
    const bids: OrderBookLevel[] = []
    const asks: OrderBookLevel[] = []
    
    for (let i = 0; i < 20; i++) {
      bids.push({
        price: lastPrice - 0.01 * (i + 1),
        size: Math.floor(Math.random() * 1000) + 100,
        orders: Math.floor(Math.random() * 20) + 1,
      })
      asks.push({
        price: lastPrice + 0.01 * (i + 1),
        size: Math.floor(Math.random() * 1000) + 100,
        orders: Math.floor(Math.random() * 20) + 1,
      })
    }
    
    setOrderBook({ bids, asks })
  }, [symbol, lastPrice])

  const handleLevelClick = (price: number, side: 'buy' | 'sell') => {
    console.log(`Order clicked: ${side} at ${price}`)
  }

  return (
    <div className="h-full flex flex-col text-xs font-mono">
      <div className="h-10 border-b border-gray-800 flex items-center justify-between px-3">
        <span className="font-semibold">DOM Ladder</span>
        <span className="text-gray-400">Depth: 20</span>
      </div>

      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="grid grid-cols-4 gap-1 px-2 py-1 border-b border-gray-800 text-gray-400">
          <div>Price</div>
          <div className="text-right">Size</div>
          <div className="text-right">Orders</div>
          <div className="text-right">%</div>
        </div>

        <div className="flex-1 overflow-y-auto">
          {orderBook.asks.reverse().map((ask, idx) => (
            <div
              key={`ask-${idx}`}
              className="grid grid-cols-4 gap-1 px-2 py-0.5 hover:bg-red-950 cursor-pointer relative"
              onClick={() => handleLevelClick(ask.price, 'sell')}
            >
              <div
                className="absolute inset-0 bg-red-900 opacity-20"
                style={{ width: `${(ask.size / 2000) * 100}%` }}
              />
              <div className="text-red-400 relative z-10">{ask.price.toFixed(2)}</div>
              <div className="text-right relative z-10">{ask.size}</div>
              <div className="text-right text-gray-400 relative z-10">{ask.orders}</div>
              <div className="text-right text-gray-400 relative z-10">
                {((ask.size / 2000) * 100).toFixed(0)}
              </div>
            </div>
          ))}

          <div className="sticky top-0 bg-blue-600 text-white font-bold py-1 px-2 flex items-center justify-between z-20">
            <span>{lastPrice.toFixed(2)}</span>
            <span className="flex items-center gap-1">
              <ArrowUp className="w-3 h-3" />
              +0.15
            </span>
          </div>

          {orderBook.bids.map((bid, idx) => (
            <div
              key={`bid-${idx}`}
              className="grid grid-cols-4 gap-1 px-2 py-0.5 hover:bg-green-950 cursor-pointer relative"
              onClick={() => handleLevelClick(bid.price, 'buy')}
            >
              <div
                className="absolute inset-0 bg-green-900 opacity-20"
                style={{ width: `${(bid.size / 2000) * 100}%` }}
              />
              <div className="text-green-400 relative z-10">{bid.price.toFixed(2)}</div>
              <div className="text-right relative z-10">{bid.size}</div>
              <div className="text-right text-gray-400 relative z-10">{bid.orders}</div>
              <div className="text-right text-gray-400 relative z-10">
                {((bid.size / 2000) * 100).toFixed(0)}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
