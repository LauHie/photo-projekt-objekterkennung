from ultralytics import YOLO
from pathlib import Path
import torch

YELLOW = "\033[33m"
RESET = "\033[0m"
RED = "\033[31m"

# ================== KONFIGURATION ==================
def main():
    CUSTOM_MODEL_YAML = Path(r"C:\Studium_KI_Programme\Photo_Projekt_Objekterkennung\yolov8-custom.yaml")
    DATA_YAML = Path(r"C:\Studium_KI_Programme\Photo_Projekt_Objekterkennung\processed_data\data.yaml")
    RUN_NAME = 'RUN_1'

    # ================== CHECKS ==================
    if not CUSTOM_MODEL_YAML.is_file():
        raise FileNotFoundError(f"Custom model YAML fehlt: {CUSTOM_MODEL_YAML}")

    if not DATA_YAML.is_file():
        raise FileNotFoundError(f"Data YAML fehlt: {DATA_YAML}")

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA nicht verfügbar! Überprüfe die PyTorch-Installation.")

    print(YELLOW + f"GPU: {torch.cuda.get_device_name(0)}" + RESET)
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

    # ================== MODEL LADEN ==================
    model = YOLO(str(CUSTOM_MODEL_YAML))

    # ================== TRAINING ==================
    train_results = model.train(
        data=str(DATA_YAML),
        epochs=50,
        imgsz=640,
        batch=16,  # Batch-Größe (16 für 4 GB VRAM)
        device=0,  # GPU
        name=RUN_NAME,
        pretrained=False,
        half=False,  # Kein AMP (GTX 1650 unterstützt es nicht gut)

        lr0=0.001,  # Anfängliche Lernrate
        lrf=0.01,  # End-Lernrate
        momentum=0.9,  # Momentum
        weight_decay=0.0005,  # L2-Regularisierung
        optimizer="AdamW",  # Optimizer

        augment=True,  # Data Augmentation aktivieren
        degrees=10.0,  # Rotation
        translate=0.1,  # Verschiebung
        scale=0.5,  # Skalierung
        shear=2.0,  # Scherung
        perspective=0.001,  # Perspektive
        fliplr=0.5,  # Horizontales Spiegeln
        mosaic=1.0,  # Mosaic-Augmentation
        mixup=0.1,  # Mixup-Augmentation
        copy_paste=0.1,  # Copy-Paste-Augmentation

        cos_lr=True,  # Cosine LR Scheduler
        patience=50,  # Early Stopping nach 50 Epochs ohne Verbesserung

        box=7.5,  # Box-Loss-Gewicht
        cls=0.5,  # Klassen-Loss-Gewicht
        dfl=1.5,  # DFL-Loss-Gewicht
        iou=0.7,  # IoU-Schwelle

        fraction=1.0,  # Alle Bilder verwenden

        save=True,  # Modell speichern
        save_period=-1,  # Nach jeder Epoche speichern
        plots=True,  # Trainingsplots erstellen

        workers=2  # 2 Worker für Stabilität (4 GB VRAM)
    )

    best_weight_path = Path(f"runs/detect/{RUN_NAME}/weights/best.pt").resolve()
    print(YELLOW + "\n=== Training beendet ===" + RESET)
    print(f"Bestes Gewicht: {best_weight_path}")
    print(f"mAP@0.5: {train_results.box.map50}")
    print(f"mAP@0.5-0.95: {train_results.box.map}")
    print(RED + f"Precision: {train_results.box.p}" + RESET)
    print(f"Recall: {train_results.box.r}")

# ================== HAUPTPROGRAMM ==================
if __name__ == '__main__':
    main()