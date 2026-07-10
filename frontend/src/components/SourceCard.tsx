type SourceCardProps = {
  source: string;
};

export function SourceCard({ source }: SourceCardProps) {
  const filename = source.split("/").pop() ?? source;

  return (
    <div className="source-card">
      <span className="source-icon" aria-hidden="true">
        📄
      </span>
      <span className="source-name" title={source}>
        {filename}
      </span>
    </div>
  );
}
