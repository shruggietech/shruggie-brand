import Link from "next/link";
import docs from "../../generated/docs.json";

export default function DocsIndex() {
  return (
    <div className="shell">
      <p className="eyebrow">shruggie-brandbuilder 1.1.2</p>
      <h1>Build from the canon</h1>
      <p className="lede">The reference set defines variance, kit anatomy, interviewing, tooling, registries, logo construction, voice, and portability.</p>
      <ul className="download-list">
        {docs.map((doc) => <li key={doc.slug}><Link href={`/docs/${doc.slug}/`}>{doc.title}</Link></li>)}
      </ul>
    </div>
  );
}
