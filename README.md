# Scooter Detection mit YOLOv8

**Projekt zur Erkennung von Scootern in Bildern mithilfe von YOLOv8 (Ultralytics).**
Dieses Repository enthält den vollständigen Code, Skripte und Dokumentation für die Objekterkennung im Rahmen des Moduls *Digitale Photogrammetrie und Bildverarbeitung* (BHT Berlin, Sommersemester 2026).

---

## Projektübersicht

### Ziel
Entwicklung eines YOLOv8-Modells zur Erkennung von Scootern in digitalen Bildern.
- **Modellleistung:** Precision 0.989, Recall 0.958, mAP@0.5 0.963 (Trainingslauf RUN_3-2).
- **Inferenzzeit:** 42.2 ms/Bild (NVIDIA GTX 1650, 4 GB VRAM).
- **Datengrundlage:** Selbst erstellter Datensatz mit positiven (Scooter) und negativen Beispielen (Hintergründe, ähnliche Objekte).

---

## Repository-Struktur

| Ordner/Datei | Beschreibung |
|--------------|--------------|
| `raw_data/` | Rohdaten (muss manuell strukturiert werden, siehe [Datenvorbereitung](#datenvorbereitung)) |
| `processed_data/` | Verarbeitete Bilder (Train/Val/Test) + YOLO-Labels |
| `runs/detect/` | Trainierte Modelle (z. B. `RUN_3-2/weights/best.pt`) |
| `scripts/` | Skripte zur Datenaufbereitung und Modellierung |
| `yolov8-custom.yaml` | Modellkonfiguration (1 Klasse: "scooter") |
| `requirements.txt` | Python-Abhängigkeiten |
| `.gitignore` | Ausgeschlossene Dateien (z. B. `.venv/`) |

---

## Voraussetzungen

- **Python 3.10+**
- **NVIDIA GPU mit CUDA-Unterstützung** (empfohlen, getestet mit GTX 1650)
- **Abhängigkeiten:** Installieren mit `pip install -r requirements.txt`

---

## Datenvorbereitung

### Manuell anzulegende Ordnerstruktur für `raw_data/`

Damit die Skripte `rename_files.py` und `prepare_data.py` korrekt funktionieren, muss der Ordner `raw_data/` vor der Ausführung der Skripte manuell mit folgender Struktur angelegt werden:

```text
raw_data/
├── full_views/          # Bilder MIT Scootern (positive Beispiele)
└── negatives/           # Bilder OHNE Scooter (negative Beispiele)
    ├── edge/            # Randbereiche von Objekten (optional, kann leer bleiben)
    ├── other/           # Diverse Umgebungen (Wald, Wiesen, etc.)
    ├── similar/         # Ähnliche Objekte (Fahrräder, Motorräder, Autos)
    └── street/          # Straßen/Gewege (typische Scooter-Umgebung)
```



Sollen dem Trainingsdatensatz neue Bilder hinzugefügt werden, müssen die Bilder in die jeweilige Kategorie eingeordnet werden. Die Umbenennung der Bilder erfolgt dann mittels Skript.

---

## Datenverarbeitungspipeline

Die Datenaufbereitung erfolgt durch eine modulare Pipeline, die aus vier Skripten besteht:

1. **`rename_files.py`** – Benennt Dateien nach dem Schema `<Kategorie>_<Index>.jpg` um.
2. **`prepare_data.py`** – Teilt die Bilder in Trainings-, Validierungs- und Testsets auf (70%/20%/10%).
3. **`create_bounding_box.py`** – Startet LabelMe für die manuelle Annotation der Scooter.
4. **`convert_in_yolo.py`** – Konvertiert LabelMe-Annotationsdateien in das YOLO-Format.

Die Pipeline kann zentral über `run_pipeline.py` gesteuert werden.

---
## Modelltraining

Das Training erfolgt mit dem Skript `run_training.py`. Wichtige Parameter für RUN_3-2:
- 120 Epochen
- Bildgröße: 640×640
- Batch-Größe: 16
- Optimierer: AdamW
- Daten-Augmentierung: Mosaic, Mixup, Rotation, Spiegeln, etc.

---
## Modellvalidierung

Das Skript `validate_model.py` ermöglicht die Auswahl eines trainierten Modells und gibt die Validierungsmetriken aus:
- mAP@0.5
- Precision
- Recall
- Modellzusammenfassung

---
## Testen des Modells

Mit `test_model.py` können trainierte Modelle auf neuen Bildern getestet werden. Wichtige Parameter:
- `imgsz`: Maximale Kantenlänge (z. B. 1024)
- `conf`: Confidence-Schwelle (0.0–1.0)

---
## Ergebnisse

Das beste Modell (RUN_3-2) erreichte:
- Precision: 0.989
- Recall: 0.958
- mAP@0.5: 0.963
- Inferenzzeit: 42.2 ms/Bild

---
**Autor:** Laurenz Hieber
