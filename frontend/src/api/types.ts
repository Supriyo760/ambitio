export interface Matter {
  id: string;
  title: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
  document_count?: number;
}

export interface MatterSummary extends Matter {
  summary: {
    documents: number;
    pages: number;
    chunks: number;
    extracted_fields: number;
    drafts: number;
    learned_rules: number;
  };
}

export interface Document {
  id: string;
  filename: string;
  status: string;
  page_count: number;
  extraction_method?: string;
  average_confidence?: number;
  warnings: string[];
}
