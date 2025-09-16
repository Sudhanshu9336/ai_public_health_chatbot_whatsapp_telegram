import React from 'react';

export default function Header({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col md:flex-row items-center justify-between mb-6 p-2 md:p-0 bg-white shadow-sm rounded-lg">
      <div className="flex items-center gap-3">{children}</div>
    </div>
  );
}
