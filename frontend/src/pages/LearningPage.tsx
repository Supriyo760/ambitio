import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

export const LearningPage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [rules, setRules] = useState<any[]>([]);

  useEffect(() => {
    apiClient.getMatters().then(data => {
      setMatters(data);
      if (data.length > 0) setActiveMatterId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (activeMatterId) {
      loadRules();
    }
  }, [activeMatterId]);

  const loadRules = async () => {
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/rules`);
      const data = await res.json();
      setRules(data.items);
    } catch (e) {
      console.error(e);
    }
  };

  const handleToggle = async (ruleId: string, currentActive: boolean) => {
    try {
      await fetch(`/api/matters/${activeMatterId}/rules/${ruleId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ active: !currentActive })
      });
      loadRules();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Edit Learning & Rules</h1>
        {matters.length > 0 && (
          <select 
            value={activeMatterId} 
            onChange={e => setActiveMatterId(e.target.value)}
            style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid var(--color-border)' }}
          >
            {matters.map(m => (
              <option key={m.id} value={m.id}>{m.title}</option>
            ))}
          </select>
        )}
      </div>

      <p style={{ color: 'var(--color-text-secondary)', marginBottom: '2rem' }}>
        Rules extracted from operator edits. These rules will be applied to future drafts in this matter.
      </p>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Rule Description</th>
              <th>Status</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {rules.length === 0 ? (
              <tr>
                <td colSpan={4} style={{ textAlign: 'center', padding: '2rem' }}>No rules learned yet. Save edits in the Draft page to extract rules.</td>
              </tr>
            ) : rules.map(r => (
              <tr key={r.id}>
                <td style={{ fontWeight: 500, maxWidth: '400px' }}>{r.description}</td>
                <td>
                  <span className={`status-pill ${r.is_active ? 'ready' : 'empty'}`}>
                    {r.is_active ? 'Active' : 'Disabled'}
                  </span>
                </td>
                <td>{new Date(r.created_at + (r.created_at.endsWith('Z') ? '' : 'Z')).toLocaleDateString()}</td>
                <td>
                  <button className="btn btn-secondary" onClick={() => handleToggle(r.id, r.is_active)}>
                    {r.is_active ? 'Disable' : 'Enable'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
