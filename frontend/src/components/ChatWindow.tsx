import { RefObject } from "react";
import type { Message } from "../types/chat";
import { ChatMessage } from "./ChatMessage";
import { WelcomeScreen } from "./WelcomeScreen";

type ChatWindowProps = {
  messages: Message[];
  loading: boolean;
  error: string | null;
  messagesEndRef: RefObject<HTMLDivElement | null>;
  onSelectPrompt: (prompt: string) => void;
  onCopy: (content: string) => void;
};

export function ChatWindow({
  messages,
  loading,
  error,
  messagesEndRef,
  onSelectPrompt,
  onCopy,
}: ChatWindowProps) {
  const showWelcome = messages.length === 0 && !loading && !error;

  return (
    <div className="chat-window">
      {showWelcome && <WelcomeScreen onSelectPrompt={onSelectPrompt} />}

      {messages.map((message, index) => (
        <ChatMessage
          key={`${message.role}-${index}`}
          message={message}
          onCopy={message.role === "assistant" ? onCopy : undefined}
        />
      ))}

      {loading && (
        <div className="message-row assistant">
          <div className="avatar" aria-hidden="true">
            AI
          </div>
          <div className="bubble assistant loading">
            <span>Assistant is thinking</span>
            <span className="thinking-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
          </div>
        </div>
      )}

      {error && <p className="error-banner">{error}</p>}
      <div ref={messagesEndRef} />
    </div>
  );
}
