"""
NetSpeed Monitor v1.0.0
Windows 11 görev çubuğu saatinin solunda ağ hızını gösterir.
"""

import tkinter as tk
import psutil
import ctypes
import ctypes.wintypes
import winreg
import time
import sys
import threading
from datetime import datetime

APP_NAME    = "NetSpeed Monitor"
REG_KEY     = r"Software\Microsoft\Windows\CurrentVersion\Run"
REG_VALUE   = "NetSpeedMonitor"
WIDTH       = 115   # widget genişliği (px)
GAP         = 2     # saatle aradaki boşluk (px)


# ──────────────────────────────────────────────────────────────── helpers ──

def fmt(bps: float) -> str:
    """Bayt/s değerini okunabilir stringe çevirir."""
    for unit in ("B/s", "KB/s", "MB/s", "GB/s"):
        if bps < 1024:
            return f"{bps:6.1f} {unit}"
        bps /= 1024
    return f"{bps:.1f} TB/s"


def find_clock_hwnd():
    """Windows görev çubuğu saatinin HWND'ini bulur (Win10 & Win11)."""
    user32 = ctypes.windll.user32
    tray   = user32.FindWindowW("Shell_TrayWnd", None)
    if not tray:
        return None

    result = [None]
    TARGET = {"TrayClockWClass", "ClockButton"}

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
    def cb(hwnd, _):
        buf = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(hwnd, buf, 64)
        if buf.value in TARGET:
            result[0] = hwnd
            return False
        return True

    user32.EnumChildWindows(tray, cb, 0)
    return result[0]


def clock_rect():
    """Saatin ekran koordinatlarını döndürür."""
    hwnd = find_clock_hwnd()
    if not hwnd:
        return None
    r = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(r))
    return r


def get_exe() -> str:
    return sys.executable if getattr(sys, "frozen", False) else __file__


def autostart_get() -> bool:
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_READ)
        winreg.QueryValueEx(k, REG_VALUE)
        winreg.CloseKey(k)
        return True
    except Exception:
        return False


def autostart_set(enable: bool):
    try:
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE)
        if enable:
            winreg.SetValueEx(k, REG_VALUE, 0, winreg.REG_SZ, f'"{get_exe()}"')
        else:
            try:
                winreg.DeleteValue(k, REG_VALUE)
            except FileNotFoundError:
                pass
        winreg.CloseKey(k)
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────── widget ──

class NetSpeedMonitor:
    BG    = "#111111"
    C_DL  = "#4ade80"   # yeşil  – indirme
    C_UL  = "#fb923c"   # turuncu – yükleme
    FONT  = ("Segoe UI", 9, "bold")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.withdraw()                       # başta gizli
        self.root.overrideredirect(True)           # çerçevesiz
        self.root.attributes("-topmost", True)     # her zaman üstte
        self.root.attributes("-alpha", 0.0)        # fade-in için

        # ── UI ──────────────────────────────────────────────────────────
        frame = tk.Frame(self.root, bg=self.BG)
        frame.pack(fill="both", expand=True)

        self.lbl_dl = tk.Label(frame, text="↓  ---", fg=self.C_DL,
                               bg=self.BG, font=self.FONT, anchor="e", padx=5)
        self.lbl_dl.pack(fill="x")

        self.lbl_ul = tk.Label(frame, text="↑  ---", fg=self.C_UL,
                               bg=self.BG, font=self.FONT, anchor="e", padx=5)
        self.lbl_ul.pack(fill="x")

        # ── Sürükleme ───────────────────────────────────────────────────
        self._ox = self._oy = 0
        self._moved = False
        for w in (frame, self.lbl_dl, self.lbl_ul):
            w.bind("<Button-1>",        self._drag_start)
            w.bind("<B1-Motion>",       self._drag_do)
            w.bind("<Double-Button-1>", lambda *_: self.snap())
            w.bind("<Button-3>",        self._menu_show)

        # ── Sağ-tık menüsü ──────────────────────────────────────────────
        self._auto_var = tk.BooleanVar(value=autostart_get())
        m = tk.Menu(self.root, tearoff=0, bg="#1e1e1e", fg="#eeeeee",
                    activebackground="#333", activeforeground="#fff",
                    font=("Segoe UI", 9))
        m.add_checkbutton(label="  Windows ile otomatik başlat",
                          variable=self._auto_var,
                          command=lambda: autostart_set(self._auto_var.get()))
        m.add_command(label="  Saate yapıştır  (çift tık)",
                      command=self.snap)
        m.add_separator()
        m.add_command(label="  Çıkış", command=self._quit)
        self._menu = m

        # ── Ağ ölçümü ───────────────────────────────────────────────────
        self._dl = self._ul = 0.0
        self._running = True
        threading.Thread(target=self._measure, daemon=True).start()

        # ── Başlat ──────────────────────────────────────────────────────
        self.root.after(120, self.snap)
        self.root.after(250, self._fade_in)
        self.root.after(1000, self._refresh)
        self.root.after(8000, self._reposition_loop)

    # ── konumlandırma ──────────────────────────────────────────────────
    def snap(self, *_):
        """Pencereyi saatin tam soluna yerleştirir."""
        r = clock_rect()
        if r:
            h  = r.bottom - r.top
            x  = r.left - WIDTH - GAP
            y  = r.top
            self.root.geometry(f"{WIDTH}x{h}+{x}+{y}")
        else:
            # fallback
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            self.root.geometry(f"{WIDTH}x40+{sw - WIDTH - 200}+{sh - 48}")
        self.root.deiconify()
        self._moved = False

    def _reposition_loop(self):
        if not self._moved:
            self.snap()
        self._moved = False
        self.root.after(10_000, self._reposition_loop)

    # ── sürükleme ──────────────────────────────────────────────────────
    def _drag_start(self, e):
        self._ox, self._oy = e.x, e.y

    def _drag_do(self, e):
        self._moved = True
        x = self.root.winfo_x() + e.x - self._ox
        y = self.root.winfo_y() + e.y - self._oy
        self.root.geometry(f"+{x}+{y}")

    # ── menü ───────────────────────────────────────────────────────────
    def _menu_show(self, e):
        self._auto_var.set(autostart_get())
        try:
            self._menu.tk_popup(e.x_root, e.y_root)
        finally:
            self._menu.grab_release()

    # ── ağ ─────────────────────────────────────────────────────────────
    def _measure(self):
        prev   = psutil.net_io_counters()
        prev_t = time.monotonic()
        while self._running:
            time.sleep(1)
            curr   = psutil.net_io_counters()
            curr_t = time.monotonic()
            dt     = (curr_t - prev_t) or 1
            self._dl = (curr.bytes_recv - prev.bytes_recv) / dt
            self._ul = (curr.bytes_sent - prev.bytes_sent) / dt
            prev, prev_t = curr, curr_t

    def _refresh(self):
        self.lbl_dl.config(text=f"↓ {fmt(self._dl)}")
        self.lbl_ul.config(text=f"↑ {fmt(self._ul)}")
        self.root.after(1000, self._refresh)

    # ── misc ───────────────────────────────────────────────────────────
    def _fade_in(self):
        a = float(self.root.attributes("-alpha"))
        if a < 0.9:
            self.root.attributes("-alpha", min(a + 0.12, 0.9))
            self.root.after(25, self._fade_in)

    def _quit(self):
        self._running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    NetSpeedMonitor().run()
