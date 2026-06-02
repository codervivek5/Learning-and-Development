import React, { useState } from 'react';
import Auth from './components/Auth';
import Layout from './components/Layout';
import PhaseAnalysis from './components/PhaseAnalysis';
import PhaseDesign from './components/PhaseDesign';
import PhaseOverview from './components/dashboard/PhaseOverview';
import PhaseDevelop from './components/PhaseDevelop';
import PhaseReview from './components/PhaseReview';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <PhaseOverview />;
      case 'analysis':
        return <PhaseAnalysis />;
      case 'design':
        return <PhaseDesign />;
      case 'develop':
        return <PhaseDevelop />;
      case 'review':
        return <PhaseReview />;
      default:
        return <div>View Scope Not Found</div>;
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