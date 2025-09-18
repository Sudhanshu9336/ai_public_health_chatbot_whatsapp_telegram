import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Try to import Gemini SDK
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    logger.warning("Google Generative AI not available. Install with: pip install google-generativeai")

from .config import GEMINI_API_KEY

# Configure Gemini if available
if HAS_GENAI and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        logger.info("✅ Google Gemini AI configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        HAS_GENAI = False

# Enhanced FAQ database with multilingual support
FAQS = {
    # Dengue
    "dengue symptoms": {
        "en": "🦟 **Dengue Symptoms:** High fever (40°C/104°F), severe headache, pain behind eyes, muscle/joint pain, nausea, vomiting, skin rash. **Seek immediate medical care** for severe symptoms like persistent vomiting, severe abdominal pain, or difficulty breathing.",
        "hi": "🦟 **डेंगू के लक्षण:** तेज़ बुखार (40°C/104°F), गंभीर सिरदर्द, आंखों के पीछे दर्द, मांसपेशियों/जोड़ों में दर्द, मतली, उल्टी, त्वचा पर चकत्ते। **तुरंत डॉक्टर से मिलें** यदि लगातार उल्टी, पेट में तेज़ दर्द, या सांस लेने में कठिनाई हो।",
        "or": "🦟 **ଡେଙ୍ଗୁର ଲକ୍ଷଣ:** ଉଚ୍ଚ ଜ୍ୱର (40°C/104°F), ଗୁରୁତର ମୁଣ୍ଡବିଥା, ଆଖି ପଛରେ ଯନ୍ତ୍ରଣା, ମାଂସପେଶୀ/ଗଣ୍ଠି ଯନ୍ତ୍ରଣା, ବାନ୍ତି, ଚର୍ମରେ ଦାଗ। **ତୁରନ୍ତ ଡାକ୍ତରଙ୍କ ପାଖକୁ ଯାଆନ୍ତୁ** ଯଦି ଲଗାତାର ବାନ୍ତି, ପେଟରେ ତୀବ୍ର ଯନ୍ତ୍ରଣା, କିମ୍ବା ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ ହୁଏ।"
    },
    
    # Malaria
    "malaria symptoms": {
        "en": "🦟 **Malaria Symptoms:** Fever with chills, sweats, headache, nausea, vomiting, body aches, fatigue. Symptoms appear 10-15 days after mosquito bite. **Get tested immediately** if you suspect malaria - early treatment saves lives.",
        "hi": "🦟 **मलेरिया के लक्षण:** ठंड के साथ बुखार, पसीना, सिरदर्द, मतली, उल्टी, शरीर में दर्द, थकान। मच्छर के काटने के 10-15 दिन बाद लक्षण दिखते हैं। **तुरंत जांच कराएं** यदि मलेरिया का संदेह हो - जल्दी इलाज जान बचाता है।",
        "or": "🦟 **ମ୍ୟାଲେରିଆର ଲକ୍ଷଣ:** ଥଣ୍ଡା ସହିତ ଜ୍ୱର, ଘାମ, ମୁଣ୍ଡବିଥା, ବାନ୍ତି, ଶରୀରରେ ଯନ୍ତ୍ରଣା, କ୍ଲାନ୍ତି। ମଶା କାମୁଡ଼ିବାର 10-15 ଦିନ ପରେ ଲକ୍ଷଣ ଦେଖାଯାଏ। **ତୁରନ୍ତ ପରୀକ୍ଷା କରାନ୍ତୁ** ଯଦି ମ୍ୟାଲେରିଆ ସନ୍ଦେହ ହୁଏ - ଶୀଘ୍ର ଚିକିତ୍ସା ଜୀବନ ବଞ୍ଚାଏ।"
    },
    
    # Prevention
    "prevention tips": {
        "en": "🛡️ **Prevention Tips:** 1) Remove stagnant water 2) Use mosquito nets while sleeping 3) Wear long sleeves/pants 4) Use repellents 5) Keep surroundings clean 6) Get vaccinated as per schedule 7) Wash hands frequently with soap.",
        "hi": "🛡️ **बचाव के उपाय:** 1) रुका हुआ पानी हटाएं 2) सोते समय मच्छरदानी का उपयोग करें 3) लंबी आस्तीन/पैंट पहनें 4) रिपेलेंट का उपयोग करें 5) आसपास सफाई रखें 6) समय पर टीकाकरण कराएं 7) साबुन से बार-बार हाथ धोएं।",
        "or": "🛡️ **ପ୍ରତିରୋଧ ଉପାୟ:** 1) ଜମା ପାଣି ହଟାନ୍ତୁ 2) ଶୋଇବା ସମୟରେ ମଶାରୀ ବ୍ୟବହାର କରନ୍ତୁ 3) ଲମ୍ବା ହାତ/ପ୍ୟାଣ୍ଟ ପିନ୍ଧନ୍ତୁ 4) ରିପେଲେଣ୍ଟ ବ୍ୟବହାର କରନ୍ତୁ 5) ଆଖପାଖ ସଫା ରଖନ୍ତୁ 6) ସମୟରେ ଟୀକା ନିଅନ୍ତୁ 7) ସାବୁନରେ ବାରମ୍ବାର ହାତ ଧୋଇବେ।"
    },
    
    # Vaccination
    "vaccine schedule": {
        "en": "💉 **Vaccination Schedule:** Varies by age group. Infants: BCG, DTP, Polio, Hepatitis B. Children: Measles, MMR. Adults: Tetanus boosters, Influenza (high-risk groups). **Consult your nearest health center** for personalized schedule.",
        "hi": "💉 **टीकाकरण समय-सारणी:** उम्र के अनुसार अलग। शिशु: BCG, DTP, पोलियो, हेपेटाइटिस B। बच्चे: खसरा, MMR। वयस्क: टिटनेस बूस्टर, इन्फ्लूएंजा (उच्च जोखिम समूह)। **व्यक्तिगत समय-सारणी के लिए निकटतम स्वास्थ्य केंद्र से संपर्क करें।**",
        "or": "💉 **ଟୀକାକରଣ ସମୟସୂଚୀ:** ବୟସ ଅନୁସାରେ ଭିନ୍ନ। ଶିଶୁ: BCG, DTP, ପୋଲିଓ, ହେପାଟାଇଟିସ B। ପିଲା: ମିଜିଲ୍ସ, MMR। ବୟସ୍କ: ଟିଟାନସ ବୁଷ୍ଟର, ଇନଫ୍ଲୁଏଞ୍ଜା (ଉଚ୍ଚ ବିପଦ ଗୋଷ୍ଠୀ)। **ବ୍ୟକ୍ତିଗତ ସମୟସୂଚୀ ପାଇଁ ନିକଟସ୍ଥ ସ୍ୱାସ୍ଥ୍ୟ କେନ୍ଦ୍ର ସହିତ ଯୋଗାଯୋଗ କରନ୍ତୁ।**"
    },
    
    # Emergency
    "emergency": {
        "en": "🚨 **Medical Emergency:** Call 108 (National Ambulance) or visit nearest hospital immediately. **Danger signs:** Difficulty breathing, chest pain, severe bleeding, unconsciousness, high fever with convulsions.",
        "hi": "🚨 **मेडिकल इमरजेंसी:** 108 (राष्ट्रीय एम्बुलेंस) पर कॉल करें या तुरंत निकटतम अस्पताल जाएं। **खतरे के संकेत:** सांस लेने में कठिनाई, सीने में दर्द, गंभीर रक्तस्राव, बेहोशी, दौरे के साथ तेज़ बुखार।",
        "or": "🚨 **ମେଡିକାଲ ଜରୁରୀକାଳୀନ:** 108 (ଜାତୀୟ ଆମ୍ବୁଲାନ୍ସ) କୁ କଲ କରନ୍ତୁ କିମ୍ବା ତୁରନ୍ତ ନିକଟସ୍ଥ ହସ୍ପିଟାଲକୁ ଯାଆନ୍ତୁ। **ବିପଦ ସଙ୍କେତ:** ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ, ଛାତିରେ ଯନ୍ତ୍ରଣା, ଗୁରୁତର ରକ୍ତସ୍ରାବ, ଅଚେତନତା, ଜ୍ୱର ସହିତ ଖିଞ୍ଚୁଣି।"
    }
}

def find_faq_answer(query: str, language: str = "en") -> Optional[str]:
    """
    Enhanced FAQ matching with multilingual support and fuzzy matching
    """
    if not query:
        return None
    
    query_lower = query.lower().strip()
    
    # Keywords for different topics
    keywords_map = {
        "dengue symptoms": ["dengue", "डेंगू", "ଡେଙ୍ଗୁ", "lakshan", "लक्षण", "ଲକ୍ଷଣ", "symptoms"],
        "malaria symptoms": ["malaria", "मलेरिया", "ମ୍ୟାଲେରିଆ", "lakshan", "लक्षण", "ଲକ୍ଷଣ", "symptoms"],
        "prevention tips": ["prevention", "bachav", "बचाव", "ପ୍ରତିରୋଧ", "tips", "उपाय", "ଉପାୟ", "protect"],
        "vaccine schedule": ["vaccine", "vaccination", "टीका", "ଟୀକା", "schedule", "समय", "ସମୟ", "immunization"],
        "emergency": ["emergency", "ambulance", "108", "hospital", "इमरजेंसी", "ଜରୁରୀକାଳୀନ", "urgent"]
    }
    
    # Find matching FAQ
    for faq_key, keywords in keywords_map.items():
        if any(keyword in query_lower for keyword in keywords):
            faq_data = FAQS.get(faq_key, {})
            if isinstance(faq_data, dict):
                return faq_data.get(language, faq_data.get("en", ""))
            return faq_data
    
    return None

async def ask_gemini(prompt: str, language: str = "en") -> Optional[str]:
    """
    Enhanced Gemini AI integration with health-focused prompting
    """
    if not HAS_GENAI or not GEMINI_API_KEY:
        logger.warning("Gemini AI not available")
        return None
    
    try:
        # Create health-focused prompt
        health_prompt = f"""
You are a helpful health information assistant for a public health chatbot in India. 
Please provide accurate, safe health information in response to: "{prompt}"

Guidelines:
1. Always include a disclaimer that this is for information only
2. Recommend consulting healthcare professionals for medical advice
3. Focus on prevention and general health awareness
4. Be culturally sensitive to Indian context
5. Keep responses concise but informative
6. If asked about serious symptoms, emphasize seeking immediate medical care

Language preference: {language}
"""
        
        # Use the generative model
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(health_prompt)
        
        if response and response.text:
            return response.text.strip()
        else:
            logger.warning("Empty response from Gemini")
            return None
            
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None

def get_health_disclaimer(language: str = "en") -> str:
    """Get appropriate health disclaimer based on language"""
    disclaimers = {
        "en": "⚠️ This information is for educational purposes only. Please consult a qualified healthcare professional for medical advice, diagnosis, or treatment.",
        "hi": "⚠️ यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। चिकित्सा सलाह, निदान या उपचार के लिए कृपया एक योग्य स्वास्थ्य पेशेवर से सलाह लें।",
        "or": "⚠️ ଏହି ସୂଚନା କେବଳ ଶିକ୍ଷାଗତ ଉଦ୍ଦେଶ୍ୟ ପାଇଁ। ଚିକିତ୍ସା ପରାମର୍ଶ, ନିଦାନ କିମ୍ବା ଚିକିତ୍ସା ପାଇଁ ଦୟାକରି ଜଣେ ଯୋଗ୍ୟ ସ୍ୱାସ୍ଥ୍ୟ ପେଶାଦାରଙ୍କ ସହିତ ପରାମର୍ଶ କରନ୍ତୁ।"
    }
    return disclaimers.get(language, disclaimers["en"])

def detect_language(text: str) -> str:
    """Simple language detection based on script and keywords"""
    if not text:
        return "en"
    
    # Check for Devanagari script (Hindi)
    if any('\u0900' <= char <= '\u097F' for char in text):
        return "hi"
    
    # Check for Odia script
    if any('\u0B00' <= char <= '\u0B7F' for char in text):
        return "or"
    
    # Check for common Hindi/Odia keywords in Latin script
    hindi_keywords = ["kya", "hai", "ke", "ka", "ki", "mein", "aur", "se", "ko"]
    odia_keywords = ["kana", "kaha", "kemiti", "kouthi", "kahaku"]
    
    text_lower = text.lower()
    
    if any(keyword in text_lower for keyword in hindi_keywords):
        return "hi"
    elif any(keyword in text_lower for keyword in odia_keywords):
        return "or"
    
    return "en"  # Default to English