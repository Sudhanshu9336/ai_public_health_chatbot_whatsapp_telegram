import React from 'react';

export default function Card({ title, children }: { title: string, children: React.ReactNode }) {
  return (
    <div className="card p-6 mb-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">{title}</h2>
      {children}
    </div>
  );
}
