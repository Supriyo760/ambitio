import React, { useState } from 'react';

export const EvaluationPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleRunEvaluation = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/evaluation/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample_set: 'default' })
      });
      const data = await res.json();
      setResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ margin: 0 }}>System Evaluation</h1>
        <button className="btn btn-primary" onClick={handleRunEvaluation} disabled={loading}>
          {loading ? 'Running...' : 'Run Default Evaluation'}
        </button>
      </div>

      <p style={{ color: 'var(--color-text-secondary)', marginBottom: '2rem' }}>
        This page runs the evaluation test suite against sample documents to measure processing completeness, retrieval precision, grounding coverage, and learning effectiveness.
      </p>

      {results && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          <div className="card" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Documents Processed</span>
              <strong style={{ fontSize: '24px' }}>{results.metrics.documents_processed}</strong>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Fields Extracted</span>
              <strong style={{ fontSize: '24px' }}>{results.metrics.structured_fields_found} / {results.metrics.structured_fields_expected}</strong>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Retrieval Precision (Top 5)</span>
              <strong style={{ fontSize: '24px' }}>{(results.metrics.retrieval_precision_at_5 * 100).toFixed(0)}%</strong>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '12px', color: 'var(--color-text-secondary)' }}>Citation Coverage</span>
              <strong style={{ fontSize: '24px' }}>{(results.metrics.citation_coverage * 100).toFixed(0)}%</strong>
            </div>
          </div>
          
          <div className="card">
            <h3 style={{ margin: 0, marginBottom: '1rem' }}>Detailed Report</h3>
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: '14px' }}>
              {results.results_markdown}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
