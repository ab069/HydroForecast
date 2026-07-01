import { create } from 'zustand'

interface WsState {
  analysis: any | null
  report: string | null
  connected: boolean
  connect: (reservoirId: string) => void
  disconnect: () => void
  setAnalysis: (data: any) => void
}

export const useWsStore = create<WsState>((set) => ({
  analysis: null,
  report: null,
  connected: false,
  ws: null as WebSocket | null,
  connect: (reservoirId: string) => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const host = window.location.host
    const ws = new WebSocket(`${protocol}//${host}/ws/forecast/${reservoirId}`)

    ws.onopen = () => {
      set({ connected: true })
      const token = localStorage.getItem('token')
      ws.send(JSON.stringify({ token }))
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'analysis') {
        set({ analysis: data.data, report: data.report })
      }
    }

    ws.onclose = () => {
      set({ connected: false })
    }

    set({ ws })
  },
  disconnect: () => {
    const state: any = get()
    if (state.ws) {
      state.ws.close()
    }
    set({ ws: null, connected: false, analysis: null, report: null })
  },
  setAnalysis: (data) => set({ analysis: data }),
}))

function get() {
  return useWsStore.getState()
}
