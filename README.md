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

#### 🌐 Online Mode
- Uses **socket programming** for real-time two-player gameplay.
- Supports LAN or Internet-based connections.
- Built-in matchmaking and move synchronization.
- Chat support between players.

#### 🤖 Computer Mode
- Play against the computer (AI logic implemented manually).
- **COMP vs COMP** and **COMP vs Player** modes available.
- The computer uses decision logic to make legal and strategic moves.

---

## ⚙️ Technologies Used
- **Python**
- **Socket Programming** (for network communication)
- **Threading** (for concurrency and real-time gameplay)
- **Custom Chess Engine**
- **Custom GUI** (likely built with Tkinter, Pygame, or similar)

---

## 🖥️ Screenshots

### 🧍 Offline Mode
<img width="1600" height="863" alt="Offline Mode" src="https://github.com/user-attachments/assets/c701d062-c281-419a-9b6d-a24186c9d96d" />

---

### 🌐 Online Mode
<img width="1610" height="858" alt="Online Mode 1" src="https://github.com/user-attachments/assets/6b611deb-82d3-4cdf-ad9e-edfe4d4f6b39" />
<img width="1603" height="874" alt="Online Mode 2" src="https://github.com/user-attachments/assets/b5d85333-3b8c-4ffc-824d-b0612bb87206" />
<img width="1615" height="867" alt="Online Mode 3" src="https://github.com/user-attachments/assets/5f293c1f-aff5-40e9-af23-8aae9fef25a5" />
<img width="1610" height="898" alt="Online Mode 4" src="https://github.com/user-attachments/assets/2b6ba02d-561f-4ad4-8646-e1967ce3e2ff" />

---

### 🤖 Computer Mode
- Supports **Computer vs Player** and **Computer vs Computer** battles.
- Watch two AIs play against each other in real-time!

🎥 [Watch Demo Video](https://github.com/user-attachments/assets/21d7cd15-6b34-405e-b65f-04a3c99e9933)

---

### 🧩 Server-Side Communication
<img width="1912" height="695" alt="Server Communication" src="https://github.com/user-attachments/assets/fe8e314b-7586-43b6-aa0d-47d099924f77" />

The server manages:
- Client connections
- Game pairing and session creation
- Real-time move broadcasting
- Connection handling and disconnection events

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
