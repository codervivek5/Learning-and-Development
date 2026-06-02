import React, { useState } from 'react';

const INITIAL_STATS = [
  { id: 1, name: 'Total Projects', count: 12, change: '+2 this week', color: 'bg-blue-500' },
  { id: 2, name: 'In Progress (ADDIE)', count: 5, change: '3 in Analysis Phase', color: 'bg-amber-500' },
  { id: 3, name: 'Completed Courses', count: 7, change: '100% review passed', color: 'bg-emerald-500' },
];

const INITIAL_PROJECTS = [
  {
    id: 101,
    title: "Cybersecurity Awareness 2026",
    target_audience: "All Global Employees",
    phase: "Analysis",
    progress: 25,
    objectives_count: 4,
    updated_at: "2 hours ago"
  },
  {
    id: 102,
    title: "FastAPI + SQLModel Backend Bootcamp",
    target_audience: "Junior L&D Developers",
    phase: "Design",
    progress: 50,
    objectives_count: 8,
    updated_at: "Yesterday"
  },
  {
    id: 103,
    title: "AI Prompt Engineering for Instructional Designers",
    target_audience: "Senior Content Authors",
    phase: "Develop",
    progress: 75,
    objectives_count: 6,
    updated_at: "3 days ago"
  }
];

const INITIAL_ACTIVITIES = [
  { id: 1, user: "System AI", action: "Generated structured curriculum skeleton", project: "Bootcamp", time: "10m ago" },
  { id: 2, user: "Admin User", action: "Approved Phase 1 Needs Analysis", project: "Cybersecurity", time: "2h ago" },
  { id: 3, user: "System AI", action: "Compiled storyboard interactivity paths", project: "Prompt Eng.", time: "1d ago" },
];

export default function PhaseOverview() {
  const [projects, setProjects] = useState(INITIAL_PROJECTS);
  const [stats, setStats] = useState(INITIAL_STATS);
  const [activities, setActivities] = useState(INITIAL_ACTIVITIES);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterPhase, setFilterPhase] = useState("All");

  const handleCreateProjectMock = () => {
    const newId = Date.now();
    const newProj = {
      id: newId,
      title: `New AI Project Reference #${projects.length + 1}`,
      target_audience: "Target Group Profile",
      phase: "Analysis",
      progress: 10,
      objectives_count: 1,
      updated_at: "Just now"
    };
    setProjects([newProj, ...projects]);
    setActivities([
      { id: Date.now(), user: "Admin User", action: "Initiated a new course workspace", project: `Proj #${projects.length + 1}`, time: "Just now" },
      ...activities
    ]);
  };

  const filteredProjects = projects.filter(proj => {
    const matchesSearch = proj.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          proj.target_audience.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPhase = filterPhase === "All" || proj.phase === filterPhase;
    return matchesSearch && matchesPhase;
  });

  return (
    <div className="flex flex-col space-y-8">
      {/* Search and Create Action */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="relative flex-1 max-w-md">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          onClick={handleCreateProjectMock}
          className="bg-blue-600 hover:bg-blue-700 text-white font-medium text-sm px-4 py-2 rounded-lg shadow-sm transition-all active:scale-95"
        >
          + Create New Project
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main Content */}
        <div className="flex-1 space-y-8">
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {stats.map((item) => (
              <div key={item.id} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex items-start space-x-4">
                <div className={`h-10 w-10 rounded-lg ${item.color} flex items-center justify-center text-white text-lg`}>
                  {item.id === 1 ? "📁" : item.id === 2 ? "⏳" : "✅"}
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-500">{item.name}</p>
                  <p className="text-2xl font-bold text-slate-900 mt-0.5">{item.count}</p>
                  <span className="text-xs font-medium text-blue-600 inline-block bg-blue-50 px-2 py-0.5 rounded mt-2">{item.change}</span>
                </div>
              </div>
            ))}
          </section>

          <section className="bg-white rounded-xl border border-slate-200 p-6">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
              <div className="flex items-center space-x-3">
                <h2 className="font-bold text-slate-900">Active Content Pipelines</h2>
                <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-0.5 rounded-full">{filteredProjects.length}</span>
              </div>
              <div className="flex bg-slate-100 p-1 rounded-lg text-xs font-semibold text-slate-600">
                {["All", "Analysis", "Design", "Develop", "Review"].map((phase) => (
                  <button
                    key={phase}
                    onClick={() => setFilterPhase(phase)}
                    className={`px-3 py-1.5 rounded-md transition-all ${filterPhase === phase ? 'bg-white text-blue-600 shadow-sm' : 'hover:text-slate-900'}`}
                  >
                    {phase}
                  </button>
                ))}
              </div>
            </div>

            {filteredProjects.length === 0 ? (
              <div className="text-center py-12 bg-slate-50 rounded-lg border border-dashed border-slate-200">
                <p className="text-slate-400 text-sm">No projects found.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {filteredProjects.map((project) => (
                  <div key={project.id} className="group border border-slate-200 hover:border-blue-200 rounded-xl p-5 bg-white transition-all hover:shadow-md relative">
                    <div className="flex justify-between items-start mb-3">
                      <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border ${
                        project.phase === 'Analysis' ? 'bg-amber-50 text-amber-700 border-amber-200' :
                        project.phase === 'Design' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                        'bg-purple-50 text-purple-700 border-purple-200'
                      }`}>
                        {project.phase}
                      </span>
                    </div>
                    <h3 className="font-bold text-slate-900 group-hover:text-blue-600 transition-colors truncate">{project.title}</h3>
                    <p className="text-xs text-slate-500 mt-1">🎯 {project.target_audience}</p>
                    
                    <div className="mt-5 space-y-1.5">
                      <div className="flex justify-between text-[10px] text-slate-400 font-bold uppercase">
                        <span>Progress</span>
                        <span>{project.progress}%</span>
                      </div>
                      <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-blue-600 h-full transition-all duration-500" style={{ width: `${project.progress}%` }}></div>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between text-[10px] text-slate-400">
                      <span>{project.objectives_count} Objectives</span>
                      <span>Updated {project.updated_at}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>

        {/* Sidebar Logs */}
        <aside className="w-full lg:w-72 space-y-4">
          <div className="bg-white border border-slate-200 rounded-xl p-6">
            <h2 className="font-bold text-slate-900 text-sm mb-4 flex items-center">
              <span className="mr-2">⚡</span> Live Audit Logs
            </h2>
            <div className="space-y-4">
              {activities.map((act) => (
                <div key={act.id} className="text-[11px] p-3 rounded-lg bg-slate-50 border border-slate-100">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-slate-800">{act.user}</span>
                    <span className="text-slate-400">{act.time}</span>
                  </div>
                  <p className="text-slate-600 line-clamp-2 mb-1">{act.action}</p>
                  <span className="text-[9px] text-blue-600 font-bold uppercase bg-blue-50 px-1.5 py-0.5 rounded">
                    ↳ {act.project}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}