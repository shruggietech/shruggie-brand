import records from '@/generated/conformance.json';

export type ConformanceRecord = (typeof records)[number];
export const conformanceRecords = records as ConformanceRecord[];
export function conformanceBySlug(slug: string) { return conformanceRecords.find((record) => record.slug === slug); }
