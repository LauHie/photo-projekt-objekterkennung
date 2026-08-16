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

# ================== KONFIGURATION ==================
SCRIPTS_DIR = Path(__file__).parent
BASE_DIR = SCRIPTS_DIR.parent

def starte_script(skript_name):
    subprocess.run(["python", str(BASE_DIR / "scripts" / "run_pipeline.py"),])






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
