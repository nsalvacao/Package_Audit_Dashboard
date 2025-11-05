import { useState } from 'react'
import VulnerabilityScan from './VulnerabilityScan'
import LockfileExport from './LockfileExport'

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

      <div className="mt-4 space-y-3">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full text-left px-4 py-2 bg-blue-50 text-blue-700 rounded-md hover:bg-blue-100 transition-colors text-sm font-medium"
        >
          {isExpanded ? '▼' : '▶'} Advanced Features
        </button>

        {isExpanded && (
          <div className="space-y-3">
            {/* Vulnerability Scanning */}
            <VulnerabilityScan managerId={manager.id} />

            {/* Lockfile Export */}
            <div className="border border-gray-200 rounded-lg p-4 bg-white">
              <h4 className="text-sm font-medium text-gray-900 mb-3">Export Lockfile</h4>
              <LockfileExport managerId={manager.id} />
            </div>

            {/* Dependency Tree Link */}
            <div className="border border-gray-200 rounded-lg p-4 bg-white">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Dependency Tree</h4>
              <p className="text-xs text-gray-600 mb-3">
                View dependency tree for all packages
              </p>
              <a
                href={`/api/advanced/${manager.id}/dependency-tree`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded transition-colors text-sm"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
                View Tree
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ManagerCard
