# Hand Gesture Mouse Pointer Control

A Python project that uses computer vision and hand tracking to control your computer's mouse pointer using intuitive hand gestures. This project leverages [OpenCV](https://opencv.org/), [MediaPipe](https://mediapipe.dev/), and [PyAutoGUI](https://pyautogui.readthedocs.io/) to provide a contactless way to interact with your computer.

![Demo GIF](demo.gif)

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

Here's a demonstration of the project in action:

![Demo GIF](demo.gif)

*Note: The above GIF was generated from the project demo video.*

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
   git clone https://github.com/yourusername/hand-gesture-mouse-control.git
   cd hand-gesture-mouse-control
