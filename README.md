# Real-time ASCII Art Webcam
# video-to-ascii

This project captures video frames from your webcam and converts them into ASCII art in real time. It uses Python along with OpenCV and NumPy for image processing.

## Features
- Real-time video capture from the webcam.
- Brightness and contrast adjustment.
- ASCII art conversion using a detailed character set.
- Floyd–Steinberg dithering for enhanced visual output.
- Live display of the ASCII art in the terminal.

## Installation

### Prerequisites
- Python 3.x
- [opencv-python](https://pypi.org/project/opencv-python/)
- [numpy](https://pypi.org/project/numpy/)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/KadirYurekturk/video-to-ascii.git
   cd video-to-ascii
   pip install -r requirements.txt
   python main.py
