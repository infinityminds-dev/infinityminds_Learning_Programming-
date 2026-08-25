import numpy as np


class MiniLLMSimulator:

    def __init__(self, vocabulary):
        self.vocab = vocabulary
        self.vocab_size = len(vocabulary)
        # Word-to-ID mappings
        self.word2id = {w: i for i, w in enumerate(vocabulary)}
        self.id2word = {i: w for i, w in enumerate(vocabulary)}

        # Random Embeddings and Weights
        np.random.seed(42)
        self.embed_dim = 4
        self.embeddings = np.random.randn(self.vocab_size, self.embed_dim)
        self.W_output = np.random.randn(self.embed_dim, self.vocab_size)

    # 1. Tokenization
    def tokenize(self, text):
        return [
            self.word2id[w]
            for w in text.lower().split()
            if w in self.word2id
        ]

    # 2. Self-Attention Mechanism (Dot-Product)
    def self_attention(self, token_vectors):
        scores = np.dot(token_vectors, token_vectors.T)
        exp_scores = np.exp(scores - np.max(scores))
        attention_weights = exp_scores / exp_scores.sum(axis=-1, keepdims=True)
        context = np.dot(attention_weights, token_vectors)
        return context

    # 3. Next Word Prediction
    def predict_next_word(self, input_text):
        tokens = self.tokenize(input_text)
        if not tokens:
            return "Unknown", None

        # Lookup Embeddings
        token_vecs = self.embeddings[tokens]

        # Context representation using Attention
        context = self.self_attention(token_vecs)

        # Output projection for last token
        last_context = context[-1]
        logits = np.dot(last_context, self.W_output)

        # Softmax probabilities
        probs = np.exp(logits) / np.sum(np.exp(logits))

        predicted_id = np.argmax(probs)
        return self.id2word[predicted_id], probs


# Execution Demo
if __name__ == "__main__":
    vocab = [
        "hello",
        "pankaj",
        "how",
        "are",
        "you",
        "ai",
        "code",
        "learning",
        "good",
    ]
    llm = MiniLLMSimulator(vocab)

    prompt = "hello pankaj how are"
    next_word, probabilities = llm.predict_next_word(prompt)

    print("=== INFINITYMinds - Mini LLM Attention Engine ===")
    print(f"Input Prompt: '{prompt}'")
    print(f"Predicted Next Word: '{next_word}'")
