import { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

const formatDate = (dateStr: string) => {
  if (!dateStr) return 'N/A';
  try {
    const d = new Date(dateStr + (dateStr.endsWith('Z') ? '' : 'Z'));
    return isNaN(d.getTime()) ? 'Invalid Date' : d.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  } catch(e) {
    return 'Invalid Date';
  }
};

export const MatterWorkspace = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [newTitle, setNewTitle] = useState('');

  useEffect(() => {
    loadMatters();
  }, []);

  const loadMatters = async () => {
    try {
      const data = await apiClient.getMatters();
      setMatters(data);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreate = async () => {
    if (!newTitle) return;
    await apiClient.createMatter(newTitle, "Demo matter");
    setNewTitle('');
    loadMatters();
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this matter and all its documents?')) return;
    await apiClient.deleteMatter(id);
    loadMatters();
  };

  return (
    <div className="animate-in" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Matters Workspace</h1>
      </div>

      <div className="glass-card" style={{ marginBottom: '2.5rem' }}>
        <h3 style={{ marginTop: 0, color: 'var(--text-primary)', marginBottom: '1.5rem', fontWeight: 500 }}>Create New Matter</h3>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <input 
            type="text" 
            value={newTitle} 
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="e.g. Smith vs Jones - Q3 Drafts"
            style={{ flex: 1 }}
          />
          <button className="btn btn-primary" onClick={handleCreate}>Create Workspace</button>
        </div>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Status</th>
              <th>Documents</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {matters.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                  No matters found. Create one above to get started.
                </td>
              </tr>
            ) : matters.map(m => (
              <tr key={m.id} style={{ transition: 'background 0.2s ease' }}>
                <td style={{ fontWeight: 500 }}>{m.title}</td>
                <td><span className={`status-pill ${m.status.toLowerCase()}`}>{m.status}</span></td>
                <td>{m.document_count || 0}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{formatDate(m.created_at)}</td>
                <td>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button className="btn btn-secondary" style={{ padding: '0.4rem 1rem', fontSize: '0.8rem' }}>Open</button>
                    <button className="btn btn-secondary" style={{ padding: '0.4rem 1rem', fontSize: '0.8rem', color: 'var(--color-error)' }} onClick={() => handleDelete(m.id)}>Delete</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
