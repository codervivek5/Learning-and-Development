import { useState, useMemo, useEffect } from 'react';
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
  Analysis: 'bg-amber-500/20 text-amber-400 border-amber-500/30',
  Design: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30',
  Develop: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  Review: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  Default: 'bg-slate-500/20 text-slate-400 border-slate-500/30'
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
      color: 'bg-rose-600',
      icon: Folder
    },
    {
      id: 2,
      name: 'In Progress',
      count: projects.filter(p => p.phase !== 'Review').length,
      change: 'Active Development',
      color: 'bg-amber-600',
      icon: Timer
    },
    {
      id: 3,
      name: 'Review Phase',
      count: projects.filter(p => p.phase === 'Review').length,
      change: 'Needs Attention',
      color: 'bg-emerald-600',
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
    } catch (error) {
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="relative w-full sm:flex-1 sm:max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-[#1C1E26] border border-slate-800 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-transparent"
          />
        </div>
        <button
          onClick={handleCreateProject}
          className="w-full sm:w-auto bg-rose-600 hover:bg-rose-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-all active:scale-95 flex items-center justify-center gap-2"
        >
          <Plus className="w-4 h-4" /> Create New
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
              <div key={item.id} className="bg-[#1C1E26] rounded-xl p-5 border border-slate-800 flex items-start space-x-4">
                <div className={`h-10 w-10 rounded-lg ${item.color} flex items-center justify-center text-white`}>
                  <item.icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-slate-400">{item.name}</p>
                  <p className="text-2xl font-bold text-white mt-0.5">{item.count}</p>
                  <span className="text-xs font-medium text-rose-400 inline-block bg-rose-500/10 px-2 py-0.5 rounded mt-2">{item.change}</span>
                </div>
              </div>
            ))}
          </section>

          <section className="bg-[#1C1E26] rounded-xl border border-slate-800 p-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-6">
              <div className="flex items-center space-x-3">
                <h2 className="font-bold text-white">Active Pipelines</h2>
                <span className="bg-slate-800 text-slate-300 text-xs font-bold px-2 py-0.5 rounded-full">{filteredProjects.length}</span>
              </div>
              <div className="flex bg-[#13151A] p-1 rounded-lg text-xs font-semibold text-slate-400 overflow-x-auto">
                {PHASES.map((phase) => (
                  <button
                    key={phase}
                    onClick={() => setFilterPhase(phase)}
                    className={`px-3 py-1.5 rounded-md transition-all whitespace-nowrap ${filterPhase === phase ? 'bg-slate-800 text-rose-400' : 'hover:text-slate-300'}`}
                  >
                    {phase}
                  </button>
                ))}
              </div>
            </div>

            {filteredProjects.length === 0 ? (
              <div className="text-center py-12 bg-[#13151A] rounded-lg border border-dashed border-slate-800">
                <AlertCircle className="w-8 h-8 text-slate-700 mx-auto mb-2" />
                <p className="text-slate-500 text-sm">No projects found.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {filteredProjects.map((project) => (
                  <div key={project.id} className="group border border-slate-800 hover:border-rose-500/50 rounded-xl p-5 bg-[#13151A] transition-all hover:bg-[#1a1d24] cursor-pointer">
                    <div className="flex justify-between items-start mb-3 gap-2">
                      <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border whitespace-nowrap ${PHASE_STYLES[project.phase] || PHASE_STYLES.Default}`}>
                        {project.phase}
                      </span>
                    </div>
                    <h3 className="font-bold text-slate-100 group-hover:text-rose-400 transition-colors truncate text-sm">{project.title}</h3>
                    <p className="text-xs text-slate-500 mt-1 flex items-center gap-1 line-clamp-1">
                      <Target className="w-3 h-3 flex-shrink-0" /> {project.description || "No description"}
                    </p>

                    <div className="mt-5 space-y-1.5">
                      <div className="flex justify-between text-[10px] text-slate-500 font-bold uppercase">
                        <span>Progress</span>
                        <span>{project.progress || 0}%</span>
                      </div>
                      <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                        <div className="bg-rose-600 h-full transition-all duration-500" style={{ width: `${project.progress || 0}%` }}></div>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-500">
                      <span className="flex items-center gap-1"><Zap className="w-3 h-3" /> {project.objectives_count || 0} Goals</span>
                      <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {project.updated_at || "Recently"}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>
          </>
          )}
        </div>

        
      </div>
    </div>
  );
}