import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/api_hooks'
import toast from 'react-hot-toast'
import { Send, Settings } from 'lucide-react'

interface OrderOracleProps {
  symbol: string
}

export function OrderOracle({ symbol }: OrderOracleProps) {
  const [side, setSide] = useState<'buy' | 'sell'>('buy')
  const [orderType, setOrderType] = useState<'market' | 'limit' | 'stop'>('limit')
  const [quantity, setQuantity] = useState('100')
  const [price, setPrice] = useState('100.00')
  const queryClient = useQueryClient()

  const placeOrderMutation = useMutation({
    mutationFn: async (orderData: any) => {
      const response = await apiClient.post('/api/orders/', orderData)
      return response.data
    },
    onSuccess: () => {
      toast.success('Order placed successfully!')
      queryClient.invalidateQueries({ queryKey: ['orders'] })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to place order')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    placeOrderMutation.mutate({
      symbol,
      side,
      order_type: orderType,
      quantity: parseFloat(quantity),
      price: orderType !== 'market' ? parseFloat(price) : undefined,
      time_in_force: 'gtc',
      broker: 'alpaca',
    })
  }

  return (
    <div className="h-full flex flex-col">
      <div className="h-10 border-b border-gray-800 flex items-center justify-between px-3">
        <span className="font-semibold">Order Entry</span>
        <button className="p-1 hover:bg-gray-800 rounded">
          <Settings className="w-4 h-4" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3">
        <div className="flex gap-1">
          <button
            type="button"
            className={`px-4 py-2 rounded font-semibold ${
              side === 'buy'
                ? 'bg-green-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
            onClick={() => setSide('buy')}
          >
            BUY
          </button>
          <button
            type="button"
            className={`px-4 py-2 rounded font-semibold ${
              side === 'sell'
                ? 'bg-red-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
            onClick={() => setSide('sell')}
          >
            SELL
          </button>
        </div>

        <select
          value={orderType}
          onChange={(e) => setOrderType(e.target.value as any)}
          className="bg-gray-800 border border-gray-700 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="market">Market</option>
          <option value="limit">Limit</option>
          <option value="stop">Stop</option>
          <option value="trailing_stop">Trailing Stop</option>
          <option value="bracket">Bracket</option>
        </select>

        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          placeholder="Quantity"
          className="bg-gray-800 border border-gray-700 rounded px-3 py-2 w-24 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {orderType !== 'market' && (
          <input
            type="number"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            placeholder="Price"
            step="0.01"
            className="bg-gray-800 border border-gray-700 rounded px-3 py-2 w-28 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        )}

        <button
          type="submit"
          disabled={placeOrderMutation.isPending}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 text-white px-6 py-2 rounded font-semibold flex items-center gap-2"
        >
          <Send className="w-4 h-4" />
          {placeOrderMutation.isPending ? 'Placing...' : 'Place Order'}
        </button>
      </form>
    </div>
  )
}
