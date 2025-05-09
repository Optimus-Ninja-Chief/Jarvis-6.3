import speech_recognition as sr
import pyttsx3
from datetime import datetime, timedelta
import wikipedia
import webbrowser
import os
import time
import psutil
import requests
from bs4 import BeautifulSoup
import random
import pyautogui
import sys
import subprocess
import socket
from GPUtil import GPUtil
import win32gui
import win32con
import threading
import winsound
import psutil
import GPUtil


class Jarvis:
    def __init__(self):
        
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        voice_choice = "0"
        self.engine.setProperty('voice', voices[int(voice_choice)].id)
        self.engine.setProperty('rate', 160)
        self.engine.setProperty('volume', 15)
        
        self.recognizer = sr.Recognizer()
        self.responses = {
            "hello": ["Hi there!", "Hello!", "Hey! How can I help?"],
            "how are you": ["I'm doing great!", "All systems operational!", "Ready to assist you!"],
            "tell me about yourself": ["I am Jarvis, A program created by M&S corp", "I am Jarvis. Fun Fact About Me. It Took 18 tries for me to start working"],
            "what's your name": ["I'm Jarvis, your AI assistant", "You can call me Jarvis"],
            "goodbye": ["Goodbye!", "See you later!", "Take care!"],
            "thanks": ["You're welcome!", "Anytime!", "Happy to help!"],
            "thank you": ["No problem Bro!", "Lez Goooo"],
            "who made you": ["I was created by M&S Corp", "I'm an AI assistant created by M&S Corp"],
            "what can you do": ["I can help with web searches, system monitoring, weather updates, and chatting!"]
        }
        self.offline_mode = not self.check_internet()

        def check_gaming_status(self):
            """Check the gaming status based on CPU usage."""
            cpu_percent = psutil.cpu_percent()
            if cpu_percent < 20:
                return "Gaming Status = Great"
            elif 20 <= cpu_percent <= 50:
                return "Gaming Status = Okay"
            else:
                return "Gaming Status = Low"

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call fake spaghetti? An impasta!",
            "Why did the bicycle fall over? Because it was two-tired!"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
    def flip_coin(self):
        answers = [
            "Let's Flip It!",
            "Okay Here We Go!"
        ]
        self.speak(random.choice(answers))
        coinSides = ["Heads", "Tails"]
        result = random.choice(coinSides)
        answerResults = [
            f"Oh! It is {result}!",
            f"Wow! It is {result}!",
        ]
        self.speak(random.choice(answerResults))
        self.speak("Would you like to flip again? (yes/no)")
        flipAgain = self.listen()
        if flipAgain and 'yes' in flipAgain.lower():
            self.flip_coin()  # Recursive call for another flip
        elif flipAgain and 'no' in flipAgain.lower():
            self.speak("Alright, thanks for playing!")

    def set_alarm(self):
        """Set an alarm with voice commands and continue other functions"""

    def parse_alarm_time(self, spoken_time):
        """Convert spoken time to datetime object"""
        try:
            now = datetime.now()
            
            if "in" in spoken_time:
                parts = spoken_time.split()
                if "minutes" in spoken_time or "minute" in spoken_time:
                    minutes = int(''.join(filter(str.isdigit, parts[1])))
                    return now + timedelta(minutes=minutes)
                elif "hours" in spoken_time or "hour" in spoken_time:
                    hours = int(''.join(filter(str.isdigit, parts[1])))
                    return now + timedelta(hours=hours)
            
            elif ":" in spoken_time:
                hour, minute = map(int, spoken_time.split(":"))
                alarm_time = now.replace(hour=hour, minute=minute, second=0)
                if alarm_time <= now:
                    alarm_time += timedelta(days=1)
                return alarm_time
            
            else:
                hour = int(''.join(filter(str.isdigit, spoken_time)))
                alarm_time = now.replace(hour=hour, minute=0, second=0)
                if alarm_time <= now:
                    alarm_time += timedelta(days=1)
                return alarm_time
        except:
            return None
        
    def alarm_thread(alarm_time, alarm_label=""):
        """Run alarm in background thread"""
        while datetime.now() < alarm_time:
            time.sleep(1)
            
        for _ in range(3):
            winsound.Beep(1000, 1000)
            time.sleep(0.5)
            
        wake_message = f"Dude! It's {alarm_time.strftime('%I:%M %p')}"
        if alarm_label:
            wake_message += f" - The Reminder You Set was: {alarm_label}"
            
    def set_alarm(self):
        """Set an alarm with voice commands and continue other functions"""
        from datetime import timedelta  

        def alarm_thread(alarm_time, alarm_label=""):
            """Run alarm in background thread"""
            while datetime.now() < alarm_time:
                if datetime.now() >= alarm_time:
                    break

            for _ in range(3):
                winsound.Beep(1000, 1000)
                time.sleep(0.5)

            wake_message = f"Wake up! It's {alarm_time.strftime('%I:%M %p')}"
            if alarm_label:
                wake_message += f" - Reminder for: {alarm_label}"

            self.speak(wake_message)

            self.speak("Would you like to snooze for 5 minutes?")
            response = self.listen()

            if response and any(word in response.lower() for word in ['yes', 'yeah', 'yep', 'sure']):
                new_time = datetime.now() + timedelta(minutes=5)
                self.speak(f"Alarm snoozed until {new_time.strftime('%I:%M %p')}")
                alarm_thread(new_time, alarm_label)

        self.speak("How would you like to set the alarm?")
        self.speak("I would reccommend using the 24 hour format")


        time_input = self.listen()
        if not time_input:
            self.speak("Sorry, I couldn't understand the time")
            return False

        alarm_time = self.parse_alarm_time(time_input.lower())
        if not alarm_time:
            self.speak("Sorry, I couldn't understand the time format")
            return False

        self.speak("Would you like to add a label or reminder message?")
        label_input = self.listen()
        alarm_label = label_input if label_input else ""

        if not hasattr(self, 'active_alarms'):
            self.active_alarms = []
        self.active_alarms.append((alarm_time, alarm_label))

        self.speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
        if alarm_label:
            self.speak(f"with reminder: {alarm_label}")

        alarm_thread_obj = threading.Thread(
            target=alarm_thread,
            args=(alarm_time, alarm_label),
            daemon=True
        )
        alarm_thread_obj.start()
        return True

    def offline_jars(self):
        if socket.create_connection(("8.8.8.8", 53), timeout=3):
            self.speak("You Are Running In Offline Mode.")
            self.speak("Switching To Offline Jarvis")
            

    def speak(self, text):
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def minimize_window_by_title(self, title, wait_time=2):
        """Minimize window by title after waiting for it to open"""
        time.sleep(wait_time)  
        try:
            window = win32gui.FindWindow(None, title)
            if window:
                win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
                return True
        except Exception as e:
            print(f"Error minimizing window: {e}")
        return False
    
    def offline_jarvis(self):
        def check_internet_connection():
            url = "http://www.google.com"
            timeout = 5
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    return True
            except (requests.ConnectionError, requests.Timeout):
                pass
            return False
        if check_internet_connection():
            self.speak("Running In Online Mode")
        else:
            self.speak("ohio gyattz")

    def clear_screen(self):
        try:
            if os.name == 'nt':
                os.system('cls')
                os.system('cls') 
                os.system('clear')
        except Exception as e:
            print(f"Error clearing screen: {e}")

    def type_text(self, text_to_type):
        try:
            time.sleep(2)
            pyautogui.write(text_to_type)
            return True
        except Exception as e:
            print(f"Error typing text: {e}")
            return False

    def listen(self):
        with sr.Microphone() as source:
            print("\nListening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio) if not self.offline_mode else self.recognizer.recognize_sphinx(audio)
                print(f"You: {text}")
                return text.lower()
            except Exception as e:
                print(f"Error: {e}")
                return ""

    def greet(self):
        hour = datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Jarvis. How can I help you?")
        if self.offline_mode:
            self.speak("Running in offline mode")

    def get_weather(self, city="Ahmedabad"):
        if self.offline_mode:
            return "Weather information unavailable in offline mode"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://www.google.com/search?q=weather+{city}"
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            temp = soup.select('#wob_tm')[0].getText()
            desc = soup.select('#wob_dc')[0].getText()
            humidity = soup.select('#wob_hm')[0].getText()
            
            return f"The temperature in {city} is {temp}°C. Weather is {desc} with {humidity} humidity."
        except:
            return "Sorry, I couldn't fetch the weather information."

    def process_command(self, command):
        command = command.lower().strip()
        
        for key in self.responses:
            if key in command:
                response = random.choice(self.responses[key])
                self.speak(response)
                return True

        if 'wikipedia' in command and not self.offline_mode:
            self.speak('Searching Wikipedia...')
            query = command.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                self.speak(results)
            except:
                self.speak("Sorry, I couldn't find that on Wikipedia")
            self.clear_screen()

        elif 'open drive' in command:
            os.system("start explorer https://drive.google.com/drive/my-drive")
            self.speak("Opening Google Drive")
            self.clear_screen()

        elif 'open settings' in command:
            os.system("control.exe")
            self.speak("Opening Settings")
            self.clear_screen()

        elif 'open roblox' in command:
            try:
                roblox_paths = [
                    r"C:\Users\ADMIN\AppData\Local\Roblox"
                ]
                
                for path in roblox_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        versions = os.listdir(expanded_path)
                        if versions:
                            latest = max(versions)
                            roblox_exe = os.path.join(expanded_path, latest, "RobloxPlayerLauncher.exe")
                            if os.path.exists(roblox_exe):
                                os.startfile(roblox_exe)
                                self.speak("Opening Roblox")
                                self.clear_screen()
                                return True
                self.speak("Roblox Is Gyatted")
                self.speak("Sorry, I couldn't find Roblox installation")
            except Exception as e:
                self.speak("Error opening Roblox")
                print(f"Error: {e}")
            except Exception as e:
                self.speak("Error opening Roblox")
                print(f"Error: {e}")

        elif 'open asphalt' in command:
            try:
                asphalt_paths = [
                    r"C:\Program Files\WindowsApps\Gameloft.Asphalt9_2.9.1.0_x64__n80b4h9cj9kk8",
                    r"C:\Program Files (x86)\Gameloft\Asphalt 9"
                ]

                for path in asphalt_paths:
                    if os.path.exists(path):
                        asphalt_exe = os.path.join(path, "Asphalt9.exe")
                        if os.path.exists(asphalt_exe):
                            os.startfile(asphalt_exe)
                            self.speak("Opening Asphalt Legends Unite")
                            self.clear_screen()
                            return True

                self.speak("Could not find Asphalt installation")
            except Exception as e:
                self.speak("Error opening Asphalt")
                print(f"Error: {e}")

        elif 'open powerpoint' in command:
            try:
                pointy_paths = [
                    r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE"
                ]

                for path in pointy_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak("Opening Microsoft PowerPoint")
                        self.clear_screen()
                        return True

                self.speak("Could not find Microsoft PowerPoint installation")
            except Exception as e:
                self.speak("Error opening Microsoft PowerPoint")
                print(f"Error: {e}")

        elif 'update' in command:
            self.speak("Updating Jarvis")
            self.clear_screen()
            subprocess.Popen([sys.executable, __file__])
            sys.exit()

        elif 'Gaming Status' in command:
            status_of_deez_nutz = self.check_gaming_status()
            self.speak(status_of_deez_nutz)

        elif 'help me' in command:
            self.speak("Sure, Here Are The Commands!")
            commands = [
                "Please Refer To User Maual"
            ]
            for cmd in commands:
                self.speak(cmd)
            self.clear_screen()

        elif 'gmail' in command:
            webbrowser.open("https://mail.google.com")
            self.speak("Opening Gmail")
            self.clear_screen()

        elif 'open jiosaavn' in command:
            webbrowser.open("https://www.jiosaavn.com")
            self.speak("Opening JioSaavn")
            self.clear_screen()

        elif 'open youtube' in command and not self.offline_mode:
            webbrowser.open("youtube.com")
            self.speak("Opening YouTube")
            self.clear_screen()

        elif 'open google' in command and not self.offline_mode:
            webbrowser.open("google.com")
            self.speak("Opening Google")
            self.clear_screen()

        elif 'set alarm' in command:
            self.speak("Sure, let's set an alarm.")
            self.set_alarm()

        elif 'time' in command:
            strTime = datetime.now().strftime("%I:%M %p")
            self.speak(f"The time is {strTime}")
            self.clear_screen()

        elif 'system status' in command:
            memory = psutil.virtual_memory().percent  
            memory = psutil.virtual_memory().percent
            if cpu < 20:
                self.speak("CPU usage is low")
            elif cpu > 20:
                self.speak("CPU usage is okay")
            elif cpu > 50:
                self.speak("CPU usage is getting high")
            elif cpu > 80:
                self.speak("CPU usage is critical")

        elif 'gaming mode' in command:
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            gpus = GPUtil.getGPUs()
            gpu = gpus[0]
            gpu_memory = gpu.memoryUtil * 100  # Retain for potential future use
            gpu_memory = gpu.memoryUtil * 100
            self.speak("Activating Gaming Mode")
            try:
                roblox_paths = [
                    r"C:\Users\ADMIN\AppData\Local\Roblox"
                ]
                
                for path in roblox_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        versions = os.listdir(expanded_path)
                        if versions:
                            latest = max(versions)
                            roblox_exe = os.path.join(expanded_path, latest, "RobloxPlayerLauncher.exe")
                            if os.path.exists(roblox_exe):
                                os.startfile(roblox_exe)
                                self.speak("Launching Roblox")
                                time.sleep(2)

                asphalt_paths = [
                    r"C:\Program Files\WindowsApps\Gameloft.Asphalt9_2.9.1.0_x64__n80b4h9cj9kk8",
                    r"C:\Program Files (x86)\Gameloft\Asphalt 9"
                ]

                for path in asphalt_paths:
                    if os.path.exists(path):
                        asphalt_exe = os.path.join(path, "Asphalt9.exe")
                        if os.path.exists(asphalt_exe):
                            os.startfile(asphalt_exe)
                            self.speak("Launching Asphalt Legends Unite")
                            time.sleep(5)
                            if gpu > 80:
                                self.speak("GPU usage is critical")
                            elif gpu >= 50:
                                self.speak("GPU usage is high")
                            elif gpu >= 20:
                                self.speak("GPU usage is okay")
                            else:
                                self.speak("GPU usage is low")
                            break

                self.speak("Gaming Mode Activated")
                self.clear_screen()

            except Exception as e:
                self.speak("Error activating gaming mode")
                self.speak("Opening Mainframe Panel For Error Analysis")
                self.clear_screen()
                try:
                    self.maximize_window_by_title("C:\Windows\py.exe")
                except:
                    self.speak("Error opening mainframe panel")
                    self.speak("Please check the error manually in the command prompt panel.") 

        elif 'open youtube app' in command:
            try:
                youtube_paths = [
                    r"C:\Program Files\WindowsApps\GoogleLLC.YouTube_1.0.0.0_x64__8wekyb3d8bbwe\YouTube.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"C:\Users\<YourUsername>\AppData\Local\Microsoft\Windows\Start Menu\Programs\Edge Apps",
                    r"C:\Users\<YourUsername>\AppData\Local\Microsoft\Windows\Start Menu\Programs\Chrome Apps"
                ]

                for path in youtube_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak("Opening YouTube app")
                        self.clear_screen()
                        return True

                self.speak("Could not find YouTube app installation")
            except Exception as e:
                self.speak("Error opening YouTube app")
                print(f"Error: {e}")

        elif 'gaming status' in command:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_load = gpu.load * 100
                    gpu_memory = gpu.memoryUtil * 100

                    
                    if gpu_load < 20:
                        self.speak("GPU usage is low")
                    elif gpu_load > 20:
                        self.speak("GPU usage is okay")
                    elif gpu_load > 50:
                        self.speak("GPU usage is getting high")
                    elif gpu_load > 80:
                        self.speak("GPU usage is critical")
            except:
                self.speak("Error fetching GPU usage")

        elif 'weather' in command and not self.offline_mode:
            city = "Ahmedabad"
            if 'in' in command:
                city = command.split('in')[1].strip()
            weather_info = self.get_weather(city)
            self.speak(weather_info)
            self.clear_screen()
        
        elif 'type' in command:
            text_to_type = command.replace('type', '').strip()
            if text_to_type:
                self.speak(f"I'll type: {text_to_type}")
                self.type_text(text_to_type)
                pyautogui.press('enter')
            else:
                self.speak("What would you like me to type?")
                text_to_type = self.listen()
                if text_to_type:
                    self.speak(f"Typing: {text_to_type}")
                    self.type_text(text_to_type)

        elif 'search' in command and not self.offline_mode:
            webbrowser.open("www.google.com")
            self.speak("What would you like me to search?")
            search_query = self.listen()
            if search_query:
                self.type_text(search_query)
                pyautogui.press('enter')
                self.speak(f"The Results For '{search_query}' Are Displayed In Your Web Browser ")

        elif "coin flip" in command:
            self.flip_coin()

        elif 'screenshot' in command:
            screenshot = pyautogui.screenshot()
            screenshot.save(f"screenshot_{time.strftime('%Y%m%d_%H%M')}.png")
            self.speak("Screenshot taken")
            self.clear_screen()

        elif 'game bar' in command:
            self.speak("opening game bar")
            pyautogui.hotkey('win', 'g')
            self.clear_screen()

        elif 'lock ' in command:
            os.system('rundll32.exe user32.dll,LockWorkStation')
            self.speak("Computer locked")

        elif 'close' in command:
            for _ in range(5):    
                pyautogui.hotkey('alt', 'f4')
            
            self.speak("Window's closed")

        elif 'clear' in command:
            time.sleep(2)

        elif 'minimise' in command:
            pyautogui.hotkey('win', 'd')
            self.speak("Minimising all windows")
            self.clear_screen()

        elif 'enter' in command:
            try:
                pyautogui.press('enter')
                self.speak("Pressed enter key")
            except Exception as e:
                self.speak("Error pressing enter key")
                print(f"Error: {e}")

        elif 'open word' in command:
            try:
                word_paths = [
                    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE"
                ]

                for path in word_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak("Opening Microsoft Word")
                        self.clear_screen()
                        return True

                self.speak("Could not find Microsoft Word installation")
            except Exception as e:
                self.speak("Error opening Microsoft Word")
                print(f"Error: {e}")

        elif 'open minecraft' in command:
            try:
                minecraft_paths = [
                    r"C:\Users\%USERNAME%\AppData\Roaming\.minecraft\TLauncher.exe",
                    r"C:\Program Files\TLauncher\TLauncher.exe",
                    r"C:\Program Files (x86)\TLauncher\TLauncher.exe",
                    r"C:\Users\%USERNAME%\AppData\Roaming\.minecraft\Minecraft.exe",
                    r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe",
                    r"C:\Users\ADMIN\Desktop\Manas\Private\SKlauncher-3.2.10.exe"
                ]

                for path in minecraft_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak("Opening Minecraft")
                        self.clear_screen()
                        return True

                self.speak("Could not find Minecraft installation")
            except Exception as e:
                self.speak("Error opening Minecraft")
                print(f"Error: {e}")
        elif 'open discord' in command:
            try:
                discord_paths = [
                    r"C:\Users\%USERNAME%\AppData\Local\Discord\app-1.0.9003\Discord.exe",
                    r"C:\Users\%USERNAME%\AppData\Local\Discord\app-1.0.9003\Discord.exe",
                    r"C:\Program Files (x86)\Discord Inc\Discord\Discord.exe"
                ]

                for path in discord_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        os.startfile(expanded_path)
                        self.speak("Opening Discord")
                        self.clear_screen()
                        return True

                self.speak("Could not find Discord installation")
            except Exception as e:
                self.speak("Error opening Discord")
                print(f"Error: {e}")

        elif 'open world' in command:
            try:
                word_paths = [
                    r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
                    r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE"
                ]

                for path in word_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        self.speak("Opening Microsoft Word")
                        self.clear_screen()
                        return True

                self.speak("Could not find Microsoft Word installation")
            except Exception as e:
                self.speak("Error opening Microsoft Word")
                print(f"Error: {e}")

        elif 'open tlauncher' in command:
            try:
                tlauncher_paths = [
                    r"C:\Users\%USERNAME%\AppData\Roaming\.minecraft\TLauncher.exe",
                    r"C:\Program Files\TLauncher\TLauncher.exe",
                    r"C:\Program Files (x86)\TLauncher\TLauncher.exe"
                ]
        
                for path in tlauncher_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        os.startfile(expanded_path)
                        self.speak("Opening TLauncher")
                        self.clear_screen()
                        return True
                
                self.speak("Could not find TLauncher installation")
            except Exception as e:
                self.speak("Error opening TLauncher")
                print(f"Error: {e}")

        elif 'Run Synthesis' in command:
            self.speak("Okay, Running Synthesis") 
            os.system("explorer.exe")
            self.clear_screen()
            self.minimize_window_by_title("Windows Explorer")
            os.system("cmd")

        elif 'open whatsapp' in command:
            try:
                whatsapp_paths = [
                    r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe",
                    r"C:\Program Files (x86)\WhatsApp\WhatsApp.exe"
                ]

                for path in whatsapp_paths:
                    expanded_path = os.path.expandvars(path)
                    if os.path.exists(expanded_path):
                        os.startfile(expanded_path)
                        self.speak("Opening WhatsApp")
                        self.clear_screen()
                        return True

                self.speak("Could not find WhatsApp installation")
            except Exception as e:
                self.speak("Error opening WhatsApp")
                print(f"Error: {e}")

        elif 'exit' in command:
            self.speak("Goodbye!")
            sys.exit()
            return False

        return True

def main():
    jarvis = Jarvis()
    jarvis.greet()

    while True:
        command = jarvis.listen()
        if command:
            if not jarvis.process_command(command):
                break

if __name__ == "__main__":
    main()