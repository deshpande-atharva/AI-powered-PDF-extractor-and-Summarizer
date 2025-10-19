import type { ExtractedData } from '../types/index';

const API_URL = 'http://localhost:8000';

export async function extractPDFData(file: File): Promise<ExtractedData> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/api/extract`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to extract PDF data');
  }

  return response.json();
}
