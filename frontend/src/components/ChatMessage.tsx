import type { Message } from "../types/chat";
import { FormattedText } from "./FormattedText";
import { SourceCard } from "./SourceCard";

type ChatMessageProps = {
  message: Message;
  onCopy?: (content: string) => void;
};

export function ChatMessage({ message, onCopy }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${message.role}`}>
      {!isUser && (
        <div className="avatar" aria-hidden="true">
          AI
        </div>
      )}

      <div className="message-content">
        <div className={`bubble ${message.role}`}>
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <div className="formatted-text">
              <FormattedText content={message.content} />
            </div>
          )}
        </div>

        {!isUser && message.sources && message.sources.length > 0 && (
          <div className="sources">
            <p className="sources-label">Sources</p>
            <div className="sources-list">
              {message.sources.map((source) => (
                <SourceCard key={source} source={source} />
              ))}
            </div>
          </div>
        )}

        {!isUser && onCopy && (
          <button
            type="button"
            className="copy-button"
            onClick={() => onCopy(message.content)}
          >
            Copy answer
          </button>
        )}
      </div>
    </div>
  );
}
