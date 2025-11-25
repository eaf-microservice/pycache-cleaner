# PyCache Cleaner

![PyCache Cleaner icon](./pycache_icon.ico)

PyCache Cleaner is a small GUI utility to find and remove Python `__pycache__` folders from a selected project directory. It's a Windows-friendly desktop app built with PyQt6 and packaged with PyInstaller.

**Key points:**

- **Developer:** Fouad El Azbi
- **Company** EAF microservice
- **Contact:** `EAF.microservice@gmail.com`
- **License:** MIT (`LICENSE.txt`)

**Features:**

- Browse and select a project folder via a simple GUI.
- Optionally run in **dry-run** mode (show what would be removed).
- Optionally **backup** `__pycache__` folders before deletion.
- Progress bar and log output while cleaning.

**Files of interest in this repository:**

- `main.py` - Main application source (PyQt6 GUI).
- `main.spec` - PyInstaller spec used to build the distributable.
- `pycache_icon.ico` - Application icon referenced by the spec.
- `Pycache_cleaner.iss`, `setup.iss` - Inno Setup scripts (Windows installer builders).
- `pycache.reg` - Optional registry file included with the project.
- `build/`, `dist/`, `release/` - Packaging/build artifacts (when generated).

## Requirements

- Python 3.8+ (tested with recent 3.x)
- PyQt6
- PyInstaller (if you want to build the executable)

## Quickstart (run from source)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install PyQt6
```

3. Run the app:

```powershell
python main.py
```

When the app opens: click `Browse Folder`, choose the target project folder, then optionally toggle `Dry-run mode` or `Backup before deletion` and click `Start Cleanup`.

## Building a Windows executable

This project includes a `main.spec` configured for PyInstaller. The spec already references the icon `pycache_icon.ico` and builds a windowed application.

Typical build steps:

```powershell
pip install pyinstaller PyQt6
pyinstaller --clean --noconfirm main.spec
```

After the build finishes the app files will be in `dist\Pycache_cleaner\` (or `dist\Pycache_cleaner.exe` depending on the chosen PyInstaller mode). You can run the generated executable from there.

## Creating an installer

There are Inno Setup scripts included (`Pycache_cleaner.iss`, `setup.iss`). If you have Inno Setup installed, you can compile an installer with the Inno Setup Compiler (`iscc`):

```powershell
iscc Pycache_cleaner.iss
```

## Notes & Tips

- The app logs a developer/info block to the GUI text area; this includes the developer email.
- The `main.spec` collects `pycache_icon.ico` so keep that file next to `main.py` when building.
- `pycache.reg` is provided if you need registry entries — review it before applying.
- If you plan to distribute the app, test both the PyInstaller output and the generated installer on a clean Windows VM.

## Contributing

Issues and pull requests are welcome. For quick changes, updating `main.py` and re-building with PyInstaller is the typical workflow.

## License

This project is licensed under the MIT License — see `LICENSE.txt`.

## Acknowledgements

Built with PyQt6.
