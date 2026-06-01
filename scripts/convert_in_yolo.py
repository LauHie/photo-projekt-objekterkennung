"""
---------------
Konvertierung von Json in die txt für yolo

Format in der yolo: class_id center_x center_y width height
---------------
"""

import json
import os
from pathlib import Path

sub_dirs = [
    "train/scooter",
    "test/scooter",
    "val/scooter"
]

# Nur eine Klasse
class_to_id = {"scooter": 0}

# Basis-Ordner für die Daten
base_data_dir = "C:/Studium_KI_Programme/Photo_Projekt_Objekterkennung/processed_data/images"
base_lables_dir = "C:/Studium_KI_Programme/Photo_Projekt_Objekterkennung/processed_data/lables"

print("🚀 Starte Konvertierung von JSON zu YOLO-Format...")

# Überprüfe, ob die Labels-Ordner existieren
for subdir in sub_dirs:
    json_dir = Path(base_data_dir, subdir)
    print(f"Dateien aus {subdir.upper()} werden konvertiert")

    if not json_dir.exists():
        print(f"❌ Fehler: Verzeichnis nicht gefunden: {json_dir}")

def convert_in_yolo(json_file):
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
                        yolo_sting = f"{class_to_id[label]} {x_center:.8f} {y_center:.8f} {width_box:.8f} {height_box:.8f}"
                        print(f"Bild: {name}\nYOLO Format: {yolo_sting}")

                    return yolo_sting

    except FileNotFoundError:
        print("Datei nicht gefunden.")
    except json.decoder.JSONDecodeError:
        print("Datei nicht gefunden.")
    except Exception as e:
        print(e)

for subdir in sub_dirs:
    json_dir = Path(base_data_dir, subdir)
    print(f"Aktuelles Verzeichnis: {json_dir}")
    for json_file in json_dir.glob("*.json"):
        convert_in_yolo(json_file)