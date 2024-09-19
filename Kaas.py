import sys
import traceback
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox, QLabel, QSpacerItem, QSizePolicy, QTextEdit, QCheckBox, QMessageBox,
    QGridLayout, QProgressBar, QFrame, QProgressDialog, QFileDialog, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QFont, QColor
from datetime import datetime, timedelta
from config_manager import ConfigManager
from excel_manager import ExcelManager
from ui_components import ConfigTab, FreedomFutureTab, apply_styles
from notion_client import Client


class RecordingThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, audio_recorder):
        super().__init__()
        self.audio_recorder = audio_recorder

    def run(self):
        try:
            self.audio_recorder.record_audio()
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self, config_manager, excel_manager):
        super().__init__()
        self.config_manager = config_manager
        self.excel_manager = excel_manager
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinMaxButtonsHint)  # Ensure buttons are available
        self.init_ui()
        self.create_shortcuts()
        self.showFullScreen()  # You can remove this line if you want the window to start in a normal state

    def init_ui(self):
        self.setWindowTitle("Kaas - Adapter")

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(200)

        # Remove the Configuration button
        # config_btn = QPushButton("Configuration")  # Remove this line
        meeting_transcriber_btn = QPushButton("Meeting Transcriber")
        
        # sidebar_layout.addWidget(config_btn)  # Remove this line
        sidebar_layout.addWidget(meeting_transcriber_btn)
        
        sidebar_layout.addStretch()

        # Main content area
        self.content_stack = QStackedWidget()

        # Only keep Meeting Transcriber
        self.content_stack.addWidget(self.create_meeting_transcriber())

        # Connect sidebar buttons
        # config_btn.clicked.connect(self.show_config)  # Remove this line
        meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setCentralWidget(central_widget)
        self.create_menu_bar()

    def create_meeting_transcriber(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        title = QLabel("Meeting Transcriber")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        upload_btn = QPushButton("Upload Audio File")
        upload_btn.clicked.connect(self.upload_audio_file)
        layout.addWidget(upload_btn)

        self.file_path_label = QLabel("No file selected")
        layout.addWidget(self.file_path_label)

        transcribe_btn = QPushButton("Transcribe")
        transcribe_btn.clicked.connect(self.transcribe_audio)
        layout.addWidget(transcribe_btn)

        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        layout.addWidget(self.transcription_text)

        # Add a spacer to push the back button to the bottom
        layout.addStretch()

        # Update the back button to connect to a valid method
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.close)  # Change this line to close the application
        layout.addWidget(back_btn)

        return widget

    def show_meeting_transcriber(self):
        self.content_stack.setCurrentIndex(2)

    def upload_audio_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
        if file_path:
            self.file_path_label.setText(f"Selected file: {file_path}")

    def transcribe_audio(self):
        if self.file_path_label.text() == "No file selected":
            QMessageBox.warning(self, "No File", "Please upload an audio file first.")
            return
        
        # Here you would implement the actual transcription logic
        # For now, we'll just use a placeholder message
        transcribed_text = "This is a placeholder for the transcribed text."
        self.transcription_text.setPlainText(transcribed_text)
        
        # Send the transcribed text to Notion
        self.send_data_to_notion("Meeting Transcription", transcribed_text)

    def send_data_to_notion(self, title, content):
        notion = Client(auth="secret_fZy25xcCCrXoTvGqn63L9SCd8Mwc8zPIedrPLkAggxN")
        
        try:
            new_page = notion.pages.create(
                parent={"type": "page_id", "page_id": "1034ff1c2e9480e9af94fda8effbb79d"},
                properties={
                    "title": {"title": [{"text": {"content": title}}]},
                },
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": content}}]
                        }
                    }
                ]
            )
            print(f"Data sent to Notion successfully! Page ID: {new_page['id']}")
        except Exception as e:
            print(f"Error sending data to Notion: {str(e)}")

    def create_shortcuts(self):
        # Sidebar navigation shortcuts
        # self.create_shortcut("Ctrl+G", self.show_config, "Show Configuration")  # Remove this line
        self.create_shortcut("Ctrl+M", self.show_meeting_transcriber, "Show Meeting Transcriber")

        # Additional shortcuts
        self.create_shortcut("Ctrl+Q", self.close, "Exit Application")
        self.create_shortcut("F11", self.toggle_fullscreen, "Toggle Fullscreen")


    def create_shortcut(self, key, callback, description):
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(callback)
        shortcut.setWhatsThis(description)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

def exception_hook(exctype, value, traceback):
    print(f"Uncaught exception: {exctype}, {value}")
    print("Traceback:")
    traceback.print_tb(traceback)
    QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply styles after creating the QApplication instance
    apply_styles(app)
    
    config_manager = ConfigManager("./config.json")
    excel_manager = ExcelManager(config_manager.get_config())
    
    window = MainWindow(config_manager, excel_manager)
    window.show()
    
    sys.exit(app.exec())