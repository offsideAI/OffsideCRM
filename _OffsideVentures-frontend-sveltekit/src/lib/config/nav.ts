import {
  Building2,
  Handshake,
  LayoutDashboard,
  ListChecks,
  Settings,
  Sparkles,
  StickyNote,
  Users
} from 'lucide-svelte';
import type { IconComponent } from '$lib/types';

export interface NavItem {
  label: string;
  href: string;
  icon: IconComponent;
}

export const navItems: NavItem[] = [
  { label: 'Dashboard', href: '/app/dashboard', icon: LayoutDashboard },
  { label: 'Companies', href: '/app/companies', icon: Building2 },
  { label: 'People', href: '/app/people', icon: Users },
  { label: 'Deals', href: '/app/deals', icon: Handshake },
  { label: 'Tasks', href: '/app/tasks', icon: ListChecks },
  { label: 'Notes', href: '/app/notes', icon: StickyNote },
  { label: 'AI Copilot', href: '/app/ai', icon: Sparkles }
];

export const footerNavItems: NavItem[] = [
  { label: 'Settings', href: '/app/settings', icon: Settings }
];
