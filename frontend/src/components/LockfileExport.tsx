import axios from 'axios'
import { useState } from 'react'

interface LockfileExportProps {
  managerId: string
}

function LockfileExport({ managerId }: LockfileExportProps) {
  const [isExporting, setIsExporting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleExport = async () => {
    setIsExporting(true)
    setError(null)
    setSuccess(false)

    try {
      const response = await axios.get(`/api/advanced/${managerId}/lockfile`)

      if (response.data.error) {
        setError(response.data.error)
        return
      }

      // Create download
      const format = response.data.format || 'lockfile'
      let content: string
      let filename: string

      if (format === 'requirements.txt') {
        content = response.data.lockfile
        filename = 'requirements.txt'
      } else if (format === 'npm-list-json') {
        content = JSON.stringify(response.data.lockfile, null, 2)
        filename = 'npm-list.json'
      } else {
        content = JSON.stringify(response.data.lockfile, null, 2)
        filename = `${managerId}-lockfile.json`
      }

      const blob = new Blob([content], { type: 'text/plain' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to export lockfile')
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <div className="space-y-2">
      <button
        onClick={handleExport}
        disabled={isExporting}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded transition-colors flex items-center justify-center gap-2"
      >
        {isExporting ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
            <span>Exporting...</span>
          </>
        ) : (
          <>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>Export Lockfile</span>
          </>
        )}
      </button>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-2 text-sm text-red-700">
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-50 border border-green-200 rounded p-2 text-sm text-green-700">
          Lockfile exported successfully!
        </div>
      )}
    </div>
  )
}

export default LockfileExport
