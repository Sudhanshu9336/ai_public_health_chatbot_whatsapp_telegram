import React from 'react';

export default function LanguageBadge({ lang }: { lang: string }) {
  const map: Record<string, string> = { en: 'English', hi: 'Hindi', or: 'Odia' };
  return <span className="badge">{map[lang] || lang}</span>;
}
