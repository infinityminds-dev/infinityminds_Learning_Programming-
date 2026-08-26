# 🧠 Self-Learning Conversational AI Engine

A lightweight, zero-heavy-dependency Python AI engine built completely from scratch. It features live interactive self-learning, multi-query splitting, full session history tracking, built-in math calculation, and a smart multi-user memory merging system!

---

### 🚀 Core Features & Capabilities

* **Live Interactive Training:** If the AI doesn't understand a query, it interactively asks you for the correct response and updates its brain instantly.
* **Auto-Correct (Fuzzy Matching):** Uses spelling similarity checks (`difflib`) to handle minor typos seamlessly.
* **Multi-Sentence Splitting:** Can break down complex or multi-part user messages (joined by commas or "aur") to handle them sequentially.
* **Dynamic Math Solver:** Instantly evaluates arithmetic expressions directly within the chat.
* **Full Session Chat History:** Remembers the entire active conversation thread until you exit.
* **Smart Memory Merging:** Safely combines training data from multiple contributors without risking priority data loss.

---

### 📋 Project Structure & Files

| File Name          | Purpose                     | Key Concept                                                        |
| :----------------- | :-------------------------- | :----------------------------------------------------------------- |
| `main_engine.py`   | Main Conversational Runtime | Live training, auto-correct, session context, and math processing. |
| `merge_memory.py`  | Multi-User Memory Merger    | Safely merges friend training JSONs into your master brain.        |
| `ai_memory_*.json` | Persistent AI Brain File    | Dynamic JSON storage for patterns, intents, and trained responses. |

---

## 🛠️ How to Run & Train

### 1. ▶️ Start the AI Engine

Open your terminal in the project directory and run:

```bash
python main_engine.py
```

This will start the AI engine and open the interactive chat session.

### 2. 🧠 Train Live & Chat

Chat naturally with the AI.

If the AI doesn't understand your input, it will ask:

> **"Mujhe iska matlab nahi pata... toh kya jawab doon?"**

Type the response you want the AI to learn.

The custom response will be saved **permanently** into the AI's memory file, allowing the AI to use the learned response in future conversations.

### 3. 🤝 Merge Friend Memories

To combine training data from your friends:

1. Place your friends' exported JSON memory files inside the project directory.
2. Make sure the files contain the required AI memory data.
3. Run the merge script:

```bash
python merge_memory.py
```

The merge system will combine the available training data into your master AI memory while protecting existing priority data.

### 4. 🔄 Typical Workflow

```text
Start AI
   ↓
Chat with AI
   ↓
Unknown input?
   ↓
AI asks for the correct response
   ↓
Enter your response
   ↓
Response is saved to memory
   ↓
AI learns and uses it later
   ↓
Merge friend memories when needed
```
