import numpy as np


# ==========================================
# 1. MATHEMATICAL ACTIVATIONS
# ==========================================
def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def relu(x):
    return np.maximum(0, x)


# ==========================================
# 2. WORKING AI ENGINE CLASS
# ==========================================
class SimpleWorkingAI:

    def __init__(self, vocabulary, intents):
        self.vocab = vocabulary
        self.intents = intents
        self.vocab_size = len(vocabulary)
        self.num_classes = len(intents)

        # Word to Index mappings
        self.word2id = {w: i for i, w in enumerate(vocabulary)}

        # Neural Network Weights (Memory)
        np.random.seed(42)
        self.hidden_dim = 8
        self.W1 = np.random.randn(self.vocab_size, self.hidden_dim) * 0.1
        self.b1 = np.zeros((1, self.hidden_dim))
        self.W2 = np.random.randn(self.hidden_dim, self.num_classes) * 0.1
        self.b2 = np.zeros((1, self.num_classes))

    # Tokenization & Bag of Words (Text to Vector)
    def text_to_vector(self, text):
        vector = np.zeros((1, self.vocab_size))
        words = text.lower().split()
        for w in words:
            if w in self.word2id:
                vector[0, self.word2id[w]] = 1.0
        return vector

    # Forward Pass (Thinking Process)
    def think(self, input_vector):
        # Hidden Layer
        self.h = relu(np.dot(input_vector, self.W1) + self.b1)
        # Output Probabilities
        logits = np.dot(self.h, self.W2) + self.b2
        probs = softmax(logits)
        return probs

    # Training (Learning Process)
    def train(self, training_data, epochs=500, lr=0.1):
        for epoch in range(epochs):
            for text, target_class in training_data:
                x = self.text_to_vector(text)
                y_true = np.zeros((1, self.num_classes))
                y_true[0, target_class] = 1.0

                # Forward
                probs = self.think(x)

                # Backpropagation (Gradient Descent)
                error = probs - y_true
                dW2 = np.dot(self.h.T, error)
                db2 = error
                dh = np.dot(error, self.W2.T)
                dh[self.h <= 0] = 0
                dW1 = np.dot(x.T, dh)
                db1 = dh

                # Update Weights
                self.W2 -= lr * dW2
                self.b2 -= lr * db2
                self.W1 -= lr * dW1
                self.b1 -= lr * db1

    # Response Generation
    def reply(self, user_prompt):
        x = self.text_to_vector(user_prompt)
        probs = self.think(x)
        predicted_class = np.argmax(probs)
        confidence = probs[0, predicted_class]

        if confidence < 0.4:
            return "Mujhe ye samajh nahi aaya, thoda alag tarike se poochho."

        return self.intents[predicted_class]["response"]


# ==========================================
# 3. LIVE WORKING CHATBOT SYSTEM
# ==========================================
if __name__ == "__main__":
    # Vocabulary (AI ke seekhne ke shabda)
    vocab = [
        "hi",
        "hello",
        "hey",
        "kaise",
        "ho",
        "kaun",
        "ho",
        "tum",
        "naam",
        "kya",
        "hai",
        "bye",
        "alvida",
    ]

    # Intent Classes & Responses
    intents = {
        0: {
            "name": "greeting",
            "response": "Hello Pankaj bhai! Main ek Working AI hoon. Aaj kya plan hai?",
        },
        1: {
            "name": "identity",
            "response": "Mera naam INFINITY-AI hai, jise Pankaj ne Python me scratch se banaya hai!",
        },
        2: {
            "name": "status",
            "response": "Main ekdam badhiya hoon! Apne Neural Network ke weights calculate kar raha hoon.",
        },
        3: {
            "name": "goodbye",
            "response": "Alvida bhai! Phir milte hain naye code ke sath.",
        },
    }

    # Training Dataset
    dataset = [
        ("hi", 0),
        ("hello", 0),
        ("hey", 0),
        ("kaun ho tum", 1),
        ("tumhara naam kya hai", 1),
        ("kaise ho", 2),
        ("kaise ho tum", 2),
        ("bye", 3),
        ("alvida", 3),
    ]

    print("=== Training AI Neural Network... ===")
    ai = SimpleWorkingAI(vocab, intents)
    ai.train(dataset, epochs=1000, lr=0.1)
    print("=== AI Training Complete! Live Chat Start ===\n")

    # Interactive Loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        ai_response = ai.reply(user_input)
        print(f"AI: {ai_response}\n")
