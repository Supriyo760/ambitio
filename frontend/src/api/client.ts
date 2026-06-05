import type { Matter, MatterSummary, Document } from './types';

const API_BASE = '/api';

export const apiClient = {
  async health() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  async createMatter(title: string, description?: string): Promise<Matter> {
    const res = await fetch(`${API_BASE}/matters`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description }),
    });
    if (!res.ok) throw new Error('Failed to create matter');
    return res.json();
  },

  async getMatters(): Promise<Matter[]> {
    const res = await fetch(`${API_BASE}/matters`);
    if (!res.ok) throw new Error('Failed to list matters');
    const data = await res.json();
    return data.items;
  },

  async getMatterSummary(id: string): Promise<MatterSummary> {
    const res = await fetch(`${API_BASE}/matters/${id}`);
    if (!res.ok) throw new Error('Failed to get matter summary');
    return res.json();
  },

  async deleteMatter(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/matters/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete matter');
  },

  async uploadDocuments(matterId: string, files: File[]): Promise<{ uploaded: Document[] }> {
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    
    const res = await fetch(`${API_BASE}/matters/${matterId}/documents`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  async getDocuments(matterId: string): Promise<Document[]> {
    const res = await fetch(`${API_BASE}/matters/${matterId}/documents`);
    if (!res.ok) throw new Error('Failed to get documents');
    const data = await res.json();
    return data.items;
  },

  async processDocuments(matterId: string, documentIds: string[]): Promise<any> {
    const res = await fetch(`${API_BASE}/matters/${matterId}/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ document_ids: documentIds }),
    });
    if (!res.ok) throw new Error('Failed to process documents');
    return res.json();
  }
};
