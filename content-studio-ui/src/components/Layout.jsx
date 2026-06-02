import React from 'react';

export default function Layout({ children, currentTab, setTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'dashboard' },
    { id: 'analysis', label: '1. Analysis Phase' },
    { id: 'design', label: '2. Design Phase' },
    { id: 'develop', label: '3. Develop Phase' },
    { id: 'review', label: '4. Review Phase' }
  ];

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="p-5 text-xl font-bold border-b border-slate-800 tracking-wider">
          CONTENT STUDIO
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setTab(item.id)}
              className={`w-full text-left px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                currentTab === item.id 
                  ? 'bg-blue-600 text-white' 
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>
        <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
          Org ID: Tenant-Active-101
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold capitalize text-slate-800">
            {currentTab.replace('-', ' ')}
          </h1>
          <div className="flex items-center space-x-3">
            <span className="text-sm text-slate-600 font-medium">Vivek (AI Engineer)</span>
            <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold text-sm">
              V
            </div>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}