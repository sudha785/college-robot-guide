# College Robot Guide 🤖🏫

A multilingual humanoid-robot assistant that helps visitors find offices, departments, and staff cabins inside the college.  
Built with **Python + Flask** on the backend and **HTML/CSS** frontend, designed to run on a **Raspberry Pi** inside a humanoid robot.

---

## ✨ Features

- 🔍 **Search by name / department / room number**
- 🌐 **Multilingual support**
  - English  
  - Hindi (हिन्दी)  
  - Kannada (ಕನ್ನಡ)  
  - Telugu (తెలుగు)  
  - Tamil (தமிழ்)
- 🗣️ **Text-to-speech directions** using Google TTS
- 🧭 **Campus map panel** on the right side
- 🎛️ **Quick access buttons** for common locations:
  - Admissions, Accounts, Principal, Exam Cell, CSE Dept, ECE Dept
- 📱 Designed to run in **kiosk mode** on Raspberry Pi (robot display)

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Jinja2 templates  
- **Data:** JSON (`offices.json`)  
- **TTS:** `gTTS` (Google Text-to-Speech)  
- **Target hardware:** Raspberry Pi (3/4) with display + speaker

---

## 📂 Project Structure

```text
robot-guide/
├─ app.py                     # Flask app (backend + routes)
├─ offices.json               # Offices & staff data (multilingual)
├─ convert_offices_csv_to_json.py  # Helper script (optional)
│
├─ templates/
│   └─ index.html             # Main UI template
│
└─ static/
    ├─ style.css              # Frontend styling
    └─ campus_map.png         # Campus map image
