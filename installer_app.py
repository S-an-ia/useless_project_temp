"""
Useless Alarm Clock — Self-Contained Windows Installer
=======================================================
This script, when bundled with PyInstaller, becomes
UselessAlarmClock_Setup.exe. It:
  1. Shows a friendly Tkinter installer GUI
  2. Copies the app into Program Files
  3. Creates Desktop + Start Menu shortcuts
  4. Registers an Uninstall entry in Windows Apps/Programs
  5. Optionally launches the app after install
"""

import os
import sys
import shutil
import winreg
import ctypes
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


# ── Constants ────────────────────────────────────────────────
APP_NAME       = "ACNA (Alarm Clock Nobody Asked for)"
APP_VERSION    = "1.0"
PUBLISHER      = "Sanin"
EXE_NAME       = "ACNA.exe"
INSTALL_SUBDIR = "ACNA"
UNINSTALL_EXE  = "Uninstall.exe"
REG_KEY        = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\ACNA"

DARK_BG        = "#111111"
ACCENT         = "#59c878"
WHITE          = "#ffffff"
GRAY           = "#888888"


def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


def default_install_dir():
    pf = os.environ.get("PROGRAMFILES", r"C:\Program Files")
    return os.path.join(pf, INSTALL_SUBDIR)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def elevate():
    """Re-launch self with admin rights."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


# ── Shortcut helper using VBScript (no external deps) ────────
def create_shortcut(target, shortcut_path, icon=None, description=""):
    vbs = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
Set oLink = oWS.CreateShortcut("{shortcut_path}")
oLink.TargetPath = "{target}"
oLink.WorkingDirectory = "{os.path.dirname(target)}"
oLink.Description = "{description}"
'''
    if icon:
        vbs += f'oLink.IconLocation = "{icon}"\n'
    vbs += "oLink.Save\n"
    tmp = os.path.join(os.environ.get("TEMP", r"C:\Temp"), "_ua_shortcut.vbs")
    with open(tmp, "w") as f:
        f.write(vbs)
    subprocess.run(["cscript", "//NoLogo", tmp], capture_output=True)
    try:
        os.remove(tmp)
    except Exception:
        pass


def create_uninstaller_script(install_dir):
    """Write a small batch uninstaller into the install directory."""
    unreg_reg = (
        f'reg delete "HKLM\\{REG_KEY}" /f >nul 2>&1\n'
        f'reg delete "HKCU\\{REG_KEY}" /f >nul 2>&1\n'
    )
    desktop_lnk = os.path.join(
        os.path.expanduser("~"), "Desktop", f"{APP_NAME}.lnk"
    )
    start_dir = os.path.join(
        os.environ.get("APPDATA", ""),
        "Microsoft", "Windows", "Start Menu", "Programs", APP_NAME
    )
    bat = f"""@echo off
echo Uninstalling {APP_NAME}...
taskkill /F /IM {EXE_NAME} >nul 2>&1
timeout /t 1 /nobreak >nul
rmdir /s /q "{install_dir}"
del /f /q "{desktop_lnk}" >nul 2>&1
rmdir /s /q "{start_dir}" >nul 2>&1
{unreg_reg}
echo Done. {APP_NAME} has been removed.
pause
"""
    bat_path = os.path.join(install_dir, UNINSTALL_EXE)
    with open(bat_path, "w") as f:
        f.write(bat)
    return bat_path


def register_uninstaller(install_dir, uninstall_bat):
    """Add entry to Windows Settings > Apps."""
    try:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_KEY)
    except PermissionError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_KEY)

    exe_path = os.path.join(install_dir, EXE_NAME)
    values = {
        "DisplayName":     APP_NAME,
        "DisplayVersion":  APP_VERSION,
        "Publisher":       PUBLISHER,
        "InstallLocation": install_dir,
        "DisplayIcon":     exe_path,
        "UninstallString": f'cmd /c "{uninstall_bat}"',
        "NoModify":        1,
        "NoRepair":        1,
    }
    for name, val in values.items():
        if isinstance(val, int):
            winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)
        else:
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, val)
    winreg.CloseKey(key)


def do_install(install_dir, progress_cb, status_cb):
    """Copy files & wire up shortcuts. Called on a background thread."""

    src = resource_path("app")   # PyInstaller bundles app/ subfolder

    # 1 ─ Copy files
    status_cb("Copying files...")
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    shutil.copytree(src, install_dir)
    progress_cb(40)

    # 2 ─ Desktop shortcut
    status_cb("Creating Desktop shortcut...")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    create_shortcut(
        target=os.path.join(install_dir, EXE_NAME),
        shortcut_path=os.path.join(desktop, f"{APP_NAME}.lnk"),
        icon=os.path.join(install_dir, EXE_NAME),
        description=APP_NAME,
    )
    progress_cb(60)

    # 3 ─ Start Menu shortcut
    status_cb("Creating Start Menu entry...")
    start_menu = os.path.join(
        os.environ.get("APPDATA", ""),
        "Microsoft", "Windows", "Start Menu", "Programs", APP_NAME
    )
    os.makedirs(start_menu, exist_ok=True)
    create_shortcut(
        target=os.path.join(install_dir, EXE_NAME),
        shortcut_path=os.path.join(start_menu, f"{APP_NAME}.lnk"),
        icon=os.path.join(install_dir, EXE_NAME),
        description=APP_NAME,
    )
    progress_cb(80)

    # 4 ─ Uninstaller + registry
    status_cb("Registering uninstaller...")
    uninstall_bat = create_uninstaller_script(install_dir)
    register_uninstaller(install_dir, uninstall_bat)
    progress_cb(100)

    status_cb("Installation complete!")


# ── GUI ──────────────────────────────────────────────────────

class InstallerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} Setup")
        self.geometry("540x380")
        self.resizable(False, False)
        self.configure(bg=DARK_BG)

        # Center on screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - 540) // 2
        y = (sh - 380) // 2
        self.geometry(f"540x380+{x}+{y}")

        self._build_ui()

    def _build_ui(self):

        # ── Header ─────────────────────────────────
        header = tk.Frame(self, bg=ACCENT, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"⏰  {APP_NAME}  Setup",
            font=("Segoe UI", 18, "bold"),
            bg=ACCENT, fg=DARK_BG
        ).pack(expand=True)

        # ── Body ───────────────────────────────────
        body = tk.Frame(self, bg=DARK_BG)
        body.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(
            body,
            text="Install location:",
            font=("Segoe UI", 10),
            bg=DARK_BG, fg=GRAY
        ).pack(anchor="w")

        dir_frame = tk.Frame(body, bg=DARK_BG)
        dir_frame.pack(fill="x", pady=(4, 16))

        self.dir_var = tk.StringVar(value=default_install_dir())
        dir_entry = tk.Entry(
            dir_frame,
            textvariable=self.dir_var,
            font=("Segoe UI", 10),
            bg="#222222", fg=WHITE,
            relief="flat",
            insertbackground=WHITE
        )
        dir_entry.pack(fill="x", ipady=6)

        # Progress bar
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor="#222222",
            background=ACCENT,
            bordercolor=DARK_BG,
            lightcolor=ACCENT,
            darkcolor=ACCENT,
        )

        self.progress = ttk.Progressbar(
            body,
            style="green.Horizontal.TProgressbar",
            length=480, mode="determinate"
        )
        self.progress.pack(fill="x", pady=(0, 8))

        self.status_label = tk.Label(
            body,
            text="Ready to install.",
            font=("Segoe UI", 9),
            bg=DARK_BG, fg=GRAY
        )
        self.status_label.pack(anchor="w")

        # ── Buttons ────────────────────────────────
        btn_frame = tk.Frame(body, bg=DARK_BG)
        btn_frame.pack(side="bottom", fill="x", pady=(10, 0))

        self.install_btn = tk.Button(
            btn_frame,
            text="Install",
            font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg=DARK_BG,
            activebackground="#75dc91",
            relief="flat", cursor="hand2",
            command=self._start_install
        )
        self.install_btn.pack(side="right", ipadx=20, ipady=6)

        tk.Button(
            btn_frame,
            text="Cancel",
            font=("Segoe UI", 11),
            bg="#333333", fg=WHITE,
            activebackground="#444444",
            relief="flat", cursor="hand2",
            command=self.destroy
        ).pack(side="right", ipadx=14, ipady=6, padx=(0, 8))

    def _start_install(self):
        self.install_btn.config(state="disabled")
        install_dir = self.dir_var.get().strip()

        def run():
            try:
                do_install(install_dir, self._set_progress, self._set_status)
                self.after(0, self._on_success, install_dir)
            except Exception as e:
                self.after(0, self._on_error, str(e))

        threading.Thread(target=run, daemon=True).start()

    def _set_progress(self, val):
        self.after(0, lambda: self.progress.config(value=val))

    def _set_status(self, msg):
        self.after(0, lambda: self.status_label.config(text=msg))

    def _on_success(self, install_dir):
        if messagebox.askyesno(
            "Installation Complete",
            f"{APP_NAME} has been installed!\n\n"
            "A shortcut has been added to your Desktop and Start Menu.\n\n"
            "Launch the app now?",
            parent=self
        ):
            exe = os.path.join(install_dir, EXE_NAME)
            subprocess.Popen([exe])
        self.destroy()

    def _on_error(self, err):
        self.install_btn.config(state="normal")
        messagebox.showerror("Installation Failed", f"Error:\n{err}", parent=self)


if __name__ == "__main__":
    if not is_admin():
        elevate()
    app = InstallerApp()
    app.mainloop()
