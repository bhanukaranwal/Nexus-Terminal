import { useEffect, useState, useRef } from 'react'

export function useWebSocket(url: string) {
  const [data, setData] = useState<any>(null)
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const wsUrl = `ws://localhost:8000${url}`
    const ws = new WebSocket(wsUrl)

    ws.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected:', url)
    }

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data)
        setData(parsed)
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected:', url)
    }

    wsRef.current = ws

    return () => {
      ws.close()
    }
  }, [url])

  return { data, isConnected }
}
