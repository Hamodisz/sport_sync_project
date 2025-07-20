def append_brand_signature(text, lang="العربية"):
    if lang == "العربية":
        signature = "\n\n📎 توقيع: تمت التوصية عبر نظام Sport Sync، النسخة المحمية ©"
    else:
        signature = "\n\n📎 Signature: Recommended by Sport Sync, protected version ©"
    return text.strip() + signature
