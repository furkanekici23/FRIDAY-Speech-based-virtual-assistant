import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from gtts import gTTS
import pygame 
import os
import json
import tempfile 
import datetime
import requests
import subprocess
import webbrowser

# pygame başlat
pygame.init()
pygame.mixer.init()

# .py dosyasının bulunduğu klasör
base_dir = os.path.dirname(os.path.abspath(__file__))
AUDIO_FILE = os.path.join(base_dir, "command.wav")

def record_audio(duration=5, fs=44100):
    """Mikrofon kaydı yapar."""
    print("🔴 Listening... (5 seconds)")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    wav.write(AUDIO_FILE, fs, audio)
    print("✅ Recording saved.")

def speech_to_text(audio_file=AUDIO_FILE):
    """Ses dosyasını metne çevirir (İngilizce)."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)
    try:
        print("💡 Trying to recognize in English...")
        text = recognizer.recognize_google(audio_data, language="en-US")
        print(f"✅ English Recognized: {text}")
        return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio (English).")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Google Speech API error (English); {e}")
        return None

def text_to_speech(text):
    """Metni ses dosyasına dönüştürür ve çalar."""
    tts = gTTS(text=text, lang='en')
    tts_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts_file = tmpfile.name

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except pygame.error:
            pass

        tts.save(tts_file)
        pygame.mixer.music.load(tts_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error during TTS playback: {e}")
    finally:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        try:
            pygame.mixer.music.unload()
        except pygame.error:
            pass
        if tts_file and os.path.exists(tts_file):
            os.remove(tts_file)

API_KEY_WEATHER = "9392a66a98aefd1725e82248c8b7efa4"

def get_weather_response(city_name):
    base_url = "http://api.weatherstack.com/current"
    params = {
        'access_key': API_KEY_WEATHER,
        'query': city_name,
        'units': 'm'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if "success" in data and data["success"] is False:
            return "Sorry, I couldn't retrieve the weather information. Please check the city name or API key."
        current = data.get('current', {})
        location = data.get('location', {})
        if not current or not location:
            return "Sorry, weather data is not available right now."
        temp = current.get('temperature')
        desc = current.get('weather_descriptions', ["No description"])[0]
        humidity = current.get('humidity')
        wind_speed = current.get('wind_speed')
        city = location.get('name')
        country = location.get('country')
        return (f"The current weather in {city}, {country} is {desc.lower()} with a temperature of {temp}°C, "
                f"humidity at {humidity}%, and wind speed of {wind_speed} km/h.")
    except Exception as e:
        return f"An error occurred while retrieving weather data: {e}"


def start_app(): # SORUNLU
    prompt = (
        "Which application do you want to run? "
        "You can say 'spotify', 'fifa', 'youtube' or 'google chrome'."
    )
    while True:
        text_to_speech(prompt)
        record_audio()
        user_text_inner = speech_to_text()

        if user_text_inner is None:
            text_to_speech("I couldn't understand you. Please try again.")
            continue

        user_text_inner = user_text_inner.lower()

        if "spotify" in user_text_inner:
         webbrowser.open("https://open.spotify.com")
         return "Opening Spotify."
         break

        elif "youtube" in user_text_inner:
         webbrowser.open("https://youtube.com")
         return "Opening Youtube."
         break

        elif "fifa" in user_text_inner:
            os.startfile(r"D:\FIFA 25\EA SPORTS FC 25\FC25.exe")
            return "Opening FC 25."
        
            break
        elif "white" in user_text_inner:
            os.startfile(r"D:\Steam\steam.exe")
             
            return "Opening steam."
             
        
            break
        elif "google"  in user_text_inner or "chrome" in user_text_inner:
            webbrowser.open("https://www.google.com.tr/")
            return "Opening Google Chrome."
        
            break
        else:
            text_to_speech("I couldn't find the application. Please say the name again.")

    
def get_bot_response(user_input): #MAİN
    user_input_lower = user_input.lower()

    # Uygulama açma
    if any(kw in user_input_lower for kw in ["start","run","spotify","fifa","chrome"]):
        start_app()
        return f"App is running."

    # Saat sorguları
    if any(kw in user_input_lower for kw in ["what time is it", "time", "current time"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    # Tarih sorguları
    if any(kw in user_input_lower for kw in ["what is the date", "what day is it", "today's date", "current date"]):
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    # Hava durumu sorguları
    weather_keywords = ["weather", "temperature", "forecast", "rain", "sunny", "cloudy", "snow"]
    if any(kw in user_input_lower for kw in weather_keywords):
        if "in " in user_input_lower:
            city = user_input_lower.split("in ")[-1].strip().rstrip("?.!")
            return get_weather_response(city)
        else:
            return "Please specify the city you want the weather information for."

    # JSON'dan cevap alma (dosya yolunu kendi dosya yoluna göre ayarla)
    try:
        json_file_path = r"D:\Masaüstü\CODİNG\python\projeler\1_python_for_fun_projemsiler\friday\responses.json"
        with open(json_file_path, 'r', encoding='utf-8') as f:
            responses = json.load(f)

        for category, info in responses.items():
            if "keywords" in info and isinstance(info["keywords"], list):
                for keyword in info["keywords"]:
                    if keyword in user_input_lower:
                        if "response" in info:
                            return info["response"]
        return "I'm sorry, I didn't understand that. Can you please repeat? If you want to end program,you can say 'exit' "
    except FileNotFoundError:
        return "I apologize, but I'm having trouble accessing my response data."
    except json.JSONDecodeError:
        return "There was an error processing my response data."
    except Exception:
        return "An unexpected error occurred while processing your request."


#################################################################################
print("🤖 Bot: Hi,I am Friday! How can I help you ?  F.Y.I., you can say'exit' to quit.")
text_to_speech("Hi,I am Friday! How can I help you ? F.Y.I., you can say'exit' to quit.")

try:
    while True:
        record_audio()
        user_text = speech_to_text()

        if user_text:
            print(f"🗣️ You: {user_text}")
            if user_text.lower() in ["exit", "quit", "goodbye friday", "bye friday", "goodbye", "bye"]:
                print("Bot: Goodbye!")
                text_to_speech("Goodbye!")
                break

            bot_response = get_bot_response(user_text)
            print(f"🤖 Bot: {bot_response}")
            text_to_speech(bot_response)

        else:
            # Ses algılanamadığında yazılı giriş al
            
            text_to_speech("I didn't catch that. Please type your command.")
            user_text = input("I didn't catch that. Please type your command: ").strip()


            if user_text.lower() in ["exit", "quit", "goodbye friday", "bye friday", "goodbye", "bye"]:
                print("🤖 Bot: Goodbye!")
                text_to_speech("Goodbye!")
                break

            print(f"🗣️ You (typed): {user_text}")
            bot_response = get_bot_response(user_text)
            print(f"🤖 Bot: {bot_response}")
            text_to_speech(bot_response)

except KeyboardInterrupt:
    print("\nFriday is shutting down.")
except Exception as e:
    print(f"An unexpected error occurred in the main loop: {e}")
finally:
    pygame.quit()
    if os.path.exists(AUDIO_FILE):
        os.remove(AUDIO_FILE)


