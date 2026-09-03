import Link from "next/link";
import { notFound } from "next/navigation";
import ReactMarkdown from "react-markdown";
import docs from "../../../generated/docs.json";

export function generateStaticParams() {
  return docs.map((doc) => ({ slug: doc.slug }));
}

export default async function DocPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const doc = docs.find((item) => item.slug === slug);
  if (!doc) notFound();
  return (
    <div className="shell doc-layout">
      <nav className="doc-nav" aria-label="Brandbuilder references">
        <Link href="/docs/">All references</Link>
        {docs.map((item) => <Link href={`/docs/${item.slug}/`} key={item.slug}>{item.title}</Link>)}
      </nav>
      <article className="prose"><ReactMarkdown>{doc.content}</ReactMarkdown></article>
    </div>
  );
}
