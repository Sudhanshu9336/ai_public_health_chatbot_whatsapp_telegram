from __future__ import annotations
import json
import os
import re
from typing import Any, Dict, List, Text

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

RASA_LANGS = {"en": "English", "hi": "Hindi", "or": "Odia"}


def _safe_text(s: str) -> str:
    return s.replace("<", "").replace(">", "")


def _lang_from_text(text: str) -> str:
    text_l = text.lower().strip()
    if "lang hi" in text_l or "hindi" in text_l or "हिंदी" in text_l:
        return "hi"
    if "lang or" in text_l or "odia" in text_l or "ଓଡ଼ିଆ" in text_l:
        return "or"
    return "en"


class ActionSetLanguage(Action):
    def name(self) -> Text:
        return "action_set_language"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        last = tracker.latest_message.get("text") or ""
        lang = _lang_from_text(last)
        dispatcher.utter_message(text=f"Language set to {RASA_LANGS.get(lang, 'English')}.")
        return [SlotSet("language", lang)]


class ActionLookupSymptoms(Action):
    def name(self) -> Text:
        return "action_lookup_symptoms"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        disease = next(
            (e.get("value") for e in tracker.latest_message.get("entities", []) if e.get("entity") == "disease"),
            None,
        )
        lang = tracker.get_slot("language") or "en"
        msg = {
            "en": f"Common symptoms of {disease or 'the disease'} may include fever, fatigue, headache, and condition-specific signs. For exact guidance, contact a doctor.",
            "hi": f"{disease or 'रोग'} के सामान्य लक्षण: बुखार, थकान, सिरदर्द और रोग-विशेष लक्षण हो सकते हैं। सटीक सलाह के लिए डॉक्टर से मिलें।",
            "or": f"{disease or 'ରୋଗ'}ର ସାଧାରଣ ଲକ୍ଷଣ: ଜ୍ୱର, କ୍ଲାନ୍ତି, ମୁଣ୍ଡବିଥା ଏବଂ ବିଶେଷ ଲକ୍ଷଣ। ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ।",
        }[lang]
        dispatcher.utter_message(text=_safe_text(msg))
        return []


class ActionPrevention(Action):
    def name(self) -> Text:
        return "action_prevention_tips"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        lang = tracker.get_slot("language") or "en"
        msg = {
            "en": "General prevention: wash hands often, use safe water, wear masks in crowds, use nets/repellents for mosquitoes, and keep vaccinations up to date.",
            "hi": "सामान्य बचाव: हाथ बार-बार धोएँ, साफ पानी पिएँ, भीड़ में मास्क पहनें, मच्छरों से बचाव करें, और टीकाकरण समय पर कराएँ।",
            "or": "ସାଧାରଣ ପ୍ରତିରୋଧ: ହାତ ଭଲଭାବେ ଧୋଇବେ, ସୁରକ୍ଷିତ ପାଣି ପିବେ, ଭିଡ଼ରେ ମାସ୍କ ପିନ୍ଧିବେ, ମାଛିମାଛାରୁ ସତର୍କ ରହିବେ, ଟୀକା ସମୟରେ ନେବେ।",
        }[lang]
        dispatcher.utter_message(text=_safe_text(msg))
        return []


class ActionVaccineSchedule(Action):
    def name(self) -> Text:
        return "action_vaccine_schedule"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        lang = tracker.get_slot("language") or "en"
        stage = "infant"
        text = tracker.latest_message.get("text", "").lower()

        if any(w in text for w in ["child", "kid", "बच्च", "ଶିଶୁ"]):
            stage = "child"
        elif any(w in text for w in ["adolescent", "teen", "किशोर", "କିଶୋର"]):
            stage = "adolescent"
        elif any(w in text for w in ["adult", "वयस्क", "ବୟସ୍କ"]):
            stage = "adult"

        path = os.getenv("VACCINE_SCHEDULE_PATH", "vaccines/vaccine_schedule.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data.get(stage, [])
            lines = [f"- {x['age']}: {x['vaccine']}" for x in items]
            body = "\n".join(lines) or "No data."
        except Exception:
            body = "Schedule not available."

        msg = {
            "en": f"Recommended {stage} vaccine schedule:\n{body}",
            "hi": f"अनुमोदित {stage} टीकाकरण समय-सारणी:\n{body}",
            "or": f"ସୁପାରିଶୀତ {stage} ଟୀକାକରଣ ସମୟସୂଚୀ:\n{body}",
        }[lang]
        dispatcher.utter_message(text=_safe_text(msg))
        return []


class ActionOutbreaks(Action):
    def name(self) -> Text:
        return "action_outbreaks"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        loc = next(
            (e.get("value") for e in tracker.latest_message.get("entities", []) if e.get("entity") == "location"),
            None,
        )
        feed = os.getenv("PUBLIC_HEALTH_ALERTS_FEED_FILE", "data/mock_outbreaks.json")
        try:
            with open(feed, "r", encoding="utf-8") as f:
                data = json.load(f)
            alerts = data.get("alerts", [])
            relevant = [a for a in alerts if not loc or a["region"].lower() == loc.lower()]
            if not relevant:
                dispatcher.utter_message(text="No active alerts found for your region at the moment.")
                return []
            resp = [f"{a['region']}: {a['disease']} ({a['severity']}). Advice: {a['advice']}" for a in relevant]
            dispatcher.utter_message(text="\n".join(resp))
        except Exception:
            dispatcher.utter_message(text="Could not fetch outbreak data right now.")
        return []


class ActionSubscribe(Action):
    def name(self) -> Text:
        return "action_subscribe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("phone")
        if not phone:
            m = re.search(r"\+?\d{10,15}", tracker.latest_message.get("text", ""))
            if m:
                phone = m.group(0)

        if not phone:
            dispatcher.utter_message(
                text="Please share your phone number with country code (e.g., +91XXXXXXXXXX)."
            )
            return []

        backend = os.getenv("BACKEND_HOST", "http://localhost:8000")
        try:
            requests.post(
                f"{backend}/subscribers",
                json={"phone": phone, "language": tracker.get_slot("language") or "en"},
                timeout=5,
            )
            dispatcher.utter_message(text=f"Subscribed {phone} for health alerts on SMS/WhatsApp.")
        except Exception:
            dispatcher.utter_message(text="Couldn't subscribe right now. Please try again later.")

        return [SlotSet("phone", phone)]


class ActionUnsubscribe(Action):
    def name(self) -> Text:
        return "action_unsubscribe"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("phone")
        backend = os.getenv("BACKEND_HOST", "http://localhost:8000")
        try:
            if phone:
                requests.delete(f"{backend}/subscribers/{phone}", timeout=5)
                dispatcher.utter_message(text=f"Unsubscribed {phone}.")
            else:
                dispatcher.utter_message(text="No phone on file. Send 'unsubscribe +<number>' to remove.")
        except Exception:
            dispatcher.utter_message(text="Couldn't unsubscribe right now.")
        return []


class ActionFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        lang = tracker.get_slot("language") or "en"
        msg = {
            "en": "I'm not fully sure. Could you rephrase, or ask about symptoms, prevention, vaccines, or outbreaks?",
            "hi": "मुझे पूरी तरह समझ नहीं आया। कृपया दोबारा लिखें या लक्षण, बचाव, टीकाकरण, या प्रकोप के बारे में पूछें।",
            "or": "ମୁଁ ପୁରା ବୁଝିପାରିଲିନି। ଦୟାକରି ପୁଣି ଲେଖନ୍ତୁ କିମ୍ବା ଲକ୍ଷଣ/ପ୍ରତିରୋଧ/ଟୀକା/ପ୍ରକୋପ ବିଷୟରେ ପଚାରନ୍ତୁ।",
        }[lang]
        dispatcher.utter_message(text=msg)
        return []
