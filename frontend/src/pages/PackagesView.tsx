import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import { useAppStore } from '../store/appStore'

interface Package {
  name: string
  version: string
}

export function PackagesView() {
  const { selectedManager, confirmBeforeUninstall } = useAppStore()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPackages, setSelectedPackages] = useState<string[]>([])
  const queryClient = useQueryClient()

  const { data: packages, isLoading } = useQuery({
    queryKey: ['packages', selectedManager],
    queryFn: async () => {
      if (!selectedManager) return []
      const res = await axios.get<{ packages: Package[] }>(`/api/managers/${selectedManager}/packages`)
      return res.data.packages
    },
    enabled: !!selectedManager,
  })

  const uninstallMutation = useMutation({
    mutationFn: async (packageName: string) => {
      await axios.delete(`/api/managers/${selectedManager}/packages/${encodeURIComponent(packageName)}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['packages', selectedManager] })
    },
  })

  const handleUninstall = (packageName: string) => {
    if (confirmBeforeUninstall && !window.confirm(`Uninstall ${packageName}?`)) return
    uninstallMutation.mutate(packageName)
  }

  const filteredPackages = packages?.filter(pkg =>
    pkg.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  if (!selectedManager) {
    return <div className="text-center py-12 text-gray-500">Select a package manager from Overview</div>
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-4">
        <input
          type="search"
          placeholder="Search packages..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border rounded-md"
        />
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Batch Actions
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-8">Loading packages...</div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Package</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Version</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredPackages.map(pkg => (
                <tr key={pkg.name} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{pkg.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{pkg.version}</td>
                  <td className="px-6 py-4 text-right text-sm">
                    <button
                      onClick={() => handleUninstall(pkg.name)}
                      disabled={uninstallMutation.isPending}
                      className="text-red-600 hover:text-red-900 disabled:opacity-50"
                    >
                      Uninstall
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
