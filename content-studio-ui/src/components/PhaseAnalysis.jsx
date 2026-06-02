import React, { useState } from 'react';

export default function PhaseAnalysis() {
  const [loading, setLoading] = useState(false);

  const handleAnalysis = (e) => {
    e.preventDefault();
    setLoading(true);
    // Backend API execution loop mapping endpoint hit integration here
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-3xl">
      <h3 className="text-lg font-medium text-slate-900 mb-4">Training Needs Analysis (TNA)</h3>
      <form onSubmit={handleAnalysis} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Project Title</label>
          <input type="text" className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="e.g. GDPR Compliance Training" required />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Target Audience</label>
          <textarea className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" rows="3" placeholder="Describe the learners..." required></textarea>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Upload Corporate Material (PDF/DOCX/PPTX)</label>
          <input type="file" className="w-full px-3 py-2 border border-slate-300 border-dashed rounded-lg bg-slate-50 cursor-pointer" />
        </div>
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50">
          {loading ? 'Processing through LangGraph Nodes...' : 'Run Analysis Node'}
        </button>
      </form>
    </div>
  );
}