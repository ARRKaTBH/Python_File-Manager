# 📂 Python File Manager Utility

A powerful, customizable, and zero-dependency command-line utility to automatically organize files, clean up empty directories, and schedule daily background file management tasks.

## ⚠️ The Problem
We all have a messy `Downloads` or `Desktop` folder. Manually sorting files by extension into different folders is tedious, repetitive, and time-consuming. Existing tools are often bloated, require complex installations, or lack customizability.

## ✨ Features
- **📂 Auto-Organization:** Instantly moves files into categorized folders based on their extensions.
- **⏰ Smart Daily Scheduler:** Set a time (e.g., `10:00`) and the script sleeps efficiently in the background, waking up to organize your folders daily using zero CPU while waiting.
- **⚙️ JSON Configuration:** Easily customize file categories without touching any Python code (`config.json`).
- **🔍 Recursive Deep Scanning:** Option to scan and organize files hidden deep inside nested subfolders.
- **🛡️ Dry Run Mode (Preview):** Preview exactly which files will be moved or deleted *before* actually modifying your file system.
- **🧹 Deep Folder Cleanup:** Intelligently deletes empty directories from the bottom up, clearing out deeply nested empty folders.

## 🐍 Requirements
- **Python 3.6+**
- No external libraries or `pip install` required! It runs entirely on Python's built-in standard library.

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [](https://github.com/ARRKaTBH/Python_File-Manager.git)
   cd Python_File-Manager