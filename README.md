# Hand Gesture Mouse Pointer Control

A Python project that uses computer vision and hand tracking to control your computer's mouse pointer using intuitive hand gestures. This project leverages [OpenCV](https://opencv.org/), [MediaPipe](https://mediapipe.dev/), and [PyAutoGUI](https://pyautogui.readthedocs.io/) to provide a contactless way to interact with your computer.

![Demo Screenshot](demo_screenshot.png)

---

## Features

- **Pointer Movement:**  
  Move the mouse pointer by simply moving your index finger.

- **Left Click / Drag:**  
  Perform left-clicks by extending your thumb. Hold the gesture for a short period to initiate dragging.

- **Right Click / Drag:**  
  Trigger right-clicks by raising your middle finger. Similarly, holding the gesture will start a drag.

- **Scrolling:**  
  Activate scroll mode by performing a pinch gesture (bringing the index finger and thumb close together) and move your finger vertically to scroll.

---

## Demo

Watch the project in action! Check out the [demo video](video/demo.mp4).

> **Note:** If your browser does not support video playback, download the video from the repository and play it with your favorite media player.

---

## Requirements

- **Python Version:** Python 3.6 or higher
- **Libraries:**
  - [OpenCV](https://pypi.org/project/opencv-python/) (`opencv-python`)
  - [MediaPipe](https://pypi.org/project/mediapipe/)
  - [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/Hand_Gesture_Controller.git
   cd hand-gesture-mouse-control
