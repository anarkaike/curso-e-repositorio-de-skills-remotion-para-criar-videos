
import google.generativeai as genai
try:
    print(f"Version: {genai.__version__}")
    if hasattr(genai, 'ImageGenerationModel'):
        print("✅ ImageGenerationModel exists")
    else:
        print("❌ ImageGenerationModel missing")
except Exception as e:
    print(e)
