
# 🎮 Gesture-Controlled Flappy Bird

A Python implementation of **Flappy Bird** that you can play using **hand gestures** via your webcam.  
This project uses **OpenCV** and **MediaPipe** to detect gestures (fist & open palm) and **Pygame** for rendering the game.

<img width="1044" height="960" alt="image" src="https://github.com/user-attachments/assets/4f9cb4dc-55d7-4f49-a1c3-375c3cc2feca" />
---

## 🚀 Features
- **Gesture-based controls**:
  - ✊ **Fist** → Flap the bird (jump).
  - 🖐️ **Open Palm** → Make the bird dive down.
- Classic **Flappy Bird gameplay** (pipes, scoring, collisions).
- Smooth rendering with **Pygame**.
- Real-time **hand gesture detection** with **OpenCV + MediaPipe**.
- Restart the game using your hand gestures (no keyboard needed).

---

## 📂 Project Structure
```
├── main.py              # Entry point – starts the game
├── game.py              # Core game logic and rendering
├── bird.py              # Bird class (player character)
├── pipe.py              # Pipe class (obstacles)
├── gesture_detector.py  # Hand gesture detection (OpenCV + MediaPipe)
├── toppipe.png          # Top pipe image
├── bottompipe.png       # Bottom pipe image
├── flappybird.png       # Bird sprite
├── flappybirdbg.png     # Background image
└── .gitignore           # Git ignore rules
```

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Gesture_Controlled_Flappy_Bird.git
   cd Gesture_Controlled_Flappy_Bird
   ```

2. **Set up a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Linux/Mac
   .venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is missing, manually install:
   ```bash
   pip install pygame opencv-python mediapipe
   ```

---

## ▶️ How to Play
Run the game with:
```bash
python main.py
```

- ✊ **Fist** → Flap upwards  
- 🖐️ **Palm** → Dive downwards  
- 🎮 Spacebar also works as a backup flap control  

---

## 📷 Demo
*(Add a GIF or screenshot of your gameplay here if you want)*

---

## ⚡ Future Improvements
- Add menu screen and pause functionality.
- Train a custom gesture model for more controls.
- Difficulty scaling with score progression.
- High-score saving system.

---

## 🧑‍💻 Author
Developed by **Amyun Ghimire**  
📌 Project for exploring **computer vision + game development**
