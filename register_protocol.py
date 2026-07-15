import winreg
import os
import sys

def register_protocol():
    # Use the python executable that runs this script (the venv python)
    python_exe = sys.executable
    script_path = os.path.abspath("main.py")
    
    # The command Windows will run: "C:\...\python.exe" "C:\...\main.py" "%1"
    command = f'"{python_exe}" "{script_path}" "%1"'
    
    try:
        # Create aerodl key
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes\aerodl")
        winreg.SetValue(key, "", winreg.REG_SZ, "URL:Aero Downloader Protocol")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        
        # Create shell\open\command keys
        cmd_key = winreg.CreateKey(key, r"shell\open\command")
        winreg.SetValue(cmd_key, "", winreg.REG_SZ, command)
        
        print("Protocolo 'aerodl://' registrado exitosamente en Windows.")
    except Exception as e:
        print("Error registrando el protocolo:", e)

if __name__ == "__main__":
    register_protocol()
