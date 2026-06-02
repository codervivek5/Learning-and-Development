import React, { useState } from 'react';
import Auth from './components/Auth';
import Layout from './components/Layout';
import PhaseAnalysis from './components/PhaseAnalysis';
import PhaseDesign from './components/PhaseDesign';
import PhaseOverview from './components/dashboard/PhaseOverview';
import PhaseDevelop from './components/PhaseDevelop';
import PhaseReview from './components/PhaseReview';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');

  // Central state pipeline tracking data flowing from Analysis down to Review
  const [pipelineState, setPipelineState] = useState({
    analysisData: null,
    designBlueprint: null,
    developmentAssets: null,
  });

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <PhaseOverview />;
      case 'analysis':
        return (
          <PhaseAnalysis
            onAdvancePipeline={(metrics) => {
              setPipelineState(prev => ({ ...prev, analysisData: metrics }));
              setActiveTab('design'); // Triggers smooth navigation to Phase 2
            }}
          />
        );
      case 'design':
        return (
          <PhaseDesign
            injectedAnalysis={pipelineState.analysisData}
            onSaveBlueprint={(blueprint) => {
              setPipelineState(prev => ({ ...prev, designBlueprint: blueprint }));
              setActiveTab('develop'); // Triggers smooth navigation to Phase 3
            }}
          />
        );
      case 'develop':
        return (
          <PhaseDevelop
            injectedBlueprint={pipelineState.designBlueprint}
            onCompleteAssets={(assets) => {
              setPipelineState(prev => ({ ...prev, developmentAssets: assets }));
              setActiveTab('review'); // Triggers smooth navigation to Phase 4
            }}
          />
        );
      case 'review':
        return (
          <PhaseReview
            completePipelineContext={pipelineState}
            onSystemSignoff={() => {
              // Handle post-signoff cleanup or dashboard redirection
              setActiveTab('dashboard');
            }}
          />
        );
      default:
        return (
          <div className="p-6 bg-slate-950 border border-slate-800 rounded-xl text-slate-400 font-mono text-xs">
            View Scope Not Found
          </div>
        );
    }
  };

  if (!isAuthenticated) {
    return <Auth onLoginSuccess={() => setIsAuthenticated(true)} />;
  }

  return (
    <Layout currentTab={activeTab} setTab={setActiveTab}>
      {renderContent()}
    </Layout>
  );
}