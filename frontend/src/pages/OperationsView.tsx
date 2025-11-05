import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { useAppStore } from '../store/appStore'

export function OperationsView() {
  const { selectedManager } = useAppStore()
  const [packages, setPackages] = useState('')

  const batchUninstall = useMutation({
    mutationFn: async (pkgs: string[]) => {
      await axios.post(`/api/advanced/${selectedManager}/batch-uninstall`, { packages: pkgs })
    },
  })

  const exportLockfile = useMutation({
    mutationFn: async () => {
      const res = await axios.get(`/api/advanced/${selectedManager}/lockfile`)
      const blob = new Blob([JSON.stringify(res.data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${selectedManager}-lockfile.json`
      a.click()
    },
  })

  if (!selectedManager) {
    return <div className="text-center py-12 text-gray-500">Select a package manager from Overview</div>
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium mb-4">Batch Uninstall</h3>
        <textarea
          placeholder="Enter package names (one per line)"
          value={packages}
          onChange={(e) => setPackages(e.target.value)}
          className="w-full h-32 px-3 py-2 border rounded-md"
        />
        <button
          onClick={() => batchUninstall.mutate(packages.split('\n').filter(Boolean))}
          disabled={!packages || batchUninstall.isPending}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
        >
          {batchUninstall.isPending ? 'Uninstalling...' : 'Batch Uninstall'}
        </button>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium mb-4">Export Lockfile</h3>
        <button
          onClick={() => exportLockfile.mutate()}
          disabled={exportLockfile.isPending}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          {exportLockfile.isPending ? 'Exporting...' : 'Export Lockfile'}
        </button>
      </div>
    </div>
  )
}
