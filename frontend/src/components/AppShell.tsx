import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { Briefcase, FileText, LayoutList, Search, FileEdit, BookOpen, BarChart } from 'lucide-react';
import '../styles/tokens.css';

export const AppShell: React.FC = () => {
  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', background: 'var(--bg-gradient)' }}>
      {/* Sidebar */}
      <div className="glass-panel" style={{ width: '280px', display: 'flex', flexDirection: 'column', margin: '1rem', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
        <div style={{ padding: '2rem 1.5rem', background: '#fdfbf7', borderBottom: '1px solid var(--surface-border)' }}>
          <h2 style={{ margin: 0, fontSize: '20px', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ width: 32, height: 32, borderRadius: 10, background: 'var(--primary-accent)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
               <Briefcase size={16} color="white" />
            </div>
            Ambitio AI
          </h2>
        </div>
        <nav style={{ flex: 1, padding: '1.5rem 1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', overflowY: 'auto' }}>
          <NavItem to="/" icon={<Briefcase size={18} />} label="Matters Workspace" />
          <NavItem to="/documents" icon={<FileText size={18} />} label="Documents" />
          <NavItem to="/review" icon={<FileText size={18} />} label="Document Review" />
          <NavItem to="/facts" icon={<LayoutList size={18} />} label="Extracted Facts" />
          <NavItem to="/evidence" icon={<Search size={18} />} label="Evidence DB" />
          <NavItem to="/draft" icon={<FileEdit size={18} />} label="Draft Generator" />
          <NavItem to="/learning" icon={<BookOpen size={18} />} label="Rule Learning" />
          <NavItem to="/evaluation" icon={<BarChart size={18} />} label="Evaluation" />
        </nav>
      </div>

      {/* Main Content */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', margin: '1rem 1rem 1rem 0' }}>
        {/* Top bar placeholder */}
        <div className="glass-panel" style={{ height: '70px', borderRadius: 'var(--radius-lg)', display: 'flex', alignItems: 'center', padding: '0 2rem', marginBottom: '1rem' }}>
          <span style={{ fontWeight: 600, color: 'var(--text-secondary)', letterSpacing: '0.05em', textTransform: 'uppercase', fontSize: '0.85rem' }}>Active Workspace</span>
        </div>
        
        {/* Page Outlet */}
        <div className="glass-panel" style={{ flex: 1, overflowY: 'auto', padding: '3rem', borderRadius: 'var(--radius-lg)', position: 'relative' }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

const NavItem: React.FC<{ to: string, icon: React.ReactNode, label: string }> = ({ to, icon, label }) => {
  return (
    <NavLink 
      to={to} 
      style={({ isActive }) => ({
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        padding: '0.85rem 1.15rem',
        borderRadius: '12px',
        color: isActive ? 'var(--primary-accent)' : 'var(--text-secondary)',
        background: isActive ? '#fdf3e7' : 'transparent',
        border: '1px solid transparent',
        fontWeight: isActive ? 600 : 500,
        textDecoration: 'none',
        transition: 'all 0.2s ease'
      })}
    >
      {icon}
      <span style={{ letterSpacing: '0.02em' }}>{label}</span>
    </NavLink>
  );
};
