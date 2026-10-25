"""
File Manager Utility
A command-line tool to organize files, edit text, and clean directories.
Features: Recursive scanning, Dry Run mode, external JSON config, and Smart Daily Auto-Run.
"""

import json
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

CONFIG_FILE = "config.json"

def load_config() -> dict:
    """Loads file categories from config.json, creating it with defaults if missing."""
    default_config = {
        ".png": "images", ".jpg": "images", ".jpeg": "images",
        ".pdf": "docs", ".txt": "docs", ".docx": "docs",
        ".py": "code", ".js": "code", ".html": "code",
        ".csv": "spreadsheets", ".xlsx": "spreadsheets",
        ".mp4": "videos", ".mp3": "audio"
    }
    
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        with config_path.open("w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
        print(f"[*] Created default configuration file at {CONFIG_FILE}")
        return default_config

    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def process_move_files(source: Path, dest: Path, category_map: dict, scan_subfolders: bool, dry_run: bool) -> None:
    """Core logic to scan and safely move files based on configuration."""
    if not dry_run:
        dest.mkdir(exist_ok=True, parents=True)

    # Use rglob for deep scanning, iterdir for surface-level only
    file_iterator = source.rglob("*") if scan_subfolders else source.iterdir()
    
    # Collect all valid files first to count them accurately
    valid_files = [f for f in file_iterator if f.is_file()]
    items_found = len(valid_files)
    
    if items_found == 0:
        print("[*] No files found to move in the specified directory.")
        return

    print(f"[*] Found {items_found} files. Starting {'DRY RUN (Preview)' if dry_run else 'move'}...")

    moved_count = 0
    for file in valid_files:
        ext = file.suffix.lower()
        
        if ext in category_map:
            folder_type = category_map[ext]
            target_folder = dest / folder_type
            dest_file = target_folder / file.name
            
            # Handle filename collisions (e.g., if "image.png" already exists)
            count = 1
            while dest_file.exists():
                dest_file = target_folder / f"{file.stem}_{count}{file.suffix}"
                count += 1

            if dry_run:
                print(f"[PREVIEW] Would move: {file.name} -> {target_folder.name}/")
            else:
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_file))
                
            moved_count += 1

    action_text = "Would move" if dry_run else "Moved"
    print(f"[+] Success: {action_text} {moved_count} out of {items_found} files.")


def move_files() -> None:
    """Interactive prompt wrapper for moving files immediately."""
    source = Path(input("Enter source path: ").strip())
    if not source.is_dir():
        print("[-] Error: Source directory does not exist.")
        return

    dest = Path(input("Enter destination path: ").strip())
    scan_subfolders = input("Include subfolders (recursive)? (y/n): ").strip().lower() == 'y'
    dry_run = input("Enable Dry Run (preview only, no files moved)? (y/n): ").strip().lower() == 'y'

    category_map = load_config()
    process_move_files(source, dest, category_map, scan_subfolders, dry_run)


def auto_run_scheduler() -> None:
    """Calculates wait time and efficiently sleeps until the target time to run daily."""
    print("\n--- Smart Daily Auto-Run Scheduler ---")
    target_time = input("Enter time to run daily (HH:MM, 24-hour format, e.g. 10:00 or 14:30): ").strip()
    
    try:
        target_hour, target_minute = map(int, target_time.split(':'))
        if not (0 <= target_hour <= 23 and 0 <= target_minute <= 59):
            raise ValueError
    except ValueError:
        print("[-] Error: Invalid time format. Please use HH:MM (00:00 to 23:59).")
        return

    source = Path(input("Enter source path to monitor: ").strip())
    if not source.is_dir():
        print("[-] Error: Source directory does not exist.")
        return

    dest = Path(input("Enter destination path: ").strip())
    scan_subfolders = input("Include subfolders (recursive)? (y/n): ").strip().lower() == 'y'
    category_map = load_config()

    print(f"\n[+] Scheduler started! Watching: {source}")
    print("[*] Leave this terminal window open. Press Ctrl+C to stop the scheduler.")

    try:
        while True:
            now = datetime.now()
            # Create a timestamp for TODAY at the target time
            next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
            
            # If that time has already passed today, schedule it for TOMORROW
            if now >= next_run:
                next_run += timedelta(days=1)
                
            # Calculate the exact number of seconds to wait
            wait_seconds = (next_run - now).total_seconds()
            
            print(f"\n[*] Next cleanup scheduled for: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"[*] Sleeping for {int(wait_seconds)} seconds. Goodnight! 🌙")
            
            # The script completely goes to sleep here, using zero CPU
            time.sleep(wait_seconds)
            
            # Wakes up and executes immediately
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Time to work! Running cleanup...")
            process_move_files(source, dest, category_map, scan_subfolders, dry_run=False)
                
    except KeyboardInterrupt:
        print("\n[*] Scheduler stopped by user. Returning to main menu.")


def write_file() -> None:
    """Appends user-provided text to an existing file."""
    file_path = Path(input("Enter file path to append to: ").strip())
    if not file_path.is_file():
        print("[-] Error: File not found.")
        return
        
    text_to_add = input("Enter text to append: ")
    try:
        with file_path.open(mode="a+", encoding="utf-8") as file_obj:
            file_obj.write(f"\n{text_to_add}")
        print("[+] Text successfully appended.")
    except Exception as e:
        print(f"[-] Error writing to file: {e}")


def read_file() -> None:
    """Reads and prints the contents of a file."""
    file_path = Path(input("Enter file path to read: ").strip())
    if not file_path.is_file():
        print("[-] Error: File not found.")
        return
        
    try:
        with file_path.open(mode="r", encoding="utf-8") as file_obj:
            content = file_obj.read()
            print("\n--- File Content ---")
            print(content)
            print("--------------------\n")
    except Exception as e:
        print(f"[-] Error reading file: {e}")


def delete_empty_folders() -> None:
    """Finds and deletes completely empty directories within a target path (bottom-up)."""
    target_dir = Path(input("Enter directory path to clean: ").strip())
    if not target_dir.is_dir():
        print("[-] Error: Directory not found.")
        return

    dry_run = input("Enable Dry Run (preview only, no deletions)? (y/n): ").strip().lower() == 'y'
    deleted_count = 0
    
    # Using rglob to find all directories, then sorting by depth (deepest first)
    folders = [f for f in target_dir.rglob("*") if f.is_dir()]
    folders = sorted(folders, key=lambda p: len(p.parts), reverse=True)

    for folder in folders:
        if not any(folder.iterdir()):
            if dry_run:
                print(f"[PREVIEW] Would delete empty folder: {folder}")
                deleted_count += 1
            else:
                try:
                    folder.rmdir()
                    print(f"[+] Deleted empty folder: {folder.name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"[-] Could not delete {folder.name}: {e}")
                    
    action_text = "Would delete" if dry_run else "Deleted"
    print(f"[*] Cleanup complete. {action_text} {deleted_count} empty folders.")


def main():
    """Main menu loop for the application."""
    while True:
        print("\n=== File Manager Menu ===")
        print("1. Organize/Move Files (Supports Recursive & Dry Run)")
        print("2. Schedule Smart Auto-Run (Daily Cleanup)")
        print("3. Append Text to File")
        print("4. Read a File")
        print("5. Delete Empty Folders (Deep Clean)")
        print("6. Exit")
        
        try:
            choice = int(input("\nSelect an option (1-6): "))
        except ValueError:
            print("[-] Invalid input. Please enter a number.")
            continue

        if choice == 1:
            move_files()
        elif choice == 2:
            auto_run_scheduler()
        elif choice == 3:
            write_file()
        elif choice == 4:
            read_file()
        elif choice == 5:
            delete_empty_folders()
        elif choice == 6:
            print("Exiting program. Goodbye!")
            break
        else:
            print("[-] Invalid choice. Please select a valid number between 1 and 6.")


if __name__ == "__main__":
    # This ensures the script runs the menu only if executed directly (not imported)
    main()