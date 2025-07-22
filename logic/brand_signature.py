# logic/brand_signature.py

def add_brand_signature(prompt: str) -> str:
    signature = "\n\n— تم توليد هذه التوصية بواسطة Sports Sync 🤖"
    return prompt + signature
