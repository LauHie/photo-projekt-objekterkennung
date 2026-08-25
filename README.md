# Scooter Detection mit YOLOv8

**Projekt zur Erkennung von Scootern in Bildern mithilfe von YOLOv8 (Ultralytics).**
Dieses Repository enthält den vollständigen Code, trainierte Modelle und Tools zur **Datenverarbeitung, Annotation und Objekterkennung** für das Projekt im Modul *Digitale Photogrammetrie und Bildverarbeitung* (BHT Berlin).

---

## Projektübersicht

### **Ziel**
Entwicklung eines **robusten YOLOv8-Modells** zur Erkennung von Scootern in digitalen Bildern.
- **Datengrundlage:** Selbst erstellter Datensatz mit positiven (Scooter) und negativen Beispielen (Hintergründe, ähnliche Objekte).
- **Modellleistung:** Precision **0.989**, Recall **0.958**, mAP@0.5 **0.963** (Trainingslauf `RUN_3-2`).
- **Inferenzzeit:** **42.2 ms/Bild** (NVIDIA GTX 1650, 4 GB VRAM).

---

## Repository-Struktur

| Ordner/Datei | Beschreibung |
|--------------|--------------|
| `raw_data/` | **Rohdaten** (muss manuell strukturiert werden, siehe unten|
| `processed_data/` | Verarbeitete Bilder (Train/Val/Test) + YOLO-Labels |
| `runs/detect/` | Trainierte Modelle (z. B. `RUN_3-2/weights/best.pt`) |
| `scripts/` | Skripte zur Datenaufbereitung (`rename_files.py`, `prepare_data.py`, etc.) |
| `yolov8-custom.yaml` | Modellkonfiguration (1 Klasse: "scooter") |
| `requirements.txt` | Python-Abhängigkeiten (Ultralytics, LabelMe, etc.) |
| `.gitignore` | Ausgeschlossene Dateien (z. B. `.venv/`) |

---

## Wichtige Hinweise

### **1. Große Dateien**
- Das Repository enthält **Bilddaten** (`raw_data/`, `processed_data/`) größer etwa 1.6 GB.
- **Empfehlung:** Falls der Download zu lange dauert, können Sie die Ordner nach dem Klonen löschen und nur den Code behalten.

---

### **Manuell anzulegende Ordnerstruktur für `raw_data/`**

Damit die Skripte **`rename_files.py`** und **`prepare_data.py`** korrekt funktionieren, **muss** der Ordner `raw_data/` **vor der Ausführung der Skripte** manuell mit folgender Struktur angelegt werden:
Sollen dem Trainingsdatensatz neue Bilder hinzugefügt werden, so müssen die Bilder in die jeweilige Kategorie eingeordnet werden. Die Umbennennung der Bilder erfolgt dann mittels Script.

raw_data/
├── full_views/          # Bilder MIT Scootern (positive Beispiele)
└── negatives/           # Bilder OHNE Scooter (negative Beispiele)
    ├── edge/           # Randbereiche von Objekten (optional, leer lassen)
    ├── other/          # Diverse Umgebungen (Wald, Wiesen, etc.)
    ├── similar/        # Ähnliche Objekte (Fahrräder, Motorräder, Autos)
    └── street/         # Straßen/Gewege (typische Scooter-Umgebung)
