type FormattedTextProps = {
  content: string;
};

export function FormattedText({ content }: FormattedTextProps) {
  const blocks = content.split(/\n\n+/).filter((block) => block.trim());

  if (blocks.length === 0) {
    return null;
  }

  return (
    <div className="formatted-text">
      {blocks.map((block, index) => {
        const lines = block.split("\n");
        const isList = lines.every((line) => /^[-*]\s+/.test(line.trim()));

        if (isList) {
          return (
            <ul key={index}>
              {lines.map((line, lineIndex) => (
                <li key={lineIndex}>{line.trim().replace(/^[-*]\s+/, "")}</li>
              ))}
            </ul>
          );
        }

        return <p key={index}>{block}</p>;
      })}
    </div>
  );
}
