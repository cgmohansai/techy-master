import google.generativeai as genai

# PASTE YOUR API KEY HERE
genai.configure(api_key="AIzaSyCk9NWeREdZSXunPXlXlOq6-NXlhEBUB38")

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")