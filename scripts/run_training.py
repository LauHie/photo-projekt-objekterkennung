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
        epochs=100,
        imgsz=640,
        batch=16,
        device=0,   # 0 = GPU
        name=RUN_NAME,
        pretrained=False,
        half=False,
        workers=2  # Kann auf 0 gesetzt werden, falls Probleme bestehen
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