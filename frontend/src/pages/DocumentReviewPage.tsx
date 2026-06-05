import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

export const DocumentReviewPage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [documents, setDocuments] = useState<any[]>([]);
  const [activeDocId, setActiveDocId] = useState<string>('');
  const [pages, setPages] = useState<any[]>([]);

  useEffect(() => {
    apiClient.getMatters().then(data => {
      setMatters(data);
      if (data.length > 0) setActiveMatterId(data[0].id);
    });
  }, []);

  useEffect(() => {
    if (activeMatterId) {
      loadDocuments();
    }
  }, [activeMatterId]);

  useEffect(() => {
    if (activeDocId) {
      loadPages();
    }
  }, [activeDocId]);

  const loadDocuments = async () => {
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/documents`);
      const data = await res.json();
      setDocuments(data.items);
      if (data.items.length > 0) {
        setActiveDocId(data.items[0].id);
      } else {
        setPages([]);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const loadPages = async () => {
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/documents/${activeDocId}/pages`);
      const data = await res.json();
      setPages(data.items);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Document Review</h1>
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

      <div style={{ display: 'flex', gap: '2rem', flex: 1, minHeight: 0 }}>
        {/* Document List Panel */}
        <div className="card" style={{ width: '250px', overflowY: 'auto' }}>
          <h4 style={{ margin: 0, marginBottom: '1rem' }}>Documents</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {documents.map(d => (
              <div 
                key={d.id} 
                onClick={() => setActiveDocId(d.id)}
                style={{ 
                  padding: '0.5rem', 
                  backgroundColor: d.id === activeDocId ? 'var(--color-evidence-highlight)' : 'transparent',
                  border: '1px solid',
                  borderColor: d.id === activeDocId ? 'var(--color-primary)' : 'var(--color-border)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '13px'
                }}
              >
                <strong>{d.filename}</strong>
                <div style={{ color: 'var(--color-text-secondary)', marginTop: '0.25rem' }}>
                  {d.page_count} Pages | Conf: {d.average_confidence?.toFixed(2) || 'N/A'}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Extracted Text Panel */}
        <div className="card" style={{ flex: 1, overflowY: 'auto', backgroundColor: '#fff' }}>
          {pages.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--color-text-secondary)' }}>
              No pages processed yet.
            </div>
          ) : (
            pages.map(p => (
              <div key={p.id} style={{ marginBottom: '2rem', borderBottom: '1px solid var(--color-border)', paddingBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                  <h4 style={{ margin: 0 }}>Page {p.page_number}</h4>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <span className="status-pill">{p.extraction_method}</span>
                    <span className="status-pill">Conf: {p.confidence?.toFixed(2) || 'N/A'}</span>
                  </div>
                </div>
                
                {p.warnings && p.warnings.length > 0 && (
                  <div style={{ padding: '0.5rem', backgroundColor: 'var(--color-low-confidence-bg)', color: 'var(--color-warning)', borderRadius: '4px', fontSize: '13px', marginBottom: '1rem' }}>
                    <strong>Warnings: </strong> {p.warnings.join(', ')}
                  </div>
                )}
                
                <div style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: '13px', lineHeight: 1.5 }}>
                  {p.text}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
