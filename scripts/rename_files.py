"""
Skript zum Umbenennen der Bilder im raw_data Ordner um so einheitliche Bezeichnungen zu erhalten
"""
import os
from pathlib import Path
import sys

# ================== ORDNERPFAD ==================
FOLDER_PATH_FullVIEWS = Path(__file__).parent.parent / "raw_data" / "full_views"
FOLDER_PATH_NEGATIVES = Path(__file__).parent.parent / "raw_data" / "negatives"


# ================== FUNKTIONEN ==================
def get_lastcount(name_class):
    subfolder_path = r'C:\Studium_KI_Programme\Photo_Projekt_Objekterkennung\processed_data\images'
    max_count = -1  # Falls keine passenden Dateien gefunden werden

    for root, dirs, files in os.walk(subfolder_path):
        for file in files:
            # Prüfe, ob die Datei mit name_class_ beginnt und auf .jpg endet
            if file.startswith(name_class + '_') and file.endswith('.jpg'):
                # Extrahiere den Teil nach dem Unterstrich (ohne .jpg)
                count_part = file[len(name_class) + 1 : -4]  # -4, um ".jpg" zu entfernen
                if count_part.isdigit():  # Prüfe, ob es sich um eine Zahl handelt
                    count = int(count_part)
                    if count > max_count:
                        max_count = count

    return max_count

def define_sub_folder():

    """
    Parameter:
    Kategorien = [edge, other, similar, street] 
    :return: Name der Kategorie, Bild-Count Startpunkt
    """
    name = input("Kategorie eingeben (scooter oder Negatives: other, similar, street, edge)-->: ")
    print(f"{get_lastcount(name)} Bilder in processed_data bereits abgelegt")
    count_start: int = int(input("Index angeben: "))

    return name, count_start

def rename_files_in_folder():
    while True:
        try:
            name, count_start = define_sub_folder()

            # Liste alle Dateien im Ordner auf
            if name == 'scooter':
                sub_folder = Path(FOLDER_PATH_FullVIEWS)
            else:
                sub_folder = Path(FOLDER_PATH_NEGATIVES) / name

            # Prüfe, ob der Ordner existiert
            if not sub_folder.exists():
                print(f"Ordner nicht gefunden: {sub_folder}")
                sys.exit(1)  # Beende das Skript mit Fehlercode

            files = os.listdir(sub_folder)

            # Filtere nur Dateien
            files = [f for f in files if os.path.isfile(os.path.join(sub_folder, f))]

            # Sortiere die Dateien alphabetisch
            files.sort()

            counter = count_start

            for filename in files:
                if counter < 10:
                    s = f"{counter:03d}"
                elif 100 > counter >= 10:
                    s = f"{counter:03d}"
                elif counter > 100:
                    s = f"{counter}"

                # Erstelle den neuen Dateinamen
                new_name = f"{name}_{s}"

                # Extrahiere die Dateiendung der ursprünglichen Datei
                file_extension = os.path.splitext(filename)[1]

                # Vollständiger Pfad der alten und neuen Datei
                old_file = os.path.join(sub_folder, filename)
                new_file = os.path.join(sub_folder, new_name + file_extension)

                # Benenne die Datei um
                os.rename(old_file, new_file)

                print(f"Umbenannt: {filename} -> {new_name}{file_extension}")

                # Erhöhe den Zähler
                counter += 1

            # Frage, ob eine weitere Kategorie umbenannt werden soll
            schleife = input("\nMöchtest du eine weitere Kategorie umbenennen? [1 = Ja / 2 = Nein]: ").strip()
            if schleife == '2':
                break  # Schleife beenden
            elif schleife != '1':
                print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")

        except Exception as e:
            print(f"Fehler in rename_files.py: {e}")
            sys.exit(1)  # Beende das Skript mit Fehlercode


# ================== MAIN ==================
if __name__ == "__main__":
    rename_files_in_folder()