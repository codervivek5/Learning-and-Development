import React from 'react';
import { ArrowLeft, Settings, Plus, LayoutGrid, CheckCircle2, FileText, MousePointerClick, Zap } from 'lucide-react';

export default function PhaseDesign() {
  return (
    <div className="bg-[#13151A] text-slate-300 min-h-screen p-6 font-sans flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">eLearning - Design</h1>
          <p className="text-sm text-slate-400">Design engaging learning experience with AI-powered assistance.</p>
        </div>
        <div className="flex flex-wrap items-center gap-4 md:gap-8 mt-4 md:mt-0">
           {/* Stepper logic similar to analysis */}
           <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Analysis</span></div>
           <div className="w-8 h-[1px] bg-slate-700"></div>
           <div className="flex items-center gap-1 text-rose-500"><div className="w-2.5 h-2.5 rounded-full bg-rose-500"></div><span className="text-xs">Design</span></div>
           <div className="w-8 h-[1px] bg-slate-700"></div>
           <div className="flex items-center gap-1 text-slate-500 hidden sm:flex"><div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div><span className="text-xs">Develop</span></div>
          <button className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm font-medium">
            <ArrowLeft className="w-4 h-4" /> Back to Analysis
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 flex-1 overflow-hidden">
        {/* Left: Outline */}
        <div className="w-full lg:w-72 bg-[#1C1E26] border border-slate-800 rounded-xl p-4 flex flex-col h-[300px] lg:h-auto">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Course Outline</span>
            <div className="flex gap-2"><Settings className="w-4 h-4 text-slate-400"/><Plus className="w-4 h-4 text-slate-400"/></div>
          </div>
          <div className="space-y-4 overflow-y-auto flex-1 text-sm">
            <div>
              <div className="flex items-center gap-2 text-white font-medium mb-2"><div className="w-4 h-4 bg-rose-500/20 rounded flex items-center justify-center"><LayoutGrid className="w-2 h-2 text-rose-500"/></div> Module 1: Introduction</div>
              <div className="pl-6 space-y-2 text-slate-400 border-l border-slate-800 ml-2">
                <div className="flex items-center gap-2"><FileText className="w-3 h-3"/> 1.1 Welcome</div>
                <div className="flex items-center gap-2 text-white bg-slate-800/50 py-1 px-2 rounded -ml-2"><FileText className="w-3 h-3 text-rose-500"/> 1.2 What is Cybersecurity?</div>
                <div className="flex items-center gap-2"><FileText className="w-3 h-3"/> 1.3 Why its Matters</div>
                <div className="flex items-center gap-2"><CheckCircle2 className="w-3 h-3"/> 1.4 Knowledge Check</div>
              </div>
            </div>
            {/* Mock other modules */}
            {['Module 2: Common Threats', 'Module 3: Safe Online Practices', 'Module 4: Data Protection'].map(m => (
              <div key={m} className="flex items-center gap-2 text-slate-400 font-medium"><div className="w-4 h-4 bg-slate-800 rounded flex items-center justify-center"><LayoutGrid className="w-2 h-2 text-slate-500"/></div> {m}</div>
            ))}
          </div>
          <button className="mt-4 w-full border border-rose-500/50 text-rose-500 py-2 rounded text-sm hover:bg-rose-500/10 transition">+ Add Module</button>
        </div>

        {/* Center: Workspace */}
        <div className="flex-1 bg-[#1C1E26] border border-slate-800 rounded-xl flex flex-col">
          <div className="px-4 py-2 border-b border-slate-800 flex items-center gap-4 text-slate-400 text-sm">
            <span>Heading 2 ▼</span>
            <div className="flex gap-2"><b>B</b> <i>I</i> <u>U</u> <s>S</s></div>
            <div className="w-px h-4 bg-slate-700"></div>
            <span>🔗</span>
          </div>
          <div className="p-8 flex-1 overflow-y-auto prose prose-invert max-w-none text-sm text-slate-300">
            <h1 className="text-2xl text-white font-bold mb-4">1.2 What is Cybersecurity?</h1>
            <h2 className="text-blue-400 font-medium text-lg mt-6 mb-2">1.2.1 Overview</h2>
            <p className="mb-6">Cybersecurity is the practice of protecting systems, network, and data from digital attacks, unauthorized access, and damage...</p>

            <h2 className="text-blue-400 font-medium text-lg mt-6 mb-2">1.2.2 Key Topics</h2>
            <ul className="list-disc pl-5 mb-6 space-y-1">
              <li>Definition of Cybersecurity</li>
              <li>The CIA Triad (Confidentiality, Integrity, Availability)</li>
              <li>Examples of Cyber Threats</li>
            </ul>

            <h2 className="text-blue-400 font-medium text-lg mt-6 mb-2">1.2.3 Learning Flow</h2>
            <table className="w-full text-left border-collapse border border-slate-700">
              <thead><tr className="bg-slate-800"><th className="p-2 border border-slate-700">Step</th><th className="p-2 border border-slate-700">Learning Activity</th><th className="p-2 border border-slate-700">Instructional Notes</th><th className="p-2 border border-slate-700">Duration</th></tr></thead>
              <tbody>
                <tr><td className="p-2 border border-slate-700">1</td><td className="p-2 border border-slate-700">Introduce the concept</td><td className="p-2 border border-slate-700">Use real-life analogy</td><td className="p-2 border border-slate-700">1 min</td></tr>
                <tr><td className="p-2 border border-slate-700">2</td><td className="p-2 border border-slate-700">Explain CIA Triad</td><td className="p-2 border border-slate-700">Media / Illustration</td><td className="p-2 border border-slate-700">1 min</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Right: AI Suggestions */}
        <div className="w-full lg:w-80 bg-[#1C1E26] border border-slate-800 rounded-xl p-4 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-bold flex items-center gap-2 text-white"><Zap className="w-4 h-4 text-purple-500"/> INTERACTIVITY</span>
            <span className="text-[10px] text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded">AI Powered</span>
          </div>
          <p className="text-xs text-slate-500 mb-4">Based on your content, we recommend:</p>
          <div className="space-y-3 overflow-y-auto">
            {[{icon: FileText, title: 'Knowledge Check (MCQ)', desc: 'Add a 3-question quiz'}, {icon: MousePointerClick, title: 'Drag and Drop', desc: 'Use to match components'}].map((item,i) => (
              <div key={i} className="bg-[#13151A] border border-slate-800 p-3 rounded-lg flex flex-col gap-2">
                <div className="flex items-center gap-2 text-slate-300 font-medium text-sm"><item.icon className="w-4 h-4"/> {item.title}</div>
                <p className="text-[10px] text-slate-500">{item.desc}</p>
                <button className="self-end border border-slate-600 text-xs px-3 py-1 rounded hover:bg-slate-800">Add</button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Footer Actions */}
      <div className="flex justify-end gap-4 mt-6">
         <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm hover:bg-slate-800"><LayoutGrid className="w-4 h-4"/> Save Progress</button>
         <button className="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2 rounded flex items-center gap-2 text-sm font-medium"><LayoutGrid className="w-4 h-4"/> Generate Content</button>
      </div>
    </div>
  );
}