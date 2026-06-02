import React, { useState, useMemo, useEffect } from 'react';
import {
  Search,
  Plus,
  Folder,
  Timer,
  CheckCircle2,
  Target,
  Zap,
  Clock,
  AlertCircle
} from 'lucide-react';
import { projectApi } from '../../services/api';

const PHASES = ["All", "Analysis", "Design", "Develop", "Review"];

const PHASE_STYLES = {
  Analysis: 'bg-amber-50 text-amber-700 border-amber-200',
  Design: 'bg-indigo-50 text-indigo-700 border-indigo-200', // Changed to Indigo
  Develop: 'bg-purple-50 text-purple-700 border-purple-200',
  Review: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Default: 'bg-slate-50 text-slate-700 border-slate-200'
};

const INITIAL_ACTIVITIES = [
  { id: 1, user: "System AI", action: "Generated structured curriculum skeleton", project: "Bootcamp", time: "10m ago" },
  { id: 2, user: "Admin User", action: "Approved Phase 1 Needs Analysis", project: "Cybersecurity", time: "2h ago" },
  { id: 3, user: "System AI", action: "Compiled storyboard interactivity paths", project: "Prompt Eng.", time: "1d ago" },
];

export default function PhaseOverview() {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activities, setActivities] = useState(INITIAL_ACTIVITIES);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterPhase, setFilterPhase] = useState("All");

  // Fetch projects from Backend
  useEffect(() => {
    const loadProjects = async () => {
      try {
        const data = await projectApi.getAll();
        setProjects(data);
      } catch (err) {
        console.error("Connection Error:", err);
      } finally {
        setIsLoading(false);
      }
    };
    loadProjects();
  }, []);

  // Derived Statistics - Keeps counts in sync with the actual project list
  const stats = useMemo(() => [
    {
      id: 1,
      name: 'Total Projects',
      count: projects.length,
      change: '+2 this week',
      color: 'bg-indigo-500', // Changed to Indigo
      icon: Folder
    },
    {
      id: 2,
      name: 'In Progress',
      count: projects.filter(p => p.phase !== 'Review').length,
      change: 'Active Development',
      color: 'bg-amber-500',
      icon: Timer
    },
    {
      id: 3,
      name: 'Review Phase',
      count: projects.filter(p => p.phase === 'Review').length,
      change: 'Needs Attention',
      color: 'bg-emerald-500',
      icon: CheckCircle2
    },
  ], [projects]);

  const handleCreateProject = async () => {
    try {
      const newProj = await projectApi.create(
        `AI Project #${projects.length + 1}`,
        "Generated course via Dashboard"
      );
      
      setProjects([newProj, ...projects]);
      setActivities([
        { id: Date.now(), user: "Admin User", action: "Initiated a new course workspace", project: newProj.title, time: "Just now" },
        ...activities
      ]);
    } catch (err) {
      alert("Check if Backend server is running!");
    }
  };

  const filteredProjects = useMemo(() => projects.filter(proj => {
    const matchesSearch = proj.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      proj.target_audience.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPhase = filterPhase === "All" || proj.phase === filterPhase;
    return matchesSearch && matchesPhase;
  }), [projects, searchQuery, filterPhase]);

  return (
    <div className="flex flex-col space-y-8">
      {/* Search and Create Action */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="relative w-full md:flex-1 md:max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" // Changed focus to Indigo
          />
        </div>
        <button
          onClick={handleCreateProject}
          className="w-full md:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm px-4 py-2 rounded-lg shadow-sm transition-all active:scale-95 flex items-center justify-center gap-2" // Changed bg to Indigo
        >
          <Plus className="w-4 h-4" /> Create New Project
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Main Content */}
        <div className="flex-1 space-y-8">
          {isLoading ? (
            <div className="h-64 flex flex-col items-center justify-center text-slate-500 gap-4">
              <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
              <p className="text-sm font-mono animate-pulse">Syncing with Node API...</p>
            </div>
          ) : (
            <>
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {stats.map((item) => (
              <div key={item.id} className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex items-start space-x-4">
                <div className={`h-10 w-10 rounded-lg ${item.color} flex items-center justify-center text-white text-lg`}>
                  <item.icon className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-500">{item.name}</p>
                  <p className="text-2xl font-bold text-slate-900 mt-0.5">{item.count}</p>
                  <span className="text-xs font-medium text-indigo-600 inline-block bg-indigo-50 px-2 py-0.5 rounded mt-2">{item.change}</span> {/* Changed to Indigo */}
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
                {PHASES.map((phase) => (
                  <button
                    key={phase}
                    onClick={() => setFilterPhase(phase)}
                    className={`px-3 py-1.5 rounded-md transition-all ${filterPhase === phase ? 'bg-white text-indigo-600 shadow-sm' : 'hover:text-slate-900'}`} // Changed text to Indigo
                  >
                    {phase}
                  </button>
                ))}
              </div>
            </div>

            {filteredProjects.length === 0 ? (
              <div className="text-center py-12 bg-slate-50 rounded-lg border border-dashed border-slate-200">
                <AlertCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                <p className="text-slate-400 text-sm">No projects found.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                {filteredProjects.map((project) => (
                  <div key={project.id} className="group border border-slate-200 hover:border-indigo-200 rounded-xl p-5 bg-white transition-all hover:shadow-md relative"> {/* Changed hover border to Indigo */}
                    <div className="flex justify-between items-start mb-3">
                      <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border ${PHASE_STYLES[project.phase] || PHASE_STYLES.Default}`}>
                        {project.phase}
                      </span>
                    </div>
                    <h3 className="font-bold text-slate-900 group-hover:text-indigo-600 transition-colors truncate">{project.title}</h3> {/* Changed hover text to Indigo */}
                    <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                      <Target className="w-3 h-3" /> {project.description || "No description provided"}
                    </p>

                    <div className="mt-5 space-y-1.5">
                      <div className="flex justify-between text-[10px] text-slate-400 font-bold uppercase">
                        <span>Progress</span>
                        <span>{project.progress || 0}%</span>
                      </div>
                      <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-indigo-600 h-full transition-all duration-500" style={{ width: `${project.progress || 0}%` }}></div> {/* Changed progress bar to Indigo */}
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-50 flex items-center justify-between text-[10px] text-slate-400">
                      <span className="flex items-center gap-1"><Zap className="w-3 h-3" /> {project.objectives_count} Objectives</span>
                      <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {project.updated_at}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
          </>
          )}
        </div>

        {/* Sidebar Logs */}
        <aside className="w-full lg:w-72 space-y-4">
          <div className="bg-white border border-slate-200 rounded-xl p-6">
            <h2 className="font-bold text-slate-900 text-sm mb-4 flex items-center">
              <Zap className="w-4 h-4 mr-2 text-amber-500" /> Live Audit Logs
            </h2>
            <div className="space-y-4">
              {activities.map((act) => (
                <div key={act.id} className="text-[11px] p-3 rounded-lg bg-slate-50 border border-slate-100">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-slate-800">{act.user}</span>
                    <span className="text-slate-400">{act.time}</span>
                  </div>
                  <p className="text-slate-600 line-clamp-2 mb-1">{act.action}</p>
                  <span className="text-[9px] text-indigo-600 font-bold uppercase bg-indigo-50 px-1.5 py-0.5 rounded"> {/* Changed log tag to Indigo */}
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