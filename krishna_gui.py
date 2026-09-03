"""
Bal Krishna Janmashtami Native Desktop App (Tkinter)
Exact 1:1 glowing dot-art rendering with 21-stage animation and smooth playback.
Zero dependencies required (pure Python standard library).
"""

import os
import sys
import json
import math
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "krishna_dots.json")

class KrishnaDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Happy Krishna Janmashtami • Divine Glowing Dot Art")
        self.root.geometry("1100x880")
        self.root.configure(bg="#030408")

        # Load dot data
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.dots = self.data["dots"]
        self.total_dots = len(self.dots)
        self.base_w = self.data["width"]
        self.base_h = self.data["height"]

        self.current_idx = 0
        self.is_playing = True
        self.speed = 1.0
        self.dots_per_frame = 5

        self.setup_ui()
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Button-1>", self.on_click)
        self.root.bind("<space>", lambda e: self.toggle_play())
        self.root.bind("<r>", lambda e: self.replay())
        self.root.bind("<R>", lambda e: self.replay())
        self.animate()

    def setup_ui(self):
        # Header / HUD
        self.hud_frame = tk.Frame(self.root, bg="#0a0e1a", highlightbackground="#ffd700", highlightthickness=1)
        self.hud_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=12)

        self.lbl_title = tk.Label(self.hud_frame, text="✨ BAL KRISHNA JANMASHTAMI • 21-STAGE REVEAL",
                                  font=("Segoe UI", 12, "bold"), fg="#ffd700", bg="#0a0e1a")
        self.lbl_title.pack(side=tk.LEFT, padx=16, pady=8)

        self.lbl_stage = tk.Label(self.hud_frame, text="Stage 1: Outer Silhouette (Krishna + Pot)",
                                  font=("Segoe UI", 10), fg="#50c8ff", bg="#0a0e1a")
        self.lbl_stage.pack(side=tk.RIGHT, padx=16, pady=8)

        # Canvas (Fills entire screen)
        self.canvas = tk.Canvas(self.root, bg="#030408", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

    def on_click(self, event):
        if self.current_idx >= self.total_dots:
            self.replay()
        else:
            self.toggle_play()

    def on_resize(self, event=None):
        if event and event.widget != self.root:
            return
        self.redraw_all()

    def toggle_play(self):
        self.is_playing = not self.is_playing

    def replay(self):
        self.current_idx = 0
        self.is_playing = True
        self.canvas.delete("all")

    def get_scale_and_offsets(self):
        cw = max(100, self.canvas.winfo_width())
        ch = max(100, self.canvas.winfo_height())
        scale = min((cw - 40) / self.base_w, (ch - 40) / self.base_h)
        ox = (cw - self.base_w * scale) / 2
        oy = (ch - self.base_h * scale) / 2
        return scale, ox, oy

    def redraw_all(self):
        self.canvas.delete("all")
        scale, ox, oy = self.get_scale_and_offsets()
        r_size = max(2, 2.3 * scale)

        for i in range(self.current_idx):
            d = self.dots[i]
            sx = ox + d["x"] * scale
            sy = oy + d["y"] * scale
            color_hex = f"#{d['r']:02x}{d['g']:02x}{d['b']:02x}"
            self.canvas.create_oval(sx - r_size, sy - r_size, sx + r_size, sy + r_size,
                                   fill=color_hex, outline="")

    def animate(self):
        if self.is_playing and self.current_idx < self.total_dots:
            scale, ox, oy = self.get_scale_and_offsets()
            r_size = max(2, 2.3 * scale)

            step = math.ceil(self.dots_per_frame * self.speed)
            end_idx = min(self.total_dots, self.current_idx + step)
            for i in range(self.current_idx, end_idx):
                d = self.dots[i]
                sx = ox + d["x"] * scale
                sy = oy + d["y"] * scale
                color_hex = f"#{d['r']:02x}{d['g']:02x}{d['b']:02x}"
                self.canvas.create_oval(sx - r_size, sy - r_size, sx + r_size, sy + r_size,
                                       fill=color_hex, outline="")

            self.current_idx = end_idx

            if self.current_idx > 0:
                cur_dot = self.dots[min(self.current_idx - 1, self.total_dots - 1)]
                self.lbl_stage.configure(text=f"{cur_dot['stage']}. {cur_dot['stageName']}")

            if self.current_idx >= self.total_dots:
                self.is_playing = False

        self.root.after(16, self.animate)

def main():
    root = tk.Tk()
    app = KrishnaDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
