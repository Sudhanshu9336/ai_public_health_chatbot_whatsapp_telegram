import os
from typing import Optional

# Try to import Gemini SDK (google.generativeai). If not available, fall back to simple behaviour
try:
    import google.generativeai as genai
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

from .config import GEMINI_API_KEY

if HAS_GENAI and GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# simple FAQ mapping to ensure offline behaviour
FAQS = {
    "dengue symptoms": "Common dengue symptoms: high fever, severe headache, pain behind the eyes, muscle and joint pain, nausea, and rash. Seek medical care for severe symptoms.",
    "malaria symptoms": "Common malaria symptoms: fever, chills, sweats, headaches, nausea and vomiting. See a health center quickly if you suspect malaria.",
    "vaccine schedule": "Vaccination schedules differ by vaccine and age — check your local health authority for specific dates.",
    "prevention": "Prevention tips: keep surroundings clean, remove standing water, use mosquito nets, use repellents, vaccinate when applicable."
}

def find_faq_answer(query: str) -> Optional[str]:
    q = (query or "").lower()
    # naive keyword matching
    for key, answer in FAQS.items():
        if key in q or any(word in q for word in key.split()):
            return answer
    return None

async def ask_gemini(prompt: str) -> str:
    if not HAS_GENAI or not GEMINI_API_KEY:
        raise RuntimeError("Gemini client not available - set GEMINI_API_KEY and install google-generativeai")
    try:
        # Use simple text generation call - adapt if library API changes
        model = genai.get_model("gpt-4o-mini") if hasattr(genai, "get_model") else None
        # Many installs expose a generate_text style API — we handle both patterns:
        try:
            # Attempt new-style API
            resp = genai.generate_text(model="gemini-1.5" if hasattr(genai, "generate_text") else "gemini-1.5", input=prompt)
            return resp.text if hasattr(resp, "text") else (resp.get("output", "") if isinstance(resp, dict) else str(resp))
        except Exception:
            # Fallback to older generate_content or generate call
            if hasattr(genai, "generate"):
                out = genai.generate(model="gemini-1.5-flash", prompt=prompt)
                return getattr(out, "output", str(out))
            if hasattr(genai, "generate_content"):
                out = genai.generate_content(model="gemini-1.5-flash", contents=prompt)
                return getattr(out, "text", str(out))
        return "Sorry, no response from Gemini."
    except Exception as e:
        return f"Gemini error: {e}"
