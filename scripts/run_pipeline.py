"""
Hauptskript zur Steuerung der YOLO-Datenverarbeitungspipeline.
Führt alle Skripte in der richtigen Reihenfolge aus:
1. rename_files.py       -> Benennt Dateien um
2. prepare_data.py       -> Bereitet die Datenstruktur vor
3. create_bounding_box.py -> Erstellt Bounding Boxes mit labelme
4. convert_in_yolo.py    -> Konvertiert Labels in YOLO-Format
"""

import subprocess
import sys
from pathlib import Path

# Farbcodes
YELLOW = "\033[33m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
MAGENTA = "\033[35m"

# ================== KONFIGURATION ==================
SCRIPTS_DIR = Path(__file__).parent  # Ordner, in dem dieses Skript liegt
BASE_DIR = SCRIPTS_DIR.parent        # Projekt-Root

# Liste der Skripte in der richtigen Reihenfolge
PIPELINE_SCRIPTS = [
    ("rename_files.py", "Umbenennen der Bilder"),
    ("prepare_data.py", "Datenstruktur vorbereiten (train/val/test)")

    # ("create_bounding_box.py", "Bounding Boxes erstellen (mit labelme)"),
    # ("convert_in_yolo.py", "Labels in YOLO-Format konvertieren")
]

# ================== FUNKTION ==================
def starte_script(skript_name: str) -> bool:
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
            check=False,
            stdout=None,   # Eingaben/Ausgaben an die Konsole weiterleiten
            stderr=None,   # Eingaben/Ausgaben an die Konsole weiterleiten
            text=True,
            encoding="utf-8",
        )

        # Prüfe den Exit-Code manuell
        if result.returncode != 0:
            print(RED + f"\nFehler in {skript_name}!" + RESET)
            return False
        else:
            print(GREEN + f"\n{skript_name} erfolgreich ausgeführt." + RESET)
            return True

    except Exception as e:
        print(RED + f"\nFehler: {e}" + RESET)
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
    ║   1. Dateien umbenennen                                                    
    ║   2. Datenstruktur vorbereiten (train/val/test)                           
    ║   3. Bounding Boxes erstellen (mit labelme)                               
    ║   4. Labels in YOLO-Format konvertieren                                    
    ║                                                                              
    """)

    print(YELLOW + f"Projektverzeichnis: {BASE_DIR}" + RESET)
    print(YELLOW + f"Skriptverzeichnis:   {SCRIPTS_DIR}\n" + RESET)

    # Schleife für alle Skripte in der Pipeline
    for skript_name, description in PIPELINE_SCRIPTS:
        print(MAGENTA + f"\n############__{description}__############" + RESET)

        success = starte_script(skript_name)

        if not success:
            # Frage den Benutzer, ob die Pipeline abgebrochen oder fortgesetzt werden soll
            choice = input(
                RED + f"\nFehler in '{skript_name}'. Soll die Pipeline abgebrochen werden? [j/n]: " + RESET
            ).strip().lower()

            if choice == 'j':
                print(RED + "\nPipeline abgebrochen!" + RESET)
                sys.exit(1)
            else:
                print(YELLOW + "\nFahre mit dem nächsten Schritt fort..." + RESET)
                continue

        print(GREEN + f"\n############__{description} abgeschlossen!__############" + RESET)

    print(GREEN + "\nAlle Skripte erfolgreich ausgeführt! Pipeline abgeschlossen." + RESET)