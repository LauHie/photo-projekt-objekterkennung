"""
Hauptskript zur Steuerung der YOLO-Datenverarbeitungspipeline, für die einfache Vorbereitung von Trainingsdaten.

Dieses Skript ruft alle anderen Skripte in der richtigen Reihenfolge auf:
1. rename_files.py       -> Benennt Dateien um
2. prepare_data.py       -> Bereitet die Datenstruktur vor
3. create_bounding_box.py -> Erstellt Bounding Boxes mit labelme
4. convert_in_yolo.py    -> Konvertiert Labels in YOLO-Format
"""

import subprocess
import sys
from pathlib import Path
import ultralytics
import os
import torch

YELLOW = "\033[33m"
RESET = "\033[0m"
RED = "\033[31m"

# ================== KONFIGURATION ==================
SCRIPTS_DIR = Path(__file__).parent # Ordner, in dem dieses Skript liegt
BASE_DIR = SCRIPTS_DIR.parent       # Projekt-Root (z. B. Photo_Projekt_Objekterkennung)

# ================== FUNKTION ==================
def starte_script(skript_name):
    """
        Führt ein Python-Skript aus der Pipeline aus.

        Returns:
            bool: True, wenn das Skript erfolgreich ausgeführt wurde, sonst False.
        """
    skript_path = SCRIPTS_DIR / skript_name
    if not skript_path.exists():
        print(RED + f"Skript nicht gefunden: {skript_path}" + RESET)
        return False

    print(YELLOW + f"\nStarte Skript: {skript_name} ..." + RESET)

    try:
        result = subprocess.run(
            ["python", str(skript_path)],
            stdout=None,
            stderr=None,
            text=True,
            encoding="utf-8",
        )
        return True

    except subprocess.CalledProcessError as e:
        print(RED + f"\nFehler: {e}")
        return False

    except Exception as e:
        print(RED + f"\nFehler: {e}")
        return False

# ================== MAIN ==================
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
    ║                                                                              
    ║   YOLO Objekterkennung - Datenverarbeitungspipeline                       
    ║                                                                              
    ║   Dieses Programm bereitet die Bilder für die Objekterkennung mit YOLO   
    ║   vor. Es führt folgende Schritte aus:                                      
    ║                                                                              
    ║   1.Dateien umbenennen                                      
    ║   2.Datenstruktur vorbereiten: Bilder nach dem gesetzten Verhältnis aufteilen (train/val/test)                           
    ║   3.Bounding Boxes erstellen (mit labelme)                               
    ║   4.Labels in YOLO-Format konvertieren                                                                                                
    ║                                                                              
    """)
    print(YELLOW + f"Projektverzeichnis: {BASE_DIR}" + RESET)
    print(YELLOW + f"Skriptverzeichnis:   {SCRIPTS_DIR}\n" + RESET)

    print(YELLOW + '\n############__Umbenennen der Bilder__############' + RESET)
    success = starte_script('rename_files.py')
    if not success:
        print(RED + f"\n Pipeline abgebrochen!" + RESET)
        sys.exit(1)
