'use client';

import { useState } from 'react';

export function CopyValue({ value, label }: { value: string; label: string }) {
  const [status, setStatus] = useState('');
  async function copy() {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(value);
      setStatus(`Copied ${label}`);
    } catch {
      setStatus(`Copy failed. Select the ${label} value instead.`);
    }
  }
  return <><button className="guide-copy" type="button" onClick={copy} aria-label={`Copy ${label}`}>Copy</button><span className="sr-only" data-copy-status aria-live="polite">{status}</span></>;
}
