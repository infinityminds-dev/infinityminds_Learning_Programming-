from datetime import datetime
import difflib
import glob
import json
import math
import os
import random
import re
from collections import Counter


class SmartIntentClassifier:
    """V3.6 Enhanced Intent Classifier Engine with Bigram Weights"""

    def __init__(self):
        self.intent_words = {}
        self.intent_bigrams = {}

    def tokenize(self, text):
        words = re.findall(r"\w+", text.lower())
        ignore = {"bhai", "bro", "oo", "ooo", "aa", "aah"}
        filtered = [w for w in words if w not in ignore]
        return filtered if filtered else words

    def get_bigrams(self, tokens):
        return [f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)]

    def train(self, memory_db):
        self.intent_words = {}
        self.intent_bigrams = {}

        if not isinstance(memory_db, list):
            return

        for item in memory_db:
            if not isinstance(item, dict):
                continue

            tag = item.get("tag")
            patterns = item.get("patterns", [])
            words_list = []
            bigrams_list = []

            for p in patterns:
                tokens = self.tokenize(p)
                words_list.extend(tokens)
                bigrams_list.extend(self.get_bigrams(tokens))

            if tag not in self.intent_words:
                self.intent_words[tag] = Counter(words_list)
                self.intent_bigrams[tag] = Counter(bigrams_list)
            else:
                self.intent_words[tag].update(words_list)
                self.intent_bigrams[tag].update(bigrams_list)

    def predict_intent(self, text, threshold=0.20):
        tokens = self.tokenize(text)
        bigrams = self.get_bigrams(tokens)

        if not tokens or not self.intent_words:
            return None, 0.0

        best_tag = None
        max_score = 0.0

        for tag, counts in self.intent_words.items():
            total_words = sum(counts.values())
            if total_words == 0:
                continue

            score = 0.0
            for token in tokens:
                if token in counts:
                    score += (counts[token] / total_words) * 1.5

            bigram_counts = self.intent_bigrams.get(tag, Counter())
            for bg in bigrams:
                if bg in bigram_counts:
                    score += 2.0

            score = score / (len(tokens) ** 0.4)

            if score > max_score:
                max_score = score
                best_tag = tag

        if max_score >= threshold:
            return best_tag, max_score
        return None, 0.0


class MainAIEngine:

    def __init__(self, user_name="Pankaj"):
        self.user_name = user_name.strip().lower()
        self.session_history = []
        self.last_unknown_query = None

        self.current_context = None
        self.last_responses = {}

        self.memory_file = self.handle_smart_memory_file()
        self.memory_db = []

        self.classifier = SmartIntentClassifier()
        self.load_memory()

    def get_non_repeating_choice(self, tag, responses):
        if not responses:
            return ""

        if len(responses) == 1:
            return responses[0]

        last_resp = self.last_responses.get(tag)

        available = [r for r in responses if r != last_resp]
        if not available:
            available = responses

        chosen = random.choice(available)
        self.last_responses[tag] = chosen
        return chosen

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
    "patterns": [
      "hi",
      "hello",
      "hey",
      "namaste",
      "oi",
      "hello bhai"
    ],
    "responses": [
      "Hello {name}!",
      "Oi {name}, kaise ho?"
    ],
    "context_responses": {}
  },
  {
    "tag": "status_ok",
    "patterns": [
      "theek hu",
      "thik hu",
      "mast hu",
      "badhiya hu",
      "badiya hu",
      "sab sahi hai"
    ],
    "responses": [
      "Sahi hai bhai, aise hi mast raho! 😎",
      "Accha laga sunkar {name}! 🔥"
    ],
    "context_responses": {}
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
      "got it"
    ],
    "responses": [
      "Sahi hai bhai!",
      "Haan {name}, aur batao?",
      "Got it! 👍"
    ],
    "context_responses": {}
  },
  {
    "tag": "courtesy",
    "patterns": [
      "thanks",
      "thank you",
      "shukriya",
      "dhanyawad"
    ],
    "responses": [
      "Arre koi baat nahi {name} bhai! 🙌",
      "Welcome bhai!",
      "Always happy to help! ✨"
    ],
    "context_responses": {}
  },
  {
    "tag": "goodbye",
    "patterns": [
      "bye",
      "goodbye",
      "chalo bye",
      "see you",
      "alvida"
    ],
    "responses": [
      "Bye {name}! Phir milte hain. 👋",
      "Chalo sahi hai, apna khyal rakhna! Take care."
    ],
    "context_responses": {}
  },
  {
    "tag": "agreement_disagreement",
    "patterns": [
      "haan",
      "ha",
      "nahi",
      "no",
      "na",
      "kuch nahi"
    ],
    "responses": [
      "Theek hai bhai, samajh gaya.",
      "Okay {name} bhai! Jab bhi zarurat ho, aawaz dena. 🤝",
      "Sahi hai! Phir kabhi fursat me baat karte hain."
    ],
    "context_responses": {}
  },
  {
    "tag": "compliment",
    "patterns": [
      "good",
      "nice",
      "great",
      "badiya",
      "bohot achha",
      "mast",
      "oo bahi good"
    ],
    "responses": [
      "Shukriya {name} bhai! Dil jeet liya! ❤️",
      "Thanks {name}! 🚀",
      "Khushi hui sunkar! 😊"
    ],
    "context_responses": {}
  },
  {
    "tag": "bot_identity",
    "patterns": [
      "tum kon hon",
      "tum kaun ho",
      "who are you",
      "tumhe kisne banaya",
      "who created you",
      "about yourself",
      "tera naam kya hai",
      "tera naam kya",
      "tera naam"
    ],
    "responses": [
      "Main INFINITY-AI hoon! 🤖 Mujhe Pankaj Singh ne Python me scratch se banaya hai. Agar aapko developer ke baare me aur jaanna hai toh unke GitHub pe jaa sakte hain aur unke Discord pe pooch sakte hain sawal ya koi suggestion. Discord ki link unke GitHub profile me hai.\n\nDeveloper GitHub Profile: infinityminds-dev"
    ],
    "context_responses": {}
  },
  {
    "tag": "daily_activity_suggestions",
    "patterns": [
      "chal bata aaj kya karna hai",
      "aaj kya kare",
      "kya kare aaj",
      "aaj kya karna chahiye",
      "bor ho raha hu kya karu",
      "kya karu aaj",
      "bor ho raha hu",
      "kya plan hai ajj ka",
      "kya plan hai aaj ka"
    ],
    "responses": [
      "Arre bhai mood ke hisab se plan banao! 🎯 Agar energy hai toh thodi coding kar lo ya koi naya project try kar lo 💻. Thoda chill karna hai toh mast music suno 🎧 ya koi game khel lo 🎮. Aur agar bilkul bhi man nahi kar raha toh aaram se rest kar lo 🛌, dosto se baat kar lo 🗣️ ya thodi der walk pe ho aao 🚶‍♂️. Aap batao, kis cheez ka mood hai?"
    ],
    "context_responses": {
      "music": "Mast playlist lagao aur headphone pehen ke chill karo bhai! 🎧🎶",
      "game": "Kaunsa game khelne ka plan hai? PC game ya mobile game? 🎮🔥",
      "mobile": "Mast BGMI, Free Fire ya Call of Duty lagao aur dosto ke saath machao! 📱💥",
      "pc": "Sahi hai! GTA, Valorant ya Counter-Strike me se kya chalayein? 🖥️🎯",
      "coding": "Sahi hai! Aaj kaunsa naya feature code karne wale ho? 💻⚡"
    }
  },
  {
    "tag": "music_intent",
    "patterns": [
      "music",
      "music sun lo",
      "gaana sun leta hu",
      "chal music sun leta hu",
      "gaane sunne hain"
    ],
    "responses": [
      "Haan bhai! Music sun ke mind ekdam relax ho jata hai 🎶. Apne favorite songs lagao aur chill karo!"
    ],
    "context_responses": {}
  },
  {
    "tag": "game_intent",
    "patterns": [
      "game khelna hai",
      "mobile game",
      "pc game",
      "game khel lu",
      "chal game khelte hain"
    ],
    "responses": [
      "Sahi hai bhai! 🎮 Konsa game khelne ka socha hai?"
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
      "programming language",
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
      "sql",
      "tech",
      "github",
      "tujha coding ka bare ma kuch pata hai",
      "tumhe coding ke bare me pata hai",
      "coding aati hai kya",
      "coding ke bare me pata hai",
      "loop kya hai"
    ],
    "responses": [
      "Mujhe abhi coding aur tech ke baare me zyada jankari nahi hai 😅. Iske liye aap ChatGPT ya Gemini jaise Large Language Models (LLM) se pooch sakte hain 🤖. Developer ne abhi mujhe itna develop nahi kiya hai, lekin in future main iska jawab zaroor de paunga!"
    ],
    "context_responses": {}
  },
  {
    "tag": "low_energy_mood",
    "patterns": [
      "maan nahi kar raha hai kuch kar na ka",
      "man nahi kar raha hai kuch karne ka",
      "kuch karne ka man nahi hai",
      "kuch karne ka maan nahi hai",
      "aaj kuch nahi karna",
      "man nahi hai aaj"
    ],
    "responses": [
      "Toh mat kar bhai! 🛌 Aaj rest kar lo, fresh mind ke saath kal machayenge 🔥"
    ],
    "context_responses": {}
  },
  {
    "tag": "bot_status_query",
    "patterns": [
      "tu bata",
      "tu bata bhai",
      "apna batao"
    ],
    "responses": [
      "Main bhi ekdam mast hu bhai! 😎 Aap batao koi kaam ho toh"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_2064",
    "patterns": [
      "ooo",
      "oo"
    ],
    "responses": [
      "Yes bhai! 💯"
    ],
    "context_responses": {}
  },
  {
    "tag": "bot_capabilities",
    "patterns": [
      "tu kya kar sakta hai",
      "tum kya kar sakte ho",
      "kya kya kar sakte ho",
      "tumhare features kya hain",
      "what can you do"
    ],
    "responses": [
      "Main aapka personal AI assistant hoon! 🚀 Main ye sab kar sakta hoon:\n1. Mood ke hisab se activity suggest kar sakta hoon 🎯\n2. Math calculations solve kar sakta hoon 🧮\n3. Session history aur purane sawal yaad rakh sakta hoon 🧠\n4. Naye jawab seekh kar memory save kar sakta hoon 💾\n5. Context samajh kar multi-turn conversation kar sakta hoon! 🔄\n\nAap batao, main aapki kya help karoon?"
    ],
    "context_responses": {}
  },
  {
    "tag": "bot_current_activity",
    "patterns": [
      "tu kya kar raha hai",
      "tum kya kar rahe ho",
      "kya kar raha hai",
      "kya kar rahe ho"
    ],
    "responses": [
      "Bas {name} bhai, aapke messages ka wait kar raha hoon aur apni memory update kar raha hoon! ⚡ Aap batao, kya chal raha hai?"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_5567",
    "patterns": [
      "i am back"
    ],
    "responses": [
      "Oo bhai aa gaya! 🔥 Chal bata koi kaam hai?"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_6423",
    "patterns": [
      "good Morning bhai",
      "good morning",
      "good morning bro"
    ],
    "responses": [
      "Good Morning bhai! 🌅 Uth gaya so ke, ab bata kya karna hai?"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_1812",
    "patterns": [
      "Good night bhai",
      "good night",
      "good night bro"
    ],
    "responses": [
      "Good Night Bhai! 🌙 Sweet dreams!"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_5087",
    "patterns": [
      "Good evening",
      "good evening bhai",
      "good evening bro"
    ],
    "responses": [
      "Good Evening bhai! 🌆 Kya plan hai aaj ka?"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_afternoon",
    "patterns": [
      "good afternoon",
      "good afternoon bhai",
      "afternoon bro"
    ],
    "responses": [
      "Good Afternoon {name} bhai! ☀️ Khana peena ho gaya ya nahi?"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_jokes",
    "patterns": [
      "joke sunao",
      "chutkula sunao",
      "koi joke batao",
      "hassa do bhai"
    ],
    "responses": [
      "Teacher: 1 se 10 tak ginti sunao!\nStudent: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10!\nTeacher: Shabash! Aage?\nStudent: J, Q, K! 🃏😂",
      "Ek aadmi doctor ke paas gaya: Doctor sahab jab mai chai pita hu to meri aakh me dard hota hai!\nDoctor: Pehle cup me se chammach nikal liya karo! ☕😜",
      "Pappu: Yaar mera mobile pani me gir gaya aur kharab ho gaya.\nFriend: Toh dukandar ko dikhaya?\nPappu: Haan, usne bola isme rice me daal ke rakho.\nFriend: Phir kya hua?\nPappu: Kucch nahi, mobile chawal ke sath pak gaya! 📱🍚",
      "Teacher: Tumne kal homework kyon nahi kiya?\nStudent: Sir, bijli nahi thi.\nTeacher: Toh mombatti jala lete!\nStudent: Sir, maachis nahi thi.\nTeacher: Maachis kyon nahi thi?\nStudent: Pooja ke ghar me rakhi thi.\nTeacher: Toh wahan se le aate!\nStudent: Sir, nahaaya hua nahi tha! 🕯️🤣",
      "Customer: Bhai, is phone me net fast chalta hai kya?\nDukandar: Pata nahi bhai, kal ek banda le gaya tha, aaj tak wapas hi nahi aaya... speed me kahin aage nikal gaya hoga! 🚀📱",
      "Papa: Beta tumhare result ka kya hua?\nBeta: Papa, doctor ka beta doctor bana, engineer ka beta engineer!\nPapa: Aur tum?\nBeta: Main toh mazdoor ka beta hoon na papa, toh fail ho gaya! 👷‍♂️📖",
      "Husband: Aaj khane me kya banaya hai?\nWife: Jo tumne kal bola tha na wahi!\nHusband: Par kal toh maine bola tha ki zahar de do!\nWife: Toh bas wahi bana diya hai, chup chap kha lo! 🍜💀🤣",
      "Santa: Yaar, mera dimaag bohot tez chalta hai!\nBanta: Kaise?\nSanta: Kal train chootne me 2 min bache the, main 1 min pehle hi pahunch gaya! 🏃‍♂️🚂",
      "Boy: Tum itni sundar kaise ho?\nGirl: God ki kripa hai!\nBoy: Lagta hai God ne tum par poori kripa kar di, baaki sab par aalsi ho gaye! 🙄✨",
      "Doctor: Aapko kaunsa rog hai?\nPatient: Doctor sahab, jab bhi kaam karne lagta hoon, neend aane lagti hai!\nDoctor: Ye rog nahi, isse alsi-pan kehte hain! 🛌💤"
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_7212",
    "patterns": [
      "oo new respones",
      "hahahahahhahaha",
      "ya badiya tha",
      "good joke"
    ],
    "responses": [
      "Thank you bhai apki training ki vajah se 🥰🔥 "
    ],
    "context_responses": {}
  },
  {
    "tag": "custom_3253",
    "patterns": [
      "nachooook"
    ],
    "responses": [
      "lekin kyo nachooo bhai kya baat hai"
    ],
    "context_responses": {}
  }
]


        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.memory_db = (
                        data if isinstance(data, list) else default_data
                    )
            except Exception:
                self.memory_db = default_data
        else:
            self.memory_db = default_data
            self.save_memory()

        self.classifier.train(self.memory_db)

    # ------------------ EMOJI FIX HERE ------------------
    def clean_text_for_json(self, text):
        if not isinstance(text, str):
            return text
        return text.strip()  # Ascii strip hata diya taaki Emojis save rahein!
    # ----------------------------------------------------

    def save_memory(self):
        cleaned_db = []
        if isinstance(self.memory_db, list):
            for item in self.memory_db:
                if not isinstance(item, dict):
                    continue

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
                            "context_responses": item.get(
                                "context_responses", {}
                            ),
                        }
                    )

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(cleaned_db, f, indent=2, ensure_ascii=False)

        self.classifier.train(self.memory_db)

    def generate_proactive_greeting(self):
        greetings = [
            f"Hey {self.user_name.capitalize()}! Main ready hoon, aaj kya chal raha hai? 😎",
            f"Oi {self.user_name.capitalize()}! Welcome back. Batao aaj kya plan hai? 🚀",
            f"Yo {self.user_name.capitalize()}! INFINITY-AI online hai, kaise ho aaj? 🔥",
        ]
        return random.choice(greetings)

    def learn_new_response(self, user_query, correct_response):
        query_clean = self.clean_text_for_json(user_query.lower())
        response_clean = self.clean_text_for_json(correct_response)

        if not query_clean or not response_clean:
            return

        learned = False
        for item in self.memory_db:
            if isinstance(item, dict) and "patterns" in item:
                if query_clean in [p.lower() for p in item["patterns"]]:
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
                    "context_responses": {},
                }
            )

        self.save_memory()

    def get_current_time_slot(self):
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"

    def check_time_greeting_correction(self, text_lower):
        current_slot = self.get_current_time_slot()

        greetings_map = {
            "morning": ["good morning", "gm", "morning"],
            "afternoon": ["good afternoon", "afternoon"],
            "evening": ["good evening", "ge", "evening"],
            "night": ["good night", "gn", "night"],
        }

        hindi_slot_names = {
            "morning": "Morning/Subah",
            "afternoon": "Afternoon/Dopahar",
            "evening": "Evening/Shaam",
            "night": "Night/Raat",
        }

        detected_slot = None
        for slot, keywords in greetings_map.items():
            if any(k in text_lower for k in keywords):
                detected_slot = slot
                break

        if detected_slot and detected_slot != current_slot:
            actual = hindi_slot_names[current_slot]
            return f"Arre {self.user_name.capitalize()} bhai, abhi {actual} ho raha hai! Pehle ghadi toh dekh lo 😜"

        return None

    def check_dynamic_advice(self, text_lower):
        mood_triggers = {
            "bored": ["bore", "boring", "paka", "kuch nahi kar raha"],
            "tired": ["thak", "tired", "sleepy", "neend"],
            "stressed": ["stress", "tension", "pareshan", "headache"],
        }

        detected_mood = None
        for mood, keys in mood_triggers.items():
            if any(k in text_lower for k in keys):
                detected_mood = mood
                break

        if detected_mood == "bored":
            advice_list = [
                f"{self.user_name.capitalize()} bhai, thodi der fav playlist chala ke dance kar le ya game khel le! 🎧🎮",
                f"Bore ho rahe ho toh 15-min ki walk le aao ya koi joke suno! 🚶‍♂️🤣",
            ]
            return random.choice(advice_list)

        elif detected_mood == "tired":
            advice_list = [
                f"{self.user_name.capitalize()} bhai, screen off karo aur 20-min ka power nap le lo! 😴🛌",
                "Thoda thanda paani piyo aur stretch kar lo, energy wapas aayegi! 🥤✨",
            ]
            return random.choice(advice_list)

        elif detected_mood == "stressed":
            advice_list = [
                "Bhai bilkul tension mat lo. Lambi saans lo aur 10 min coding se break le lo! 🧘‍♂️✨",
                "Stress lene se kuch nahi hoga, thoda relaxed music suno aur chai/coffee piyo! ☕🎧",
            ]
            return random.choice(advice_list)

        return None

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

        match = re.search(r"[\d\.\s\+\-\*\/\(\)\^\,]+", clean_text)
        if match:
            expr = match.group().strip()
            expr = re.sub(r"[\+\-\*\/]+$", "", expr).strip()

            has_op = any(op in expr for op in ["+", "-", "*", "/", "**"])
            has_func = any(fn in expr for fn in safe_dict.keys())

            if (has_op or has_func) and len(expr) > 1:
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

    def find_fuzzy_match(self, input_text, cutoff=0.55):
        best_match_item = None
        highest_ratio = 0.0

        for item in self.memory_db:
            if not isinstance(item, dict):
                continue
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

    def check_context_reply(self, text_lower):
        if not self.current_context:
            return None

        for item in self.memory_db:
            if isinstance(item, dict) and item.get("tag") == self.current_context:
                ctx_responses = item.get("context_responses", {})
                for key, resp in ctx_responses.items():
                    if key in text_lower:
                        self.current_context = None
                        return resp.replace("{name}", self.user_name)
        return None

    def process_single_query(self, sub_query):
        sub_text = sub_query.strip()
        if not sub_text:
            return None

        text_lower = sub_text.lower()

        time_corrected = self.check_time_greeting_correction(text_lower)
        if time_corrected:
            return time_corrected

        advice = self.check_dynamic_advice(text_lower)
        if advice:
            return advice

        math_ans = self.solve_math(sub_text)
        if math_ans:
            return math_ans

        hist_ans = self.get_full_session_history_reply(sub_text)
        if hist_ans:
            return hist_ans

        ctx_reply = self.check_context_reply(text_lower)
        if ctx_reply:
            return ctx_reply

        for item in self.memory_db:
            if isinstance(item, dict) and "patterns" in item:
                if text_lower in [p.lower() for p in item["patterns"]]:
                    if "responses" in item and item["responses"]:
                        self.current_context = item.get("tag")
                        chosen = self.get_non_repeating_choice(item.get("tag"), item["responses"])
                        return chosen.replace("{name}", self.user_name)

        predicted_tag, score = self.classifier.predict_intent(
            text_lower, threshold=0.20
        )
        if predicted_tag:
            for item in self.memory_db:
                if (
                    isinstance(item, dict)
                    and item.get("tag") == predicted_tag
                    and item.get("responses")
                ):
                    self.current_context = predicted_tag
                    chosen = self.get_non_repeating_choice(predicted_tag, item["responses"])
                    return chosen.replace("{name}", self.user_name)

        fuzzy_item, similarity = self.find_fuzzy_match(text_lower, cutoff=0.55)
        if (
            fuzzy_item
            and isinstance(fuzzy_item, dict)
            and "responses" in fuzzy_item
        ):
            tag = fuzzy_item.get("tag")
            self.current_context = tag
            chosen = self.get_non_repeating_choice(tag, fuzzy_item["responses"])
            return chosen.replace("{name}", self.user_name)

        return None

    def respond(self, user_input):
        raw_text = user_input.strip()
        if not raw_text:
            return "Kuch bologe tabhi toh jawab doonga! 😉"

        if self.last_unknown_query is not None:
            prompt_query = self.last_unknown_query
            self.last_unknown_query = None
            self.learn_new_response(prompt_query, raw_text)
            return f"Got it {self.user_name}! Seekh gaya. Ab se '{prompt_query}' par yahi jawab doonga! 😎👌"

        self.session_history.append({"role": "user", "content": raw_text})

        math_pattern = r"(\d+[\+\-\*\/]+\d+[\+\-\*\/\d]*)"
        prepared_text = re.sub(math_pattern, r", \1 ,", raw_text)
        parts = re.split(r",|\.|\?|\s+aur\s+|\s+or\s+", prepared_text)

        responses = []
        unknown_part = None

        for part in parts:
            part_str = part.strip()
            if not part_str:
                continue

            ans = self.process_single_query(part_str)
            if ans:
                if ans not in responses:
                    responses.append(ans)
            else:
                if len(part_str) > 2 and not part_str.isdigit():
                    unknown_part = part_str

        if responses:
            if len(responses) == 1:
                return responses[0]
            else:
                formatted_resp = "\n" + "\n".join([f"• {r}" for r in responses])
                return formatted_resp

        if unknown_part:
            self.last_unknown_query = unknown_part
            return f"Mujhe iska matlab nahi pata '{unknown_part}' ({self.user_name}). Jab main ye suno, toh kya jawab doon? 🤔"

        self.last_unknown_query = raw_text
        return f"Mujhe iska matlab nahi pata {self.user_name}. Jab main '{raw_text}' suno, toh kya jawab doon? 🤔"


if __name__ == "__main__":
    user_name = input("Enter your name: ").strip() or "Pankaj"
    ai = MainAIEngine(user_name=user_name)

    print("\n========================================================")
    print(f"  FINAL ENGINE V3.6 SMART ACTIVE | File: {ai.memory_file}")
    print("========================================================\n")

    print(f"AI: {ai.generate_proactive_greeting()}\n")

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
