import json
import shutil
from pathlib import Path

CONFIG_FILE = "config.json"

def load_config() -> dict:
    default_config = {".png": "images", ".jpg": "images", ".pdf": "docs", ".txt": "docs"}
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        with config_path.open("w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    with config_path.open("r") as f:
        return json.load(f)

def move_files() -> None:
    category_map = load_config()
    source = Path(input("Enter source path: ").strip())
    dest = Path(input("Enter destination path: ").strip())
    
    if not source.is_dir():
        return
        
    recursive = input("Include subfolders? (y/n): ").strip().lower() == 'y'
    dry_run = input("Dry run preview? (y/n): ").strip().lower() == 'y'

    if not dry_run: dest.mkdir(exist_ok=True, parents=True)
    
    files = source.rglob("*") if recursive else source.iterdir()
    
    for file in files:
        if file.is_file() and file.suffix.lower() in category_map:
            target_folder = dest / category_map[file.suffix.lower()]
            dest_file = target_folder / file.name
            
            if dry_run:
                print(f"[PREVIEW] Would move: {file.name} -> {target_folder.name}/")
            else:
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_file))

def delete_empty_folders() -> None:
    target_dir = Path(input("Enter directory to clean: ").strip())
    if not target_dir.is_dir(): return
    
    folders = sorted([f for f in target_dir.rglob("*") if f.is_dir()], key=lambda p: len(p.parts), reverse=True)
    for folder in folders:
        if not any(folder.iterdir()):
            folder.rmdir()
            print(f"Deleted empty folder: {folder.name}")

def main():
    while True:
        print("\n1. Move Files (Advanced)\n2. Clean Empty Folders\n3. Exit")
        choice = input("Select: ").strip()
        if choice == '1': move_files()
        elif choice == '2': delete_empty_folders()
        elif choice == '3': break

if __name__ == "__main__":
    main()