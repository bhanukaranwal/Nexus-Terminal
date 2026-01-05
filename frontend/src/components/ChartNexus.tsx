import { useEffect, useRef, useState } from 'react'
import { createChart, IChartApi, ISeriesApi, CandlestickData } from 'lightweight-charts'
import { useWebSocket } from '@/lib/websocket_nexus'
import { Settings, TrendingUp, Volume2 } from 'lucide-react'

interface ChartNexusProps {
  symbol: string
}

export function ChartNexus({ symbol }: ChartNexusProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<IChartApi | null>(null)
  const candlestickSeriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null)
  const volumeSeriesRef = useRef<ISeriesApi<'Histogram'> | null>(null)
  const [chartType, setChartType] = useState<'candlestick' | 'line' | 'bar'>('candlestick')
  const [indicators, setIndicators] = useState<string[]>(['volume'])
  
  const { data: marketData } = useWebSocket(`/ws/market/${symbol}`)

  useEffect(() => {
    if (!chartContainerRef.current) return

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: '#0a0a0a' },
        textColor: '#d1d5db',
      },
      grid: {
        vertLines: { color: '#1f2937' },
        horzLines: { color: '#1f2937' },
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
        borderColor: '#374151',
      },
      rightPriceScale: {
        borderColor: '#374151',
      },
      crosshair: {
        mode: 1,
      },
    })

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#10b981',
      downColor: '#ef4444',
      borderVisible: false,
      wickUpColor: '#10b981',
      wickDownColor: '#ef4444',
    })

    const volumeSeries = chart.addHistogramSeries({
      color: '#6366f1',
      priceFormat: {
        type: 'volume',
      },
      priceScaleId: '',
    })

    volumeSeries.priceScale().applyOptions({
      scaleMargins: {
        top: 0.8,
        bottom: 0,
      },
    })

    chartRef.current = chart
    candlestickSeriesRef.current = candlestickSeries
    volumeSeriesRef.current = volumeSeries

    const sampleData: CandlestickData[] = generateSampleData()
    candlestickSeries.setData(sampleData)
    volumeSeries.setData(sampleData.map((d) => ({ time: d.time, value: Math.random() * 1000000, color: d.close > d.open ? '#10b98180' : '#ef444480' })))

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        })
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.remove()
    }
  }, [])

  useEffect(() => {
    if (marketData && candlestickSeriesRef.current) {
      const newCandle: CandlestickData = {
        time: Math.floor(Date.now() / 1000) as any,
        open: marketData.open || 100,
        high: marketData.high || 102,
        low: marketData.low || 99,
        close: marketData.close || 101,
      }
      candlestickSeriesRef.current.update(newCandle)
    }
  }, [marketData])

  return (
    <div className="h-full flex flex-col">
      <div className="h-10 border-b border-gray-800 flex items-center justify-between px-3">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-lg">{symbol}</span>
          <span className="text-green-500 text-sm">+2.45%</span>
        </div>
        <div className="flex items-center gap-2">
          <button className="p-1.5 hover:bg-gray-800 rounded" onClick={() => setChartType('candlestick')}>
            <TrendingUp className="w-4 h-4" />
          </button>
          <button className="p-1.5 hover:bg-gray-800 rounded" onClick={() => setIndicators([...indicators, 'rsi'])}>
            <Volume2 className="w-4 h-4" />
          </button>
          <button className="p-1.5 hover:bg-gray-800 rounded">
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>
      <div ref={chartContainerRef} className="flex-1" />
    </div>
  )
}

function generateSampleData(): CandlestickData[] {
  const data: CandlestickData[] = []
  let basePrice = 100
  const now = Math.floor(Date.now() / 1000)
  
  for (let i = 100; i >= 0; i--) {
    const time = (now - i * 86400) as any
    const open = basePrice + (Math.random() - 0.5) * 2
    const close = open + (Math.random() - 0.5) * 3
    const high = Math.max(open, close) + Math.random() * 2
    const low = Math.min(open, close) - Math.random() * 2
    
    data.push({ time, open, high, low, close })
    basePrice = close
  }
  
  return data
}
