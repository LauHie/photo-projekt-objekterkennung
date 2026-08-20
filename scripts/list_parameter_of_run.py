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