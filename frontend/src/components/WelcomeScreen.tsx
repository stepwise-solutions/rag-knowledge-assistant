const SUGGESTED_PROMPTS = [
  "Explain the main concepts in this document.",
  "Summarise the key recommendations.",
  "Compare the different approaches described.",
];

type WelcomeScreenProps = {
  onSelectPrompt: (prompt: string) => void;
};

export function WelcomeScreen({ onSelectPrompt }: WelcomeScreenProps) {
  return (
    <div className="welcome-screen">
      <h2>What would you like to know?</h2>
      <p>
        Ask questions and retrieve grounded answers from your indexed document
        knowledge base.
      </p>

      <div className="suggestions">
        <p className="suggestions-label">Try asking:</p>
        {SUGGESTED_PROMPTS.map((prompt) => (
          <button
            key={prompt}
            type="button"
            className="suggestion-chip"
            onClick={() => onSelectPrompt(prompt)}
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
