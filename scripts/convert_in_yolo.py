"""
---------------
Konvertierung von Json in die .txt für yolo

Format in der label-Datei für YOLO: class_id, center_x, center_y, width, height
---------------
"""

import json
import os
from pathlib import Path
import sys

# ================== KONFIGURATION ==================
sys.stdout.reconfigure(encoding='utf-8')
YELLOW = "\033[33m"
RESET = "\033[0m"
RED = "\033[31m"

SUBFOLDER_PATH = [
    "train/scooter",
    "test/scooter",
    "val/scooter"
]

# Nur eine Klasse
CLASS_TO_ID = {"scooter": 0}

# Basis-Ordner für die Daten
BASE_DATA_DIR = Path(__file__).parent.parent / "processed_data" / "images"
BASE_LABELS_DIR = Path(__file__).parent.parent / "processed_data" / "labels"

# ================== FUNKTIONEN ==================
def list_folder(sub_dirs,base_dir):
    for sub_dir in sub_dirs:
        json_dir = Path(base_dir, sub_dir)
        print(f"\U0001F4C4 Dateien aus {sub_dir.upper()} werden konvertiert")

        if not json_dir.exists():
            print(f"####_Fehler: Verzeichnis nicht gefunden: {json_dir}")

def convert_in_yolo(json_file, class_to_id: dict[str, int]):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            daten = json.load(file)
            if isinstance(daten, dict):
                if "imagePath" in daten:
                    name = daten["imagePath"]
                if "shapes" in daten:
                    shapes = daten["shapes"]
                    shapes_dict = shapes[0]
                    if "points" in shapes_dict:
                        points = shapes_dict["points"]

                        x_min = points[0][0]
                        y_min = points[0][1]
                        x_max = points[1][0]
                        y_max = points[1][1]

                        image_height = daten.get("imageHeight")
                        image_width = daten.get("imageWidth")

                        x_center = (x_min + x_max) / 2 / image_width
                        y_center = (y_min + y_max) / 2 / image_height
                        width_box = (x_max - x_min) / image_width
                        height_box = (y_max - y_min) / image_height

                    if "label" in shapes_dict:
                        label = shapes_dict["label"]
                        yolo_string = f"{class_to_id[label]} {x_center:.8f} {y_center:.8f} {width_box:.8f} {height_box:.8f}"

                        return name, yolo_string

    except FileNotFoundError:
        print("Datei nicht gefunden.")
    except json.decoder.JSONDecodeError:
        print("Datei nicht gefunden.")
    except Exception as e:
        print(e)

def save_yolo_string(name_string, lable_string, base_dir, sub_dir):
    name = name_string.split('.')[0] + '.txt'
    full_path = Path(base_dir) / sub_dir / name
    if full_path.exists() and full_path.exists():
        print(YELLOW + f"Label-txt: {name} bereits vorhanden\n" + RESET)
    else:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(lable_string)
        print(RED + "Speichere .txt\n" + RESET)

# ================== MAIN ==================
if __name__ == "__main__":
    print(RED + "\U0001F4C1 \U000027A1 \U0001F4D1 Starte Konvertierung von JSON zu YOLO-Format..." + RESET)

    # Auflisten der Verzeichnisse
    list_folder(SUBFOLDER_PATH,BASE_DATA_DIR)

    # Konvertieren der .json zu yolo .txt so wie speichern der .txt im richtigen Verzeichnis.
    for subdir in SUBFOLDER_PATH:
        json_path = Path(BASE_DATA_DIR, subdir)
        print(YELLOW + f"\n\U0001F4C1\U0001F4C1\U0001F4C1 Aktuelles Verzeichnis: {json_path}"+ RESET)
        for json_file in json_path.glob("*.json"):
            file_name, label = convert_in_yolo(json_file,CLASS_TO_ID)
            print(f"Bild: {file_name}\nYOLO Format: {label}")
            try:
                save_yolo_string(file_name, label, BASE_LABELS_DIR, subdir)

            except Exception as e:
                print(f'####_Fehler beim Speichern der Datei: {json_file} mit {e}')

    print("\n" + RED + ">>> " + "\033[1m" +
          "KONVERTIERUNG ABGESCHLOSSEN" +
          "\033[0m" + RESET + "\n")
