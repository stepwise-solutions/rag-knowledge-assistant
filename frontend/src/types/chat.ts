export type MessageRole = "user" | "assistant";

export type Message = {
  role: MessageRole;
  content: string;
  sources?: string[];
};

export type ChatResponse = {
  answer: string;
  sources?: string[];
};

export type Theme = "light" | "dark";
