import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppSettings {
  // Display settings
  theme: 'light' | 'dark' | 'auto'
  compactMode: boolean
  showIcons: boolean

  // Behavior settings
  confirmBeforeUninstall: boolean
  autoRefresh: boolean
  refreshInterval: number // in seconds

  // API settings
  apiBaseUrl: string
  requestTimeout: number // in milliseconds

  // Feature flags
  enableBatchOperations: boolean
  enableVulnerabilityScanning: boolean
  enableDependencyTrees: boolean
}

interface AppState extends AppSettings {
  // Actions
  updateSettings: (settings: Partial<AppSettings>) => void
  resetSettings: () => void

  // UI State
  selectedManager: string | null
  setSelectedManager: (managerId: string | null) => void

  activeTab: string
  setActiveTab: (tab: string) => void
}

const defaultSettings: AppSettings = {
  theme: 'light',
  compactMode: false,
  showIcons: true,
  confirmBeforeUninstall: true,
  autoRefresh: false,
  refreshInterval: 30,
  apiBaseUrl: '/api',
  requestTimeout: 30000,
  enableBatchOperations: true,
  enableVulnerabilityScanning: true,
  enableDependencyTrees: true,
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      ...defaultSettings,
      selectedManager: null,
      activeTab: 'overview',

      updateSettings: (settings) => set((state) => ({ ...state, ...settings })),
      resetSettings: () => set({ ...defaultSettings }),
      setSelectedManager: (managerId) => set({ selectedManager: managerId }),
      setActiveTab: (tab) => set({ activeTab: tab }),
    }),
    {
      name: 'package-audit-settings',
      partialize: (state) => ({
        // Only persist settings, not UI state
        theme: state.theme,
        compactMode: state.compactMode,
        showIcons: state.showIcons,
        confirmBeforeUninstall: state.confirmBeforeUninstall,
        autoRefresh: state.autoRefresh,
        refreshInterval: state.refreshInterval,
        apiBaseUrl: state.apiBaseUrl,
        requestTimeout: state.requestTimeout,
        enableBatchOperations: state.enableBatchOperations,
        enableVulnerabilityScanning: state.enableVulnerabilityScanning,
        enableDependencyTrees: state.enableDependencyTrees,
      }),
    }
  )
)
