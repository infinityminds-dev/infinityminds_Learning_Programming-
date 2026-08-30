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
    requested_v4 = model_type == "v4.0"

    if requested_v4 and not tf_available:
        model_type = "v3.6"
        selected_model_val = "v3.6"
        startup_notice = "⚠️ Cannot switch to v4.0 (Neural): TensorFlow library is not installed in environment! Auto-fallback to v3.6 Legacy."
    else:
        selected_model_val = model_type
        startup_notice = ""

    try:
        existing_files = glob.glob("ai_memory_*.json")

        for f in existing_files:
            if os.path.exists(f) and os.path.getsize(f) < 50:
                try:
                    os.remove(f)
                except Exception:
                    pass

        valid_files = get_valid_memory_files()
        target_file = (
            target_memory
            if target_memory
            else (valid_files[0] if valid_files and not force_new else None)
        )
        extracted_name = "user"

        if target_file:
            filename_only = os.path.basename(target_file).replace(".json", "")
            parts = filename_only.split("_")
            if (
                len(parts) >= 3
                and parts[0] == "ai"
                and parts[1] == "memory"
            ):
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
                    startup_notice = (
                        f"Switched to v3.6. Nayi file bani: {new_file_name}"
                    )

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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Infinity AI Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            height: 100%;
            width: 100%;
            background: #09090b;
            color: #ececec;
            font-family: 'Inter', -apple-system, sans-serif;
            overflow: hidden;
        }

        .app-wrapper {
            display: flex;
            flex-direction: column;
            height: 100dvh;
            width: 100%;
            position: relative;
        }

        /* Top Bar */
        header { 
            background: #09090b; 
            padding: 14px 18px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            flex-shrink: 0;
            z-index: 10;
            border-bottom: 1px solid #18181b;
        }

        .icon-btn {
            background: #18181b;
            border: 1px solid #27272a;
            color: #e4e4e7;
            width: 38px;
            height: 38px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.2s;
        }
        .icon-btn:hover { background: #27272a; }

        .brand-title {
            font-size: 15px;
            font-weight: 600;
            color: #f4f4f5;
            letter-spacing: -0.3px;
        }

        /* Side Navigation Drawer (Sidebar) */
        .sidebar-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            backdrop-filter: blur(4px);
            z-index: 99;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .sidebar-overlay.active { opacity: 1; pointer-events: auto; }

        .sidebar {
            position: fixed;
            top: 0; left: -300px;
            width: 290px;
            height: 100%;
            background: #0e0e11;
            border-right: 1px solid #1f1f23;
            z-index: 100;
            display: flex;
            flex-direction: column;
            padding: 20px 16px;
            gap: 16px;
            transition: left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .sidebar.active { left: 0; }

        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 6px;
        }
        .sidebar-title { font-size: 16px; font-weight: 700; color: #fff; }

        .btn-new-chat {
            background: #18181b;
            color: #fff;
            border: 1px solid #27272a;
            padding: 12px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        .btn-new-chat:hover { background: #27272a; border-color: #3f3f46; }

        .sidebar-section-title {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #71717a;
            font-weight: 600;
            margin-top: 8px;
        }

        /* Custom Memory List in Sidebar */
        .memory-list-container {
            display: flex;
            flex-direction: column;
            gap: 6px;
            overflow-y: auto;
            flex: 1;
        }

        .memory-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: #141417;
            border: 1px solid #1f1f24;
            border-radius: 10px;
            cursor: pointer;
            font-size: 13px;
            color: #a1a1aa;
            transition: all 0.2s;
        }
        .memory-item:hover { background: #1c1c21; color: #fff; }
        .memory-item.active {
            background: #1e1b4b;
            border-color: #4f46e5;
            color: #c7d2fe;
            font-weight: 600;
        }

        /* Chat Area */
        .chat-container { 
            flex: 1; 
            overflow-y: auto; 
            -webkit-overflow-scrolling: touch;
            padding: 16px; 
            display: flex; 
            flex-direction: column; 
            gap: 12px; 
            max-width: 800px;
            width: 100%;
            margin: 0 auto;
        }

        .message { 
            padding: 12px 16px; 
            border-radius: 14px; 
            max-width: 85%; 
            line-height: 1.5; 
            word-break: break-word; 
            font-size: 14px; 
        }
        .user-msg { 
            background: #4f46e5; 
            align-self: flex-end; 
            color: #ffffff; 
            border-bottom-right-radius: 4px;
        }
        .ai-msg { 
            background: #141417; 
            align-self: flex-start; 
            border: 1px solid #232328; 
            color: #d1d5db; 
            border-bottom-left-radius: 4px;
        }
        .notice-msg { 
            background: rgba(234, 179, 8, 0.08); 
            border: 1px solid rgba(234, 179, 8, 0.25); 
            color: #fde047; 
            align-self: center; 
            font-size: 12px; 
            text-align: center; 
            width: 100%; 
            border-radius: 10px;
        }

        /* Input Area */
        .input-wrapper {
            padding: 12px 16px 20px 16px;
            background: #09090b;
            flex-shrink: 0;
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
        }

        .input-box { 
            display: flex; 
            flex-direction: column;
            padding: 10px 14px; 
            background: #131316; 
            border: 1px solid #232328; 
            border-radius: 18px;
            gap: 10px; 
            transition: border-color 0.2s;
        }
        .input-box:focus-within { border-color: #3f3f46; }

        input[type="text"] { 
            width: 100%;
            padding: 4px; 
            border: none;
            background: transparent; 
            color: #fff; 
            outline: none; 
            font-size: 14px; 
        }
        input[type="text"]::placeholder { color: #52525b; }

        .input-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Model Badge Button (Replacing Select Dropdown) */
        .model-badge-btn {
            background: #1c1c21;
            color: #e4e4e7;
            border: 1px solid #2c2c34;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .model-badge-btn:hover { background: #27272a; border-color: #3f3f46; }

        button.send-btn { 
            width: 32px;
            height: 32px;
            background: #4f46e5; 
            color: white; 
            border: none; 
            border-radius: 50%; 
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: background 0.2s; 
        }
        button.send-btn:hover { background: #4338ca; }

        /* Custom Dark Modal Popup (For Models & New File) */
        .modal-overlay {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0,0,0,0.75);
            backdrop-filter: blur(5px);
            z-index: 200;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal-overlay.active { display: flex; }

        .modal-card {
            background: #121216;
            border: 1px solid #27272d;
            border-radius: 20px;
            width: 100%;
            max-width: 380px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            animation: modalIn 0.2s ease-out;
        }

        @keyframes modalIn {
            from { transform: scale(0.95); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .modal-title { font-size: 16px; font-weight: 600; color: #fff; }

        .modal-body {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .model-card-option {
            background: #18181d;
            border: 1px solid #232328;
            border-radius: 12px;
            padding: 12px 14px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
        }
        .model-card-option:hover { background: #22222a; border-color: #3f3f46; }
        .model-card-option.selected {
            background: #1e1b4b;
            border-color: #6366f1;
        }

        .model-opt-info h4 { font-size: 14px; color: #f4f4f5; font-weight: 600; }
        .model-opt-info p { font-size: 11px; color: #a1a1aa; margin-top: 2px; }

        .modal-input {
            width: 100%;
            background: #18181d;
            border: 1px solid #27272a;
            padding: 12px 14px;
            border-radius: 10px;
            color: #fff;
            outline: none;
            font-size: 14px;
        }
        .modal-input:focus { border-color: #4f46e5; }

        .modal-btn-confirm {
            background: #4f46e5;
            color: #fff;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }
        .modal-btn-confirm:hover { background: #4338ca; }
    </style>
</head>
<body>
    <div class="sidebar-overlay" id="overlay" onclick="toggleSidebar()"></div>

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <span class="sidebar-title">Infinity AI Hub</span>
            <button class="icon-btn" onclick="toggleSidebar()">✕</button>
        </div>

        <button class="btn-new-chat" onclick="openNewFileModal()">
            <span>➕</span> New JSON Memory
        </button>

        <div class="sidebar-section-title">Saved Memories</div>
        <div class="memory-list-container" id="memory-list">
            {% for mf in memory_files %}
                <div class="memory-item {% if mf == current_memory %}active{% endif %}" onclick="selectMemory('{{ mf }}')">
                    <span>💾</span>
                    <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{{ mf }}</span>
                </div>
            {% endfor %}
        </div>
    </div>

    <div class="modal-overlay" id="modelModal" onclick="closeModal('modelModal', event)">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">Select AI Engine</div>
                <button class="icon-btn" onclick="closeModalDirect('modelModal')">✕</button>
            </div>
            <div class="modal-body">
                <div class="model-card-option {% if selected_val == 'v4.0' %}selected{% endif %}" onclick="selectModel('v4.0')">
                    <div class="model-opt-info">
                        <h4>v4.0 (Neural Engine)</h4>
                        <p>TensorFlow deep-learning classifier with embeddings</p>
                    </div>
                    <span>🧠</span>
                </div>
                <div class="model-card-option {% if selected_val == 'v3.6' %}selected{% endif %}" onclick="selectModel('v3.6')">
                    <div class="model-opt-info">
                        <h4>v3.6 (Smart Legacy)</h4>
                        <p>Fast keyword similarity engine (Zero-dependency)</p>
                    </div>
                    <span>⚡</span>
                </div>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="newFileModal" onclick="closeModal('newFileModal', event)">
        <div class="modal-card">
            <div class="modal-header">
                <div class="modal-title">Create New Memory</div>
                <button class="icon-btn" onclick="closeModalDirect('newFileModal')">✕</button>
            </div>
            <div class="modal-body">
                <input type="text" id="new-username-input" class="modal-input" placeholder="Enter owner name (e.g. alex)">
                <button class="modal-btn-confirm" onclick="submitNewJson()">Create File</button>
            </div>
        </div>
    </div>

    <div class="app-wrapper">
        <header>
            <button class="icon-btn" onclick="toggleSidebar()">☰</button>
            <div class="brand-title">Infinity AI Hub</div>
            <div style="width: 38px;"></div>
        </header>

        <div class="chat-container" id="chat-box">
            {% if notice %}
            <div class="message notice-msg">{{ notice }}</div>
            {% endif %}
            <div class="message ai-msg">Hey bro! Infinity AI Hub custom dark sheet interface ke saath ready hai. 😎</div>
        </div>

        <div class="input-wrapper">
            <div class="input-box">
                <input type="text" id="user-input" placeholder="Message Infinity AI..." autofocus>
                
                <div class="input-actions">
                    <div class="model-badge-btn" onclick="openModal('modelModal')">
                        <span id="model-badge-text">{% if selected_val == 'v4.0' %}🔴 v4.0 (Neural){% else %}⚡ v3.6 (Legacy){% endif %}</span>
                        <span style="font-size: 10px;">▼</span>
                    </div>

                    <button class="send-btn" onclick="sendMessage()">➔</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        let currentSelectedModel = "{{ selected_val }}";
        let currentSelectedMemory = "{{ current_memory }}";

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('overlay').classList.toggle('active');
        }

        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModalDirect(id) { document.getElementById(id).classList.remove('active'); }
        function closeModal(id, event) {
            if (event.target.id === id) closeModalDirect(id);
        }

        function openNewFileModal() {
            toggleSidebar();
            openModal('newFileModal');
            setTimeout(() => document.getElementById('new-username-input').focus(), 100);
        }

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

        async function selectModel(modelType) {
            closeModalDirect('modelModal');
            const response = await fetch('/switch_model', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: modelType, memory: currentSelectedMemory })
            });
            const data = await response.json();
            
            currentSelectedModel = data.selected_val;
            document.getElementById('model-badge-text').innerText = data.selected_val === 'v4.0' ? '🔴 v4.0 (Neural)' : '⚡ v3.6 (Legacy)';
            
            if (data.notice) appendMessage(data.notice, 'ai', true);
        }

        async function selectMemory(memoryFileName) {
            toggleSidebar();
            const response = await fetch('/switch_memory', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ memory_file: memoryFileName, model: currentSelectedModel })
            });
            const data = await response.json();
            currentSelectedMemory = data.current_memory;
            
            // Update active state in UI
            document.querySelectorAll('.memory-item').forEach(el => {
                if (el.innerText.includes(memoryFileName)) el.classList.add('active');
                else el.classList.remove('active');
            });

            if (data.notice) appendMessage(data.notice, 'ai', true);
        }

        async function submitNewJson() {
            const userName = document.getElementById('new-username-input').value.trim() || 'user';
            closeModalDirect('newFileModal');
            document.getElementById('new-username-input').value = '';

            const response = await fetch('/create_new_json', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: userName })
            });
            const data = await response.json();
            if (data.notice) appendMessage(data.notice, 'ai', true);

            if (data.memory_files) {
                currentSelectedMemory = data.current_memory;
                const container = document.getElementById('memory-list');
                container.innerHTML = '';
                data.memory_files.forEach(file => {
                    const div = document.createElement('div');
                    div.className = `memory-item ${file === data.current_memory ? 'active' : ''}`;
                    div.onclick = () => selectMemory(file);
                    div.innerHTML = `<span>💾</span><span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${file}</span>`;
                    container.appendChild(div);
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
        current_memory=selected_memory_file,
    )


@app.route("/switch_model", methods=["POST"])
def switch_model():
    try:
        data = request.json or {}
        model_type = data.get("model", "v3.6")
        target_mem = data.get("memory", None)
        load_ai_engine(model_type, target_memory=target_mem)
        return jsonify(
            {
                "status": "success",
                "model_name": current_model_name,
                "notice": startup_notice,
                "selected_val": selected_model_val,
                "current_memory": selected_memory_file,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "notice": str(e)})


@app.route("/switch_memory", methods=["POST"])
def switch_memory():
    try:
        data = request.json or {}
        target_mem = data.get("memory_file", "")
        model_type = data.get("model", "v3.6")

        if target_mem and os.path.exists(target_mem):
            load_ai_engine(model_type, target_memory=target_mem)
            return jsonify(
                {
                    "status": "success",
                    "notice": f"Switched active memory to: {target_mem}",
                    "current_memory": selected_memory_file,
                }
            )
        return jsonify({"status": "error", "notice": "File not found!"})
    except Exception as e:
        return jsonify({"status": "error", "notice": str(e)})


@app.route("/create_new_json", methods=["POST"])
def create_new_json():
    global active_ai, startup_notice, current_model_name, selected_model_val, selected_memory_file
    try:
        import v3_6_AI_engine as engine_module

        data = request.json or {}
        custom_name = data.get("user_name", "user").strip().lower()
        if not custom_name:
            custom_name = "user"

        random_id = random.randint(1000, 9999)
        new_file_name = f"ai_memory_{custom_name}_{random_id}.json"

        active_ai = engine_module.MainAIEngine(user_name=custom_name)
        active_ai.memory_file = new_file_name
        active_ai.memory_db = []
        active_ai.save_memory()

        all_files = glob.glob("ai_memory_*.json")
        for f in all_files:
            if os.path.exists(f) and os.path.getsize(f) < 50:
                try:
                    os.remove(f)
                except Exception:
                    pass

        valid_files = get_valid_memory_files()

        if valid_files:
            best_file = valid_files[0]
            filename_only = os.path.basename(best_file).replace(".json", "")
            parts = filename_only.split("_")
            extracted_name = (
                parts[2]
                if (
                    len(parts) >= 3
                    and parts[0] == "ai"
                    and parts[1] == "memory"
                )
                else custom_name
            )

            active_ai = engine_module.MainAIEngine(user_name=extracted_name)
            active_ai.memory_file = best_file
            active_ai.load_memory()
            selected_memory_file = best_file
            startup_notice = f"Khali file instant delete kar di gayi. Bhari hui file load ho gayi: {best_file}"
        else:
            selected_memory_file = new_file_name
            startup_notice = f"Nayi file load ho gayi: {new_file_name}"

        return jsonify(
            {
                "status": "success",
                "notice": startup_notice,
                "model_name": current_model_name,
                "memory_files": get_valid_memory_files(),
                "current_memory": selected_memory_file,
            }
        )
    except Exception as e:
        return jsonify(
            {"status": "error", "notice": f"Error creating JSON: {str(e)}"}
        )


@app.route("/chat", methods=["POST"])
def chat():
    global active_ai
    try:
        data = request.json or {}
        user_msg = data.get("message", "")

        if active_ai:
            try:
                reply = active_ai.respond(user_msg)
            except Exception as e:
                try:
                    import v3_6_AI_engine as engine_module

                    active_ai = engine_module.MainAIEngine()
                    if selected_memory_file and os.path.exists(
                        selected_memory_file
                    ):
                        active_ai.memory_file = selected_memory_file
                        active_ai.load_memory()
                    reply = active_ai.respond(user_msg)
                except Exception:
                    reply = "Error: Active model issue. Switched safely to legacy mode."
        else:
            reply = "Error: No AI Engine is currently active!"

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Server Glitch Handled Safely: {str(e)}"})


if __name__ == "__main__":
    # Fix: debug=False aur use_reloader=False rakha gaya hai taaki background crash na ho
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
