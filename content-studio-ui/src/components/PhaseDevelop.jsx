import React, { useState } from 'react';
import { ArrowLeft, Settings, Plus, LayoutGrid, CheckCircle2, FileText, MousePointerClick, Zap, Eye, Image as ImageIcon, X } from 'lucide-react';

export default function PhaseDevelop() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="bg-[#13151A] text-slate-300 min-h-screen p-6 font-sans flex flex-col relative">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">eLearning - Develop</h1>
          <p className="text-sm text-slate-400">Build, enhance, and finalize your learning content.</p>
        </div>
        <div className="flex items-center gap-8">
           <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Analysis</span></div>
           <div className="w-8 h-[1px] bg-emerald-500"></div>
           <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Design</span></div>
           <div className="w-8 h-[1px] bg-slate-700"></div>
           <div className="flex items-center gap-1 text-rose-500"><div className="w-2.5 h-2.5 rounded-full bg-rose-500"></div><span className="text-xs">Develop</span></div>
          <button className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm font-medium">
            <ArrowLeft className="w-4 h-4" /> Back to Design
          </button>
        </div>
      </div>

      <div className="flex gap-6 flex-1 overflow-hidden">
        {/* Left Outline (Same as Design) */}
        <div className="w-72 bg-[#1C1E26] border border-slate-800 rounded-xl p-4 flex flex-col hidden lg:flex">
          {/* ... Omitting outline code for brevity, it's identical to PhaseDesign ... */}
          <span className="text-xs font-bold uppercase text-slate-400 mb-4">Course Outline</span>
          <div className="p-2 bg-slate-800/50 border-l-2 border-rose-500 text-white text-sm">1.2 What is Cybersecurity?</div>
        </div>

        {/* Center: Storyboard Editor */}
        <div className="flex-1 flex flex-col bg-[#1C1E26] border border-slate-800 rounded-xl overflow-hidden">
          <div className="flex border-b border-slate-800 text-sm font-medium text-slate-400">
            <button className="px-4 py-3 text-rose-500 border-b-2 border-rose-500">STORYBOARD EDITOR</button>
            <button className="px-4 py-3 hover:text-white">NOTES</button>
            <button className="px-4 py-3 hover:text-white">VERSION HISTORY</button>
          </div>

          {/* Canvas Area */}
          <div className="flex-1 bg-[#13151A] p-6 flex flex-col items-center justify-center relative">
            <div className="w-full max-w-2xl aspect-video bg-[#0A0D14] border border-slate-800 rounded-lg shadow-2xl flex items-center p-8 relative overflow-hidden">
                {/* Mock Visual from Screenshot */}
                <div className="absolute right-0 top-0 h-full w-1/2 bg-gradient-to-l from-blue-900/30 to-transparent"></div>
                <div className="relative z-10 w-1/2">
                    <h2 className="text-3xl font-bold text-white mb-4">What is<br/>Cybersecurity?</h2>
                    <div className="w-10 h-1 bg-rose-500 mb-4"></div>
                    <p className="text-xs text-slate-300 mb-4 leading-relaxed">Cybersecurity is the practice of protecting systems, networks, and data from digital attacks, unauthorized access, and damage.</p>
                </div>
                <div className="relative z-10 w-1/2 flex justify-center">
                    <div className="w-32 h-32 bg-blue-950/50 border border-blue-500/50 rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(59,130,246,0.3)]">
                        <span className="text-4xl">🔒</span>
                    </div>
                </div>
            </div>
          </div>

          {/* Properties Area */}
          <div className="h-48 border-t border-slate-800 bg-[#1C1E26] p-4">
             <div className="flex gap-4 border-b border-slate-800 pb-2 mb-4 text-xs text-slate-400">
                <span className="text-rose-500 border-b border-rose-500 pb-2">Properties</span>
                <span>Notes</span>
                <span>Accessibility</span>
             </div>
             <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="sm:col-span-2">
                    <label className="text-xs text-slate-500 block mb-1">Slide Title</label>
                    <input type="text" defaultValue="What is Cybersecurity?" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white" />
                </div>
                <div>
                    <label className="text-xs text-slate-500 block mb-1">Duration</label>
                    <input type="text" defaultValue="00:30 Sec" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white" />
                </div>
                <div>
                    <label className="text-xs text-slate-500 block mb-1">Voiceover</label>
                    <input type="text" defaultValue="Yes" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white" />
                </div>
             </div>
          </div>
        </div>

        {/* Right AI Suggestions */}
        <div className="w-80 bg-[#1C1E26] border border-slate-800 rounded-xl p-4 hidden xl:block">
           <span className="text-sm font-bold flex items-center gap-2 text-white"><Zap className="w-4 h-4 text-purple-500"/> SUGGESTIONS</span>
        </div>
      </div>

      {/* Footer */}
      <div className="flex justify-end gap-4 mt-6">
         <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm hover:bg-slate-800"><LayoutGrid className="w-4 h-4"/> Save Progress</button>
         <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm hover:bg-slate-800"><Eye className="w-4 h-4"/> Preview Storyboard</button>
         <button onClick={() => setShowModal(true)} className="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2 rounded flex items-center gap-2 text-sm font-medium"><LayoutGrid className="w-4 h-4"/> Export Content</button>
      </div>

      {/* Export Modal (Develop 2) */}
      {showModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
            <div className="bg-[#1C1E26] border border-slate-700 rounded-xl w-full max-w-4xl p-6 overflow-y-auto max-h-[90vh]">
                <div className="flex justify-between items-center mb-6">
                    <h2 className="text-xl font-bold text-white flex items-center gap-2"><Sparkles className="w-5 h-5 text-rose-500"/> Generate Storyboard</h2>
                    <button onClick={() => setShowModal(false)}><X className="text-slate-400 hover:text-white"/></button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    {[
                        {title: "Download as PDF", icon: "📄", format: "PDF"},
                        {title: "Download as Word", icon: "📝", format: "Word"},
                        {title: "Download as PPT", icon: "📊", format: "PPT"}
                    ].map((opt, i) => (
                        <div key={i} className="border border-slate-700 hover:border-rose-500 rounded-xl p-6 flex flex-col items-center text-center bg-[#13151A] cursor-pointer transition">
                            <div className="text-4xl mb-4">{opt.icon}</div>
                            <h3 className="font-bold text-white mb-4">{opt.title}</h3>
                            <ul className="text-xs text-slate-400 space-y-2 text-left w-full mb-6">
                                <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-emerald-500"/> High-quality format</li>
                                <li className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3 text-emerald-500"/> Include text, images</li>
                            </ul>
                            <button className="w-full border border-rose-500 text-rose-500 py-2 rounded flex justify-center items-center gap-2 text-sm"><CloudUpload className="w-4 h-4"/> Download {opt.format}</button>
                        </div>
                    ))}
                </div>
                <div className="flex justify-end border-t border-slate-700 pt-4">
                    <button onClick={() => setShowModal(false)} className="border border-slate-600 px-6 py-2 rounded text-white text-sm hover:bg-slate-800">Cancel</button>
                </div>
            </div>
        </div>
      )}
    </div>
  );
}