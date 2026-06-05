import React, { useState, useRef, useEffect } from 'react';
import { apiClient } from '../api/client';
import type { Matter, Document } from '../api/types';

export const DocumentsPage: React.FC = () => {
  const [matters, setMatters] = useState<Matter[]>([]);
  const [activeMatterId, setActiveMatterId] = useState<string>('');
  const [documents, setDocuments] = useState<Document[]>([]);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

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

  const loadDocuments = async () => {
    if (!activeMatterId) return;
    const docs = await apiClient.getDocuments(activeMatterId);
    setDocuments(docs);
  };

  const handleUpload = async (file: File) => {
    if (!file || !activeMatterId) return;
    try {
      await apiClient.uploadDocuments(activeMatterId, [file]);
      loadDocuments();
    } catch (e) {
      console.error(e);
      alert('Upload failed');
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleUpload(e.dataTransfer.files[0]);
    }
  };

  const handleProcess = async () => {
    if (!activeMatterId || documents.length === 0) return;
    const ids = documents.map(d => d.id);
    try {
      await apiClient.processDocuments(activeMatterId, ids);
      loadDocuments();
      alert('Processing complete!');
    } catch (e) {
      console.error(e);
      alert('Processing failed');
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>Documents</h1>
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
          <button className="btn btn-secondary" onClick={handleProcess} disabled={!activeMatterId || documents.length === 0}>
            Process All
          </button>
        </div>
      </div>

      <div 
        className="card" 
        style={{ 
          marginBottom: '2rem', 
          textAlign: 'center', 
          padding: '3rem 1rem', 
          border: dragActive ? '2px dashed var(--color-primary)' : '2px dashed var(--color-border)'
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1rem' }}>Drag and drop or click to upload legal-style documents.</p>
        <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginBottom: '1rem' }}>Supported formats: PDF, PNG, JPG, JPEG, TXT</p>
        <input 
          type="file" 
          ref={fileInputRef} 
          style={{ display: 'none' }} 
          onChange={e => e.target.files && handleUpload(e.target.files[0])}
          accept=".txt,.pdf,.png,.jpg,.jpeg"
        />
        <button className="btn btn-primary" onClick={() => fileInputRef.current?.click()}>
          Select Files
        </button>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>File Name</th>
              <th>Status</th>
              <th>Pages</th>
              <th>Extraction</th>
              <th>Warnings</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center', padding: '2rem' }}>No documents uploaded yet.</td>
              </tr>
            ) : documents.map(d => (
              <tr key={d.id}>
                <td style={{ fontWeight: 500 }}>{d.filename}</td>
                <td><span className={`status-pill ${d.status.toLowerCase()}`}>{d.status}</span></td>
                <td>{d.page_count}</td>
                <td>{d.extraction_method || '-'}</td>
                <td style={{ color: d.warnings?.length ? 'var(--color-warning)' : 'inherit' }}>
                  {d.warnings?.length ? `${d.warnings.length} warning(s)` : 'None'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
