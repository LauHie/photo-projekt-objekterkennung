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

# ================== KONFIGURATION ==================
SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent

def starte_script():
    pass



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
    print(BASE_DIR)
    print(SCRIPTS_DIR)

    # Pfad zur yolov8n.yaml-Datei
    # Korrekter Pfad zur yolov8n.yaml (YOLOv8)
    yaml_path = os.path.join(os.path.dirname(ultralytics.__file__), "cfg", "models", "v8", "yolov8n.yaml")
    print(f"Pfad zur yolov8n.yaml: {yaml_path}")

    # Überprüfe, ob die Datei existiert
    if os.path.exists(yaml_path):
        print("✅ Datei gefunden!")
    else:
        print("❌ Datei nicht gefunden. Suche in anderen Verzeichnissen...")
        # Alternative Pfade prüfen
        alternative_paths = [
            os.path.join(os.path.dirname(ultralytics.__file__), "cfg", "models", "yolov8n.yaml"),
            os.path.join(os.path.dirname(ultralytics.__file__), "models", "v8", "yolov8n.yaml"),
            os.path.join(os.path.dirname(ultralytics.__file__), "models", "yolov8n.yaml"),
        ]
        for path in alternative_paths:
            if os.path.exists(path):
                print(f"✅ Alternative Datei gefunden unter: {path}")
                yaml_path = path
                break