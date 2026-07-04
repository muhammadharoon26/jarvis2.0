<div align="center">
  
# 🤖 Jarvis Workspace Manager 2.0

**Your intelligent, hyper-fast workspace orchestrator.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/jarvis2.0)

[Features](#features) •
[Installation](#installation) •
[Usage](#usage) •
[Building](#building) •
[Contributing](#contributing)

</div>

---

## 🚀 Overview

**Jarvis Workspace Manager** is a sleek, cross-platform productivity tool designed to launch your entire work environment with a single click. Instead of manually opening folders, websites, applications, and terminal tabs one by one, Jarvis does it all for you.

With a beautiful UI, seamless system tray integration, and powerful PowerShell backend execution, Jarvis 2.0 brings you into your flow state instantly.

## ✨ Features

- 🖥️ **Modern Dashboard**: A highly polished, glassmorphism-inspired UI to configure your environments.
- 📂 **Multi-Workspace Support**: Create tailored workspaces for "Development", "Design", "Gaming", or anything else.
- 🌐 **Web & Folders**: Instantly launch your most-used directories and websites.
- 🚀 **Apps with Arguments**: Launch applications with specific flags and optional Administrator privileges.
- 💻 **Advanced Terminal Automation**: Spawns multiple terminal tabs (Windows Terminal) customized with profiles (PowerShell/CMD) and automatic `.venv` activation.
-  tray **System Tray Integration**: Quietly runs in the background. Access your workspaces directly from the system tray.
- ⚡ **Auto-Startup**: Seamlessly integrates with Windows startup so your assistant is always ready.

## 🛠️ Installation

### Prerequisites
- Windows 10/11
- Python 3.8+ (If running from source)
- Windows Terminal (For advanced terminal tabs functionality)

### Running from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/jarvis2.0.git
   cd jarvis2.0
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Jarvis:**
   ```bash
   python app.py
   ```

## 🎯 Usage

1. Open **Jarvis Manager** from your Start Menu or system tray.
2. Select or create a **Workspace** from the top dropdown.
3. Add your desired:
   - **Folders**
   - **Websites**
   - **Applications** (Optionally toggle 'Admin')
   - **Terminal Tabs** (Optionally toggle '.venv' for auto-activation)
4. Click **💾 Save Configuration**.
5. Click **🚀 Launch Workspace** or launch it directly from the system tray icon!

## 📦 Building Executable

### Option 1: Generate Spec and Build Instantly (Recommended)
You can generate the `.spec` file and build the `.exe` in one go. Make sure you bundle the required files (`gui.html` and `jarvis.ps1`) using `--add-data`. 

```powershell
pyinstaller --noconsole --name Jarvis --add-data "gui.html;." --add-data "jarvis.ps1;." app.py
```
*Note: Make sure to check the output in the newly created `dist/` directory.*

### Option 2: Build from an existing `.spec` file
If you already have a `.spec` file configured (like `Jarvis.spec`), or if you used `pyi-makespec` to generate one for manual editing, simply compile it by running:

```powershell
pyinstaller Jarvis.spec
```

## 🤝 Contributing

Contributions make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
<div align="center">
  <i>Built with ❤️ to optimize your workflow.</i>
</div>
