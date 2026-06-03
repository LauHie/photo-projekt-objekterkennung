"""
Skript zum Starten von labelme für die Erstellung von Bounding Boxes

In PowerShell um Skripte in der .venv zu starten:   powershell -ExecutionPolicy Bypass
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
LABELME_PATH = VENV_PATH / "Scripts" / "labelme.exe"  # Windows-Pfad

# Ordner für Bilder und Labels
IMAGE_DIRS = {
    "train": BASE_DIR / "processed_data" / "images" / "train" / "scooter",
    "val": BASE_DIR / "processed_data" / "images" / "val" / "scooter",
    "test": BASE_DIR / "processed_data" / "images" / "test" / "scooter"
}

# ================== HILFSFUNKTIONEN ==================
def check_environment():
    """
    Prüft, ob die virtuelle Umgebung und labelme existieren
    """
    # TODO: Implementierung
    pass

def get_images_to_label():
    """
    Sammelt alle Bilder, die noch keine JSON-Labels haben
    """
    # TODO: Implementierung
    pass

def start_labelme(image_path=None):
    """
    Startet labelme mit dem angegebenen Bild oder Ordner
    """
    # TODO: Implementierung
    pass

# ================== HAUPTPROGRAMM ==================
def main():
    """
    Hauptfunktion zum Starten des Labeling-Prozesses
    """
    print("🚀 Starte Labeling-Prozess...")

    # 1. Umgebung prüfen
    if not check_environment():
        print("❌ Fehler: Umgebung nicht korrekt konfiguriert")
        sys.exit(1)

    # 2. Bilder zum Labeln ermitteln
    images_to_label = get_images_to_label()

    if not images_to_label:
        print("✅ Alle Bilder sind bereits gelabelt!")
        return

    print(f"📷 {len(images_to_label)} Bilder zum Labeln gefunden")

    # 3. labelme starten
    # TODO: Entscheidung - einzelnes Bild oder ganzer Ordner?
    start_labelme()

    print("🎉 Labeling-Prozess gestartet!")

if __name__ == "__main__":
    main()