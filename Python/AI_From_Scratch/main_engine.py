import difflib
import glob
import json
import math
import os
import random
import re


class MainAIEngine:

    def __init__(self, user_name="Pankaj"):
        self.user_name = user_name.strip().lower()
        self.session_history = []
        self.last_unknown_query = None

        self.memory_file = self.handle_smart_memory_file()
        self.memory_db = []
        self.load_memory()

    def handle_smart_memory_file(self):
        if self.user_name == "pankaj":
            master_file = "ai_memory_pankaj_master.json"
            if os.path.exists(master_file):
                print(
                    f"\n[Access Granted] Welcome back Developer Pankaj! Loading Master File: {master_file}"
                )
            else:
                print(
                    f"\n[Info] Creating Developer Master Brain file: {master_file}"
                )
            return master_file

        if "pankaj" in self.user_name:
            print("\n" + "=" * 65)
            print(
                "❌ ACCESS DENIED: You cannot create a file starting with 'Pankaj'!"
            )
            print("Reason: This is the main developer master file.")
            print("=" * 65 + "\n")
            self.user_name = "guest_user"

        existing_files = glob.glob("ai_memory_*.json")
        user_specific_files = [
            f for f in existing_files if f"_{self.user_name}_" in f
        ]

        if user_specific_files:
            print(
                f"\n[Info] Tumhari purani memory file mil gayi: {user_specific_files[0]}"
            )
            return user_specific_files[0]

        if existing_files:
            print(
                f"\n[Notice] System me pehle se ye memory files maujood hain: {existing_files}"
            )
            choice = (
                input(
                    f"Kya tum 'ai_memory_{self.user_name}_xxxx.json' ki ek nayi file banana chahte ho? (y/n): "
                )
                .strip()
                .lower()
            )

            if choice == "n":
                selected = (
                    input("Kis purani file ko use karna hai uska naam daalo: ")
                    .strip()
                )
                if selected and os.path.exists(selected):
                    return selected

        random_id = random.randint(1000, 9999)
        new_file = f"ai_memory_{self.user_name}_{random_id}.json"
        print(f"\n[Info] Nayi memory file ban rahi hai: {new_file}")
        return new_file

    def load_memory(self):
        default_data = [
            {
                "tag": "greeting",
                "patterns": ["hi", "hello", "hey", "namaste"],
                "responses": ["Hello {name}!", "Oi {name}, kaise ho?"],
            },
            {
                "tag": "status_ok",
                "patterns": ["theek hu", "thik hu", "mast hu", "badhiya hu"],
                "responses": [
                    "Sahi hai bhai, aise hi mast raho!",
                    "Accha laga sunkar {name}!",
                ],
            },
            {
                "tag": "acknowledgement",
                "patterns": [
                    "ok",
                    "okay",
                    "k",
                    "hmm",
                    "accha",
                    "achha",
                    "sahi hai",
                ],
                "responses": [
                    "Sahi hai bhai!",
                    "Haan {name}, aur batao?",
                    "Got it!",
                ],
            },
            {
                "tag": "courtesy",
                "patterns": ["thanks", "thank you", "shukriya", "dhanyawad"],
                "responses": [
                    "Arre koi baat nahi {name} bhai!",
                    "Welcome bhai!",
                    "Always happy to help!",
                ],
            },
            {
                "tag": "goodbye",
                "patterns": ["bye", "goodbye", "chalo bye", "see you"],
                "responses": [
                    "Bye {name}! Phir milte hain.",
                    "Chalo sahi hai, apna khyal rakhna!",
                ],
            },
            {
                "tag": "agreement_disagreement",
                "patterns": ["haan", "ha", "nahi", "no", "na"],
                "responses": [
                    "Theek hai bhai, samajh gaya.",
                    "Okay, jaisa aap bolo {name}!",
                ],
            },
            {
                "tag": "compliment",
                "patterns": ["good", "nice", "great", "badiya", "bohot achha"],
                "responses": [
                    "Shukriya {name} bhai!",
                    "Thanks {name}!",
                    "Khushi hui sunkar!",
                ],
            },
  {
    "tag": "bot_identity",
    "patterns": [
      "tum kon ho",
      "tum kaun ho",
      "who are you",
      "tumhe kisne banaya",
      "who created you",
      "about yourself"
    ],
    "responses": [
      "Main INFINITY-AI hoon. Mujhe Pankaj Singh ne Python me scratch se banaya hai. Agar aapko developer ke baare me aur jaanna hai toh unke GitHub pe jaa sakte hain aur unke Discord pe pooch sakte hain sawal ya koi suggestion. Discord ki link unke GitHub profile me hai.\n\nDeveloper GitHub Profile: infinityminds-dev"
    ],
    "context_responses": {}
  },
    {
    "tag": "tech_coding_fallback",
    "patterns": [
      "python",
      "coding",
      "code",
      "programming",
      "javascript",
      "html",
      "css",
      "java",
      "c++",
      "bug",
      "error",
      "loop",
      "function",
      "array",
      "database",
      "sql"
    ],
    "responses": [
      "Mujhe abhi coding aur tech ke baare me zyada jankari nahi hai. Iske liye aap ChatGPT ya Gemini jaise Large Language Models (LLM) se pooch sakte hain. Developer ne abhi mujhe itna develop nahi kiya hai, lekin in future main iska jawab zaroor de paunga!"
    ],
    "context_responses": {}
  }


        
 ]
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    self.memory_db = json.load(f)
            except Exception:
                self.memory_db = default_data
        else:
            self.memory_db = default_data
            self.save_memory()

    def clean_text_for_json(self, text):
        if not isinstance(text, str):
            return text
        return text.encode("ascii", "ignore").decode("ascii").strip()

    def save_memory(self):
        cleaned_db = []
        for item in self.memory_db:
            clean_patterns = [
                self.clean_text_for_json(p)
                for p in item.get("patterns", [])
                if self.clean_text_for_json(p)
            ]
            clean_responses = [
                self.clean_text_for_json(r)
                for r in item.get("responses", [])
                if self.clean_text_for_json(r)
            ]

            if clean_patterns and clean_responses:
                cleaned_db.append(
                    {
                        "tag": item.get("tag", "general"),
                        "patterns": clean_patterns,
                        "responses": clean_responses,
                        "context_responses": item.get("context_responses", {}),
                    }
                )

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_db, f, indent=2, ensure_ascii=False)

    def learn_new_response(self, user_query, correct_response):
        query_clean = self.clean_text_for_json(user_query.lower())
        response_clean = self.clean_text_for_json(correct_response)

        if not query_clean or not response_clean:
            return

        learned = False
        for item in self.memory_db:
            if "patterns" in item and query_clean in [
                p.lower() for p in item["patterns"]
            ]:
                if "responses" in item:
                    if response_clean not in item["responses"]:
                        item["responses"].append(response_clean)
                    learned = True
                    break

        if not learned:
            self.memory_db.append(
                {
                    "tag": f"custom_{random.randint(1000, 9999)}",
                    "patterns": [query_clean],
                    "responses": [response_clean],
                }
            )

        self.save_memory()

    def solve_math(self, text):
        clean_text = (
            text.lower().replace("x", "*").replace("=", "").replace("^", "**")
        )

        safe_dict = {
            "sqrt": math.sqrt,
            "sin": lambda x: round(math.sin(math.radians(x)), 4),
            "cos": lambda x: round(math.cos(math.radians(x)), 4),
            "tan": lambda x: round(math.tan(math.radians(x)), 4),
            "fact": math.factorial,
            "abs": abs,
            "pi": math.pi,
            "e": math.e,
        }

        match = re.search(r"[\d\.\s\+\-\*\/\(\)\^\,\w]+", clean_text)
        if match:
            expr = match.group().strip()
            expr = re.sub(r"[\+\-\*\/]+$", "", expr)

            has_op = any(op in expr for op in ["+", "-", "*", "/", "**"])
            has_func = any(fn in expr for fn in safe_dict.keys())

            if has_op or has_func:
                try:
                    res = eval(expr, {"__builtins__": None}, safe_dict)
                    if isinstance(res, float) and res.is_integer():
                        res = int(res)
                    return f"Math: {expr} = {res}"
                except Exception:
                    return None
        return None

    def get_full_session_history_reply(self, text):
        text_lower = text.lower()
        if any(
            k in text_lower
            for k in [
                "sawal",
                "history",
                "pehle",
                "pehla",
                "phele",
                "question",
                "kya kya",
            ]
        ):
            user_queries = [
                h["content"]
                for h in self.session_history
                if h["role"] == "user"
            ]
            if len(user_queries) <= 1:
                return "Abhi tak session me aur koi purana sawal nahi hai!"

            past_all = [
                f"{i+1}. {q}" for i, q in enumerate(user_queries[:-1])
            ]
            return "Poori Session History -> " + " | ".join(past_all)
        return None

    def find_fuzzy_match(self, input_text, cutoff=0.65):
        best_match_item = None
        highest_ratio = 0.0

        for item in self.memory_db:
            for pattern in item.get("patterns", []):
                ratio = difflib.SequenceMatcher(
                    None, input_text.lower(), pattern.lower()
                ).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match_item = item

        if highest_ratio >= cutoff:
            return best_match_item, highest_ratio
        return None, 0.0

    def process_single_query(self, sub_query):
        sub_text = sub_query.strip()
        if not sub_text:
            return None

        math_ans = self.solve_math(sub_text)
        if math_ans:
            return math_ans

        hist_ans = self.get_full_session_history_reply(sub_text)
        if hist_ans:
            return hist_ans

        text_lower = sub_text.lower()

        for item in self.memory_db:
            if "patterns" in item and text_lower in [
                p.lower() for p in item["patterns"]
            ]:
                if "responses" in item and item["responses"]:
                    return random.choice(item["responses"]).replace(
                        "{name}", self.user_name
                    )

        fuzzy_item, similarity = self.find_fuzzy_match(
            text_lower, cutoff=0.65
        )
        if fuzzy_item and "responses" in fuzzy_item:
            return random.choice(fuzzy_item["responses"]).replace(
                "{name}", self.user_name
            )

        return None

    def respond(self, user_input):
        raw_text = user_input.strip()
        if not raw_text:
            return "Kuch bologe tabhi toh jawab doonga!"

        if self.last_unknown_query is not None:
            prompt_query = self.last_unknown_query
            self.last_unknown_query = None
            self.learn_new_response(prompt_query, raw_text)
            return f"Got it {self.user_name}! Seekh gaya. Ab se '{prompt_query}' par yahi jawab doonga!"

        self.session_history.append({"role": "user", "content": raw_text})

        parts = re.split(r",|\s+aur\s+", raw_text, maxsplit=2)
        responses = []
        unknown_part = None

        for part in parts:
            ans = self.process_single_query(part)
            if ans:
                responses.append(ans)
            else:
                unknown_part = part.strip()
                break

        if unknown_part and not responses:
            self.last_unknown_query = unknown_part
            return f"Mujhe iska matlab nahi pata '{unknown_part}' ({self.user_name}). Jab main ye suno, toh kya jawab doon?"

        if responses:
            return " | ".join(responses)

        self.last_unknown_query = raw_text
        return f"Mujhe iska matlab nahi pata {self.user_name}. Jab main '{raw_text}' suno, toh kya jawab doon?"


if __name__ == "__main__":
    user_name = input("Enter your name: ").strip() or "Pankaj"
    ai = MainAIEngine(user_name=user_name)

    print("\n========================================================")
    print(f"  FINAL ENGINE ACTIVE | File: {ai.memory_file}")
    print("========================================================\n")

    while True:
        try:
            user_input = input(f"{ai.user_name}: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print(
                    f"Session Ended. Permanent Brain saved in {ai.memory_file}!"
                )
                break

            response = ai.respond(user_input)
            print(f"AI: {response}\n")

        except (EOFError, KeyboardInterrupt):
            break
