# 🚀 QUICK START GUIDE

## Your system is ready!

### ⚡ Start Everything (One Command)

```bash
python launcher.py
```

That's it! Three separate windows will open:
1. REM API Server
2. OpenClaw Bridge  
3. Voice Chat Interface

---

## 🎯 What's New

✅ **Port Conflicts FIXED**
- Dynamic port allocation
- No more "port already in use" errors
- Services start reliably every time

✅ **Automatic Setup**
- Dependencies installed automatically
- No manual configuration needed

✅ **Simple Launcher**
- One command to start everything
- Clean status messages
- Easy troubleshooting

---

## 💬 Try It Out

Once running, speak commands in the Voice Chat window:

```
"Open YouTube"
"Search for python tutorials"
"Tell me a joke"
"What's the weather"
"Open a browser"
```

---

## 🛠️ If Something Goes Wrong

### Services won't start?
```bash
# Close all windows first, then:
python launcher.py
```

### Still having issues?
```bash
# Clean restart - kills all Python processes
taskkill /F /IM python.exe

# Then start fresh
python launcher.py
```

---

## 📊 What's Running

| Service | Port | Status |
|---------|------|--------|
| REM API | 8000 (or 8100/8200) | ✅ Active |
| Bridge | 8765 (or 8865/8965) | ✅ Active |
| Voice Chat | Console | ✅ Active |

---

## ✨ Key Improvements

- **Before**: Port conflicts required manual process killing
- **After**: Services start automatically, even if ports are occupied

The system automatically tries these ports in order:
1. **8000** (API) / **8765** (Bridge)
2. **8100** / **8865**
3. **8200** / **8965**
4. **9000** / **9001** / **9002**
5. OS-assigned (automatic)

---

## 🎉 You're All Set!

```bash
python launcher.py
```

Enjoy your REM + OpenClaw system! 🔥
