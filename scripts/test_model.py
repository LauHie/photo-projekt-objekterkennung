"""
YOLOv8 Scooter Detection Test Script

ZWECK:
Dieses Skript ermöglicht das interaktive Testen eines trainierten YOLOv8-Modells
auf neuen Bildern. Es ist speziell für die Erkennung von Scootern optimiert und
bietet eine benutzerfreundliche Oberfläche zur Anpassung von Inferenz-Parametern.

VORAUSSETZUNGEN:
- PyTorch mit CUDA-Unterstützung (für GPU-Beschleunigung)
- Ultralytics YOLOv8 (`pip install ultralytics`)
- OpenCV (`pip install opencv-python`)
- Matplotlib (`pip install matplotlib`)
- Vorhandene Dateien:
  - Trainiertes Modell in `runs/detect/<RUN_NAME>/weights/best.pt`
  - Testbilder in `processed_data/images/test/scooter/` (Format: `scooter_XXX.jpg`)

FUNKTIONSWEISE:
1. **Modellauswahl:**
   - Listet alle verfügbaren Trainingsläufe in `runs/detect/` auf.
   - Lädt das ausgewählte Modell (`best.pt`).

2. **Bildauswahl:**
   - Zeigt alle verfügbaren Testbilder in `processed_data/images/test/scooter/` an.
   - Lädt das ausgewählte Bild (erwartet Format: `scooter_XXX.jpg`).

3. **Inferenz-Parameter:**
   - **max_side:** Maximale Kantenlänge (z. B. 1024, 1280) für Letterbox-Resizing.
     - Erhält das Seitenverhältnis des Originalbilds.
     - Größere Werte verbessern die Erkennungsgenauigkeit, benötigen aber mehr VRAM.
   - **conf_thr:** Confidence-Schwelle (0.0–1.0).
     - Niedrigere Werte erhöhen die Empfindlichkeit (mehr Erkennungen, aber auch mehr False Positives).
     - Höhere Werte reduzieren False Positives (weniger Erkennungen, aber präziser).

4. **Inferenz & Visualisierung:**
   - Führt die Objekterkennung auf dem Bild durch.
   - Zeichnet Bounding-Boxes und Confidence-Werte direkt ins Bild.
   - Zeigt das Ergebnis mit Matplotlib an (vollständiges Bild, skaliert für die Anzeige).
   - Gibt detaillierte Infos zu jedem erkannten Objekt aus (Klasse, Confidence, Box-Koordinaten).

5. **Interaktive Wiederholung:**
   - Ermöglicht das Testen weiterer Bilder ohne Neustart des Skripts.

AUSGABE:
- Konsolenausgabe mit:
  - Anzahl der erkannten Objekte.
  - Details zu jedem Objekt (Klasse, Confidence, Bounding-Box-Koordinaten, Größe).
  - Tipps zur Parameteranpassung, falls keine Objekte erkannt werden.
- Grafische Anzeige des Bildes mit:
  - Grüne Bounding-Boxes um erkannte Scooter.
  - Beschriftung mit Klassenname und Confidence-Wert.

HINWEISE:
- **Für große Bilder (z. B. 2000×3000):**
  - Verwende `max_side=1024` oder `1280` für bessere Erkennung kleiner Scooter.
  - Höhere Werte erhöhen den VRAM-Verbrauch.
- **Bei Doppeldetektionen:**
  - Erhöhe die `conf_thr` (z. B. auf 0.5–0.7), um schwache Erkennungen zu filtern.
- **Bei fehlenden Erkennungen:**
  - Reduziere die `conf_thr` (z. B. auf 0.1–0.2).
  - Erhöhe `max_side` (z. B. auf 1280).

BEISPIEL:
    python test_model.py
    # 1. Wähle Modell (z. B. RUN_3)
    # 2. Wähle Bild (z. B. scooter_618.jpg)
    # 3. Passe Parameter an (z. B. max_side=1024, conf_thr=0.5)
    # 4. Betrachte die Erkennungen im Matplotlib-Fenster
"""

from pathlib import Path
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# ================== FUNKTIONEN ==================
def print_section(title: str) -> None:
    """Formatiert und druckt eine Überschrift."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def get_user_input(
    prompt: str,
    default,
    input_type=float,
    min_val=None,
    max_val=None,
) -> float:
    """Fragt den Nutzer nach einem Wert und prüft die Grenzen."""
    while True:
        try:
            user_input = input(f"{prompt} (Standard: {default}): ").strip()
            if not user_input:
                return default
            value = input_type(user_input)
            if min_val is not None and value < min_val:
                print(f"Wert muss mindestens {min_val} sein.")
                continue
            if max_val is not None and value > max_val:
                print(f"Wert darf maximal {max_val} sein.")
                continue
            return value
        except ValueError:
            print("Ungültige Eingabe – bitte eine Zahl eingeben.")


# ================== MAIN ==================
def main() -> None:
    # ================== 1. MODELL AUSWÄHLEN ==================
    RUN_DIR = Path(__file__).parent.parent / "runs" / "detect"
    folders = [
        f.name
        for f in RUN_DIR.iterdir()
        if f.is_dir() and not f.name.startswith("val")
    ]

    print_section("VERFÜGBARE MODELLE")
    for i, folder in enumerate(folders, 1):
        print(f"{i}. {folder}")

    choice = input("\nNummer des Modells eingeben (oder Name): ").strip()
    try:
        run_name = folders[int(choice) - 1]
    except (ValueError, IndexError):
        run_name = choice

    model_path = RUN_DIR / run_name / "weights" / "best.pt"
    if not model_path.exists():
        print(f"Modell nicht gefunden: {model_path}")
        exit()

    print(f"\n Modell geladen: {model_path}")
    model = YOLO(str(model_path))

    # ================== 2. TESTBILD AUSWÄHLEN ==================
    print_section("TESTBILD AUSWÄHLEN")
    test_dir = Path(__file__).parent.parent / "processed_data/images/test/scooter"
    test_images = sorted(test_dir.glob("scooter_*.jpg"))

    if not test_images:
        print("Keine Testbilder gefunden in 'processed_data/images/test/scooter/'")
        print("Bitte Bilder im Format 'scooter_XXX.jpg' (z.B. scooter_001.jpg) hinzufügen.")
        exit()

    print("\nVerfügbare Testbilder:")
    for i, img_path in enumerate(test_images, 1):
        print(f"{i}. {img_path.name}")

    img_number = input("\n3‑stellige Nummer des Bildes eingeben (z.B. 618 für scooter_618.jpg): ").strip()
    if not img_number.isdigit() or len(img_number) != 3:
        print("Ungültige Eingabe – bitte eine 3‑stellige Zahl eingeben.")
        exit()

    test_img_path = test_dir / f"scooter_{img_number}.jpg"
    if not test_img_path.exists():
        print(f"Bild 'scooter_{img_number}.jpg' nicht gefunden.")
        exit()

    print(f"\nTestbild: {test_img_path.name}")

    # ================== 3. ORIGINALBILD LADEN ==================
    print_section("BILD LADEN")
    img_bgr = cv2.imread(str(test_img_path))
    if img_bgr is None:
        print("Bild konnte nicht geladen werden.")
        exit()

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    height, width = img_rgb.shape[:2]
    print(f"Originalgröße: {width}×{height}")

    # ================== 4. INFERENZ‑PARAMETER ==================
    print_section("INFERENZ‑PARAMETER")

    # Maximale Kantenlänge – wird intern letterboxed
    max_side = get_user_input(
        "Maximale Kantenlänge (z.B. 1024, 1280)",
        default=1024,
        input_type=int,
        min_val=320,
        max_val=2048,
    )

    # Confidence‑Schwelle
    conf_thr = get_user_input(
        "Confidence‑Schwelle (0.0–1.0)",
        default=0.2,
        input_type=float,
        min_val=0.0,
        max_val=1.0,
    )

    print(f"\nVerwendete Parameter → max_side={max_side}, confidence={conf_thr}")

    # ================== 5. INFERENZ DURCHFÜHREN ==================
    print_section("INFERENZ‑ERGEBNISSE")

    results = model(
        test_img_path,
        conf=conf_thr,
        imgsz=max_side,   # ← nur die maximale Kante, Seitenverhältnis bleibt erhalten
        verbose=False,
    )

    # --------------------------------------------------------------
    # Ergebnis auswerten und Bounding‑Boxes auf das Original‑Bild malen
    # --------------------------------------------------------------
    for result in results:
        n_obj = len(result.boxes)
        print(f"\nErkannte Objekte (conf={conf_thr}, max_side={max_side}): {n_obj}")

        if n_obj == 0:
            print("  Keine Scooter erkannt.")
            print("  Tipps:")
            print(f"    - Versuche eine niedrigere Confidence‑Schwelle (z.B. {max(0.0, conf_thr-0.1):.1f}).")
            print(f"    - Erhöhe die maximale Kantenlänge (z.B. {min(2048, max_side+320)}).")
            continue

        # Bounding‑Boxes einzeichnen
        for i, box in enumerate(result.boxes):
            class_id = int(box.cls)                     # Klassen‑ID hier immer 0
            class_name = model.names[class_id]           # Klassen‑Name („scooter“)
            confidence = box.conf.item()                 # Confidence‑Wert
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            print(f"  Objekt {i+1}:")
            print(f"    Klasse: {class_name} (ID: {class_id})")
            print(f"    Confidence: {confidence:.2f}")
            print(f"    Bounding Box: ({x1}, {y1}) → ({x2}, {y2})")
            print(f"    Breite: {x2-x1}px, Höhe: {y2-y1}px")

            # Box und Label ins Bild malen
            cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), thickness=6, lineType=cv2.LINE_AA)
            cv2.putText(
                img_rgb,
                f"{class_name} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # ================== 6. BILD MIT MATPLOTLIB ANZEIGEN ==================
    print_section("BILD ANZEIGEN (Matplotlib)")

    # Ändern nur die Anzeige‑Größe, nicht die eigentlichen Pixel.
    max_display_dim = 1200  # maximale Breite/Höhe in Pixel für das Fenster
    scale_disp = min(max_display_dim / width, max_display_dim / height, 1.0)
    disp_w, disp_h = int(width * scale_disp), int(height * scale_disp)

    plt.figure(figsize=(disp_w / 100, disp_h / 100))
    plt.imshow(img_rgb)
    plt.axis("off")
    plt.title(f"Ergebnisse für {test_img_path.name}\n"
              f"Confidence={conf_thr}, max_side={max_side}")
    plt.tight_layout()
    plt.show()

    # ================== 7. WEITERE TESTS ==================
    print_section("WEITERE OPTIONEN")
    again = input("\nMöchtest du ein weiteres Bild testen? (j/n): ").strip().lower()
    if again == "j":
        main()
    else:
        print("\nProgramm beendet.")


if __name__ == "__main__":
    main()