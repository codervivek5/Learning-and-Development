import { useState, useRef } from 'react';
import { CloudUpload, FileText, Check, Edit2, Trash2, LayoutGrid, ArrowLeft, Sparkles, Type, X } from 'lucide-react';
import { projectApi } from '../services/api';
import PhaseStepper from './PhaseStepper';

export default function PhaseAnalysis({ onAdvancePipeline }) {
  const [title, setTitle] = useState("New Cybersecurity Course");
  const [description, setDescription] = useState("Employees across all departments including IT, Finance, HR.");
  const [objectives, setObjectives] = useState([]);
  const [newObjective, setNewObjective] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const fileInputRef = useRef(null);
  
  // State for the raw input content you mentioned
  const [contentSource, setContentSource] = useState('raw_input'); // 'file' or 'raw_input'
  const [rawContent, setRawContent] = useState("Learn how to build a REST API using FastAPI.");

  const handleStartAnalysis = async () => {
    setIsSubmitting(true);
    try {
      const result = await projectApi.create(title, description);
      onAdvancePipeline(result); // Moves to Design Phase
    } catch (err) {
      alert("Error starting analysis: " + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle file uploads
  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    files.forEach(file => {
      const fileObj = {
        id: Date.now() + Math.random(),
        name: file.name,
        size: (file.size / (1024 * 1024)).toFixed(2),
        type: file.name.split('.').pop().toUpperCase(),
        status: 'Completed'
      };
      setUploadedFiles(prev => [...prev, fileObj]);
    });
  };

  const handleDragDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const files = Array.from(e.dataTransfer.files);
    files.forEach(file => {
      const fileObj = {
        id: Date.now() + Math.random(),
        name: file.name,
        size: (file.size / (1024 * 1024)).toFixed(2),
        type: file.name.split('.').pop().toUpperCase(),
        status: 'Completed'
      };
      setUploadedFiles(prev => [...prev, fileObj]);
    });
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
  };

  // New function to call your AI service
  const handleGenerateAIObjectives = async () => {
    if (!rawContent.trim()) return alert("Please enter some content first.");
    
    setIsGenerating(true);
    try {
      // Note: In a real flow, we'd create the project first or use a temp ID
      // For now, we'll pass a dummy ID or the ID of the project being created
      const result = await projectApi.generateAIObjectives(999, contentSource, rawContent);
      if (result.objectives) {
        setObjectives(result.objectives);
      }
    } catch (err) {
      console.error("AI Generation Error:", err);
    } finally {
      setIsGenerating(false);
    }
  };

  const addObjective = () => {
    if(newObjective.trim()) {
      setObjectives([...objectives, newObjective]);
      setNewObjective("");
    }
  };

  return (
    <div className="bg-[#13151A] text-slate-300 min-h-screen p-4 md:p-6 font-sans">
      {/* Header & Stepper */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 md:gap-8 mb-8">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-white mb-1">eLearning - Analysis</h1>
          <p className="text-sm text-slate-400">Understand goals, audience, content requirements, and learning objectives.</p>
        </div>
        <div className="w-full md:w-auto flex flex-col sm:flex-row items-start sm:items-center gap-4">
          <PhaseStepper currentPhase="analysis" hideOnMobile={false} />
          <button className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm font-medium transition-colors whitespace-nowrap w-full sm:w-auto justify-center">
            <ArrowLeft className="w-4 h-4" /> Back
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {/* Section 1: Content Upload */}
        <div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
            <h2 className="text-white font-semibold flex items-center gap-2">1. Content Source <span className="text-slate-500 text-xs">ⓘ</span></h2>
            <div className="flex bg-[#1C1E26] p-1 rounded-lg border border-slate-800 w-full sm:w-auto">
              <button 
                onClick={() => setContentSource('file')}
                className={`flex-1 sm:flex-none px-3 py-1 rounded text-xs flex items-center justify-center gap-2 transition-colors ${contentSource === 'file' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-white'}`}
              >
                <CloudUpload className="w-3 h-3"/> Files
              </button>
              <button 
                onClick={() => setContentSource('raw_input')}
                className={`flex-1 sm:flex-none px-3 py-1 rounded text-xs flex items-center justify-center gap-2 transition-colors ${contentSource === 'raw_input' ? 'bg-slate-800 text-white' : 'text-slate-500 hover:text-white'}`}
              >
                <Type className="w-3 h-3"/> Raw Text
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {contentSource === 'file' ? (
              <div 
                onDragOver={(e) => { e.preventDefault(); }}
                onDrop={handleDragDrop}
                className="bg-[#1C1E26] border-2 border-slate-800 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center hover:border-rose-500/50 transition-colors"
              >
                <CloudUpload className="w-12 h-12 text-rose-500/60 mb-3" />
                <p className="text-white font-medium mb-1">Drag & Drop files here</p>
                <p className="text-xs text-slate-500 mb-4">or</p>
                <input 
                  ref={fileInputRef}
                  type="file"
                  multiple
                  onChange={handleFileSelect}
                  className="hidden"
                  accept=".pdf,.doc,.docx,.ppt,.pptx,.txt"
                />
                <button 
                  onClick={() => fileInputRef.current?.click()}
                  className="border border-rose-500 text-rose-500 px-4 py-1.5 rounded text-sm hover:bg-rose-500/10 transition"
                >
                  Browse Files
                </button>
              </div>
            ) : (
              <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-4 flex flex-col">
                <textarea 
                  value={rawContent}
                  onChange={(e) => setRawContent(e.target.value)}
                  placeholder="Paste your source text or curriculum notes here..."
                  className="w-full h-32 bg-[#13151A] border border-slate-700 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-rose-500 resize-none"
                />
                <button 
                  onClick={handleGenerateAIObjectives}
                  disabled={isGenerating}
                  className="mt-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-900 text-white text-xs font-bold py-2 rounded-lg flex items-center justify-center gap-2 transition-all active:scale-95"
                >
                  <Sparkles className={`w-3 h-3 ${isGenerating ? 'animate-spin' : ''}`} />
                  {isGenerating ? "AI is Analyzing..." : "Generate Objectives from Text"}
                </button>
              </div>
            )}

            <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-white font-medium text-sm">Uploaded Files ({uploadedFiles.length})</span>
                {uploadedFiles.length > 0 && (
                  <button className="text-rose-500 text-xs hover:text-rose-400">Clear All</button>
                )}
              </div>
              <div className="space-y-3 max-h-48 overflow-y-auto">
                {uploadedFiles.length === 0 ? (
                  <p className="text-xs text-slate-500">No files uploaded yet</p>
                ) : (
                  uploadedFiles.map((file) => (
                    <div key={file.id} className="flex items-center justify-between p-3 bg-[#13151A] rounded-lg">
                      <div className="flex items-center gap-3 flex-1 min-w-0">
                        <div className="bg-rose-500/20 p-2 rounded flex-shrink-0"><FileText className="w-4 h-4 text-rose-500" /></div>
                        <div className="min-w-0 flex-1">
                          <p className="text-sm text-white font-medium truncate">{file.name}</p>
                          <p className="text-xs text-slate-500">{file.size} MB • {file.type}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2 flex-shrink-0">
                        <span className="text-emerald-500 text-xs font-medium">✓</span>
                        <button 
                          onClick={() => removeFile(file.id)}
                          className="text-slate-500 hover:text-rose-500 p-1 transition"
                        >
                          <X className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Target Audience */}
        <div>
          <h2 className="text-white font-semibold mb-1 flex items-center gap-2">2. Target Audience Description <span className="text-slate-500 text-xs">ⓘ</span></h2>
          <p className="text-xs text-slate-400 mb-4">Provide details about your learners to help AI generate relevant objectives.</p>
          <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="space-y-1">
                <label className="text-xs text-slate-400">Project Title <span className="text-rose-500">*</span></label>
                <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500" />
              </div>
              <div className="space-y-1">
                <label className="text-xs text-slate-400">Target Audience <span className="text-rose-500">*</span></label>
                <input type="text" value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500" />
              </div>
              <div className="space-y-1">
                <label className="text-xs text-slate-400">Knowledge Level <span className="text-rose-500">*</span></label>
                <select className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500"><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select>
              </div>
              <div className="space-y-1">
                <label className="text-xs text-slate-400">Environment <span className="text-rose-500">*</span></label>
                <select className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500"><option>Self-paced</option><option>Instructor-led</option><option>Hybrid</option></select>
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Learning Objectives */}
        <div>
          <h2 className="text-white font-semibold mb-1 flex items-center gap-2">3. Learning Objectives <span className="text-slate-500 text-xs">ⓘ</span></h2>
          <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
            <div className="space-y-3">
              {objectives.map((obj, i) => (
                <div key={i} className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-3 gap-3">
                  <div className="flex gap-4 items-start flex-1">
                    <span className="text-slate-500">{i+1}</span>
                    <span className="text-sm text-white">{obj}</span>
                  </div>
                  <div className="flex gap-2 sm:shrink-0 justify-end">
                    <button className="flex items-center gap-1 border border-emerald-500/50 text-emerald-500 px-2 py-1 rounded text-xs hover:bg-emerald-500/10"><Check className="w-3 h-3"/> Accept</button>
                    <button className="flex items-center gap-1 border border-slate-600 text-slate-300 px-2 py-1 rounded text-xs hover:bg-slate-700"><Edit2 className="w-3 h-3"/> Edit</button>
                    <button className="flex items-center gap-1 border border-rose-500/50 text-rose-500 px-2 py-1 rounded text-xs hover:bg-rose-500/10"><Trash2 className="w-3 h-3"/> Discard</button>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 flex gap-3">
              <input value={newObjective} onChange={e => setNewObjective(e.target.value)} type="text" placeholder="Type your custom objective here..." className="flex-1 bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500" />
              <button onClick={addObjective} className="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2 rounded text-sm transition-colors">Add</button>
            </div>
          </div>
        </div>

        {/* Bottom Actions */}
        <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-3 pt-4 border-t border-slate-800">
          <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center justify-center gap-2 text-sm hover:bg-slate-800 transition">
            <LayoutGrid className="w-4 h-4"/> Save Progress
          </button>
          <button 
            onClick={handleStartAnalysis}
            disabled={isSubmitting}
            className="bg-rose-500 hover:bg-rose-600 disabled:bg-rose-900 text-white px-6 py-2 rounded flex items-center justify-center gap-2 text-sm font-medium transition-all"
          >
            <Sparkles className={`w-4 h-4 ${isSubmitting ? 'animate-spin' : ''}`}/> 
            {isSubmitting ? 'Processing AI...' : 'Start AI Analysis'}
          </button>
        </div>
      </div>
    </div>
  );
}