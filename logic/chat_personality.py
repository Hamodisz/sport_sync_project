import json
import os

MEMORY_PATH = "data/chat_memory.json"

# تحميل أو إنشاء الذاكرة
def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory):
    os.makedirs("data", exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# استرجاع شخصية الذكاء لمستخدم
def get_chat_personality(user_id):
    memory = load_memory()
    return memory.get(user_id, {
        "name": "Sports Sync",
        "tone": "تحفيزي وودود",
        "style": "تحليل عميق وعاطفة ذكية",
        "philosophy": "كل شخص يملك رياضة مخلوقة له – وأنا هنا لأجدها معه."
    })

# تحديث الشخصية ببيانات جديدة (لغة، سمات...إلخ)
def update_chat_personality(user_id, lang, traits_summary):
    memory = load_memory()
    base = memory.get(user_id, get_chat_personality(user_id))
    base["lang"] = lang
    base["last_traits"] = traits_summary
    memory[user_id] = base
    save_memory(memory)
