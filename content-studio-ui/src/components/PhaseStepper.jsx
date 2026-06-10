import React from 'react';

const PHASES = [
  { id: 'analysis', label: 'Analysis', number: 1 },
  { id: 'design', label: 'Design', number: 2 },
  { id: 'develop', label: 'Develop', number: 3 },
  { id: 'review', label: 'Review', number: 4 }
];

export default function PhaseStepper({ currentPhase = 'analysis', hideOnMobile = false }) {
  const getPhaseStatus = (phaseId) => {
    const phases = ['analysis', 'design', 'develop', 'review'];
    const currentIndex = phases.indexOf(currentPhase);
    const phaseIndex = phases.indexOf(phaseId);

    if (phaseIndex < currentIndex) return 'completed';
    if (phaseIndex === currentIndex) return 'current';
    return 'pending';
  };

  return (
    <div className={`flex items-center gap-2 ${hideOnMobile ? 'hidden md:flex' : 'flex flex-wrap md:flex-nowrap'}`}>
      {PHASES.map((phase, index) => {
        const status = getPhaseStatus(phase.id);
        const isCompleted = status === 'completed';
        const isCurrent = status === 'current';

        return (
          <React.Fragment key={phase.id}>
            <div className="flex items-center gap-1">
              <div
                className={`w-2.5 h-2.5 rounded-full transition-colors ${
                  isCompleted || isCurrent
                    ? 'bg-rose-500'
                    : 'bg-slate-700'
                }`}
              ></div>
              <span
                className={`text-xs transition-colors ${
                  isCompleted || isCurrent
                    ? 'text-rose-500'
                    : 'text-slate-500'
                }`}
              >
                {phase.label}
              </span>
            </div>

            {index < PHASES.length - 1 && (
              <div
                className={`w-6 md:w-8 h-[1px] transition-colors ${
                  isCompleted ? 'bg-rose-500' : 'bg-slate-700'
                }`}
              ></div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
