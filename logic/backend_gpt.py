import json
from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141
from logic.user_analysis import save_user_analysis
from logic.prompt_engine import build_main_prompt
from logic.brand_signature import add_brand_signature
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def apply_all_analysis_layers(text):
    return {
        "traits_1_40": apply_layers_1_40(text),
        "traits_41_80": apply_layers_41_80(text),
        "traits_81_100": apply_layers_81_100(text),
        "traits_101_141": apply_layers_101_141(text),
    }

def format_answers_for_prompt(answers):
    parts = []
    for i in range(20):
        val = answers.get(f'q{i+1}', '')
        if isinstance(val, list):
            parts.append(f"Q{i+1}: {' / '.join(val)}")
        else:
            parts.append(f"Q{i+1}: {str(val)}")
    extra = answers.get("custom_input", "")
    if extra:
        parts.append(f"Extra: {extra}")
    return '\n'.join(parts)

def generate_sport_recommendation(answers, lang="العربية"):
    user_id = answers.get("user_id", "unknown")
    full_text = format_answers_for_prompt(answers)
    analysis = apply_all_analysis_layers(full_text)
    save_user_analysis(user_id, analysis)

    prompt = build_main_prompt(analysis, lang)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ خطأ أثناء الاتصال بـ OpenAI:", str(e))
        return ["عذرًا، حدث خطأ أثناء توليد التوصية. يرجى المحاولة لاحقًا."]

    recommendations = []
    for line in content.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            recommendations.append(line.strip())

    if len(recommendations) < 3:
        recommendations = [content]

    return [add_brand_signature(r) for r in recommendations]
