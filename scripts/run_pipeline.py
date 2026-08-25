"""
YOLO Data Processing Pipeline Controller

ZWECK:
Dieses Hauptskript steuert die **komplette Datenverarbeitungspipeline** für die
YOLOv8-Objekterkennung. Es führt alle notwendigen Vorverarbeitungsschritte **automatisiert
und in der richtigen Reihenfolge** aus, um Rohdaten in ein für YOLOv8 trainierbares
Format zu konvertieren.

VORAUSSETZUNGEN:
- Python 3.8+
- Alle Skripte in `scripts/` müssen vorhanden sein:
  - `rename_files.py`
  - `prepare_data.py`
  - `create_bounding_box.py`
  - `convert_in_yolo.py`
- LabelMe muss installiert sein (`pip install labelme`)
- Die Ordnerstruktur für `raw_data/` muss manuell angelegt sein (siehe README)

FUNKTIONSWEISE:
1. **rename_files.py:**
   - Benennt alle Bilder in `raw_data/` nach einem einheitlichen Schema um
   - Format: `<Kategorie>_<Index>.jpg` (z. B. `scooter_001.jpg`, `street_001.jpg`)
   - Verhindert Duplikate und stellt Konsistenz sicher

2. **prepare_data.py:**
   - Teilt die Bilder in Trainings-, Validierungs- und Testsets auf (70%/20%/10%)
   - Nutzt die Ordnerstruktur:
     ```
     processed_data/
     ├── images/
     │   ├── train/
     │   │   ├── negatives/
     │   │   │   ├── edge/
     │   │   │   ├── other/
     │   │   │   ├── similar/
     │   │   │   └── street/
     │   │   └── scooter/
     │   ├── val/
     │   └── test/
     └── labels/ (wird später von convert_in_yolo.py gefüllt)
     ```
   - Kopiert die Bilder in die entsprechenden Ordner

3. **create_bounding_box.py:**
   - Startet LabelMe für die **manuelle Annotation** der Scooter in den Trainings- und Validierungsbildern
   - Speichert die Annotationen als JSON-Dateien im selben Ordner wie die Bilder
   - Wichtig: Nur Bilder in `processed_data/images/{train,val}/scooter/` müssen annotiert werden

4. **convert_in_yolo.py:**
   - Konvertiert die LabelMe-JSON-Dateien in das **YOLO-Format** (`.txt`-Dateien)
   - Format: `0 <x_center> <y_center> <width> <height>` (Klassen-ID 0 für "scooter")
   - Speichert die Dateien in `processed_data/labels/{train,val,test}/`

AUSGABE:
- Vollständig vorbereiteter Datensatz in `processed_data/`:
  - Bilder in der richtigen Ordnerstruktur
  - YOLO-kompatible Label-Dateien
  - `data.yaml` mit Pfaden zu Train/Val/Test (wird von prepare_data.py erstellt)

HINWEISE:
- **Manuelle Schritte:**
  - Die Ordnerstruktur in `raw_data/` muss **vor Ausführung** manuell angelegt werden
  - Die Annotation mit LabelMe in Schritt 3 erfordert **manuelles Eingreifen**
- **Fehlerbehandlung:**
  - Bei Fehlern in einem Skript kann der Benutzer wählen, ob die Pipeline abgebrochen
    oder fortgesetzt werden soll
- **Abhängigkeiten:**
  - Alle Skripte müssen im selben Verzeichnis liegen
  - LabelMe muss für die Annotation installiert sein

BEISPIEL:
    python run_pipeline.py
    # 1. Führt rename_files.py aus
    # 2. Führt prepare_data.py aus
    # 3. Startet LabelMe für die Annotation (manueller Schritt)
    # 4. Führt convert_in_yolo.py aus
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
    ("prepare_data.py", "Datenstruktur vorbereiten (train/val/test)"),
    ("create_bounding_box.py", "Bounding Boxes erstellen (mit labelme)"),
    ("convert_in_yolo.py", "Labels in YOLO-Format konvertieren")
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