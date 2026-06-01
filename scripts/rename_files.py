import os
from pathlib import Path

# Pfad zum Ordner
folder_path = r'C:\Studium_KI_Programme\Photo_Projekt_Objekterkennung\raw_data\negatives'

def define_sub_folder():

    # Parameter
    name = input("Kategorie eingeben: ")

    # Aktueller Stand Scooter = 588
    # Aktueller Stand Street = 156
    # Aktueller Stand other = 003
    # Aktueller Stand edge = 001
    # Aktueller Stand similar = 001
    count_start: int = int(input("Index angeben: "))

    return name, count_start

def rename_files_in_folder(folder_path):

    name, count_start = define_sub_folder()

    # Liste alle Dateien im Ordner auf
    sub_folder = Path(folder_path) / name
    files = os.listdir(sub_folder)

    # Filtere nur Dateien (keine Unterordner)
    files = [f for f in files if os.path.isfile(os.path.join(sub_folder, f))]

    # Sortiere die Dateien alphabetisch (optional, falls gewünscht)
    files.sort()

    counter = count_start

    for filename in files:
        # Erstelle den neuen Dateinamen
        new_name = f"{name}_{counter}"

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

def main():
    rename_files_in_folder(folder_path)

if __name__ == "__main__":
    main()