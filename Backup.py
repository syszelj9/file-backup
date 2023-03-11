import os
import sys
import time
import zipfile
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QMessageBox, QProgressBar, QVBoxLayout, QHBoxLayout, QWidget

class BackupCreator(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize variables
        self.backup_dir = ""
        self.files_to_backup = []
        self.backup_file = ""
        self.progress = 0

        # Create GUI components
        self.title_label = QLabel("Backup Creator")
        self.backup_dir_label = QLabel("Backup Directory:")
        self.backup_dir_button = QPushButton("Select Directory")
        self.files_label = QLabel("Files to Backup:")
        self.files_button = QPushButton("Select Files")
        self.create_button = QPushButton("Create Backup")
        self.progress_bar = QProgressBar()

        # Connect signals to slots
        self.backup_dir_button.clicked.connect(self.select_backup_dir)
        self.files_button.clicked.connect(self.select_files_to_backup)
        self.create_button.clicked.connect(self.create_backup)

        # Set layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.backup_dir_label)
        layout.addWidget(self.backup_dir_button)
        layout.addWidget(self.files_label)
        layout.addWidget(self.files_button)
        layout.addWidget(self.create_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def select_backup_dir(self):
        self.backup_dir = QFileDialog.getExistingDirectory(self, "Select Backup Directory")
        if self.backup_dir:
            self.backup_dir_label.setText("Backup Directory: " + self.backup_dir)

    def select_files_to_backup(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files to Backup")
        if files:
            self.files_to_backup = files
            self.files_label.setText("Files to Backup: " + "; ".join(files))

    def create_backup(self):
        if not self.backup_dir:
            QMessageBox.warning(self, "Error", "Please select a backup directory")
            return

        if not self.files_to_backup:
            QMessageBox.warning(self, "Error", "Please select files to backup")
            return

        self.backup_file = "backup_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".zip"
        backup_path = os.path.join(self.backup_dir, self.backup_file)

        # Create backup archive
        with zipfile.ZipFile(backup_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in self.files_to_backup:
                zipf.write(file, os.path.basename(file))

                # Update progress bar
                self.progress += 100 // len(self.files_to_backup)
                self.progress_bar.setValue(self.progress)

        # Show success message
        QMessageBox.information(self, "Success", f"Backup created successfully:\n{backup_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    backup_creator = BackupCreator()
    backup_creator.setWindowTitle("Backup Creator")
    backup_creator.setFixedSize(400, 300)
    backup_creator.show()
    sys.exit(app.exec_())
