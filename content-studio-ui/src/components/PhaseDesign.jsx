import React from 'react';

export default function PhaseDesign() {
  // Static mockup state representation matching your core structured outputs
  const structuredMockSyllabus = [
    { title: "Module 1: Introduction to Framework metrics", lessons: ["Lesson 1.1: Core Guidelines", "Lesson 1.2: Scope definitions"] },
    { title: "Module 2: Practical Risk Implementation", lessons: ["Lesson 2.1: Evaluation Parameters", "Lesson 2.2: Mitigation Trees"] }
  ];

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <h3 className="text-lg font-medium text-slate-900 mb-2">Curriculum Strategy Node</h3>
        <p className="text-sm text-slate-500 mb-4">Generates a validated structural course maps blueprint tree via Gemini JSON Schema parameters.</p>
        <button className="px-4 py-2 bg-emerald-600 text-white rounded-lg text-sm font-medium hover:bg-emerald-700">
          Generate Structured Curriculum
        </button>
      </div>

      {/* Curriculum Node Tree Rendering Layout */}
      <div className="bg-slate-900 text-slate-100 p-6 rounded-xl font-mono text-sm shadow-inner">
        <div className="text-slate-400 mb-2">// Gemini Pydantic JSON Engine Outbound Response:</div>
        {structuredMockSyllabus.map((mod, i) => (
          <div key={i} className="mb-4 ml-2">
            <span className="text-yellow-400">■ {mod.title}</span>
            <div className="ml-6 mt-1 space-y-1 text-cyan-300">
              {mod.lessons.map((les, idx) => (
                <div key={idx}>↳ {les}</div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}