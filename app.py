import webview
import json
import subprocess
import os
import sys
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_exe_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.abspath(".")

class JarvisAPI:
    def __init__(self):
        self.config_path = os.path.join(get_exe_dir(), 'workspace.json')
        self.log_path = os.path.join(get_exe_dir(), 'jarvis.log')
        self.script_path = resource_path('jarvis.ps1')
        self.window = None
        self.tray = None

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {"Default Workspace": {"folders": [], "urls": [], "apps": [], "terminals": []}}

    def save_config(self, data):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=4)
            if self.tray:
                self.tray.menu = build_static_menu(self)
            return "Configuration saved successfully!"
        except Exception as e:
            return f"Error saving: {str(e)}"

    def open_logs(self):
        if os.path.exists(self.log_path):
            os.startfile(self.log_path)
            return "Opening logs..."
        return "Log file is empty or has not been created yet."

    def launch_workspace(self, workspace_name):
        try:
            subprocess.Popen([
                "powershell.exe", 
                "-ExecutionPolicy", "Bypass", 
                "-File", self.script_path, 
                "-workspaceName", workspace_name,
                "-configPath", self.config_path,
                "-logPath", self.log_path
            ], creationflags=0x08000000)
            return f"Launching {workspace_name} (Check logs for details)..."
        except Exception as e:
            return f"Launch error: {str(e)}"

    def check_startup(self):
        startup_dir = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_dir, 'Jarvis.lnk')
        return os.path.exists(shortcut_path)

    def toggle_startup(self, enable):
        startup_dir = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        shortcut_path = os.path.join(startup_dir, 'Jarvis.lnk')
        
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            exe_path = os.path.abspath(sys.argv[0])

        working_dir = get_exe_dir()

        try:
            if enable:
                ps_script = f"$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('{shortcut_path}'); $Shortcut.TargetPath = '{exe_path}'; $Shortcut.Arguments = '--hidden'; $Shortcut.WorkingDirectory = '{working_dir}'; $Shortcut.Save()"
                subprocess.run(["powershell.exe", "-Command", ps_script], creationflags=0x08000000)
                return "Jarvis will now launch automatically on startup."
            else:
                if os.path.exists(shortcut_path):
                    os.remove(shortcut_path)
                return "Jarvis removed from startup sequence."
        except Exception as e:
            return f"Error updating startup: {str(e)}"

# --- SYSTEM TRAY LOGIC ---

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)
    draw.rectangle([16, 16, 48, 48], fill=(0, 124, 186))
    return image

def build_static_menu(api):
    menu_items = []
    config = api.load_config()

    def on_workspace_click(icon, query):
        api.launch_workspace(query.text)

    for ws_name in config.keys():
        menu_items.append(item(ws_name, on_workspace_click))

    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(item('Open Dashboard', lambda: api.window.show()))
    menu_items.append(item('Quit Jarvis', quit_app))
    
    return pystray.Menu(*menu_items)

def quit_app(icon, item):
    icon.stop()
    if api.window:
        api.window.destroy()
    os._exit(0)

def initialize_background_tasks(api_instance):
    def run_tray():
        api_instance.tray = pystray.Icon("Jarvis", create_tray_icon(), "Jarvis", menu=build_static_menu(api_instance))
        api_instance.tray.run()
    
    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

# --- MAIN EXECUTION ---

if __name__ == '__main__':
    api = JarvisAPI()
    
    start_hidden = '--hidden' in sys.argv
    
    # Starting window height reduced to 750 so it naturally fits on laptop screens
    window = webview.create_window(
        'Jarvis Manager', 
        resource_path('gui.html'), 
        js_api=api, 
        width=900, 
        height=750,
        min_size=(700, 600),
        hidden=start_hidden
    )
    api.window = window

    def on_closing():
        window.hide()
        return False
    window.events.closing += on_closing

    webview.start(initialize_background_tasks, api)