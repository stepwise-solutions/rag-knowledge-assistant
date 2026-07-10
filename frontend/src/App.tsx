import { useEffect, useRef, useState } from "react";
import { ChatWindow } from "./components/ChatWindow";
import { MessageInput } from "./components/MessageInput";
import { askQuestion } from "./services/api";
import type { Message, Theme } from "./types/chat";

const THEME_KEY = "rag-assistant-theme";

function getInitialTheme(): Theme {
  const stored = localStorage.getItem(THEME_KEY);
  if (stored === "light" || stored === "dark") {
    return stored;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [theme, setTheme] = useState<Theme>(getInitialTheme);
  const [copyNotice, setCopyNotice] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(THEME_KEY, theme);
  }, [theme]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, error]);

  useEffect(() => {
    if (!copyNotice) {
      return;
    }
    const timer = window.setTimeout(() => setCopyNotice(null), 2000);
    return () => window.clearTimeout(timer);
  }, [copyNotice]);

  async function sendQuestion(question: string) {
    const trimmed = question.trim();
    if (!trimmed || loading) {
      return;
    }

    setError(null);
    setInput("");
    setMessages((current) => [
      ...current,
      { role: "user", content: trimmed },
    ]);
    setLoading(true);

    try {
      const response = await askQuestion(trimmed);
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Something went wrong. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleCopy(content: string) {
    navigator.clipboard.writeText(content).then(() => {
      setCopyNotice("Answer copied to clipboard.");
    });
  }

  function toggleTheme() {
    setTheme((current) => (current === "light" ? "dark" : "light"));
  }

  function clearConversation() {
    setMessages([]);
    setError(null);
    setInput("");
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div>
            <h1>Enterprise Knowledge Assistant</h1>
            <p>
              Ask questions and retrieve answers from your document knowledge
              base.
            </p>
          </div>
          <div className="header-actions">
            <button
              type="button"
              className="ghost-button"
              onClick={clearConversation}
              disabled={messages.length === 0 && !loading}
            >
              Clear chat
            </button>
            <button
              type="button"
              className="ghost-button"
              onClick={toggleTheme}
              aria-label="Toggle theme"
            >
              {theme === "light" ? "Dark mode" : "Light mode"}
            </button>
          </div>
        </div>
        {copyNotice && <p className="copy-notice">{copyNotice}</p>}
      </header>

      <main className="main">
        <ChatWindow
          messages={messages}
          loading={loading}
          error={error}
          messagesEndRef={messagesEndRef}
          onSelectPrompt={sendQuestion}
          onCopy={handleCopy}
        />

        <MessageInput
          value={input}
          loading={loading}
          onChange={setInput}
          onSubmit={() => sendQuestion(input)}
        />
      </main>
    </div>
  );
}

export default App;
