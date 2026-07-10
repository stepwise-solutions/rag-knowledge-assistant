import type { ChatResponse } from "../types/chat";

export async function askQuestion(question: string): Promise<ChatResponse> {
  const apiUrl = import.meta.env.VITE_API_URL;

  if (!apiUrl) {
    throw new Error("VITE_API_URL is not configured.");
  }

  const response = await fetch(`${apiUrl}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!response.ok) {
    throw new Error(`Request failed (${response.status}). Please try again.`);
  }

  const data: ChatResponse = await response.json();
  return {
    answer: data.answer,
    sources: data.sources ?? [],
  };
}
