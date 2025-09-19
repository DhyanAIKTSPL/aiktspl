import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import Chatbot from '../Chatbot';

const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-background flex text-text-primary">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Header />
        <main className="flex-1 p-6 overflow-y-auto">
          {children}
        </main>
      </div>
      <Chatbot />
    </div>
  );
};

export default DashboardLayout;
