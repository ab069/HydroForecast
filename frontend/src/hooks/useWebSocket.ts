import { useEffect } from 'react'
import { useWsStore } from '../store/wsStore'

export function useWebSocket(reservoirId: string | null) {
  const { connect, disconnect, analysis, report, connected } = useWsStore()

  useEffect(() => {
    if (reservoirId) {
      connect(reservoirId)
      return () => disconnect()
    }
  }, [reservoirId])

  return { analysis, report, connected }
}
