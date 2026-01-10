/**
 * Tab Layout Component
 * ====================
 * Two-level tab navigation:
 * - Parent tabs: AI | Manual
 * - Child tabs based on parent selection
 */

import { motion } from 'framer-motion';
import { cn } from '../lib/utils';
import {
  Sparkles,
  Wrench,
  Wand2,
  Edit3,
  Image as ImageIcon,
} from 'lucide-react';

export type ParentTab = 'ai' | 'manual';
export type AIChildTab = 'generate';
export type ManualChildTab = 'format' | 'postcard';
export type ChildTab = AIChildTab | ManualChildTab;

// Helper to get default child tab for a parent
export function getDefaultChildTab(parent: ParentTab): ChildTab {
  return parent === 'ai' ? 'generate' : 'format';
}

interface TabLayoutProps {
  parentTab: ParentTab;
  childTab: ChildTab;
  onParentTabChange: (tab: ParentTab) => void;
  onChildTabChange: (tab: ChildTab) => void;
  children: React.ReactNode;
}

const PARENT_TABS = [
  { id: 'ai' as ParentTab, label: 'AI', icon: Sparkles, description: 'AI-powered generation' },
  { id: 'manual' as ParentTab, label: 'Manual', icon: Wrench, description: 'Manual tools' },
];

const AI_CHILD_TABS = [
  { id: 'generate' as AIChildTab, label: 'Generate', icon: Wand2, description: 'Create posts with AI' },
];

const MANUAL_CHILD_TABS = [
  { id: 'format' as ManualChildTab, label: 'Format', icon: Edit3, description: 'Format & edit text' },
  { id: 'postcard' as ManualChildTab, label: 'Postcard', icon: ImageIcon, description: 'Create post cards' },
];

export function TabLayout({
  parentTab,
  childTab,
  onParentTabChange,
  onChildTabChange,
  children,
}: TabLayoutProps) {
  const childTabs = parentTab === 'ai' ? AI_CHILD_TABS : MANUAL_CHILD_TABS;

  return (
    <div className="space-y-4">
      {/* Parent Tabs */}
      <div className="flex gap-2 p-1 bg-gray-100 dark:bg-dark-border rounded-xl">
        {PARENT_TABS.map((tab) => {
          const Icon = tab.icon;
          const isActive = parentTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => {
                onParentTabChange(tab.id);
                // Auto-select first child tab when switching parents
                if (tab.id === 'ai') {
                  onChildTabChange('generate');
                } else {
                  onChildTabChange('format');
                }
              }}
              className={cn(
                'flex-1 flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-all',
                isActive
                  ? 'bg-white dark:bg-dark-surface text-linkedin-blue shadow-sm'
                  : 'text-linkedin-text-secondary hover:text-linkedin-text'
              )}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Child Tabs */}
      <div className="flex gap-1 border-b border-linkedin-border dark:border-dark-border">
        {childTabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = childTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => onChildTabChange(tab.id)}
              className={cn(
                'flex items-center gap-2 px-4 py-2.5 text-sm font-medium transition-colors relative',
                isActive
                  ? 'text-linkedin-blue'
                  : 'text-linkedin-text-secondary hover:text-linkedin-text'
              )}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
              {isActive && (
                <motion.div
                  layoutId="activeChildTab"
                  className="absolute bottom-0 left-0 right-0 h-0.5 bg-linkedin-blue"
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              )}
            </button>
          );
        })}
      </div>

      {/* Tab Content */}
      <motion.div
        key={`${parentTab}-${childTab}`}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2 }}
      >
        {children}
      </motion.div>
    </div>
  );
}

