import platform
import subprocess
import webbrowser

import pyautogui


class ActionMapper:
    def __init__(self):
        self.system_name = platform.system().lower()

    def open_vscode(self):
        try:
            subprocess.Popen(["code"])
            print("Opened VS Code.")
        except FileNotFoundError:
            print("VS Code command not found. Make sure 'code' is installed in PATH.")

    def open_browser(self):
        webbrowser.open("https://www.google.com")
        print("Opened browser.")

    def open_terminal(self):
        if "windows" in self.system_name:
            subprocess.Popen(["cmd"])
        elif "linux" in self.system_name:
            subprocess.Popen(["gnome-terminal"])
        elif "darwin" in self.system_name:
            subprocess.Popen(["open", "-a", "Terminal"])
        else:
            print("Unsupported operating system for terminal launch.")

        print("Opened terminal.")

    def open_linkedin(self):
        webbrowser.open("https://www.linkedin.com")
        print("Opened LinkedIn.")

    def open_calculator(self):
        if "windows" in self.system_name:
            subprocess.Popen(["calc"])
        elif "linux" in self.system_name:
            try:
                subprocess.Popen(["gnome-calculator"])
            except FileNotFoundError:
                print("Calculator not found. Try installing gnome-calculator.")
        elif "darwin" in self.system_name:
            subprocess.Popen(["open", "-a", "Calculator"])
        else:
            print("Unsupported operating system for calculator launch.")

        print("Opened calculator.")

    def close_active_window(self):
        pyautogui.hotkey("alt", "f4")
        print("Closed active window.")

    def run_action(self, gesture):
        if gesture == "one_finger":
            self.open_vscode()

        elif gesture == "two_fingers":
            self.open_browser()

        elif gesture == "three_fingers":
            self.open_terminal()

        elif gesture == "four_fingers":
            self.open_linkedin()

        elif gesture == "open_hand":
            self.open_calculator()

        elif gesture == "fist":
            self.close_active_window()