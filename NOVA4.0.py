import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import shutil
import smtplib
import yt_dlp  # type: ignore

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        speak("Good morning sir")
    elif current_hour < 18:
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")
    speak("I am NOVA your personal assistant. How can I help you sir?")

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)

    try:
        print("Processing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {command}\n")
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that. Could you please repeat that again?")
        speak("Sorry, I didn't understand that. Could you please repeat that again?")
        return None
    return command.lower()

def send_email(to_address, subject, content):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_address = 'sraghaw130@gmail.com'
    password = '798028609433977471'

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_address, password)
        message = f"Subject: {subject}\n\n{content}"
        server.sendmail(from_address, to_address, message)
        server.close()
        speak("Email sent successfully.")
    except Exception as e:
        speak(f"Failed to send email. Error: {str(e)}")

def organize_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension in ['.jpg', '.jpeg', '.png', '.gif']:
            destination_folder = 'Images'
        elif extension in ['.pdf', '.doc', '.docx', '.txt']:
            destination_folder = 'Documents'
        elif extension in ['.mp3', '.wav', '.flac']:
            destination_folder = 'Music'
        elif extension in ['.mp4', '.avi', '.mkv']:
            destination_folder = 'Videos'
        elif extension in ['.msi', '.zip']:
            destination_folder = 'Setups'
        elif extension in ['.pptx']:
            destination_folder = 'PPT'
        elif extension in ['.py']:
            destination_folder = 'Python Projects'
        else:
            destination_folder = 'Other'

        destination_path = os.path.join(directory, destination_folder)
        os.makedirs(destination_path, exist_ok=True)
        shutil.move(file_path, destination_path)

def download_video(video_url, output_folder):
    ydl_opts = {
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Saves with the video title as the filename 
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        speak("Download completed!")
    except Exception as e:
        speak(f"An error occurred while downloading the video: {e}")

if __name__ == "__main__":
    greet_user()
    while True:
        command = listen_for_command()

        if command:
            if 'wikipedia' in command:
                speak('Searching Wikipedia...')
                query = command.replace("wikipedia", "").strip()
                try:
                    summary = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(summary)
                    speak(summary)
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are many results. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("I couldn't find any results for that query.")
            
            elif 'open youtube' in command:
                speak('Opening YouTube')
                webbrowser.open("https://www.youtube.com/")

            elif 'open map' in command:
                speak('Opening maps')
                webbrowser.open("https://www.google.com/maps/@22.5896484,88.3115084,35982m/data=!3m1!1e3?authuser=0&entry=ttu&g_ep=EgoyMDI0MDgyMS4wIKXMDSoASAFQAw%3D%3D")
            
            elif 'open google' in command:
                speak('Opening Google')
                webbrowser.open("https://www.google.com/")
            
            elif 'open classroom' in command:
                speak('Opening Google Classroom')
                webbrowser.open("https://classroom.google.com/u/3/")
            
            elif 'open aot' in command:
                speak("Opening Academy of Technology's website")
                webbrowser.open("https://aot.edu.in/")
            
            elif 'open mail' in command:
                speak("Opening Mail")
                webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
            
            elif 'play music' in command:
                speak('Opening Spotify')
                webbrowser.open("https://open.spotify.com/")
            
            elif 'what is the time' in command:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time now is {current_time}")
            
            elif 'open code' in command:
                speak('Opening VS Code')
                code_path = r"C:\Users\arun\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code"
                os.startfile(code_path)
            
            elif 'send mail' in command:
                speak('Opening compose email')
                webbrowser.open("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox?compose=new")
            
            elif 'organize files' in command:
                speak('Please provide the directory path to organize files.')
                directory = listen_for_command()
                if directory:
                    if os.path.isdir(directory):
                        organize_files(directory)
                        speak(f"Files have been organized in {directory}.")
                    else:
                        speak("The directory path provided is not valid.")
            
            elif 'how are you' in command:
                speak("I am always fine, sir. How can I assist you today?")
            
            elif 'what is your name' in command:
                speak("My name is NOVA, your personal assistant.")
            
            elif 'what does nova mean' in command:
                speak("NOVA stands for Next Generational Optimised Virtual Assistant.")
            
            elif 'i am sad' in command:
                speak("I'm sorry to hear that. If you need anything, I'm here to help.")
            
            elif 'download video' in command:
                speak("Please type the YouTube video link in the terminal.")
                video_url = input("Enter the YouTube video link: ")
                speak("Please specify the folder to save the video.")
                output_folder = input("Enter the folder path to save the video: ")
                
                if os.path.isdir(output_folder):
                    download_video(video_url, output_folder)
                else:
                    speak("The directory path provided is not valid. Please try again.")

            elif 'exit' in command:
                speak("Okay, have a great day, sir!")
                break
