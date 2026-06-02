import React from 'react';
import { LayoutDashboard, FileText, Compass, Code, Eye, LogOut } from 'lucide-react';

export default function Layout({ children, currentTab, setTab }) {
  const navigationItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analysis', label: 'Phase 1: Analysis', icon: FileText },
    { id: 'design', label: 'Phase 2: Design', icon: Compass },
    { id: 'develop', label: 'Phase 3: Develop', icon: Code },
    { id: 'review', label: 'Phase 4: Review', icon: Eye },
  ];

  return (
    <div className="flex h-screen bg-[#070707] text-slate-100 font-sans antialiased overflow-hidden">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[#101012] border-r border-red-900/30 flex flex-col justify-between z-20 backdrop-blur-xl shadow-[0_0_40px_rgba(220,38,38,0.08)]">
        <div>
          <div className="h-16 flex items-center px-6 border-b border-red-900/20 tracking-wide">
            <span className="text-xl font-bold bg-gradient-to-r from-red-400 via-rose-500 to-red-600 bg-clip-text text-transparent tracking-wider">
              Content Studio
            </span>
          </div>

          <nav className="p-4 space-y-2">
            {navigationItems.map((item) => {
              const IconComponent = item.icon;
              const isActive = currentTab === item.id;

              return (
                <button
                  key={item.id}
                  onClick={() => setTab(item.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-300 ${isActive
                    ? 'bg-gradient-to-r from-red-600 via-rose-600 to-red-700 text-white shadow-lg shadow-red-900/50 border border-red-500/20'
                    : 'text-slate-400 hover:bg-red-950/20 hover:text-red-300 border border-transparent hover:border-red-900/20'
                    }`}
                >
                  <IconComponent
                    className={`w-4 h-4 transition-all ${isActive
                      ? 'text-white drop-shadow-[0_0_8px_rgba(239,68,68,0.8)]'
                      : 'text-slate-500'
                      }`}
                  />

                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Footer Tenant Workspace Context */}
        <div className="p-4 border-t border-red-900/20 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-red-500 via-rose-500 to-red-700 flex items-center justify-center font-semibold text-xs text-white shadow-lg shadow-red-900/40">
              ID
            </div>

            <div className="truncate max-w-[120px]">
              <p className="text-xs font-semibold text-slate-300">
                Designer Workspace
              </p>
              <p className="text-[10px] text-slate-500 truncate">
                L&D Platform
              </p>
            </div>
          </div>

          <button className="text-slate-500 hover:text-red-400 p-2 rounded-lg transition-colors">
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </aside>

      {/* Main Context Container */}
      <main className="flex-1 flex flex-col bg-[#070707] overflow-y-auto relative">

        {/* Background Glow Effects */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-150px] left-[-150px] w-[500px] h-[500px] bg-red-600/10 rounded-full blur-[180px]" />
          <div className="absolute bottom-[-150px] right-[-150px] w-[500px] h-[500px] bg-rose-600/10 rounded-full blur-[180px]" />
        </div>

        {/* <header className="h-16 border-b border-red-900/20 flex items-center justify-between px-8 bg-black/30 backdrop-blur-xl sticky top-0 z-10">
          <div className="flex items-center space-x-2">
            <h1 className="text-sm font-semibold text-slate-200 capitalize tracking-wide">
              {currentTab === 'dashboard'
                ? 'Overview Matrix'
                : `Workspace / ADDIE Model / ${currentTab}`}
            </h1>
          </div>

          <div className="flex items-center space-x-4">
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-500/10 text-red-400 border border-red-500/20 shadow-lg shadow-red-900/20">
              ● Active Session
            </span>
          </div>
        </header> */}

        <div className="p-8 max-w-7xl w-full mx-auto relative z-10">
          {children}
        </div>
      </main>
    </div>
  );
}