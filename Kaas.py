import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
    QFileDialog, QLineEdit, QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence

class TranscriptFetchThread(QThread):
    finished = pyqtSignal(str)  # Emit transcript text when done
    error = pyqtSignal(str)

    def __init__(self, file_search_dir):
        super().__init__()
        self.file_search_dir = file_search_dir

    def run(self):
        try:
            self.fetch_transcript()
        except Exception as e:
            self.error.emit(str(e))

    def fetch_transcript(self):
        # Use the file_search_dir directly in the URL
        url = f"http://115.245.248.122:8051/meeting/wisdom-file/{self.file_search_dir}"
        print(f"Fetching transcript from: {url}")  # Log URL for debugging

        response = requests.get(url)
        if response.status_code == 200:
            print(f"GET Response Text: {response.text}")  # Print the GET response (transcript)
            self.finished.emit(response.text)  # Pass transcript text to the main thread
        else:
            print(f"GET Error: {response.status_code}, {response.text}")  # Print GET error if any
            self.error.emit(f"Error fetching transcript: {response.status_code}, {response.text}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_search_dir = None  # Store file_search_dir here
        self.init_ui()
        self.create_shortcuts()

    def init_ui(self):
        self.setWindowTitle("Meeting Transcriber")
        self.setGeometry(200, 100, 1000, 600)  # Adjust window size
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-family: Arial, sans-serif;
                color: #444;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QLineEdit, QComboBox, QTextEdit {
                padding: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 14px;
                background-color: #FAFAFA;
                color: black;
            }
            QWidget {
                background-color: #F5F5F5;
            }
            QStackedWidget {
                background-color: #FFF;
            }
            QVBoxLayout {
                spacing: 15px;
            }
        """)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        # Sidebar
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #2C3E50; padding: 10px;")

        meeting_transcriber_btn = QPushButton("Meeting Transcriber")
        meeting_transcriber_btn.setStyleSheet("background-color: #3498DB; color: white;")
        sidebar_layout.addWidget(meeting_transcriber_btn)

        transcript_search_btn = QPushButton("Search Transcript")
        transcript_search_btn.setStyleSheet("background-color: #3498DB; color: white;")
        sidebar_layout.addWidget(transcript_search_btn)

        sidebar_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.create_meeting_transcriber())
        self.content_stack.addWidget(self.create_transcript_search())

        meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)
        transcript_search_btn.clicked.connect(self.show_transcript_search)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.content_stack, 1)

        self.setCentralWidget(central_widget)

    def create_meeting_transcriber(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 20, 30, 20)  # Add margins

        title = QLabel("Meeting Transcriber")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 20px;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Language:"))
        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("Enter language code (e.g., 'en')")
        layout.addWidget(self.language_input)

        layout.addWidget(QLabel("Meeting Subject:"))
        self.meeting_subject_input = QLineEdit()
        self.meeting_subject_input.setPlaceholderText("Enter meeting subject")
        layout.addWidget(self.meeting_subject_input)

        layout.addWidget(QLabel("Department:"))
        self.department_input = QComboBox()
        self.department_input.addItems(["trademan", "dhoom Studios", "serendipity"])
        layout.addWidget(self.department_input)

        layout.addWidget(QLabel("Knowledge Patterns:"))
        self.knowledge_pattern_input = QComboBox()
        self.knowledge_pattern_input.addItems(["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"])
        layout.addWidget(self.knowledge_pattern_input)

        upload_btn = QPushButton("Upload Audio File")
        upload_btn.clicked.connect(self.upload_audio_file)
        layout.addWidget(upload_btn)

        self.file_path_label = QLabel("No file selected")
        layout.addWidget(self.file_path_label)

        transcribe_btn = QPushButton("Submit Audio and Transcribe")
        transcribe_btn.clicked.connect(self.transcribe_audio)
        layout.addWidget(transcribe_btn)

        self.transcription_text = QTextEdit()
        self.transcription_text.setReadOnly(True)
        self.transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
        layout.addWidget(self.transcription_text)

        layout.addStretch()

        return widget

    def create_transcript_search(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("Search Transcript")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 20px;")
        layout.addWidget(title)

        layout.addWidget(QLabel("File Search Directory:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter file_search_dir")
        layout.addWidget(self.search_input)

        search_btn = QPushButton("Search Transcript")
        search_btn.clicked.connect(self.search_transcript)
        layout.addWidget(search_btn)

        self.search_transcription_text = QTextEdit()
        self.search_transcription_text.setReadOnly(True)
        self.search_transcription_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)  # Set scroll policy
        layout.addWidget(self.search_transcription_text)

        layout.addStretch()

        return widget

    def upload_audio_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
        if file_path:
            self.file_path_label.setText(f"Selected file: {file_path}")
            self.audio_file = file_path

    def transcribe_audio(self):
        if not self.audio_file:
            QMessageBox.warning(self, "No File", "Please upload an audio file first.")
            return

        # Other required fields
        language = self.language_input.text()
        meeting_subject = self.meeting_subject_input.text()
        department = self.department_input.currentText()
        selected_pattern = self.knowledge_pattern_input.currentText()

        if not language or not meeting_subject or not department:
            QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
            return

        # Just showing that audio is being transcribed
        self.transcription_text.setPlainText("Submitting the audio for transcription...")

        # Simulating the process
        # Replace this part with the actual API call to your transcription service
        # Assume the `file_search_dir` is returned by the transcription process

        # Example file_search_dir (replace with the actual path from your API response)
        self.file_search_dir = "+Users+traderscafe+Desktop+hakuna-matata+uploads+serendipity+2024-09-19_21-16-04"

        # Set the transcription text and show that it's transcribed
        self.transcription_text.setPlainText(f"Audio transcribed successfully! Transcript goes here...")

        # Switch to the search tab and populate the file_search_dir input field
        self.search_input.setText(self.file_search_dir)
        self.show_transcript_search()

    def search_transcript(self):
        file_search_dir = self.search_input.text()
        if not file_search_dir:
            QMessageBox.warning(self, "Missing Input", "Please enter a file_search_dir.")
            return

        # Show loader
        self.progress_dialog = QProgressDialog("Fetching transcript...", "Cancel", 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.progress_dialog.show()

        # Fetch the transcript using a separate thread
        self.transcript_thread = TranscriptFetchThread(file_search_dir)
        self.transcript_thread.finished.connect(self.on_transcript_fetched)
        self.transcript_thread.error.connect(self.on_transcript_fetch_error)
        self.transcript_thread.start()

    def on_transcript_fetched(self, transcript_text):
        self.progress_dialog.hide()  # Hide the loader
        self.search_transcription_text.setPlainText(transcript_text)  # Display transcript

    def on_transcript_fetch_error(self, error_msg):
        self.progress_dialog.hide()  # Hide the loader
        QMessageBox.critical(self, "Error", f"Failed to fetch transcript: {error_msg}")

    def show_meeting_transcriber(self):
        self.content_stack.setCurrentIndex(0)

    def show_transcript_search(self):
        # Populate the search input field with the latest file_search_dir if available
        if self.file_search_dir:
            self.search_input.setText(self.file_search_dir)
        self.content_stack.setCurrentIndex(1)

    def create_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+M"), self, activated=self.show_meeting_transcriber)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
