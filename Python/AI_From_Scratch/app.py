from datetime import datetime
import difflib
import glob
import json
import math
import os
import random
import re
from collections import Counter
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

active_ai = None
current_model_name = "None"
startup_notice = ""
selected_model_val = "v3.6"
selected_memory_file = ""

def check_tensorflow():
  try:
    import tensorflow
    return True
  except ImportError:
    return False

def get_valid_memory_files():
  """Helper function jo saari bhari hui (>= 50 bytes) JSON files return karta hai"""
  valid = []
  for f in glob.glob("ai_memory_*.json"):
    if os.path.exists(f) and os.path.getsize(f) >= 50:
      valid.append(f)
  valid.sort(key=lambda x: os.path.getsize(x), reverse=True)
  return valid

def load_ai_engine(model_type="v3.6", force_new=False, target_memory=None):
  global active_ai, current_model_name, startup_notice, selected_model_val, selected_memory_file

  tf_available = check_tensorflow()
  requested_v4 = (model_type == "v4.0")

  if requested_v4 and not tf_available:
    model_type = "v3.6"
    selected_model_val = "v3.6"
    # Clear warning message jab user v4.0 choose karne ki koshish kare
    startup_notice = "⚠️ Cannot switch to v4.0 (Neural): TensorFlow library is not installed in environment! Auto-fallback to v3.6 Legacy."
  else:
    selected_model_val = model_type
    startup_notice = ""

  try:
    existing_files = glob.glob("ai_memory_*.json")
    
    # 🌟 1st Step: Startup Scan (Purani khali files delete)
    for f in existing_files:
      if os.path.exists(f) and os.path.getsize(f) < 50:
        try:
          os.remove(f)
        except:
          pass

    valid_files = get_valid_memory_files()
    target_file = target_memory if target_memory else (valid_files[0] if valid_files and not force_new else None)
    extracted_name = "user"

    if target_file:
      filename_only = os.path.basename(target_file).replace(".json", "")
      parts = filename_only.split("_")
      if len(parts) >= 3 and parts[0] == "ai" and parts[1] == "memory":
        extracted_name = parts[2]

    selected_memory_file = target_file if target_file else ""

    if model_type == "v4.0" and tf_available:
      import main_engine as engine_module
      active_ai = engine_module.MainAIEngine(user_name=extracted_name)
      current_model_name = "v4.0 (TensorFlow Neural)"
      startup_notice = f"TensorFlow Engine loaded. File: {target_file if target_file else 'New'} ({extracted_name.capitalize()})"
    else:
      import v3_6_AI_engine as engine_module
      
      if target_file and not force_new:
        active_ai = engine_module.MainAIEngine(user_name=extracted_name)
        active_ai.memory_file = target_file
        active_ai.load_memory()
        current_model_name = "v3.6 (Legacy Lightweight)"
        if not (requested_v4 and not tf_available):
          startup_notice = f"Switched to v3.6. Memory Loaded: {target_file} ({extracted_name.capitalize()})"
      else:
        random_id = random.randint(1000, 9999)
        new_file_name = f"ai_memory_{extracted_name}_{random_id}.json"
        active_ai = engine_module.MainAIEngine(user_name=extracted_name)
        active_ai.memory_file = new_file_name
        active_ai.memory_db = []
        active_ai.save_memory()
        selected_memory_file = new_file_name
        current_model_name = "v3.6 (Legacy Lightweight)"
        if not (requested_v4 and not tf_available):
          startup_notice = f"Switched to v3.6. Nayi file bani: {new_file_name}"
        
  except Exception as e:
    active_ai = None
    current_model_name = "Error"
    startup_notice = f"Error loading engine: {str(e)}"


initial_model = "v4.0" if check_tensorflow() else "v3.6"
load_ai_engine(initial_model)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infinity AI Hub</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0e0e0e; color: #fff; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        
        header { 
            background: #191919; 
            padding: 12px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid #2d2d2d; 
            flex-wrap: wrap;
            gap: 12px;
        }

        .header-title h2 { margin: 0; font-size: 18px; color: #fff; }
        .status { font-size: 11px; color: #aaa; margin-top: 2px; }

        .control-panel { 
            display: flex; 
            align-items: center; 
            gap: 10px; 
            flex-wrap: wrap;
        }

        select { 
            background: #121212; 
            color: #ffc107; 
            border: 1px solid #444; 
            padding: 6px 10px; 
            border-radius: 6px; 
            outline: none; 
            font-size: 12px; 
            font-weight: 500;
            cursor: pointer;
        }
        select:focus { border-color: #ffc107; }

        .btn-action { 
            background-color: #212529; 
            color: #ffc107; 
            border: 1px solid #ffc107; 
            padding: 6px 12px; 
            border-radius: 6px; 
            cursor: pointer; 
            font-weight: 600; 
            font-size: 12px; 
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        .btn-action:hover { 
            background-color: #ffc107; 
            color: #121212; 
        }

        .chat-container { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 12px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 80%; line-height: 1.4; word-wrap: break-word; font-size: 14px; }
        .user-msg { background: #007bff; align-self: flex-end; color: #fff; }
        .ai-msg { background: #222; align-self: flex-start; border: 1px solid #333; color: #e0e0e0; }
        .notice-msg { background: #332600; border: 1px solid #ffc107; color: #ffc107; align-self: center; font-size: 13px; text-align: center; max-width: 90%; }
        
        .input-box { display: flex; padding: 15px; background: #191919; border-top: 1px solid #2d2d2d; gap: 10px; }
        input[type="text"] { flex: 1; padding: 12px 15px; border-radius: 6px; border: 1px solid #333; background: #121212; color: #fff; outline: none; font-size: 14px; }
        input[type="text"]:focus { border-color: #007bff; }
        
        button.send-btn { padding: 12px 24px; background: #28a745; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; font-size: 14px; transition: background 0.2s; }
        button.send-btn:hover { background: #218838; }

        @media (max-width: 600px) {
            header { flex-direction: column; align-items: flex-start; padding: 10px 15px; }
            .control-panel { width: 100%; justify-content: space-between; gap: 6px; }
            select, .btn-action { font-size: 11px; padding: 5px 8px; }
            .message { max-width: 90%; }
        }
    </style>
</head>
<body>
    <header>
        <div class="header-title">
            <h2>Infinity AI Hub 🚀</h2>
            <div class="status">Active: <span id="model-status">{{ model_name }}</span></div>
        </div>
        <div class="control-panel">
            <!-- Memory Select Dropdown -->
            <select id="memory-select" onchange="switchMemory()" title="Select Active JSON Memory">
                {% for mf in memory_files %}
                    <option value="{{ mf }}" {% if mf == current_memory %}selected{% endif %}>💾 {{ mf }}</option>
                {% endfor %}
            </select>

            <!-- Model Switch Dropdown -->
            <select id="model-select" onchange="switchModel()" title="Switch AI Engine">
                <option value="v4.0" {% if selected_val == 'v4.0' %}selected{% endif %}>v4.0 (Neural)</option>
                <option value="v3.6" {% if selected_val == 'v3.6' %}selected{% endif %}>v3.6 (Legacy)</option>
            </select>

            <button class="btn-action" onclick="createNewJsonFile()" title="Create New Memory File">➕ New JSON</button>
        </div>
    </header>

    <div class="chat-container" id="chat-box">
        {% if notice %}
        <div class="message notice-msg">{{ notice }}</div>
        {% endif %}
        <div class="message ai-msg">Hey bro Kaisa hai sab theek kya karna hai aaj 😎</div>
    </div>

    <div class="input-box">
        <input type="text" id="user-input" placeholder="Type your message here..." autofocus>
        <button class="send-btn" onclick="sendMessage()">Send</button>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');

        userInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendMessage();
        });

        function appendMessage(text, sender, isNotice = false) {
            const div = document.createElement('div');
            div.className = isNotice ? 'message notice-msg' : `message ${sender === 'user' ? 'user-msg' : 'ai-msg'}`;
            div.innerText = text;
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        async function sendMessage() {
            const text = userInput.value.trim();
            if (!text) return;

            appendMessage(text, 'user');
            userInput.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await response.json();
                appendMessage(data.reply, 'ai');
            } catch (err) {
                appendMessage("Error communicating with AI engine!", 'ai', true);
            }
        }

        async function switchModel() {
            const selectedModel = document.getElementById('model-select').value;
            const selectedMemory = document.getElementById('memory-select').value;
            
            const response = await fetch('/switch_model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: selectedModel, memory: selectedMemory })
            });
            const data = await response.json();
            
            document.getElementById('model-select').value = data.selected_val;
            document.getElementById('model-status').innerText = data.model_name;
            if (data.notice) {
                appendMessage(data.notice, 'ai', true);
            }
        }

        async function switchMemory() {
            const selectedMemory = document.getElementById('memory-select').value;
            const selectedModel = document.getElementById('model-select').value;

            const response = await fetch('/switch_memory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ memory_file: selectedMemory, model: selectedModel })
            });
            const data = await response.json();
            if (data.notice) {
                appendMessage(data.notice, 'ai', true);
            }
        }

        async function createNewJsonFile() {
            const userName = prompt("Enter your name for new Memory file:", "user");
            if (!userName) return;

            const response = await fetch('/create_new_json', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: userName })
            });
            const data = await response.json();
            if (data.notice) {
                appendMessage(data.notice, 'ai', true);
            }
            
            if (data.model_name) {
                document.getElementById('model-status').innerText = data.model_name;
            }

            // Dropdown dynamically update karo
            if (data.memory_files) {
                const memSelect = document.getElementById('memory-select');
                memSelect.innerHTML = '';
                data.memory_files.forEach(file => {
                    const opt = document.createElement('option');
                    opt.value = file;
                    opt.innerText = '💾 ' + file;
                    if (file === data.current_memory) opt.selected = true;
                    memSelect.appendChild(opt);
                });
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
  valid_mems = get_valid_memory_files()
  return render_template_string(
      HTML_TEMPLATE,
      model_name=current_model_name,
      notice=startup_notice,
      selected_val=selected_model_val,
      memory_files=valid_mems,
      current_memory=selected_memory_file
  )

@app.route("/switch_model", methods=["POST"])
def switch_model():
  data = request.json
  model_type = data.get("model", "v3.6")
  target_mem = data.get("memory", None)
  load_ai_engine(model_type, target_memory=target_mem)
  return jsonify({
      "status": "success",
      "model_name": current_model_name,
      "notice": startup_notice,
      "selected_val": selected_model_val,
      "current_memory": selected_memory_file
  })

@app.route("/switch_memory", methods=["POST"])
def switch_memory():
  data = request.json
  target_mem = data.get("memory_file", "")
  model_type = data.get("model", "v3.6")
  
  if target_mem and os.path.exists(target_mem):
    load_ai_engine(model_type, target_memory=target_mem)
    return jsonify({
        "status": "success",
        "notice": f"Switched active memory to: {target_mem}",
        "current_memory": selected_memory_file
    })
  return jsonify({"status": "error", "notice": "File not found!"})

@app.route("/create_new_json", methods=["POST"])
def create_new_json():
  global active_ai, startup_notice, current_model_name, selected_model_val, selected_memory_file
  try:
    import v3_6_AI_engine as engine_module

    data = request.json or {}
    custom_name = data.get("user_name", "user").strip().lower()
    if not custom_name:
        custom_name = "user"

    # Step 1: Nayi temporary JSON file banao
    random_id = random.randint(1000, 9999)
    new_file_name = f"ai_memory_{custom_name}_{random_id}.json"

    active_ai = engine_module.MainAIEngine(user_name=custom_name)
    active_ai.memory_file = new_file_name
    active_ai.memory_db = []
    active_ai.save_memory()

    # 🌟 Step 2: INSTANT LIVE SCAN (Double Scan logic intact!)
    all_files = glob.glob("ai_memory_*.json")
    for f in all_files:
      if os.path.exists(f) and os.path.getsize(f) < 50:
        try:
          os.remove(f)  # Usi time live delete
        except:
          pass

    # 🌟 Step 3: Fast Swap - Top trained file load karo
    valid_files = get_valid_memory_files()

    if valid_files:
      best_file = valid_files[0]
      filename_only = os.path.basename(best_file).replace(".json", "")
      parts = filename_only.split("_")
      extracted_name = parts[2] if (len(parts) >= 3 and parts[0] == "ai" and parts[1] == "memory") else custom_name

      active_ai = engine_module.MainAIEngine(user_name=extracted_name)
      active_ai.memory_file = best_file
      active_ai.load_memory()
      selected_memory_file = best_file
      startup_notice = f"Khali file instant delete kar di gayi. Bhari hui file load ho gayi: {best_file}"
    else:
      selected_memory_file = new_file_name
      startup_notice = f"Nayi file load ho gayi: {new_file_name}"

    return jsonify({
        "status": "success", 
        "notice": startup_notice, 
        "model_name": current_model_name,
        "memory_files": get_valid_memory_files(),
        "current_memory": selected_memory_file
    })
  except Exception as e:
    return jsonify(
        {"status": "error", "notice": f"Error creating JSON: {str(e)}"}
    )

@app.route("/chat", methods=["POST"])
def chat():
  global active_ai
  data = request.json
  user_msg = data.get("message", "")

  if active_ai:
    try:
      reply = active_ai.respond(user_msg)
    except Exception as e:
      # Safe Fallback to v3.6 if v4.0 crashes mid-chat
      try:
        import v3_6_AI_engine as engine_module
        active_ai = engine_module.MainAIEngine()
        if selected_memory_file and os.path.exists(selected_memory_file):
          active_ai.memory_file = selected_memory_file
          active_ai.load_memory()
        reply = active_ai.respond(user_msg)
      except:
        reply = "Error: Active model issue. Switched safely to legacy mode."
  else:
    reply = "Error: No AI Engine is currently active!"

  return jsonify({"reply": reply})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
