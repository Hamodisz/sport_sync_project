# logic/user_logger.py

import json
import os
from datetime import datetime

LOG_PATH = "data/insights_log.json"

def log_user_insight(user_id, content, event_type="user_insight"):
    os.makedirs("data", exist_ok=True)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "content": content
    }

    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", encoding="utf-8") as f:
            json.dump([entry], f, ensure_ascii=False, indent=2)
    else:
        with open(LOG_PATH, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=2)
