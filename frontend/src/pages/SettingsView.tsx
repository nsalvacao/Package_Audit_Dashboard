import { useAppStore } from '../store/appStore'

export function SettingsView() {
  const {
    confirmBeforeUninstall,
    autoRefresh,
    refreshInterval,
    compactMode,
    updateSettings,
    resetSettings,
  } = useAppStore()

  return (
    <div className="max-w-2xl space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium mb-4">General Settings</h3>

        <div className="space-y-4">
          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={confirmBeforeUninstall}
              onChange={(e) => updateSettings({ confirmBeforeUninstall: e.target.checked })}
              className="rounded"
            />
            <span>Confirm before uninstalling packages</span>
          </label>

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => updateSettings({ autoRefresh: e.target.checked })}
              className="rounded"
            />
            <span>Auto-refresh package list</span>
          </label>

          {autoRefresh && (
            <div className="ml-6">
              <label className="block text-sm text-gray-600">
                Refresh interval (seconds)
                <input
                  type="number"
                  value={refreshInterval}
                  onChange={(e) => updateSettings({ refreshInterval: parseInt(e.target.value) })}
                  min="5"
                  max="300"
                  className="mt-1 block w-32 px-3 py-2 border rounded-md"
                />
              </label>
            </div>
          )}

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={compactMode}
              onChange={(e) => updateSettings({ compactMode: e.target.checked })}
              className="rounded"
            />
            <span>Compact mode</span>
          </label>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium mb-4">Advanced</h3>
        <button
          onClick={resetSettings}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
        >
          Reset to Defaults
        </button>
      </div>
    </div>
  )
}
