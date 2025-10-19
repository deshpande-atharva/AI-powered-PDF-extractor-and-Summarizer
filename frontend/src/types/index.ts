export interface Table {
  title: string;
  headers: string[];
  rows: string[][];
}

export interface Summary {
  total_amount: number;
  invoice_count: number;
  date_range: string;
}

export interface ExtractedData {
  success: boolean;
  filename: string;
  data: {
    tables: Table[];
    summary: Summary | null;
  };
}