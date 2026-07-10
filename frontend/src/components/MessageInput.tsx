import { FormEvent, KeyboardEvent } from "react";

const MAX_CHARS = 2000;

type MessageInputProps = {
  value: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
};

export function MessageInput({
  value,
  loading,
  onChange,
  onSubmit,
}: MessageInputProps) {
  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form className="composer" onSubmit={handleSubmit}>
      <div className="composer-box">
        <textarea
          value={value}
          onChange={(event) => onChange(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your documents..."
          disabled={loading}
          rows={1}
          maxLength={MAX_CHARS}
          aria-label="Message"
        />
        <div className="composer-footer">
          <span className="char-count">
            {value.length} / {MAX_CHARS}
          </span>
          <button type="submit" disabled={loading || !value.trim()}>
            Send
          </button>
        </div>
      </div>
    </form>
  );
}
