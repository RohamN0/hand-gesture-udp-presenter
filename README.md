# Hand Gesture UDP Presenter

A real‑time hand gesture recognition system that turns your webcam into a wireless presentation remote. When you close or open specific fingers, the application sends **Page Up** or **Page Down** commands via UDP to any machine on your local network – perfect for controlling slides during presentations, reading documents, or browsing without touching the keyboard.

Built with **MediaPipe**, **OpenCV**, and a ready‑to‑use Docker setup for an isolated, reproducible environment.

## Features

- 🖐️ **Hand gesture detection** – tracks up to two hands in real time  
- 📡 **UDP broadcasting** – sends `PGUP` / `PGDN` packets to a configurable IP and port  
- 🐳 **Dockerised** – no need to install Python, OpenCV, or MediaPipe on the host; runs in a container  
- ⚡ **Cooldown control** – prevents accidental double‑triggers (adjustable in `main.py`)  
- 🪟 **Linux host only** – relies on X11 passthrough for live camera preview (can be adapted)  
-  **Offline-friendly** – uses Debian and PyPI mirrors optimised for Iranian networks; includes MediaPipe wheel for installation without internet  

## How it works

1. The webcam captures a live video frame.  
2. MediaPipe extracts 21 hand landmarks per hand.  
3. The code compares the current finger positions with the previous frame:  
   - **Page Down** – index + middle fingers move from “open” (tip above joint) to “closed” (tip below joint), while ring + pinky remain closed.  
   - **Page Up** – same finger move but from “closed” to “open”.  
4. On detection, a UDP packet containing `b"PGDN"` or `b"PGUP"` is fired to the target Windows machine (default `172.16.0.3:5005`).  
5. A receiver on the target (e.g. a Python script, AutoHotkey, or a simple server) translates the packet into actual keyboard input.

## Prerequisites

- **Linux host** with a working webcam (`/dev/video0`)  
- **Docker** and **Docker Compose** installed  
- **X11** for camera preview (the container directly renders OpenCV windows via X11 socket)  
- The target machine must be reachable on the same network and listening on UDP port `5005`

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hand-gesture-udp-presenter.git
   cd hand-gesture-udp-presenter
   ```

2. **Obtain the MediaPipe wheel**  
   The build expects the file `mediapipe-0.8.6.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl` in the project root.  
   - Download it from [PyPI](https://pypi.org/project/mediapipe/0.8.6.2/#files) (or a local mirror) and place it next to the Dockerfile.  
   - *Note:* The Dockerfile is configured to work with Iranian mirrors; if you are outside Iran, you can optionally comment the `pip config` lines to use the default PyPI – in that case you can also install MediaPipe directly with `pip` and omit the offline wheel.

3. **Build and run**
   ```bash
   docker-compose up --build
   ```
   The application will open a window showing the webcam feed with hand landmarks. Perform the gestures – the terminal will log `Sending: Page Down` or `Sending: Page Up` when detected.

4. **Set up a UDP receiver on the target machine**  
   Example Python listener:
   ```python
   import socket
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   sock.bind(("0.0.0.0", 5005))
   while True:
       data, addr = sock.recvfrom(1024)
       if data == b"PGDN":
           # simulate Page Down key press
           pass
       elif data == b"PGUP":
           # simulate Page Up key press
           pass
   ```
   Adapt the automation tool of your choice (AutoHotkey, pyautogui, etc.).

## Customisation

- **Hand signs**: The gesture logic is in the comparison of `last_y_tip` and `last_y_joint` for landmarks 8,12,16,20. You can modify these conditions to create your own gestures (e.g., swipe, thumbs‑up).
- **Keyboard commands**: Replace `b"PGDN"` / `b"PGUP"` with any string and update the receiver accordingly.
- **Use without Docker**: Install Python 3.9, MediaPipe 0.8.6.2, OpenCV, and run `main.py`. The Dockerfile provides a reference for the exact dependencies.

## Offline Build & Iranian Mirrors

The Dockerfile uses the following mirrors for package downloads:
- **Debian**: `mirror2.chabokan.net`
- **PyPI**: `archive.ito.gov.ir` and `pypi.jamko.ir`

If you are outside Iran and have unrestricted internet access, you may:
- Remove or comment the `RUN printf ... sources.list` block.
- Delete the `pip config` commands.
- Simplify the MediaPipe installation to `RUN pip install mediapipe==0.8.6.2` and omit the offline `.whl` copy.

The provided setup is optimised for environments with limited connectivity.

## License

MIT – feel free to use, modify, and share.
