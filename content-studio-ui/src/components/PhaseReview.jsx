import React from 'react';
// FIX: Added 'Check' to the import list
import { ArrowLeft, BookOpen, Calendar, Mail, FileCheck, Check } from 'lucide-react';

export default function PhaseReview() {
  return (
    <div className="bg-[#13151A] text-slate-300 min-h-screen p-6 font-sans flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-white mb-1">eLearning - Review</h1>
          <p className="text-sm text-slate-400">Share your learning with reviewers and collect feedback.</p>
        </div>
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Analysis</span></div>
          <div className="w-8 h-[1px] bg-emerald-500"></div>
          <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Design</span></div>
          <div className="w-8 h-[1px] bg-emerald-500"></div>
          <div className="flex items-center gap-1 text-emerald-500"><div className="w-2.5 h-2.5 rounded-full bg-emerald-500"></div><span className="text-xs">Develop</span></div>
          <div className="w-8 h-[1px] bg-slate-700"></div>
          <div className="flex items-center gap-1 text-rose-500"><div className="w-2.5 h-2.5 rounded-full bg-rose-500"></div><span className="text-xs">Review</span></div>
          <button className="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm font-medium">
            <ArrowLeft className="w-4 h-4" /> Back to Develop
          </button>
        </div>
      </div>

      <div className="flex gap-6 flex-1">
        {/* Left Column: Outline & Summary */}
        <div className="w-72 flex flex-col gap-6">
          <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-4">
            <span className="text-xs font-bold uppercase text-slate-400 mb-4 block">Course Outline</span>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="flex justify-between"><span>Module 1: Intro...</span> <div className="w-4 h-4 rounded-full bg-emerald-500 flex items-center justify-center"><Check className="w-3 h-3 text-white" /></div></div>
              <div className="flex justify-between"><span>Module 2: Threats</span> <div className="w-4 h-4 rounded-full bg-emerald-500 flex items-center justify-center"><Check className="w-3 h-3 text-white" /></div></div>
            </div>
          </div>

          <div className="bg-[#1C1E26] border border-slate-800 rounded-xl p-4">
            <span className="text-xs font-bold uppercase text-slate-400 mb-4 block">Review Summary</span>
            <div className="space-y-3 text-sm text-slate-300">
              <div className="flex justify-between items-center"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-slate-500"></span> Not Started</span> <span>1</span></div>
              <div className="flex justify-between items-center"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-blue-500"></span> In Review</span> <span>2</span></div>
              <div className="flex justify-between items-center"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-amber-500"></span> In Review Fixes</span> <span>1</span></div>
              <div className="flex justify-between items-center"><span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> Approved</span> <span>1</span></div>
            </div>
          </div>

          <div className="bg-rose-500/10 border border-rose-500/20 rounded-xl p-4">
            <h4 className="text-white font-bold mb-2">NEED HELP?</h4>
            <p className="text-xs text-slate-400 mb-4">Learn how reviews work and best practices for feedback</p>
            <button className="bg-rose-500 text-white text-xs px-4 py-2 rounded">View Guide</button>
          </div>
        </div>

        {/* Center/Right: Share and Progress */}
        <div className="flex-1 flex flex-col gap-6">
          <div className="flex gap-6">
            {/* Share Form */}
            <div className="flex-1 bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
              <h3 className="text-sm font-bold uppercase text-white mb-6">SHARE FOR REVIEW</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs text-slate-400 block mb-1">eLearning Name <span className="text-rose-500">*</span></label>
                  <select className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white"><option>Select eLearning</option></select>
                </div>
                <div>
                  <label className="text-xs text-slate-400 block mb-1">eLearning Link <span className="text-rose-500">*</span></label>
                  <input type="text" placeholder="Please enter link here" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white" />
                </div>
                <div>
                  <label className="text-xs text-slate-400 block mb-1">Reviewer Email <span className="text-rose-500">*</span></label>
                  <div className="relative">
                    <Mail className="absolute left-2 top-2.5 w-4 h-4 text-slate-500" />
                    <input type="email" placeholder="Enter email" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 pl-8 text-sm text-white" />
                  </div>
                </div>
                <div className="flex items-end gap-4">
                  <div className="flex-1">
                    <label className="text-xs text-slate-400 block mb-1">Due Date <span className="text-rose-500">*</span></label>
                    <div className="relative">
                      <Calendar className="absolute right-2 top-2.5 w-4 h-4 text-slate-500" />
                      <input type="date" className="w-full bg-[#13151A] border border-slate-700 rounded p-2 text-sm text-white" />
                    </div>
                  </div>
                  <button className="bg-rose-500 text-white px-6 py-2 rounded h-[38px] text-sm">Submit</button>
                </div>
              </div>
            </div>

            {/* Progress Chart */}
            <div className="w-72 bg-[#1C1E26] border border-slate-800 rounded-xl p-6 flex flex-col items-center">
              <h3 className="text-sm font-bold uppercase text-white mb-6 self-start">Review Progress</h3>
              <div className="relative w-32 h-32 rounded-full border-8 border-slate-800 flex items-center justify-center mb-4">
                {/* CSS Hack for donut mock */}
                <div className="absolute inset-0 rounded-full border-8 border-transparent border-t-emerald-500 border-r-blue-500 border-b-amber-500 rotate-45"></div>
                <span className="text-3xl font-bold text-white">7</span>
              </div>
            </div>
          </div>

          {/* Table */}
          <div className="flex-1 bg-[#1C1E26] border border-slate-800 rounded-xl p-6">
            <div className="flex border-b border-slate-800 text-sm font-medium text-slate-400 mb-4">
              <button className="pb-3 text-rose-500 border-b-2 border-rose-500">Review Links</button>
            </div>
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="text-xs text-slate-500 uppercase border-b border-slate-800">
                <tr><th className="pb-3 font-medium">eLearning Name</th><th className="pb-3 font-medium">Reviewer Email</th><th className="pb-3 font-medium">Due Date</th><th className="pb-3 font-medium">Status</th></tr>
              </thead>
              <tbody>
                <tr className="border-b border-slate-800/50"><td className="py-4">Cybersecurity Awareness</td><td>john.doe@xyz.com</td><td>May 28, 2026</td><td><span className="text-emerald-500">Approved</span></td></tr>
                <tr className="border-b border-slate-800/50"><td className="py-4">Cybersecurity Awareness</td><td>jane.smith@xyz.com</td><td>May 28, 2026</td><td><span className="text-blue-500">In Review</span></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="flex justify-end gap-4 mt-6">
        <button className="border border-slate-600 text-white px-4 py-2 rounded flex items-center gap-2 text-sm hover:bg-slate-800"><FileCheck className="w-4 h-4" /> Save Progress</button>
        <button className="bg-rose-500 hover:bg-rose-600 text-white px-6 py-2 rounded flex items-center gap-2 text-sm font-medium">Finalize & Close Review</button>
      </div>
    </div>
  );
}