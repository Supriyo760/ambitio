import React, { useState, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter } from '../api/types';

export const DraftPage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [draft, setDraft] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [editedContent, setEditedContent] = useState('');
  const [issues, setIssues] = useState<any[]>([]);

  useEffect(() => {
    apiClient.getMatters().then(data => {
      setMatters(data);
      if (data.length > 0) setActiveMatterId(data[0].id);
    });
  }, []);

  const handleGenerate = async () => {
    if (!activeMatterId) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/drafts/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ template_type: 'Case Fact Summary' })
      });
      const data = await res.json();
      setDraft(data);
      setEditedContent(data.generated_markdown);
      setIssues([]);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckGrounding = async () => {
    if (!draft) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/drafts/${draft.draft_id || draft.id}/check`, {
        method: 'POST'
      });
      const data = await res.json();
      setIssues(data.issues);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEdit = async () => {
    try {
      const res = await fetch(`/api/matters/${activeMatterId}/edits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          draft_id: draft.id,
          original_text: draft.generated_markdown,
          edited_text: editedContent
        })
      });
      const data = await res.json();
      setDraft({ ...draft, generated_markdown: editedContent });
      setEditMode(false);
      
      if (data.rule_extracted) {
        alert(`Rule Extracted: ${data.rule.description}`);
      } else {
        alert("Edits saved. No new rule extracted.");
      }
    } catch (e) {
      console.error(e);
      alert("Failed to save edit.");
    }
  };

  const renderDraftContent = (text: string) => {
    if (!text) return null;
    const parts = text.split(/(\[E\d+\])/g);
    return parts.map((part, i) => {
      if (part.match(/\[E\d+\]/)) {
        return <span key={i} style={{ 
          backgroundColor: 'var(--color-primary-light)', 
          color: 'var(--color-primary)', 
          padding: '2px 6px', 
          borderRadius: '4px', 
          fontSize: '11px', 
          fontWeight: 600,
          cursor: 'pointer'
        }}>{part}</span>;
      }
      return part;
    });
  };

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Draft Generation</h1>
        <div style={{ display: 'flex', gap: '1rem' }}>
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
          <button className="btn btn-primary" onClick={handleGenerate} disabled={loading || !activeMatterId}>
            {loading ? 'Generating...' : 'Generate Draft'}
          </button>
        </div>
      </div>

      {draft && (
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>
          {/* Main Draft Area */}
          <div style={{ flex: 2 }}>
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0 }}>{draft.draft_type || 'Case Fact Summary'}</h3>
                <div>
                  {!editMode ? (
                    <button className="btn btn-secondary" onClick={() => setEditMode(true)}>Edit</button>
                  ) : (
                    <button className="btn btn-primary" onClick={handleSaveEdit}>Save Edit</button>
                  )}
                </div>
              </div>
              
              {editMode ? (
                <textarea 
                  value={editedContent}
                  onChange={e => setEditedContent(e.target.value)}
                  style={{ width: '100%', minHeight: '400px', padding: '1rem', border: '1px solid var(--color-border)', borderRadius: '4px', fontFamily: 'inherit', fontSize: '14px', lineHeight: 1.6 }}
                />
              ) : (
                <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: '14px' }}>
                  {renderDraftContent(draft.generated_markdown)}
                </div>
              )}
            </div>
          </div>
          
          {/* Sidebar Area */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h4 style={{ margin: 0 }}>Grounding Check</h4>
                <button className="btn btn-secondary" onClick={handleCheckGrounding} disabled={loading} style={{ padding: '0.25rem 0.5rem', fontSize: '12px' }}>
                  Run Check
                </button>
              </div>
              {issues.length > 0 ? (
                <ul style={{ paddingLeft: '1rem', margin: 0, fontSize: '13px', color: 'var(--color-error)' }}>
                  {issues.map((iss, i) => (
                    <li key={i}>{iss.message}</li>
                  ))}
                </ul>
              ) : (
                <p style={{ margin: 0, fontSize: '13px', color: 'var(--color-text-secondary)' }}>No issues found.</p>
              )}
            </div>
            
            <div className="card">
              <h4 style={{ margin: 0, marginBottom: '1rem' }}>Citations</h4>
              {draft.citations && draft.citations.length > 0 ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {draft.citations.map((c: any, i: number) => (
                    <div key={i} style={{ padding: '0.5rem', backgroundColor: 'var(--color-page-bg)', borderRadius: '4px', fontSize: '12px' }}>
                      <strong>[{c.id}]</strong> {c.text}
                    </div>
                  ))}
                </div>
              ) : (
                <p style={{ margin: 0, fontSize: '13px', color: 'var(--color-text-secondary)' }}>No citations available.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
