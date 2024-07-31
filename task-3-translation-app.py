import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import Translator
from datetime import datetime

def clear_text_areas():
    """Clear the text areas for English audio and Hindi translation."""
    english_text_area.delete(1.0, tk.END)
    hindi_text_area.delete(1.0, tk.END)
    status_label.config(text="Press 'Translate' to begin")

def perform_translation():  
    """Capture English audio and translate it into Hindi."""
    clear_text_areas()
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="Listening...")

        try:
            audio_data = recognizer.listen(source, timeout=5)
            status_label.config(text="Transcribing...")

            spoken_text = recognizer.recognize_google(audio_data)
            detected_language = identify_language(spoken_text)
            if detected_language == 'en':
                
                if spoken_text.strip().lower().startswith(('m', 'o')):
                    status_label.config(text="Translation not allowed for text starting with 'm' or 'o'.")
                else:
                    english_text_area.insert(tk.END, spoken_text)  # Display English audio text
                    hindi_translation = translate_to_hindi(spoken_text)
                    hindi_text_area.insert(tk.END, hindi_translation)  # Display Hindi translation
            else:
                status_label.config(text="Only English audio is supported.")
        except sr.UnknownValueError:
            status_label.config(text="Unable to understand audio. Please try again.")
        except sr.RequestError:
            status_label.config(text="Unable to connect to the speech recognition service.")

def translate_to_hindi(text):
    """Translate the provided English text into Hindi."""
    translator = Translator()
    translation = translator.translate(text, dest='hi')
    return translation.text

def identify_language(text):
    """Identify the language of the provided text."""
    translator = Translator()
    detected_lang = translator.detect(text)
    return detected_lang.lang

def execute_translation():
    """Execute translation based on the current time."""
    current_time = datetime.now().strftime("%H:%M:%S")
    if current_time >= "18:00:00":
        perform_translation()
    else:
        status_label.config(text="Translation service available after 6 PM IST")

# Set up the main application window
app_window = tk.Tk()
app_window.title("English to Hindi Audio Translator")
app_window.geometry("600x600+460+100")
app_window.configure(bg="#ffffff")

# Frame for containing widgets
frame = tk.Frame(app_window, bg="white", highlightbackground="black", highlightthickness=2, bd=0)
frame.place(x=50, y=70, width=500, height=430)

status_label = tk.Label(frame, text="Press 'Translate' to begin", bg="white", font=('Verdana', 14))
status_label.place(x=0, y=4, width=489, height=70)

translate_btn = tk.Button(frame, text="Translate", command=execute_translation, bg="blue", fg="white", font=('Arial', 13, 'bold'))
translate_btn.place(x=200, y=80, width=100, height=30)

# Labels and text areas for displaying English audio and Hindi translation
english_label = tk.Label(frame, text="English Audio:", bg="white", font=('Verdana', 13, 'bold'))
english_label.place(x=10, y=120)

english_text_area = tk.Text(frame, wrap=tk.WORD, height=3, width=53, font=('Arial', 13, 'bold'))
english_text_area.place(x=10, y=160)

hindi_label = tk.Label(frame, text="Hindi Translation:", bg="white", font=('Verdana', 13, 'bold'))
hindi_label.place(x=10, y=230)

hindi_text_area = tk.Text(frame, wrap=tk.WORD, height=3, width=53, font=('Arial', 13, 'bold'))
hindi_text_area.place(x=10, y=270)

# Button to close the application
close_btn = tk.Button(frame, text="Close", command=app_window.quit, bg="red", fg="white", font=('Arial', 13, 'bold'))
close_btn.place(x=220, y=350, width=50, height=30)

# Start the Tkinter event loop
app_window.mainloop()
