import os
import shutil
from pathlib import Path
import random

# ================== ORDNERPFADE ==================
RAW_DATA = "C:/Studium_KI_Programme/Photo_Projekt_Objekterkennung/raw_data"
PROCESSED_DATA = "C:/Studium_KI_Programme/Photo_Projekt_Objekterkennung/processed_data/images"

# Verhältnis: 70% train, 20% val, 10% test
SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.2,
    "test": 0.1
}


# ================== FUNCTIONS ==================
def get_image_files_by_category(raw_path):
    """Erhalte alle Bilddateien aus den negativen Unterordnern getrennt nach Kategorien"""
    image_files_by_category = {
        "edge": [],
        "other": [],
        "similar": [],
        "street": []
    }

    # Durchsuche die negativen Unterordner
    for category, files_list in image_files_by_category.items():
        subdir_path = Path(raw_path) / "negatives" / category
        if subdir_path.exists():
            for file in subdir_path.iterdir():
                if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    files_list.append(file)

    return image_files_by_category


def get_full_view_files(raw_path):
    """Erhalte alle Bilddateien aus dem full_views Ordner"""
    full_views_path = Path(raw_path) / "full_views"
    image_files = []

    if full_views_path.exists():
        for file in full_views_path.iterdir():
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                image_files.append(file)

    return image_files


def split_files_by_category(files_by_category, ratios):
    """Teile Dateien entsprechend den Verhältnissen pro Kategorie"""
    split_files_by_category = {}

    for category, files in files_by_category.items():
        # Zufällige Reihenfolge
        random.shuffle(files)

        total_count = len(files)
        train_count = int(total_count * ratios["train"])
        val_count = int(total_count * ratios["val"])

        # Teile die Dateien
        train_files = files[:train_count]
        val_files = files[train_count:train_count + val_count]
        test_files = files[train_count + val_count:]

        split_files_by_category[category] = {
            "train": train_files,
            "val": val_files,
            "test": test_files
        }

    return split_files_by_category


def split_full_view_files(files, ratios):
    """Teile full_views Dateien entsprechend den Verhältnissen"""
    # Zufällige Reihenfolge
    random.shuffle(files)

    total_count = len(files)
    train_count = int(total_count * ratios["train"])
    val_count = int(total_count * ratios["val"])

    # Teile die Dateien
    train_files = files[:train_count]
    val_files = files[train_count:train_count + val_count]
    test_files = files[train_count + val_count:]

    return train_files, val_files, test_files


def copy_files_to_destination(files, destination_path):
    """Kopiere Dateien in das Zielverzeichnis"""
    for file in files:
        try:
            # Kopiere die Datei
            shutil.copy2(file, destination_path)
            print(f"Kopiert: {file.name}")
        except Exception as e:
            print(f"Fehler beim Kopieren von {file.name}: {e}")

def cleanup_raw_data():
    """
    Prüft, ob alle Bilder aus raw_data in processed_data liegen.
    Falls ja, werden sie aus raw_data gelöscht.
    """
    print("\nPrüfe, ob Bilder aus raw_data in processed_data liegen...")

    # Liste aller Bilder in raw_data
    raw_images = []

    # Durchsuche full_views
    full_views_path = Path(RAW_DATA) / "full_views"
    if full_views_path.exists():
        for file in full_views_path.iterdir():
            if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                raw_images.append(file)

    # Durchsuche negatives
    negatives_path = Path(RAW_DATA) / "negatives"
    if negatives_path.exists():
        for category in negatives_path.iterdir():
            if category.is_dir():
                for file in category.iterdir():
                    if file.is_file() and file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        raw_images.append(file)

    # Prüfe für jedes Bild in raw_data, ob es in processed_data existiert
    deleted_count = 0
    for raw_image in raw_images:
        # Extrahiere den Dateinamen
        filename = raw_image.name

        # Durchsuche processed_data nach der Datei
        found_in_processed = False
        for root, dirs, files in os.walk(PROCESSED_DATA):
            if filename in files:
                found_in_processed = True
                break

        # Falls das Bild in processed_data gefunden wurde, lösche es aus raw_data
        if found_in_processed:
            try:
                os.remove(raw_image)
                print(f"Gelöscht: {raw_image}")
                deleted_count += 1
            except Exception as e:
                print(f"Fehler beim Löschen von {raw_image}: {e}")

    print(f"\n{deleted_count} Bilder aus raw_data gelöscht (da sie in processed_data liegen).")

def process_images():
    print("Suche nach Bilddateien...")

    # Hole alle negativen Bilder nach Kategorien
    negative_files_by_category = get_image_files_by_category(RAW_DATA)

    # Zeige Anzahl der Bilder pro Kategorie
    for category, files in negative_files_by_category.items():
        print(f"Gefunden: {len(files)} {category} Bilder")

    # Hole alle full_views Bilder
    full_view_files = get_full_view_files(RAW_DATA)
    print(f"Gefunden: {len(full_view_files)} full_views Bilder")

    # Teile negative Bilder nach Kategorien
    if any(negative_files_by_category.values()):
        print("Teile negative Bilder nach Kategorien...")
        split_negative_files = split_files_by_category(negative_files_by_category, SPLIT_RATIOS)

        # Kopiere negative Bilder in die entsprechenden Ordner
        for category, splits in split_negative_files.items():
            copy_files_to_destination(splits["train"], Path(PROCESSED_DATA) / "train" / "negatives" / category)
            copy_files_to_destination(splits["val"], Path(PROCESSED_DATA) / "val" / "negatives" / category)
            copy_files_to_destination(splits["test"], Path(PROCESSED_DATA) / "test" / "negatives" / category)

        # Zeige Zusammenfassung
        print("Negative Bilder verteilt:")
        for category, splits in split_negative_files.items():
            print(f"   {category}: Train={len(splits['train'])}, Val={len(splits['val'])}, Test={len(splits['test'])}")

    # Teile full_views Bilder
    if full_view_files:
        print("Teile full_views Bilder...")
        train_full, val_full, test_full = split_full_view_files(full_view_files, SPLIT_RATIOS)

        # Kopiere full_views Bilder in die entsprechenden Ordner
        copy_files_to_destination(train_full, Path(PROCESSED_DATA) / "train" / "scooter")
        copy_files_to_destination(val_full, Path(PROCESSED_DATA) / "val" / "scooter")
        copy_files_to_destination(test_full, Path(PROCESSED_DATA) / "test" / "scooter")

        print(f"Full_views Bilder verteilt: Train={len(train_full)}, Val={len(val_full)}, Test={len(test_full)}")


# ================== MAIN ==================
if __name__ == "__main__":
    print(" Starte Datenverarbeitung...")

    # Wenn Bilder vorhanden sind, verarbeite sie
    process_images()

    # Führe Cleanup aus: Lösche Bilder aus raw_data, die bereits in processed_data liegen
    cleanup_raw_data()

    print(" Datenverarbeitung abgeschlossen!")