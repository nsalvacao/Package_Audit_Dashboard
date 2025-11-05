import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import ManagerCard from '../components/ManagerCard'

interface Manager {
  id: string
  name: string
  version: string
}

interface DiscoverResponse {
  managers: Manager[]
}

const fetchManagers = async (): Promise<Manager[]> => {
  const response = await axios.post<DiscoverResponse>('/api/discover')
  return response.data.managers
}

function Dashboard() {
  const { data: managers, isLoading, error } = useQuery({
    queryKey: ['managers'],
    queryFn: fetchManagers,
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-semibold">Error loading managers</h3>
        <p className="text-red-600 text-sm mt-1">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </p>
        <p className="text-red-600 text-sm mt-2">
          Make sure the backend server is running at http://localhost:8000
        </p>
      </div>
    )
  }

  if (!managers || managers.length === 0) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <h3 className="text-yellow-800 font-semibold text-lg">No package managers detected</h3>
        <p className="text-yellow-700 mt-2">
          No supported package managers were found on your system.
        </p>
        <p className="text-yellow-600 text-sm mt-2">
          Supported: npm, pip, winget, brew
        </p>
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-gray-900">
          Detected Package Managers
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          {managers.length} manager{managers.length !== 1 ? 's' : ''} found on your system
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {managers.map((manager) => (
          <ManagerCard key={manager.id} manager={manager} />
        ))}
      </div>
    </div>
  )
}

export default Dashboard
