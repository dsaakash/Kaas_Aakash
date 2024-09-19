# import sys
# import traceback
# import requests
# from PyQt6.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
#     QFileDialog, QLineEdit
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# from PyQt6.QtGui import QFont, QShortcut, QKeySequence

# class RecordingThread(QThread):
#     finished = pyqtSignal()
#     error = pyqtSignal(str)
    
#     def __init__(self, audio_file, language, meeting_subject, department, knowledge_patterns):
#         super().__init__()
#         self.audio_file = audio_file
#         self.language = language
#         self.meeting_subject = meeting_subject
#         self.department = department
#         self.knowledge_patterns = knowledge_patterns

#     def run(self):
#         try:
#             self.submit_audio_file()
#             self.finished.emit()
#         except Exception as e:
#             self.error.emit(str(e))

#     def submit_audio_file(self):
#         url = "http://115.245.248.122:8051/meeting/submit-meeting"
#         files = {'audio_file': open(self.audio_file, 'rb')}
#         data = {'knowledge_patterns': self.knowledge_patterns}
#         params = {
#             'language': self.language,
#             'meeting_subject': self.meeting_subject,
#             'department': self.department
#         }

#         response = requests.post(url, params=params, files=files, data=data)
#         if response.status_code == 200:
#             print("Audio submitted successfully!")
#         else:
#             print(f"Error: {response.status_code}, {response.text}")

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.audio_file = None
#         self.knowledge_patterns = ["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"]
#         self.init_ui()
#         self.create_shortcuts()
#         self.fetch_departments()

#     def init_ui(self):
#         self.setWindowTitle("Meeting Transcriber")
#         self.setGeometry(200, 100, 1000, 600)  # Adjust window size
#         self.setStyleSheet("""
#             QLabel {
#                 font-size: 14px;
#                 font-family: Arial, sans-serif;
#                 color: #444;
#             }
#             QPushButton {
#                 background-color: #1976D2;
#                 color: white;
#                 padding: 12px 24px;
#                 border-radius: 8px;
#                 font-size: 16px;
#             }
#             QPushButton:hover {
#                 background-color: #1565C0;
#             }
#             QLineEdit, QComboBox, QTextEdit {
#                 padding: 10px;
#                 border-radius: 8px;
#                 border: 1px solid #ccc;
#                 font-size: 14px;
#                 background-color: #FAFAFA;
#                 color: black;  /* Updated to black */
#             }
#             QWidget {
#                 background-color: #F5F5F5;
#             }
#             QStackedWidget {
#                 background-color: #FFF;
#             }
#             QVBoxLayout {
#                 spacing: 15px;
#             }
#         """)

#         central_widget = QWidget()
#         main_layout = QHBoxLayout(central_widget)

#         # Sidebar
#         sidebar = QWidget()
#         sidebar_layout = QVBoxLayout(sidebar)
#         sidebar.setFixedWidth(250)
#         sidebar.setStyleSheet("background-color: #2C3E50; padding: 10px;")

#         meeting_transcriber_btn = QPushButton("Meeting Transcriber")
#         meeting_transcriber_btn.setStyleSheet("background-color: #3498DB; color: white;")
#         sidebar_layout.addWidget(meeting_transcriber_btn)

#         sidebar_layout.addStretch()

#         self.content_stack = QStackedWidget()
#         self.content_stack.addWidget(self.create_meeting_transcriber())
#         meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)

#         main_layout.addWidget(sidebar)
#         main_layout.addWidget(self.content_stack, 1)

#         self.setCentralWidget(central_widget)

#     def create_meeting_transcriber(self):
#         widget = QWidget()
#         layout = QVBoxLayout(widget)
#         layout.setContentsMargins(30, 20, 30, 20)  # Add margins

#         title = QLabel("Meeting Transcriber")
#         title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
#         title.setStyleSheet("color: #333; margin-bottom: 20px;")
#         layout.addWidget(title)

#         layout.addWidget(QLabel("Language:"))
#         self.language_input = QLineEdit()
#         self.language_input.setPlaceholderText("Enter language code (e.g., 'en')")
#         layout.addWidget(self.language_input)

#         layout.addWidget(QLabel("Meeting Subject:"))
#         self.meeting_subject_input = QLineEdit()
#         self.meeting_subject_input.setPlaceholderText("Enter meeting subject")
#         layout.addWidget(self.meeting_subject_input)

#         layout.addWidget(QLabel("Department:"))
#         self.department_input = QComboBox()
#         self.department_input.setStyleSheet("color: black;")  # Change color to black
#         layout.addWidget(self.department_input)

#         layout.addWidget(QLabel("Knowledge Patterns:"))
#         self.knowledge_pattern_input = QComboBox()
#         self.knowledge_pattern_input.setStyleSheet("color: black;")  # Change color to black
#         self.knowledge_pattern_input.addItems(self.knowledge_patterns)
#         layout.addWidget(self.knowledge_pattern_input)

#         upload_btn = QPushButton("Upload Audio File")
#         upload_btn.clicked.connect(self.upload_audio_file)
#         layout.addWidget(upload_btn)

#         self.file_path_label = QLabel("No file selected")
#         self.file_path_label.setStyleSheet("color: #555;")
#         layout.addWidget(self.file_path_label)

#         transcribe_btn = QPushButton("Submit Audio and Transcribe")
#         transcribe_btn.clicked.connect(self.transcribe_audio)
#         layout.addWidget(transcribe_btn)

#         self.transcription_text = QTextEdit()
#         self.transcription_text.setReadOnly(True)
#         layout.addWidget(self.transcription_text)

#         layout.addStretch()

#         return widget

#     def fetch_departments(self):
#         departments = ["trademan", "dhoom Studios", "serendipity"]
#         self.department_input.addItems(departments)

#     def show_meeting_transcriber(self):
#         self.content_stack.setCurrentIndex(0)

#     def upload_audio_file(self):
#         file_dialog = QFileDialog()
#         file_path, _ = file_dialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.mp3 *.wav *.m4a)")
#         if file_path:
#             self.file_path_label.setText(f"Selected file: {file_path}")
#             self.audio_file = file_path

#     def transcribe_audio(self):
#         if not self.audio_file:
#             QMessageBox.warning(self, "No File", "Please upload an audio file first.")
#             return

#         language = self.language_input.text()
#         meeting_subject = self.meeting_subject_input.text()
#         department = self.department_input.currentText()
#         selected_pattern = self.knowledge_pattern_input.currentText()

#         if selected_pattern == "All of the above":
#             knowledge_patterns = ["idea_compass", "keynote", "recommendation", "github_issues", "summary"]
#         else:
#             knowledge_patterns = [selected_pattern]

#         if not language or not meeting_subject or not department:
#             QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
#             return

#         self.transcription_text.setPlainText("Submitting the audio for transcription...")

#         self.thread = RecordingThread(self.audio_file, language, meeting_subject, department, knowledge_patterns)
#         self.thread.finished.connect(self.on_transcription_finished)
#         self.thread.error.connect(self.on_transcription_error)
#         self.thread.start()

#     def on_transcription_finished(self):
#         self.transcription_text.setPlainText("Transcription completed and submitted.")

#     def on_transcription_error(self, error_msg):
#         QMessageBox.critical(self, "Error", f"Failed to submit audio: {error_msg}")

#     def create_shortcuts(self):
#         self.create_shortcut("Ctrl+M", self.show_meeting_transcriber, "Show Meeting Transcriber")
#         self.create_shortcut("Ctrl+Q", self.close, "Exit Application")

#     def create_shortcut(self, key, callback, description):
#         shortcut = QShortcut(QKeySequence(key), self)
#         shortcut.activated.connect(callback)

# def exception_hook(exctype, value, traceback):
#     print(f"Uncaught exception: {exctype}, {value}")
#     print("Traceback:")
#     traceback.print_tb(traceback)
#     QApplication.quit()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import traceback
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QComboBox, QLabel, QTextEdit, QMessageBox,
    QFileDialog, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QShortcut, QKeySequence

class RecordingThread(QThread):
    finished = pyqtSignal(str)  # Emit dir_search_path on success
    error = pyqtSignal(str)
    
    def __init__(self, audio_file, language, meeting_subject, department, knowledge_patterns):
        super().__init__()
        self.audio_file = audio_file
        self.language = language
        self.meeting_subject = meeting_subject
        self.department = department
        self.knowledge_patterns = knowledge_patterns

    def run(self):
        try:
            self.submit_audio_file()
        except Exception as e:
            self.error.emit(str(e))

    def submit_audio_file(self):
        url = "http://115.245.248.122:8051/meeting/submit-meeting"
        files = {'audio_file': open(self.audio_file, 'rb')}
        data = {'knowledge_patterns': self.knowledge_patterns}
        params = {
            'language': self.language,
            'meeting_subject': self.meeting_subject,
            'department': self.department
        }

        response = requests.post(url, params=params, files=files, data=data)
        if response.status_code == 200:
            result = response.json()
            dir_search_path = result.get('dir_search_path')
            if dir_search_path:
                self.finished.emit(dir_search_path)  # Emit the dir_search_path to the main thread
            else:
                self.error.emit("Failed to retrieve directory search path.")
        else:
            self.error.emit(f"Error: {response.status_code}, {response.text}")

class TranscriptFetchThread(QThread):
    finished = pyqtSignal(str)  # Emit transcript text when done
    error = pyqtSignal(str)

    def __init__(self, dir_search_path):
        super().__init__()
        self.dir_search_path = dir_search_path

    def run(self):
        try:
            self.fetch_transcript()
        except Exception as e:
            self.error.emit(str(e))

    def fetch_transcript(self):
        url = f"http://115.245.248.122:8051/meeting/wisdom-file/{self.dir_search_path}"
        response = requests.get(url)
        if response.status_code == 200:
            self.finished.emit(response.text)  # Pass transcript text to the main thread
        else:
            self.error.emit(f"Error fetching transcript: {response.status_code}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_file = None
        self.dir_search_path = None  # Store the directory path
        self.knowledge_patterns = ["idea_compass", "keynote", "recommendation", "github_issues", "summary", "All of the above"]
        self.init_ui()
        self.create_shortcuts()
        self.fetch_departments()

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

        sidebar_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(self.create_meeting_transcriber())
        meeting_transcriber_btn.clicked.connect(self.show_meeting_transcriber)  # Connect the button to the method

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
        layout.addWidget(self.department_input)

        layout.addWidget(QLabel("Knowledge Patterns:"))
        self.knowledge_pattern_input = QComboBox()
        self.knowledge_pattern_input.addItems(self.knowledge_patterns)
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
        layout.addWidget(self.transcription_text)

        layout.addStretch()

        return widget

    def fetch_departments(self):
        departments = ["trademan", "dhoom Studios", "serendipity"]
        self.department_input.addItems(departments)

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

        language = self.language_input.text()
        meeting_subject = self.meeting_subject_input.text()
        department = self.department_input.currentText()
        selected_pattern = self.knowledge_pattern_input.currentText()

        if selected_pattern == "All of the above":
            knowledge_patterns = ["idea_compass", "keynote", "recommendation", "github_issues", "summary"]
        else:
            knowledge_patterns = [selected_pattern]

        if not language or not meeting_subject or not department:
            QMessageBox.warning(self, "Missing Fields", "Please provide all required fields.")
            return

        self.transcription_text.setPlainText("Submitting the audio for transcription...")

        # Start the recording thread
        self.thread = RecordingThread(self.audio_file, language, meeting_subject, department, knowledge_patterns)
        self.thread.finished.connect(self.on_transcription_finished)
        self.thread.error.connect(self.on_transcription_error)
        self.thread.start()

    def on_transcription_finished(self, dir_search_path):
        self.dir_search_path = dir_search_path
        self.fetch_transcript(dir_search_path)

    def on_transcription_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"Failed to submit audio: {error_msg}")

    def fetch_transcript(self, dir_search_path):
        # Start the transcript fetch thread
        self.transcript_thread = TranscriptFetchThread(dir_search_path)
        self.transcript_thread.finished.connect(self.on_transcript_fetched)
        self.transcript_thread.error.connect(self.on_transcript_fetch_error)
        self.transcript_thread.start()

    def on_transcript_fetched(self, transcript_text):
        # Display the transcript
        self.transcription_text.setPlainText(transcript_text)

    def on_transcript_fetch_error(self, error_msg):
        QMessageBox.critical(self, "Error", f"Failed to fetch transcript: {error_msg}")

    def show_meeting_transcriber(self):
        self.content_stack.setCurrentIndex(0)

    def create_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+M"), self, activated=self.show_meeting_transcriber)
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=self.close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
