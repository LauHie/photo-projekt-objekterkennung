"""
YOLOv8 Model Validation and Evaluation Script

ZWECK:
Dieses Skript ermöglicht die Auswahl eines trainierten YOLOv8-Modells,
führt eine Validierung durch und gibt detaillierte Trainings- und
Evaluierungsmetriken aus. Es dient zur Bewertung der Modellleistung nach dem Training.

VORAUSSETZUNGEN:
- PyTorch mit CUDA-Unterstützung (für GPU-Beschleunigung)
- Ultralytics YOLOv8 (`pip install ultralytics`)
- PyYAML (`pip install pyyaml`)
- Vorhandene Trainingsläufe in `runs/detect/`
- `processed_data/data.yaml` mit Datensatz-Konfiguration

FUNKTIONSWEISE:
1. **Auswahl des Trainingslaufs:**
   - Listet alle verfügbaren Trainingsläufe in `runs/detect/` auf
   - Lädt den ausgewählten Run (entweder durch Nummer oder Namen)

2. **Anzeige der Trainingsparameter:**
   - Liest die Trainingskonfiguration aus `args.yaml`
   - Zeigt wichtige Parameter an:
     - Modellarchitektur
     - Datensatz
     - Anzahl Epochen
     - Batch-Größe
     - Bildgröße
     - Optimierer
     - Lernrate
     - Gerät (GPU/CPU)
     - Vortrainiert (True/False)

3. **Modellinformationen:**
   - Lädt das beste Modell (`best.pt`) aus dem ausgewählten Run
   - Zeigt eine Zusammenfassung der Modellarchitektur:
     - Anzahl der Layers
     - Anzahl der Parameter
     - GFLOPs (Berechnungsaufwand)
   - Zeigt die Modellgröße in MB an

4. **Validierungsmetriken:**
   - Führt eine Validierung auf dem Testdatensatz durch
   - Berechnet und zeigt folgende Metriken:
     - mAP@0.5 (Mean Average Precision bei IoU=0.5)
     - mAP@0.5-0.95 (Mean Average Precision über verschiedene IoU-Schwellen)
     - Precision (Genauigkeit der Erkennungen)
     - Recall (Vollständigkeit der Erkennungen)

5. **Klasseninformationen:**
   - Zeigt die Anzahl der Klassen und deren Namen an
   - Nützlich zur Überprüfung der Klassenkonfiguration

AUSGABE:
- Konsolenausgabe mit:
  - Trainingsparametern des ausgewählten Runs
  - Modellzusammenfassung (Layers, Parameter, GFLOPs)
  - Modellgröße in MB
  - Validierungsmetriken (mAP, Precision, Recall)
  - Klasseninformationen

HINWEISE:
- Die Validierung verwendet die in `processed_data/data.yaml` definierte
  Datensatzaufteilung (Train/Val/Test)
- Für eine vollständige Evaluation sollte der Datensatz repräsentativ sein
- Die Metriken werden auf dem Validierungs- oder Testset berechnet
- Bei großen Modellen kann die Validierung einige Zeit in Anspruch nehmen

BEISPIEL:
    python validate_model.py
    # 1. Wähle einen Trainingslauf aus (z. B. RUN_3)
    # 2. Das Skript zeigt Trainingsparameter, Modellinfo und Metriken an
"""

import yaml
from pathlib import Path
from ultralytics import YOLO
import torch
import numpy as np
from datetime import datetime
import cv2

# ================== KONFIGURATION ==================
RUN_DIR = Path(__file__).parent.parent / "runs" / "detect"

def print_section(title):
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)

if __name__ == "__main__":
    # ================== 1. TRAININGSLÄUFE AUSWÄHLEN ==================
    folders = [f.name for f in RUN_DIR.iterdir() if f.is_dir() and not f.name.startswith("val")]
    print_section("VERFÜGBARE TRAININGSLÄUFE")
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    choice = input("\nNummer des Runs eingeben (oder Name): ")
    try:
        run_name = folders[int(choice) - 1]
    except (ValueError, IndexError):
        run_name = choice

    run_path = RUN_DIR / run_name

    # ================== 2. TRAININGSPARAMETER ==================
    print_section("TRAININGSPARAMETER")
    args_path = run_path / "args.yaml"
    with open(args_path, "r") as f:
        args = yaml.safe_load(f)

    for key, value in args.items():
        if key in ['model', 'data', 'epochs', 'batch', 'imgsz', 'optimizer', 'lr0', 'device', 'pretrained']:
            print(f"{key:15}: {value}")

    # ================== 3. MODELLINFORMATIONEN ==================
    print_section("MODELLINFORMATIONEN")
    model = YOLO(f"{run_path}/weights/best.pt")
    print("\nModellzusammenfassung:")
    # Statt model.info direkt auszugeben, extrahieren wir die wichtigsten Infos
    model_summary = str(model.info)
    if "YOLOv8" in model_summary and "summary" in model_summary:
        # Extrahiere die Zusammenfassung (z.B. "73 layers, 11,125,971 parameters, 28.4 GFLOPs")
        summary_line = [line for line in model_summary.split('\n') if 'layers' in line and 'parameters' in line]
        if summary_line:
            print(summary_line[0])
    else:
        print(model_summary)  # Fallback, falls die Extraktion fehlschlägt

    model_size = Path(f"{run_path}/weights/best.pt").stat().st_size / (1024 * 1024)
    print(f"\nModellgröße: {model_size:.2f} MB")

    # ================== 4. VALIDIERUNGSMETRIKEN ==================
    print_section("VALIDIERUNGSMETRIKEN")
    metrics = model.val(data=Path(__file__).parent.parent / "processed_data/data.yaml", verbose=False)
    print(f"mAP@0.5:       {metrics.box.map50:.4f}")
    print(f"mAP@0.5-0.95:  {metrics.box.map:.4f}")
    print(f"Precision:     {metrics.box.p[0]:.4f}")
    print(f"Recall:        {metrics.box.r[0]:.4f}")

    # ================== 5. KLASSENINFORMATIONEN ==================
    print_section("KLASSENINFORMATIONEN")
    print(f"Anzahl Klassen: {len(metrics.names)}")
    for class_id, class_name in metrics.names.items():
        print(f"Klasse {class_id}: {class_name}")