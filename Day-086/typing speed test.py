import tkinter as tk
from tkinter import font
import time
import random

# ── Text samples ──────────────────────────────────────────────────────────────
SAMPLES = [
    "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump.",
    "To be or not to be, that is the question. Whether 'tis nobler in the mind to suffer the slings and arrows of outrageous fortune.",
    "Space, the final frontier. These are the voyages of the starship Enterprise. Its continuing mission to explore strange new worlds.",
    "In the beginning God created the heavens and the earth. The earth was formless and empty, darkness was over the surface of the deep.",
    "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief.",
    "All happy families are alike; each unhappy family is unhappy in its own way. Everything was in confusion in the Oblonskys' house.",
    "Call me Ishmael. Some years ago, never mind how long precisely, having little money in my purse, I thought I would sail about a little.",
    "It is a truth universally acknowledged that a single man in possession of a good fortune must be in want of a wife.",
    "The sky above the port was the color of television, tuned to a dead channel. All the neon was reflected in the black mirror of the bay.",
    "Far out in the uncharted backwaters of the unfashionable end of the western spiral arm of the Galaxy lies a small unregarded yellow sun.",
]

# ── Color palette ─────────────────────────────────────────────────────────────
BG          = "#0d0f12"
PANEL       = "#13161c"
BORDER      = "#1e2330"
ACCENT      = "#e2b96f"          # warm amber
ACCENT2     = "#5b8af0"          # cool blue
CORRECT     = "#4ade80"          # green
ERROR       = "#f87171"          # red
MUTED       = "#4a5568"
TEXT_DARK   = "#1a1d24"
WHITE       = "#f0f4ff"
SUBTEXT     = "#7a8299"

SPEEDS = [
    (0,  "Beginner",   ERROR),
    (20, "Slow",       "#fb923c"),
    (40, "Average",    ACCENT),
    (70, "Fast",       ACCENT2),
    (100,"Pro",        CORRECT),
    (130,"Elite",      "#c084fc"),
]

def speed_label(wpm):
    label, color = SPEEDS[0][1], SPEEDS[0][2]
    for threshold, lbl, clr in SPEEDS:
        if wpm >= threshold:
            label, color = lbl, clr
    return label, color


class TypingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TypeTrainer")
        self.geometry("860x660")
        self.resizable(False, False)
        self.configure(bg=BG)

        # State
        self.start_time   = None
        self.running      = False
        self.current_text = ""
        self.high_scores  = []   # list of wpm ints

        # Fonts
        self.font_mono   = font.Font(family="Courier", size=15, weight="normal")
        self.font_label  = font.Font(family="Helvetica", size=11, weight="bold")
        self.font_large  = font.Font(family="Helvetica", size=36, weight="bold")
        self.font_small  = font.Font(family="Helvetica", size=10)
        self.font_title  = font.Font(family="Helvetica", size=20, weight="bold")

        self._build_ui()
        self._new_text()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ──
        top = tk.Frame(self, bg=BG, pady=18)
        top.pack(fill="x", padx=30)

        tk.Label(top, text="TYPE", bg=BG, fg=ACCENT,
                 font=self.font_title).pack(side="left")
        tk.Label(top, text="TRAINER", bg=BG, fg=WHITE,
                 font=self.font_title).pack(side="left")

        self.hs_label = tk.Label(top, text="🏆  —", bg=BG, fg=SUBTEXT,
                                  font=self.font_label)
        self.hs_label.pack(side="right")

        # ── Stats row ──
        stats = tk.Frame(self, bg=BG)
        stats.pack(fill="x", padx=30, pady=(0, 14))

        self.wpm_var  = tk.StringVar(value="—")
        self.acc_var  = tk.StringVar(value="—")
        self.time_var = tk.StringVar(value="0s")

        for label, var, col in [
            ("WPM",      self.wpm_var,  ACCENT),
            ("ACCURACY", self.acc_var,  ACCENT2),
            ("TIME",     self.time_var, WHITE),
        ]:
            box = tk.Frame(stats, bg=PANEL, bd=0,
                           highlightbackground=BORDER, highlightthickness=1)
            box.pack(side="left", padx=(0, 12), ipadx=18, ipady=10)
            tk.Label(box, textvariable=var, bg=PANEL, fg=col,
                     font=self.font_large).pack()
            tk.Label(box, text=label, bg=PANEL, fg=SUBTEXT,
                     font=self.font_small).pack()

        # ── Sample text display ──
        txt_frame = tk.Frame(self, bg=PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        txt_frame.pack(fill="x", padx=30, pady=(0, 14))

        self.sample_box = tk.Text(
            txt_frame, wrap="word", height=4,
            bg=PANEL, fg=MUTED,
            insertbackground=ACCENT,
            font=self.font_mono,
            padx=18, pady=14,
            bd=0, relief="flat",
            state="disabled",
            cursor="arrow",
            selectbackground=PANEL,
        )
        self.sample_box.pack(fill="x")
        self.sample_box.tag_config("correct", foreground=CORRECT)
        self.sample_box.tag_config("error",   foreground=ERROR,
                                   background="#2d1515")
        self.sample_box.tag_config("current", foreground=WHITE,
                                   underline=True)
        self.sample_box.tag_config("pending", foreground=MUTED)

        # ── Input area ──
        inp_frame = tk.Frame(self, bg=PANEL,
                             highlightbackground=BORDER, highlightthickness=1)
        inp_frame.pack(fill="x", padx=30, pady=(0, 14))

        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self._on_type)

        self.entry = tk.Entry(
            inp_frame,
            textvariable=self.entry_var,
            bg=PANEL, fg=WHITE,
            insertbackground=ACCENT,
            font=self.font_mono,
            bd=0, relief="flat",
        )
        self.entry.pack(fill="x", ipady=14, padx=18)
        self.entry.bind("<space>", self._on_space)
        self.entry.bind("<Return>", lambda e: self._restart())

        # ── Progress bar ──
        prog_bg = tk.Frame(self, bg=BORDER, height=4)
        prog_bg.pack(fill="x", padx=30, pady=(0, 14))
        self.prog_fill = tk.Frame(prog_bg, bg=ACCENT, height=4)
        self.prog_fill.place(x=0, y=0, relheight=1, width=0)
        self._prog_width = 0

        # ── Buttons ──
        btn_row = tk.Frame(self, bg=BG)
        btn_row.pack(pady=4)

        for txt, cmd, fg, bg_c in [
            ("NEW TEXT",  self._new_text,  TEXT_DARK, ACCENT),
            ("RESTART",   self._restart,   WHITE,     BORDER),
        ]:
            tk.Button(
                btn_row, text=txt, command=cmd,
                bg=bg_c, fg=fg,
                activebackground=ACCENT, activeforeground=TEXT_DARK,
                font=self.font_label,
                bd=0, padx=24, pady=10,
                cursor="hand2", relief="flat",
            ).pack(side="left", padx=6)

        # ── High-score table ──
        tk.Label(self, text="RECENT SCORES", bg=BG, fg=SUBTEXT,
                 font=self.font_small).pack(pady=(18, 4))

        self.score_frame = tk.Frame(self, bg=BG)
        self.score_frame.pack()

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Start typing to begin…")
        tk.Label(self, textvariable=self.status_var,
                 bg=BG, fg=SUBTEXT, font=self.font_small).pack(pady=(12, 0))

    # ── Text management ───────────────────────────────────────────────────────

    def _new_text(self):
        self.current_text = random.choice(SAMPLES)
        self._restart()

    def _restart(self):
        self.start_time = None
        self.running    = False
        self.entry_var.set("")
        self.wpm_var.set("—")
        self.acc_var.set("—")
        self.time_var.set("0s")
        self.status_var.set("Start typing to begin…")
        self._render_sample(0)
        self._set_progress(0)
        self.entry.config(state="normal",
                          highlightbackground=BORDER,
                          highlightthickness=1)
        self.entry.focus_set()

    # ── Rendering ─────────────────────────────────────────────────────────────

    def _render_sample(self, typed_len):
        text = self.current_text
        typed = self.entry_var.get()

        self.sample_box.config(state="normal")
        self.sample_box.delete("1.0", "end")
        self.sample_box.insert("end", text)

        # Colour each typed character
        for i, ch in enumerate(typed[:len(text)]):
            start = f"1.{i}"
            end   = f"1.{i+1}"
            tag   = "correct" if ch == text[i] else "error"
            self.sample_box.tag_add(tag, start, end)

        # Underline cursor position
        cur = len(typed)
        if cur < len(text):
            self.sample_box.tag_add("current", f"1.{cur}", f"1.{cur+1}")

        self.sample_box.config(state="disabled")

    def _set_progress(self, fraction):
        self._prog_width = fraction
        total = 800  # approx pixel width
        self.prog_fill.place(width=int(total * fraction))

    # ── Typing logic ──────────────────────────────────────────────────────────

    def _on_type(self, *_):
        typed = self.entry_var.get()
        text  = self.current_text

        if not typed:
            return

        # Start timer on first keystroke
        if not self.running:
            self.running    = True
            self.start_time = time.time()
            self._tick()

        self._render_sample(len(typed))

        # Progress
        progress = min(len(typed) / len(text), 1.0)
        self._set_progress(progress)

        # Live stats
        elapsed = time.time() - self.start_time
        words   = len(typed.split())
        wpm     = int(words / elapsed * 60) if elapsed > 0 else 0

        correct = sum(1 for a, b in zip(typed, text) if a == b)
        acc     = int(correct / len(typed) * 100) if typed else 100

        self.wpm_var.set(str(wpm))
        self.acc_var.set(f"{acc}%")

        lbl, color = speed_label(wpm)
        self.status_var.set(f"{lbl}  ·  keep going…")

        # Finished?
        if len(typed) >= len(text):
            self._finish(wpm, acc, elapsed)

    def _on_space(self, event):
        # Allow normal space; just used for live feedback
        pass

    def _tick(self):
        if self.running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_var.set(f"{elapsed}s")
            self.after(1000, self._tick)

    def _finish(self, wpm, acc, elapsed):
        self.running = False
        self.entry.config(state="disabled")

        lbl, color = speed_label(wpm)

        self.high_scores.append(wpm)
        self.high_scores.sort(reverse=True)
        best = self.high_scores[0]
        self.hs_label.config(text=f"🏆  {best} WPM")

        self.status_var.set(
            f"✓ Done!  {wpm} WPM  ·  {acc}% accuracy  ·  "
            f"{elapsed:.1f}s  ·  {lbl}"
        )
        self._set_progress(1.0)
        self._update_scoreboard()

    def _update_scoreboard(self):
        for w in self.score_frame.winfo_children():
            w.destroy()

        top5 = self.high_scores[:5]
        for rank, wpm in enumerate(top5, 1):
            lbl, color = speed_label(wpm)
            row = tk.Frame(self.score_frame, bg=BG)
            row.pack(side="left", padx=10)
            tk.Label(row, text=f"#{rank}", bg=BG, fg=SUBTEXT,
                     font=self.font_small).pack()
            tk.Label(row, text=f"{wpm}", bg=BG, fg=color,
                     font=self.font_label).pack()
            tk.Label(row, text="WPM", bg=BG, fg=SUBTEXT,
                     font=self.font_small).pack()


if __name__ == "__main__":
    app = TypingApp()
    app.mainloop()