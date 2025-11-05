import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import axios from 'axios'
import ConfirmationModal from './ConfirmationModal'

interface Package {
  name: string
  version: string
}

interface PackageListResponse {
  manager_id: string
  manager_name: string
  total: number
  packages: Package[]
}

interface PackageListProps {
  managerId: string
  managerName: string
}

function PackageList({ managerId, managerName }: PackageListProps) {
  const [selectedPackage, setSelectedPackage] = useState<Package | null>(null)
  const [showConfirmModal, setShowConfirmModal] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const queryClient = useQueryClient()

  const {
    data,
    isLoading,
    error,
  } = useQuery<PackageListResponse>({
    queryKey: ['packages', managerId],
    queryFn: async () => {
      const response = await axios.get(`/api/managers/${managerId}/packages`)
      return response.data
    },
  })

  const uninstallMutation = useMutation({
    mutationFn: async (packageName: string) => {
      await axios.delete(`/api/managers/${managerId}/packages/${packageName}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['packages', managerId] })
      setShowConfirmModal(false)
      setSelectedPackage(null)
    },
  })

  const handleUninstallClick = (pkg: Package) => {
    setSelectedPackage(pkg)
    setShowConfirmModal(true)
  }

  const handleConfirmUninstall = () => {
    if (selectedPackage) {
      uninstallMutation.mutate(selectedPackage.name)
    }
  }

  const filteredPackages = data?.packages.filter((pkg) =>
    pkg.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm">
        <p className="text-red-800 font-semibold">Error loading packages</p>
        <p className="text-red-600 mt-1">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </p>
      </div>
    )
  }

  if (!data || data.packages.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
        <p className="text-gray-600">No packages found</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Search bar */}
      <div className="flex items-center space-x-2">
        <input
          type="text"
          placeholder="Search packages..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
        <span className="text-sm text-gray-500">
          {filteredPackages?.length || 0} of {data.total}
        </span>
      </div>

      {/* Package table */}
      <div className="border border-gray-200 rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Package
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Version
              </th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredPackages?.map((pkg) => (
              <tr key={pkg.name} className="hover:bg-gray-50 transition-colors">
                <td className="px-4 py-3 text-sm font-medium text-gray-900">
                  {pkg.name}
                </td>
                <td className="px-4 py-3 text-sm text-gray-500">{pkg.version}</td>
                <td className="px-4 py-3 text-sm text-right">
                  <button
                    onClick={() => handleUninstallClick(pkg)}
                    className="text-red-600 hover:text-red-800 font-medium transition-colors"
                  >
                    Uninstall
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Confirmation Modal */}
      <ConfirmationModal
        isOpen={showConfirmModal}
        onClose={() => {
          setShowConfirmModal(false)
          setSelectedPackage(null)
        }}
        onConfirm={handleConfirmUninstall}
        title="Confirm Uninstall"
        message={
          <div className="space-y-2">
            <p className="text-gray-700">
              Are you sure you want to uninstall{' '}
              <span className="font-semibold">{selectedPackage?.name}</span>?
            </p>
            <div className="bg-yellow-50 border border-yellow-200 rounded p-3 mt-3">
              <p className="text-yellow-800 text-sm">
                <strong>⚠️ Warning:</strong> A snapshot will be created automatically
                before uninstallation.
              </p>
            </div>
          </div>
        }
        confirmText="Yes, Uninstall"
        cancelText="Cancel"
        confirmButtonClass="bg-red-600 hover:bg-red-700"
        isLoading={uninstallMutation.isPending}
      />

      {/* Error toast for uninstall */}
      {uninstallMutation.isError && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-sm">
          <p className="text-red-800 font-semibold">Uninstall failed</p>
          <p className="text-red-600 mt-1">
            {uninstallMutation.error instanceof Error
              ? uninstallMutation.error.message
              : 'Unknown error occurred'}
          </p>
        </div>
      )}

      {/* Success toast */}
      {uninstallMutation.isSuccess && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-sm">
          <p className="text-green-800 font-semibold">
            Package uninstalled successfully!
          </p>
        </div>
      )}
    </div>
  )
}

export default PackageList
