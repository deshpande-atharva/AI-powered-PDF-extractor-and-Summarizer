// frontend/src/components/DataTable.tsx
import React from 'react';
import type { Table } from '../types';

interface DataTableProps {
  table: Table;
}

const DataTable: React.FC<DataTableProps> = ({ table }) => {
  // Function to format currency values
  const formatValue = (value: string) => {
    if (typeof value === 'string' && value.includes('$')) {
      return value;
    }
    if (typeof value === 'string' && /^\d+\.?\d*$/.test(value)) {
      const num = parseFloat(value);
      if (!isNaN(num)) {
        return `$${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      }
    }
    return value;
  };

  // Check if a row is a total row (contains words like total, subtotal, etc.)
  const isTotalRow = (row: string[]) => {
    return row.some(cell => 
      typeof cell === 'string' && 
      cell.toLowerCase().match(/\b(total|subtotal|grand total|sum)\b/)
    );
  };

  return (
    <div className="data-table-container">
      {table.title && <h3 className="table-title">{table.title}</h3>}
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {table.headers.map((header, index) => (
                <th key={index} className={`header-${index}`}>
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {table.rows.map((row, rowIndex) => {
              const isTotal = isTotalRow(row);
              return (
                <tr 
                  key={rowIndex} 
                  className={`
                    ${rowIndex % 2 === 0 ? 'even-row' : 'odd-row'}
                    ${isTotal ? 'total-row' : ''}
                  `}
                >
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} className={`cell-${cellIndex}`}>
                      {formatValue(cell)}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;