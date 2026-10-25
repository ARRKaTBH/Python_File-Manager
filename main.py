import shutil
from pathlib import Path

def move_files() -> None:
    category_map = {
        ".png": "images", ".jpg": "images", ".jpeg": "images",
        ".pdf": "docs", ".txt": "docs", ".py": "code",
        ".csv": "spreadsheets", ".mp4": "videos",
    }
    
    source = Path(input("Enter source path: ").strip())
    dest = Path(input("Enter destination path: ").strip())

    if not source.is_dir():
        print("Source directory not found.")
        return

    dest.mkdir(exist_ok=True, parents=True)
    moved_count = 0

    for file in source.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            if ext in category_map:
                folder_type = category_map[ext]
                target_folder = dest / folder_type
                target_folder.mkdir(exist_ok=True)
                
                dest_file = target_folder / file.name
                count = 1
                while dest_file.exists():
                    dest_file = target_folder / f"{file.stem}_{count}{file.suffix}"
                    count += 1

                shutil.move(str(file), str(dest_file))
                moved_count += 1

    print(f"Moved {moved_count} files successfully.")

def write_file() -> None:
    file_path = Path(input("Enter file path to append to: ").strip())
    if file_path.is_file():
        text_to_add = input("Enter text to append: ")
        with file_path.open(mode="a+", encoding="utf-8") as f:
            f.write(f"\n{text_to_add}")
        print("Text appended.")

def read_file() -> None:
    file_path = Path(input("Enter file path to read: ").strip())
    if file_path.is_file():
        with file_path.open(mode="r", encoding="utf-8") as f:
            print("\n" + f.read() + "\n")

def main():
    while True:
        print("\n1. Move Files\n2. Append Text\n3. Read File\n4. Exit")
        choice = input("Select an option: ").strip()
        if choice == '1':
            move_files()
        elif choice == '2':
            write_file()
        elif choice == '3':
            read_file()
        elif choice == '4':
            break

if __name__ == "__main__":
    main()