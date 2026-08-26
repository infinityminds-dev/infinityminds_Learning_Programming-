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

| File Name | Purpose | Key Concept |
| :--- | :--- | :--- |
| `main_engine.py` | Main Conversational Runtime | Live training, auto-correct, session context, and math processing. |
| `merge_memory.py` | Multi-User Memory Merger | Safely merges friend training JSONs into your master brain. |
| `ai_memory_*.json` | Persistent AI Brain File | Dynamic JSON storage for patterns, intents, and trained responses. |

---

### 🛠️ How to Run & Train
Start the AI Engine:
Run the following command in your terminal:
python main_engine.py
Train Live:
Chat naturally. If an input is unknown, the AI will prompt you: "Mujhe iska matlab nahi pata... toh kya jawab doon?" Type the response, and it will be saved permanently!
Merge Friend Memories:
Place your friends' exported JSON files in the directory and run:
python merge_memory.py
   
