# ♟️ Adhoc Multiplayer Chess Game (Socket + Threading)

## 📌 Overview
This is a **custom-built Chess game** developed entirely **independently** — without any external assistance or AI-generated code.

The project uses **Python sockets** and **multithreading** to create an **adhoc networked chess system**, supporting:
- **Offline (Player vs Player)**
- **Online (Player vs Player over LAN/Internet)**
- **Computer (Player vs AI / Computer vs Computer)** modes.

It’s a full-fledged chess engine and GUI built from scratch, handling real-time move synchronization, chat, and matchmaking through sockets.

---

## 🚀 Features

### 🎮 Game Modes

#### 🧍 Offline Mode
- Play locally with a friend on the same machine.  
- Fully functional chess rules (check, checkmate, stalemate, pawn promotion, castling, en passant).

---

### 🌐 Online Mode
- Uses **socket programming** for real-time two-player gameplay.
- Supports **LAN or Internet-based** connections.
- Built-in matchmaking and chat.
- Handles disconnections gracefully and resynchronizes game states.

#### 🖼️ Screenshots

**Game Lobby & Connection Setup**
<br>
<img width="1610" height="858" alt="Online Mode 1" src="https://github.com/user-attachments/assets/6b611deb-82d3-4cdf-ad9e-edfe4d4f6b39" />

---

**In-Game Chat and Move Synchronization**
<br>
<img width="1603" height="874" alt="Online Mode 2" src="https://github.com/user-attachments/assets/b5d85333-3b8c-4ffc-824d-b0612bb87206" />

---

**Active Gameplay Interface**
<br>
<img width="1615" height="867" alt="Online Mode 3" src="https://github.com/user-attachments/assets/5f293c1f-aff5-40e9-af23-8aae9fef25a5" />

---

**Match Completion and Result Display**
<br>
<img width="1610" height="898" alt="Online Mode 4" src="https://github.com/user-attachments/assets/2b6ba02d-561f-4ad4-8646-e1967ce3e2ff" />

---

### 🤖 Computer Mode
- Supports both:
  - **COMP vs PLAYER**
  - **COMP vs COMP (automated AI battle)**  
- The AI logic is implemented natively with legal-move validation and simple heuristics.  
- Watch the AI play against itself in full chess simulation.

#### 🎥 Demo Video
https://github.com/user-attachments/assets/21d7cd15-6b34-405e-b65f-04a3c99e9933  

*(Click the link above to watch the AI-vs-AI gameplay demo directly on GitHub.)*

---

### 🧩 Server-Side Communication
The server manages:
- Client connections  
- Game pairing & synchronization  
- Move broadcasting  
- Thread-safe message handling  
- Connection & disconnection events  

<img width="1912" height="695" alt="Server Communication" src="https://github.com/user-attachments/assets/fe8e314b-7586-43b6-aa0d-47d099924f77" />

---

## 🧠 Architecture Overview
```text
+---------------------+           +----------------------+
|      Player 1       |  <---->   |       Server         |
| (Client - Socket)   |           | (Socket + Threads)   |
+---------------------+           +----------------------+
             ↑                                 ↓
+---------------------+           +----------------------+
|      Player 2       |  <---->   |       AI Engine      |
| (Client - Socket)   |           | (Optional Component) |
+---------------------+           +----------------------+
