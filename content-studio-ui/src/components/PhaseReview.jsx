import React from 'react';

export default function PhaseReview() {
  return (
    <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-3xl">
      <h3 className="text-lg font-medium text-slate-900 mb-2">Compliance & Human-in-the-Loop Node Evaluation</h3>
      <p className="text-sm text-slate-600 mb-4">Fetches LangGraph state checkpointers to cross check organizational rules logs and compliance checks metric scoring loops.</p>
      <span className="px-2 py-1 text-xs font-semibold bg-amber-100 text-amber-800 rounded">Pending Approval Stage</span>
    </div>
  );
}