from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from gtts import gTTS
import subprocess

app = Flask(__name__)
app.secret_key = "change-this-secret"  # important for sessions

# --------- Load Office Data ---------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "offices.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    OFFICES = json.load(f)

# --------- Supported Languages ---------
LANGUAGES = {
    "en": {"label": "English", "gtts_lang": "en"},
    "hi": {"label": "Hindi (हिन्दी)", "gtts_lang": "hi"},
    "kn": {"label": "Kannada (ಕನ್ನಡ)", "gtts_lang": "kn"},
    "te": {"label": "Telugu (తెలుగు)", "gtts_lang": "te"},
    "ta": {"label": "Tamil (தமிழ்)", "gtts_lang": "ta"}
}

# --------- UI Text for Each Language ---------
UI_TEXT = {
    "en": {
        "title": "College Robot Guide",
        "welcome": "Welcome! How can I help you?",
        "search_placeholder": "Enter name / department / room number",
        "search_button": "Search",
        "type_to_begin": "Type a name, department, or room number to begin.",
        "results_for": "Showing results for:",
        "no_results": "No matching office found. Please check spelling or contact Help Desk.",
        "speak_button": "Speak Directions",
        "quick_admissions": "Admissions",
        "quick_accounts": "Accounts",
        "quick_principal": "Principal",
        "quick_exam_cell": "Exam Cell",
        "quick_cse": "CSE Dept",
        "quick_ece": "ECE Dept"
    },
    "hi": {
        "title": "कॉलेज रोबोट गाइड",
        "welcome": "स्वागत है! मैं आपकी कैसे मदद कर सकता हूँ?",
        "search_placeholder": "नाम / विभाग / कक्ष संख्या दर्ज करें",
        "search_button": "खोजें",
        "type_to_begin": "शुरू करने के लिए नाम, विभाग या कक्ष संख्या टाइप करें।",
        "results_for": "इसके लिए परिणाम:",
        "no_results": "कोई मेल खाता कार्यालय नहीं मिला। कृपया वर्तनी जाँचें या हेल्प डेस्क से संपर्क करें।",
        "speak_button": "दिशा सुनाएँ",
        "quick_admissions": "प्रवेश",
        "quick_accounts": "लेखा विभाग",
        "quick_principal": "प्राचार्य",
        "quick_exam_cell": "परीक्षा कक्ष",
        "quick_cse": "CSE विभाग",
        "quick_ece": "ECE विभाग"
    },
    "kn": {
        "title": "ಕಾಲೇಜು ರೋಬೋಟ್ ಮಾರ್ಗದರ್ಶಿ",
        "welcome": "ಸ್ವಾಗತ! ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಲಿ?",
        "search_placeholder": "ಹೆಸರು / ವಿಭಾಗ / ಕೋಣೆ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ",
        "search_button": "ಹುಡುಕಿ",
        "type_to_begin": "ಆರಂಭ ಮಾಡಲು ಹೆಸರು, ವಿಭಾಗ ಅಥವಾ ಕೋಣೆ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ.",
        "results_for": "ಇದಕ್ಕಾಗಿ ಫಲಿತಾಂಶಗಳು:",
        "no_results": "ಹೊಂದುವ ಕಚೇರಿ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪೆಲಿಂಗ್ ಪರಿಶೀಲಿಸಿ ಅಥವಾ ಸಹಾಯ ಕೇಂದ್ರವನ್ನು ಸಂಪರ್ಕಿಸಿ.",
        "speak_button": "ದಿಕ್ಕುಗಳನ್ನು ಓದಿ",
        "quick_admissions": "ಪ್ರವೇಶ",
        "quick_accounts": "ಲೆಕ್ಕಪತ್ರ",
        "quick_principal": "ಮುಖ್ಯಶಿಕ್ಷಕರು",
        "quick_exam_cell": "ಪರೀಕ್ಷಾ ಕಚೇರಿ",
        "quick_cse": "CSE ವಿಭಾಗ",
        "quick_ece": "ECE ವಿಭಾಗ"
    },
    "te": {
        "title": "కాలేజ్ రోబోట్ గైడ్",
        "welcome": "స్వాగతం! నేను మీకు ఎలా సహాయం చేయగలను?",
        "search_placeholder": "పేరు / విభాగం / గది నంబర్ నమోదు చేయండి",
        "search_button": "శోధించండి",
        "type_to_begin": "ప్రారంభించడానికి పేరు, విభాగం లేదా గది నంబర్ ఇవ్వండి.",
        "results_for": "దీనికి ఫలితాలు:",
        "no_results": "సరిపోలే కార్యాలయం కనబడలేదు. దయచేసి స్పెల్లింగ్ తనిఖీ చేయండి.",
        "speak_button": "దిశలను వినిపించు",
        "quick_admissions": "అడ్మిషన్స్",
        "quick_accounts": "అకౌంట్స్",
        "quick_principal": "ప్రిన్సిపాల్",
        "quick_exam_cell": "ఎగ్జామ్ సెల్",
        "quick_cse": "CSE విభాగం",
        "quick_ece": "ECE విభాగం"
    },
    "ta": {
        "title": "கல்லூரி ரோபோட் வழிகாட்டி",
        "welcome": "வரவேற்கிறோம்! நான் எப்படி உதவலாம்?",
        "search_placeholder": "பெயர் / துறை / அறை எண் உள்ளிடுங்கள்",
        "search_button": "தேடுக",
        "type_to_begin": "தொடங்க பெயர், துறை அல்லது அறை எண்ணை உள்ளிடுங்கள்.",
        "results_for": "இதற்கான முடிவுகள்:",
        "no_results": "பொருந்தும் அலுவலகம் எதுவும் கிடைக்கவில்லை.",
        "speak_button": "வழியை ஒலியாகக் கேட்க",
        "quick_admissions": "சேர்க்கை",
        "quick_accounts": "கணக்குப் பிரிவு",
        "quick_principal": "முதல்வர்",
        "quick_exam_cell": "தேர்வு அலுவலகம்",
        "quick_cse": "CSE துறை",
        "quick_ece": "ECE துறை"
    }
}

# --------- Helper Functions ---------

def get_lang():
    lang = session.get("lang", "en")
    if lang not in LANGUAGES:
        lang = "en"
    return lang


def search_offices(query):
    if not query:
        return []
    query = query.lower()
    results = []
    for office in OFFICES:
        text = (
            office.get("name", "") + " " +
            office.get("role", "") + " " +
            office.get("department", "") + " " +
            office.get("room", "")
        ).lower()
        if query in text:
            results.append(office)
    return results


def speak_text(text, lang_code):
    """Uses Google TTS to play audio."""
    lang_info = LANGUAGES.get(lang_code, LANGUAGES["en"])
    tts_lang = lang_info["gtts_lang"]

    audio_path = os.path.join(BASE_DIR, "tts_output.mp3")
    tts = gTTS(text=text, lang=tts_lang)
    tts.save(audio_path)

    try:
        subprocess.run(["mpg123", "-q", audio_path])
    except:
        print("ERROR: Install mpg123 to play audio.")


# --------- Routes ---------

@app.route("/", methods=["GET"])
def index():
    lang = get_lang()
    ui = UI_TEXT[lang]

    query = request.args.get("q", "").strip()
    raw_results = search_offices(query) if query else []

    # Attach translated directions
    results = []
    for office in raw_results:
        dir_key = f"directions_{lang}"
        directions = office.get(dir_key) or office.get("directions_en", "")
        office_copy = dict(office)
        office_copy["directions"] = directions
        results.append(office_copy)

    return render_template(
        "index.html",
        query=query,
        results=results,
        lang=lang,
        languages=LANGUAGES,
        ui=ui
    )


@app.route("/set_lang/<lang_code>")
def set_lang(lang_code):
    if lang_code in LANGUAGES:
        session["lang"] = lang_code
    return redirect(url_for("index"))


@app.route("/speak", methods=["POST"])
def speak():
    lang = get_lang()
    text = request.form.get("text", "").strip()
    query = request.form.get("query", "").strip()

    if text:
        speak_text(text, lang)

    if query:
        return redirect(url_for("index", q=query))
    return redirect(url_for("index"))


# --------- Run App ---------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
