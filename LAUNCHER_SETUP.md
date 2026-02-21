# 🚀 REM + OpenClaw Launcher Setup

## Quick Setup (3 Steps)

### **Step 1: Install PyInstaller** (Optional - for .exe version)
```bash
pip install pyinstaller
```

### **Step 2: Build Desktop Launcher** (Creates .exe)
```bash
cd "C:\Users\hardi\Chat bot\Rem_project"
python build_exe.py
```

This creates:
- ✅ `C:\Users\<User>\Desktop\REM_Launcher.exe` - Main launcher
- ✅ `C:\Users\<User>\Desktop\Start_REM_Services.bat` - Backup launcher

### **Step 3: Double-Click on Desktop**
- **Click `REM_Launcher.exe`** to start all services
- Or **click `Start_REM_Services.bat`** if exe doesn't work

---

## What Each File Does

| File | Purpose | How to Use |
|------|---------|-----------|
| `start_all_services.bat` | Batch launcher for local testing | `start_all_services.bat` |
| `launcher.py` | Python launcher (can be run anywhere) | `python launcher.py` |
| `build_exe.py` | Creates .exe from launcher.py | `python build_exe.py` |
| `create_desktop_shortcut.bat` | Creates desktop shortcut | `create_desktop_shortcut.bat` |

---

## Usage Options

### **Option 1: Quick Start (.bat file - LOCAL)**
```bash
cd "C:\Users\hardi\Chat bot\Rem_project"
start_all_services.bat
```

### **Option 2: Python Launcher (ANYWHERE)**
```bash
python launcher.py
```
- Works from any directory
- Better error handling
- Automatic port checking

### **Option 3: Desktop .exe (EASIEST)**
1. Run: `python build_exe.py`
2. Double-click `REM_Launcher.exe` on Desktop
3. All services start automatically

### **Option 4: Desktop Shortcut**
```bash
create_desktop_shortcut.bat
```
Creates a shortcut that runs `launcher.py`

---

## What Happens When You Run Any Launcher

```
┌─────────────────────────────────────────────────────┐
│ 1. Check Python Virtual Environment                 │
│    (makes sure venv is activated)                   │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 2. Check Ollama Service                             │
│    (warns if not running, allows proceeding)        │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 3. Start REM API Server (Port 8000)                 │
│    - Open new terminal window                       │
│    - Wait for startup (3 sec)                       │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 4. Start OpenClaw Bridge (Port 8765)                │
│    - Open new terminal window                       │
│    - Wait for startup (3 sec)                       │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 5. Start OpenClaw Gateway (Port 9001)               │
│    - Open new terminal window                       │
│    - Wait for startup (3 sec)                       │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ 6. Start REM Voice Chat Interface                   │
│    - Open new terminal window                       │
│    - Ready for voice input                          │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│ ✅ ALL SERVICES RUNNING                             │
│                                                     │
│ Say voice commands in "REM Voice Chat" window!     │
│                                                     │
│ Press CTRL+C to stop all services                   │
└─────────────────────────────────────────────────────┘
```

---

## Services That Start

| # | Service | Port | What It Does |
|---|---------|------|------------|
| 1 | **REM API Server** | 8000 | Core LLM, TTS, ASR endpoints |
| 2 | **OpenClaw Bridge** | 8765 | HTTP gateway to REM services |
| 3 | **OpenClaw Gateway** | 9001 | WebSocket gateway for agent routing |
| 4 | **REM Voice Chat** | - | Interactive voice interface |

---

## How to Use After Startup

### **Voice Commands**
Speak in the "REM Voice Chat" window:
```
"Open YouTube and search for cat videos"
"What is machine learning?"
"Open Google"
"Tell me a joke"
```

### **HTTP API (for integration)**
```bash
# Check health
curl http://127.0.0.1:8765/health

# Generate with LLM
curl -X POST http://127.0.0.1:8765/llm/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"What is AI?"}'
```

### **OpenClaw Dashboard**
Open new terminal:
```bash
openclaw dashboard
```

---

## Troubleshooting

### **"Virtual environment not detected"**
- Make sure you activated venv first:
  ```bash
  .venv\Scripts\activate
  ```

### **"Ollama not found"**
- Start Ollama in a new terminal:
  ```bash
  ollama serve
  ```
- You can continue anyway when prompted

### **Ports already in use**
- Check what's using the port:
  ```bash
  netstat -ano | findstr :8000
  ```
- Kill the process using `taskkill /PID <pid> /F`

### **"Module not found" errors**
- Reinstall dependencies:
  ```bash
  pip install -r requirements.txt
  pip install -r server/requirements_api.txt
  ```

### **Something crashes on startup**
- Check the terminal window for error messages
- Read the error carefully - it usually tells you what's wrong
- You can restart individual services manually

---

## Creating Custom Launchers

You can also create custom launchers that add more services:

**Edit `launcher.py`** - Add new services before the `while True` loop:
```python
self.start_service(
    "My Custom Service",
    [sys.executable, "path/to/service.py"],
    cwd=self.project_root,
    wait_port=8888  # Optional
)
```

Then rebuild the exe:
```bash
python build_exe.py
```

---

## Production Deployment

For production use:

1. **Use Task Scheduler** to auto-start on Windows boot
2. **Use nssm** (Non-Sucking Service Manager) to run as Windows Service
3. **Use Docker** for containerized deployment

Example with nssm:
```bash
nssm install REM_Service python.exe "C:\path\to\launcher.py"
nssm start REM_Service
```

---

## Summary

| Need | Solution |
|------|----------|
| **Quick test** | `start_all_services.bat` |
| **Portable script** | `python launcher.py` |
| **Desktop icon** | Run `build_exe.py` → Double-click .exe |
| **Auto-start on boot** | Create Task Scheduler task pointing to .exe |
| **Remote access** | Use OpenClaw Dashboard (localhost:9001) |

---

**All services will launch in separate terminal windows and work together!** 🎉
