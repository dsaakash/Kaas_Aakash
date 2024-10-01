```markdown
# Meeting Transcriber and Transcript Search Application

This is a PyQt6-based desktop application that allows users to upload audio files, transcribe them, and search for the resulting transcript using a `file_search_dir`. The application has two primary functionalities:
1. Upload an audio file for transcription.
2. Automatically or manually search for the transcript based on the `file_search_dir` provided after transcription.

## Features

- **Audio Upload and Transcription**: Upload an audio file and submit it for transcription.
- **Search Transcript**: Once the transcription is completed, you can search and retrieve the transcript using a `file_search_dir`.
- **Automatic Tab Switch**: After transcription, the application switches to the search tab and populates the `file_search_dir`.

## Requirements

- Python 3.6 or above
- PyQt6
- Requests

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository/meeting-transcriber.git
   ```

2. Navigate into the directory:
   ```bash
   cd meeting-transcriber
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
or 

Run Setup.py

## Running the Application

1. Run the `main.py` file to start the application:
   ```bash
   python Kaas.py
   ```

2. The application will open with two tabs:
    - **Meeting Transcriber**: This tab allows you to upload audio files for transcription.
    - **Search Transcript**: This tab lets you search for transcripts using the `file_search_dir`.

## Usage Instructions

### Step 1: Upload and Transcribe Audio

- Open the **Meeting Transcriber** tab.
- Click the `Upload Audio File` button to select an audio file.
- After selecting the audio file, click `Submit Audio and Transcribe`.

![Upload Audio File](screenshots/upload-audio.png)

- The application will simulate the transcription and generate a `file_search_dir`.

### Step 2: Search for Transcript

- After the transcription, the application will automatically switch to the **Search Transcript** tab, and the `file_search_dir` will be automatically filled in.
- Click `Search Transcript` to fetch the transcript for the corresponding audio file.

![Search Transcript](screenshots/search-transcript.png)

## Screenshots

### Upload Audio

![Upload Audio](screenshots/upload-audio.png)

### Transcription in Progress

![Transcription in Progress](screenshots/transcription-in-progress.png)

### Search Transcript

![Search Transcript](screenshots/search-transcript.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Explanation:
1. **Screenshots**: For the screenshots, you need to take snapshots of the app while using it. You can place the images inside a folder like `screenshots/` in the project directory.
2. **Screenshots Folder**: Create a folder named `screenshots` in the same directory where `README.md` is located. Place your screenshots there:
   - `upload-audio.png` (Screenshot of the audio upload step)
   - `transcription-in-progress.png` (Screenshot of the transcription process)
   - `search-transcript.png` (Screenshot of the search transcript tab)

### How to Add Screenshots:
- Take screenshots of the app (while uploading audio, transcription, and searching).
- Place those images inside a folder named `screenshots/` in your project directory.
- Reference those images in your `README.md` using relative paths like this:
  ```markdown
  ![Upload Audio File](screenshots/upload-audio.png)
  ```

This `README.md` gives users a clear guide on how to install, run, and use the application with visual references. Let me know if you need further modifications!
