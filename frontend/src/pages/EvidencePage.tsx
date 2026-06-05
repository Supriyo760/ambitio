import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

export const EvidencePage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('hybrid');
  const [topK, setTopK] = useState(5);

  useEffect(() => {
    apiClient.getMatters().then(data => {
      setMatters(data);
      if (data.length > 0) setActiveMatterId(data[0].id);
    });
  }, []);

  const handleSearch = async () => {
    if (!activeMatterId || !query) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, mode, top_k: topK }),
      });
      const data = await res.json();
      setResults(data.results);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Evidence Retrieval</h1>
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

      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
          <input 
            type="text" 
            value={query} 
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search documents for evidence..."
            style={{ flex: 1, padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--color-border)' }}
          />
          <button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', fontSize: '13px' }}>
          <label>Mode:
            <select value={mode} onChange={e => setMode(e.target.value)} style={{ marginLeft: '0.5rem', padding: '0.25rem' }}>
              <option value="hybrid">Hybrid</option>
              <option value="semantic">Semantic</option>
              <option value="keyword">Keyword</option>
            </select>
          </label>
          <label>Top K:
            <input type="number" value={topK} onChange={e => setTopK(Number(e.target.value))} min={1} max={20} style={{ marginLeft: '0.5rem', padding: '0.25rem', width: '60px' }} />
          </label>
        </div>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {results.length === 0 && query && !loading && (
          <p style={{ color: 'var(--color-text-secondary)', textAlign: 'center' }}>No results found.</p>
        )}
        {results.map((r, i) => (
          <div key={i} className="card" style={{ backgroundColor: 'var(--color-evidence-highlight)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <strong style={{ fontSize: '14px', color: 'var(--color-primary)' }}>{r.evidence_id} - {r.document_title} (Page {r.page_number})</strong>
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Score: {r.score.toFixed(2)} | {r.reason}</span>
            </div>
            <p style={{ margin: 0, fontSize: '14px', lineHeight: 1.5 }}>
              {r.passage}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
