"""
Skript zum Starten von labelme für die Erstellung einer Bounding Box

Bei Ausführung über die Powershell, sicherstellen das die .venv aktiv ist!
***Debug-Bypass***___________________________________________________________________________
PowerShell: Skripte in der .venv zu starten:    powershell -ExecutionPolicy Bypass
                                                .\.venv\Scripts\Activate.ps1

Funktionen:
1. Virtuelle Umgebung aktivieren
2. labelme mit den richtigen Bildern starten
3. Optional: Automatische Ordnerstruktur prüfen
"""

import os
import subprocess
import sys
from pathlib import Path

# ================== KONFIGURATION ==================
# Pfade definieren
BASE_DIR = Path("C:/Studium_KI_Programme/Photo_Projekt_Objekterkennung")
VENV_PATH = BASE_DIR / ".venv"
LABELME_PATH = VENV_PATH / "Scripts" / "labelme.exe"

# ================== HILFSFUNKTION ==================
def check_environment(path_to_check: Path):
    try:
        if path_to_check.exists() and path_to_check.is_dir():
            return True
        elif path_to_check.exists() and path_to_check.is_file():
            return True

    except FileNotFoundError as e:
        print(f"Pfad nicht gefunden__##__: {e}")

    except PermissionError as e:
        print(f"Berechtigungsfehler__##__: {e}")

    except OSError as e:
        print(f"OS Fehler__##__ {e}")

    except Exception as e:
        print(e)

def activate_environment(path_to_activate: Path, check: bool):
    try:
        if check:
            is_powershell = "PSVersion" in os.environ

            if is_powershell:
                activate_script = path_to_activate / "Scripts" / "Activate.ps1"
                command = f'& "{activate_script}"'
            else:
                activate_script = path_to_activate / "Scripts" / "Activate.bat"
                command = f'call "{activate_script}"'

            #Ausführen vom Kommand und Stausmeldung entgegennehmen
            status = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            if status.returncode != 0:
                print(f"Fehler beim Aktivieren der Umgebung")
            elif status.returncode == 0:
                print("#######__VENV-AKTIV__#######")

    except OSError as e:
        print(f"OS Fehler__##__ {e}")

# ================== MAIN ==================
def main():
    print("####__Starte Labeling-Prozess...__####")

    if not check_environment(BASE_DIR):
        print("XXXXXX_Projektverzeichnis Fehler: Umgebung nicht korrekt konfiguriert")
        sys.exit(1)

    if not check_environment(VENV_PATH):
        print("XXXXXX_Virtuelles Environment Fehler: Umgebung nicht korrekt konfiguriert")
        sys.exit(1)

    if not check_environment(LABELME_PATH):
        print("XXXXXX_Labelme-Fehler: Datei nicht gefunden")
        sys.exit(1)

    elif check_environment(VENV_PATH):
        activate_environment(VENV_PATH, check=True)

    try:
        os.chdir(BASE_DIR / "processed_data" / "images")
        subprocess.run([str(LABELME_PATH)], check=True)

    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()