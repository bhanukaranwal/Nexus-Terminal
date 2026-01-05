import { useState } from 'react'
import { Layout, Save, Upload, Grid, Maximize2 } from 'lucide-react'

interface WorkspaceEvolutionProps {
  layout: string
  onLayoutChange: (layout: string) => void
}

export function WorkspaceEvolution({ layout, onLayoutChange }: WorkspaceEvolutionProps) {
  const [showMenu, setShowMenu] = useState(false)

  const layouts = [
    { id: 'standard', name: 'Standard', icon: Grid },
    { id: 'trading', name: 'Trading Focus', icon: Layout },
    { id: 'analysis', name: 'Analysis', icon: Maximize2 },
  ]

  return (
    <div className="relative">
      <button
        onClick={() => setShowMenu(!showMenu)}
        className="flex items-center gap-2 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 rounded text-sm"
      >
        <Layout className="w-4 h-4" />
        Workspace
      </button>

      {showMenu && (
        <div className="absolute right-0 top-full mt-1 w-48 bg-gray-900 border border-gray-700 rounded shadow-lg z-50">
          <div className="p-2 border-b border-gray-700">
            <div className="text-xs text-gray-400 mb-2">Layouts</div>
            {layouts.map((l) => (
              <button
                key={l.id}
                onClick={() => {
                  onLayoutChange(l.id)
                  setShowMenu(false)
                }}
                className={`w-full flex items-center gap-2 px-2 py-1.5 rounded text-sm hover:bg-gray-800 ${
                  layout === l.id ? 'bg-blue-900' : ''
                }`}
              >
                <l.icon className="w-4 h-4" />
                {l.name}
              </button>
            ))}
          </div>
          
          <div className="p-2">
            <button className="w-full flex items-center gap-2 px-2 py-1.5 rounded text-sm hover:bg-gray-800">
              <Save className="w-4 h-4" />
              Save Layout
            </button>
            <button className="w-full flex items-center gap-2 px-2 py-1.5 rounded text-sm hover:bg-gray-800">
              <Upload className="w-4 h-4" />
              Load Layout
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
