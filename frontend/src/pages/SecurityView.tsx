import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { useAppStore } from '../store/appStore'

export function SecurityView() {
  const { selectedManager } = useAppStore()

  const { data, isLoading } = useQuery({
    queryKey: ['vulnerabilities', selectedManager],
    queryFn: async () => {
      if (!selectedManager) return null
      const res = await axios.get(`/api/advanced/${selectedManager}/vulnerabilities`)
      return res.data
    },
    enabled: !!selectedManager,
  })

  if (!selectedManager) {
    return <div className="text-center py-12 text-gray-500">Select a package manager from Overview</div>
  }

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium mb-4">Vulnerability Scan</h3>
        {isLoading ? (
          <div>Scanning...</div>
        ) : data?.vulnerabilities?.length > 0 ? (
          <div className="space-y-2">
            {data.vulnerabilities.map((vuln: any, i: number) => (
              <div key={i} className="p-3 border rounded bg-red-50">
                <div className="font-medium">{vuln.package}</div>
                <div className="text-sm text-gray-600">{vuln.title}</div>
                <div className="text-xs text-red-600">Severity: {vuln.severity}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-green-600">No vulnerabilities found!</div>
        )}
      </div>
    </div>
  )
}
