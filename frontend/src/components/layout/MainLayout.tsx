import React from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="min-h-screen bg-dark-bg text-dark-text flex">
      <Sidebar />
      <div className="flex-1 lg:ml-60 min-h-screen flex flex-col relative">
        <Header />
        <main className="flex-1">
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;
