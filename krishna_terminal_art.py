"""
Bal Krishna Janmashtami Terminal Dot-Art
Exact 1:1 Recreation of Bal Krishna (Makhan Chor) in ANSI 24-bit TrueColor.
Zero external dependencies required (runs purely on Python standard library).

Features:
- ANSI 24-bit True Color dot rendering
- Small dot character: • (U+2022)
- Character aspect ratio compensation (~2.05)
- Dynamic Auto-Fit to exact terminal viewport to prevent scrolling
- Progressive drawing sequence across all stages
- Loads precomputed coordinates and colors from krishna_dots.json
"""

import os
import sys
import time
import json
import shutil
import argparse

# Enable UTF-8 encoding and ANSI escape sequences on Windows console
if sys.platform == "win32":
    os.system("")  # Enable VT100 / ANSI escape sequences
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

RESET = "\033[0m"
DOT = "•"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "krishna_dots.json")

def load_dots_data():
    """
    Load precomputed dot coordinates and color information from krishna_dots.json.
    """
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Could not find dot dataset at {DATA_FILE}")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    dots_raw = data.get("dots", [])
    if not dots_raw:
        raise ValueError("No dot data found in dataset.")

    min_y = min(d["y"] for d in dots_raw)
    max_y = max(d["y"] for d in dots_raw)
    min_x = min(d["x"] for d in dots_raw)
    max_x = max(d["x"] for d in dots_raw)

    h_span = max(1.0, max_y - min_y)
    w_span = max(1.0, max_x - min_x)

    processed_dots = []
    for d in dots_raw:
        ny = (d["y"] - min_y) / h_span
        nx = (d["x"] - min_x) / w_span
        r = int(d.get("r", 255))
        g = int(d.get("g", 215))
        b = int(d.get("b", 0))

        processed_dots.append({
            "stage": d.get("stage", 1),
            "stage_name": d.get("stageName", "Artwork"),
            "ny": ny,
            "nx": nx,
            "rgb": (r, g, b),
            "ansi": f"\033[38;2;{r};{g};{b}m"
        })

    # Sort strictly by stage, then top-to-bottom and left-to-right
    processed_dots.sort(key=lambda item: (item["stage"], item["ny"], item["nx"]))
    return processed_dots, h_span, w_span

def render_artwork(static_only=False, target_rows=None, target_cols=None):
    """
    Render Bal Krishna Dot-Art in ANSI 24-bit TrueColor, fitted to the terminal screen.
    """
    term_size = shutil.get_terminal_size((120, 40))
    term_cols = term_size.columns
    term_lines = term_size.lines

    dots, h_span, w_span = load_dots_data()

    # Font aspect ratio compensation (character height / width ≈ 2.05)
    char_aspect = 2.05
    art_aspect = (w_span / h_span) * char_aspect

    if target_rows is not None and target_cols is not None:
        target_h = target_rows
        target_w = target_cols
    elif target_rows is not None:
        target_h = target_rows
        target_w = int(target_h * art_aspect)
    elif target_cols is not None:
        target_w = target_cols
        target_h = int(target_w / art_aspect)
    else:
        # Auto-fit to the user's current terminal viewport
        max_h = max(24, term_lines - 3)
        target_h = min(58, max_h)
        target_w = int(target_h * art_aspect)

        # Ensure width also fits cleanly inside terminal
        if target_w > term_cols - 2:
            target_w = term_cols - 2
            target_h = int(target_w / art_aspect)

    # Center horizontally and position starting at line 1
    offset_x = max(1, (term_cols - target_w) // 2)
    offset_y = 1

    # Map dots to screen grid coordinates
    screen_dots = []
    for d in dots:
        r = int(round(d["ny"] * (target_h - 1))) + offset_y
        c = int(round(d["nx"] * (target_w - 1))) + offset_x
        screen_dots.append({
            "r": r,
            "c": c,
            "stage": d["stage"],
            "stage_name": d["stage_name"],
            "ansi": d["ansi"]
        })

    # Clear terminal screen completely and hide cursor
    os.system("cls" if os.name == "nt" else "clear")
    sys.stdout.write("\033[2J\033[H\033[?25l")
    sys.stdout.flush()

    if static_only:
        # Immediate static render
        buf = []
        for d in screen_dots:
            buf.append(f"\033[{d['r']};{d['c']}H{d['ansi']}{DOT}{RESET}")
        sys.stdout.write("".join(buf))
        sys.stdout.flush()
    else:
        # Progressive drawing animation
        batch_size = 6
        delay = 0.002

        for i in range(0, len(screen_dots), batch_size):
            batch = screen_dots[i:i + batch_size]
            buf = []
            for d in batch:
                buf.append(f"\033[{d['r']};{d['c']}H{d['ansi']}{DOT}{RESET}")
            sys.stdout.write("".join(buf))
            sys.stdout.flush()
            time.sleep(delay)

    # Position cursor safely below the artwork and restore cursor visibility
    final_row = target_h + offset_y + 1
    sys.stdout.write(f"\033[{final_row};1H\033[?25h\n")
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description="Bal Krishna Janmashtami Terminal Dot-Art")
    parser.add_argument("--static", action="store_true", help="Render static frame instantly without animation")
    parser.add_argument("--rows", type=int, default=None, help="Explicit terminal height in rows (e.g., 36, 45, 58)")
    parser.add_argument("--cols", type=int, default=None, help="Explicit terminal width in columns (e.g., 80, 120, 140)")
    args = parser.parse_args()

    render_artwork(static_only=args.static, target_rows=args.rows, target_cols=args.cols)

if __name__ == "__main__":
    main()
