import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

export const ExtractedFactsPage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [facts, setFacts] = useState<any[]>([]);

  const [filterType, setFilterType] = useState('All');
  const [filterReview, setFilterReview] = useState(false);

  useEffect(() => {
    apiClient.getMatters().then(data => {
      setMatters(data);
      if (data.length > 0) setActiveMatterId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (activeMatterId) {
      loadFacts();
    }
  }, [activeMatterId]);

  const loadFacts = async () => {
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/fields`);
      const data = await res.json();
      setFacts(data.items);
    } catch (e) {
      console.error(e);
    }
  };

  const filteredFacts = facts.filter(f => {
    if (filterType !== 'All' && f.field_type !== filterType) return false;
    if (filterReview && !f.needs_review) return false;
    return true;
  });

  const uniqueTypes = ['All', ...Array.from(new Set(facts.map(f => f.field_type)))];

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Extracted Facts</h1>
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

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', alignItems: 'center' }}>
        <label>Filter Type:
          <select value={filterType} onChange={e => setFilterType(e.target.value)} style={{ marginLeft: '0.5rem', padding: '0.25rem' }}>
            {uniqueTypes.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>
        <label>
          <input type="checkbox" checked={filterReview} onChange={e => setFilterReview(e.target.checked)} /> Needs Review Only
        </label>
      </div>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Field Name</th>
              <th>Value</th>
              <th>Type</th>
              <th>Confidence</th>
              <th>Source Text</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredFacts.length === 0 ? (
              <tr><td colSpan={6} style={{ textAlign: 'center', padding: '2rem' }}>No facts found.</td></tr>
            ) : (
              filteredFacts.map(f => (
              <tr key={f.id}>
                <td style={{ fontWeight: 600 }}>{f.field_name}</td>
                <td>{f.value}</td>
                <td><span style={{ fontSize: '12px', color: 'var(--color-text-muted)' }}>{f.field_type}</span></td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '40px', height: '6px', background: '#e2e8f0', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ width: `${f.confidence * 100}%`, height: '100%', background: f.confidence > 0.8 ? 'var(--color-success)' : 'var(--color-warning)' }} />
                    </div>
                    <span style={{ fontSize: '12px' }}>{(f.confidence * 100).toFixed(0)}%</span>
                  </div>
                </td>
                <td style={{ maxWidth: '250px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', fontSize: '12px', color: 'var(--color-text-secondary)' }}>
                  {f.raw_text}
                </td>
                <td><span className={`status-pill ${f.needs_review ? 'warning' : 'ready'}`}>{f.needs_review ? 'REVIEW' : 'ACCEPTED'}</span></td>
              </tr>
            )))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
