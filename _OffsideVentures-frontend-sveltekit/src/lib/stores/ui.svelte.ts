import { browser } from '$app/environment';

const STORAGE_KEY = 'ov:sidebar-collapsed';

class UiStore {
  sidebarCollapsed = $state(false);

  constructor() {
    if (browser) {
      this.sidebarCollapsed = localStorage.getItem(STORAGE_KEY) === '1';
    }
  }

  toggleSidebar() {
    this.sidebarCollapsed = !this.sidebarCollapsed;
    if (browser) localStorage.setItem(STORAGE_KEY, this.sidebarCollapsed ? '1' : '0');
  }
}

export const ui = new UiStore();
