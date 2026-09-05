import records from '@/generated/brands.json';

export type Brand = (typeof records)[number];
export const brands = records as Brand[];
export function brandBySlug(slug: string) { return brands.find((brand) => brand.slug === slug); }
