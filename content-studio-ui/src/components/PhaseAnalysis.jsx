import React, { useState } from 'react';
import { CloudUpload, FileText, Check, Edit2, Trash2, LayoutGrid, ArrowLeft } from 'lucide-react';
import { projectApi } from '../services/api';

export default function PhaseAnalysis({ onAdvancePipeline }) {
  const [title, setTitle] = useState("New Cybersecurity Course");
  const [description, setDescription] = useState("Employees across all departments including IT, Finance, HR.");
  const [objectives, setObjectives] = useState([
    "Understand key cybersecurity threats such as phishing, malware, ransomware, and social engineering.",
    "Identify best practices for maintaining strong passwords and protecting sensitive information.",
    "Apply safe browsing techniques and recognize suspicious websites and links.",
    "Understand data privacy principles and compliance requirements.",
    "Respond appropriately to security incidents and report potential threats."
  ]);
  const [newObjective, setNewObjective] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  const addObjective = () => {
    if(newObjective.trim()) {
      setObjectives([...objectives, newObjective]);
      setNewObjective("");
    }
  };

  return (
    <div className="bg-[#13151A] text-slate-300 min-h-screen p-6 font-sans">
      {/* Header & Stepper */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">eLearning - Analysis</h1>
          <p className="text-sm text-slate-400">Understand goals, audience, content requirements, and learning objectives.</p>
        </div>
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1 text-rose-500"><div className="w-2.5 h-2.5 rounded-full bg-rose-500"></div><span className="text-xs">Analysis</span></div>
            <div className="w-8 h-[1px] bg-slate-700"></div>
            <div className="flex items-center gap-1 text-slate-500"><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><span className="text-xs">Design</span></div>
            <div className="w-8 h-[1px] bg-slate-700"></div>
            <div className="flex items-center gap-1 text-slate-500"><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><span className="text-xs">Develop</span></div>
            <div className="w-8 h-[1px] bg-slate-700"></div>
            <div className="flex items-center gap-1 text-slate-500"><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><span className="text-xs">Review</span></div>
          </div>
          <button className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm font-medium transition-colors">
            <ArrowLeft className="w-4 h-4" /> Back to Project Overview
          </button>
        </div>
      </div>

      <div className="space-y-6">
        {/* Section 1: Content Upload */}
        <div>
          <h2 className="text-white font-semibold mb-3 flex items-center gap-2">1. Content Upload <span className="text-slate-500 text-xs">ⓘ</span></h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-[#1C1E26] border border-slate-800 border-dashed rounded-xl p-8 flex flex-col items-center justify-center text-center">
              <CloudUpload className="w-10 h-10 text-rose-500 mb-3" />
              <p className="text-white font-medium mb-1">Drag & Drop files here</p>
              <p className="text-slate-500 text-sm mb-4">or</p>
              <button className="border border-rose-500 text-rose-500 px-4 py-1.5 rounded text-sm hover:bg-rose-500/10 transition">Browse Files</button>
              <div className="mt-6 flex items-center gap-2 text-xs text-slate-500">
                <span>Supported formats:</span>
                {['PDF','PPTX','DOCX','MP4','TXT','...'].map(f => <span key={f} className="bg-rose-500/20 text-rose-400 px-1.5 py-0.5 rounded">{f}</span>)}
              </div>
            </div>
            <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-white font-medium">Uploaded Files (3)</span>
                <button className="text-rose-500 text-sm">Manage All</button>
              </div>
              <div className="space-y-3">
                {['Cybersecurity_Policy_Guide.pdf', 'IT_Security_Best_Practices.docx', 'Cybersecurity_Stats_2025.pptx'].map((file, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-[#13151A] rounded-lg">
                    <div className="flex items-center gap-3">
                      <div className="bg-rose-500/20 p-2 rounded"><FileText className="w-4 h-4 text-rose-500" /></div>
                      <div>
                        <p className="text-sm text-white font-medium">{file}</p>
                        <p className="text-xs text-slate-500">{1.2 * (i+1)} MB • {file.split('.')[1].toUpperCase()}</p>
                      </div>
                    </div>
                    <span className="text-emerald-500 text-xs font-medium">Completed</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Target Audience */}
        <div>
          <h2 className="text-white font-semibold mb-1 flex items-center gap-2">2. Target Audience Description <span className="text-slate-500 text-xs">ⓘ</span></h2>
          <p className="text-xs text-slate-400 mb-4">Provide details about your learners to help AI generate relevant objectives.</p>
          <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Project Title <span className="text-rose-500">*</span></label>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500" />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Target Audience Description <span className="text-rose-500">*</span></label>
              <input type="text" value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none focus:border-rose-500" />
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Prior Knowledge Level <span className="text-rose-500">*</span></label>
              <select className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none"><option>Select</option></select>
            </div>
            <div className="space-y-1">
              <label className="text-xs text-slate-400">Learning Environment <span className="text-rose-500">*</span></label>
              <select className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white focus:outline-none"><option>Self-paced (Online)</option></select>
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
        <div className="flex justify-between items-center pt-4">
          <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm hover:bg-slate-800"><LayoutGrid className="w-4 h-4"/> Save Progress</button>
          <button 
            onClick={handleStartAnalysis}
            disabled={isSubmitting}
            className="bg-rose-500 hover:bg-rose-600 disabled:bg-rose-900 text-white px-6 py-2 rounded flex items-center gap-2 text-sm font-medium transition-all"
          >
            <LayoutGrid className={`w-4 h-4 ${isSubmitting ? 'animate-spin' : ''}`}/> 
            {isSubmitting ? 'Processing AI...' : 'Start AI Analysis'}
          </button>
        </div>
      </div>
    </div>
  );
}