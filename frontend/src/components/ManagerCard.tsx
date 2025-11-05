import { useState } from 'react'
import PackageList from './PackageList'

interface Manager {
  id: string
  name: string
  version: string
}

interface ManagerCardProps {
  manager: Manager
}

const getManagerIcon = (id: string): string => {
  const icons: Record<string, string> = {
    npm: '📦',
    pip: '🐍',
    winget: '🪟',
    brew: '🍺',
  }
  return icons[id] || '📋'
}

function ManagerCard({ manager }: ManagerCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <span className="text-3xl">{getManagerIcon(manager.id)}</span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{manager.name}</h3>
            <p className="text-sm text-gray-500">v{manager.version}</p>
          </div>
        </div>
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Active
        </span>
      </div>

      <div className="mt-4 space-y-2">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full text-left px-4 py-2 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors text-sm font-medium"
        >
          {isExpanded ? '▼' : '▶'} View Packages
        </button>

        {isExpanded && (
          <div className="mt-3">
            <PackageList managerId={manager.id} managerName={manager.name} />
          </div>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-100 flex space-x-2">
        <button
          className="flex-1 px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
          disabled
          title="Coming soon"
        >
          Export
        </button>
        <button
          className="flex-1 px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200 transition-colors"
          disabled
          title="Coming soon"
        >
          Snapshot
        </button>
      </div>
    </div>
  )
}

export default ManagerCard
