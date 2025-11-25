import sys
import os
import shutil
import pathlib
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QTextEdit, QCheckBox, QProgressBar, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class CleanerThread(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    done = pyqtSignal(str)

    def __init__(self, target_path, dry_run, backup):
        super().__init__()
        self.target_path = target_path
        self.dry_run = dry_run
        self.backup = backup

    def run(self):
        pycache_dirs = []
        for root, dirs, _ in os.walk(self.target_path):
            for d in dirs:
                if d == '__pycache__':
                    pycache_dirs.append(os.path.join(root, d))

        total = len(pycache_dirs)
        if total == 0:
            self.done.emit("No __pycache__ folders found.")
            return

        backup_dir = None
        if self.backup:
            backup_dir = f"backup_pycache_{os.path.basename(self.target_path)}"
            os.makedirs(backup_dir, exist_ok=True)

        for i, folder in enumerate(pycache_dirs, start=1):
            self.progress.emit(int((i / total) * 100))
            self.log.emit(f"Processing: {folder}")

            if backup_dir:
                try:
                    shutil.copytree(folder, os.path.join(
                        backup_dir, os.path.basename(folder)), dirs_exist_ok=True)
                except Exception:
                    pass

            if not self.dry_run:
                shutil.rmtree(folder, ignore_errors=True)

        self.done.emit("Cleanup complete.")


class PyCacheCleaner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCache Cleaner")
        self.setGeometry(300, 200, 600, 450)
        # Set app icon
        icon_path = os.path.join(pathlib.Path(
            __file__).parent, "pycache_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()

        self.label = QLabel("Select a project folder:")
        layout.addWidget(self.label)

        self.btn_browse = QPushButton("Browse Folder")
        self.btn_browse.clicked.connect(self.browse)
        layout.addWidget(self.btn_browse)

        self.path_label = QLabel("No folder selected.")
        layout.addWidget(self.path_label)

        self.dry_run = QCheckBox("Dry-run mode (show only)")
        layout.addWidget(self.dry_run)

        self.backup = QCheckBox("Backup before deletion")
        layout.addWidget(self.backup)

        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        # Default developer info message
        self.log_box.setPlainText(
            "App name : PyCache Cleaner\n"
            "Appversion: v1.0.0\n"
            "Developer: Fouad El Azbi\n"
            "Company: EAF microservice.\n"
            "Email: EAF.microservice@gmail.com")
        layout.addWidget(self.log_box)

        self.btn_start = QPushButton("Start Cleanup")
        self.btn_start.clicked.connect(self.start_cleanup)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def browse(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.path_label.setText(folder)
            # Clear previous log and show developer info for the new folder
            self.log_box.clear()
            self.log_box.setPlainText(
                f"Developer Info: PyCache Cleaner v1.0 by Fouad El Azbi\nReady to clean folder: {folder}\n")

    def start_cleanup(self):
        target = self.path_label.text()
        if target == "No folder selected.":
            QMessageBox.warning(self, "Error", "Please select a valid folder.")
            return

        dry = self.dry_run.isChecked()
        backup = self.backup.isChecked()

        # Disable start button to prevent multiple clicks
        self.btn_start.setEnabled(False)

        self.worker = CleanerThread(target, dry, backup)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(lambda t: self.log_box.append(t))
        self.worker.done.connect(self.finish)
        self.worker.start()

    def finish(self, msg):
        # Re-enable start button when done
        self.btn_start.setEnabled(True)
        QMessageBox.information(self, "Done", msg)
        self.log_box.append("\n" + msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PyCacheCleaner()
    win.show()
    sys.exit(app.exec())
