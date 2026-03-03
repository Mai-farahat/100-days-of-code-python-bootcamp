"""
WatermarkPro - A Tkinter desktop application to add watermarks to images.
Supports text watermarks and logo/image watermarks.
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox, font
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageEnhance
import os
import sys


# ─────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────
BG        = "#0f0f13"
PANEL     = "#1a1a24"
ACCENT    = "#7c5cfc"
ACCENT2   = "#c084fc"
TEXT      = "#e8e6f0"
SUBTEXT   = "#8b87a0"
BORDER    = "#2a2a3a"
SUCCESS   = "#34d399"
DANGER    = "#f87171"
ENTRY_BG  = "#12121a"


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WatermarkPro")
        self.geometry("1180x780")
        self.minsize(900, 640)
        self.configure(bg=BG)
        self.resizable(True, True)

        # ── State ────────────────────────────────────
        self.original_image   = None   # PIL Image (original)
        self.preview_image    = None   # PIL Image (with watermark applied)
        self.photo_image      = None   # ImageTk.PhotoImage shown in canvas
        self.logo_image       = None   # PIL Image for logo watermark
        self.logo_path_var    = tk.StringVar(value="No logo selected")
        self.wm_type          = tk.StringVar(value="text")   # "text" | "logo"
        self.wm_text          = tk.StringVar(value="© YourBrand.com")
        self.wm_color         = "#ffffff"
        self.wm_opacity       = tk.IntVar(value=70)
        self.wm_size          = tk.IntVar(value=36)
        self.wm_position      = tk.StringVar(value="bottom-right")
        self.wm_tile          = tk.BooleanVar(value=False)
        self.logo_opacity     = tk.IntVar(value=80)
        self.logo_scale       = tk.IntVar(value=20)          # % of image width
        self.input_path       = ""
        self.output_dir       = ""

        self._build_ui()

    # ──────────────────────────────────────────
    #  UI construction
    # ──────────────────────────────────────────
    def _build_ui(self):
        self._style_ttk()

        # ── Top bar ──────────────────────────────────
        topbar = tk.Frame(self, bg=PANEL, height=56)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="💧 WatermarkPro",
                 font=("Georgia", 17, "bold"), fg=ACCENT2, bg=PANEL
                 ).pack(side="left", padx=20, pady=12)

        tk.Label(topbar, text="Add text or logo watermarks to any image",
                 font=("Helvetica", 10), fg=SUBTEXT, bg=PANEL
                 ).pack(side="left", padx=4, pady=12)

        # ── Main layout ──────────────────────────────
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=0, pady=0)

        # Left sidebar (controls)
        sidebar = tk.Frame(main, bg=PANEL, width=310)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        # Right: preview + action bar
        right = tk.Frame(main, bg=BG)
        right.pack(fill="both", expand=True, side="left")

        self._build_sidebar(sidebar)
        self._build_preview(right)

    def _style_ttk(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TScale",
                        background=PANEL,
                        troughcolor=ENTRY_BG,
                        sliderlength=16)
        style.configure("TRadiobutton",
                        background=PANEL,
                        foreground=TEXT,
                        font=("Helvetica", 10))
        style.configure("TCheckbutton",
                        background=PANEL,
                        foreground=TEXT,
                        font=("Helvetica", 10))

    # ─── Sidebar ─────────────────────────────────────
    def _build_sidebar(self, parent):
        canvas = tk.Canvas(parent, bg=PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.sb_frame = tk.Frame(canvas, bg=PANEL)

        self.sb_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.sb_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        pad = {"padx": 18, "pady": 5}

        # ── Section: Image ─────────────────────────────
        self._section_label("IMAGE", self.sb_frame)

        self._accent_button(self.sb_frame, "📂  Open Image", self._open_image)\
            .pack(fill="x", **pad)

        self.img_label = tk.Label(self.sb_frame,
            text="No image loaded", font=("Helvetica", 9),
            fg=SUBTEXT, bg=PANEL, anchor="w", wraplength=250)
        self.img_label.pack(fill="x", **pad)

        self._divider(self.sb_frame)

        # ── Section: Watermark type ────────────────────
        self._section_label("WATERMARK TYPE", self.sb_frame)

        type_row = tk.Frame(self.sb_frame, bg=PANEL)
        type_row.pack(fill="x", **pad)
        ttk.Radiobutton(type_row, text="Text", variable=self.wm_type,
                        value="text", command=self._toggle_wm_type
                        ).pack(side="left", padx=(0,20))
        ttk.Radiobutton(type_row, text="Logo / Image", variable=self.wm_type,
                        value="logo", command=self._toggle_wm_type
                        ).pack(side="left")

        self._divider(self.sb_frame)

        # ── Section: Text watermark ────────────────────
        self.text_frame = tk.Frame(self.sb_frame, bg=PANEL)
        self.text_frame.pack(fill="x")

        self._section_label("TEXT WATERMARK", self.text_frame)

        self._field_label("Watermark text", self.text_frame)
        entry = tk.Entry(self.text_frame, textvariable=self.wm_text,
                         bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Helvetica", 11), bd=8)
        entry.pack(fill="x", padx=18, pady=4)
        entry.bind("<KeyRelease>", lambda e: self._refresh_preview())

        self._field_label("Font size", self.text_frame)
        self._slider_row(self.text_frame, self.wm_size, 10, 120, "pt")

        self._field_label("Text color", self.text_frame)
        self.color_btn = tk.Button(
            self.text_frame, text=f"  {self.wm_color}  ",
            bg=self.wm_color, fg=self._contrasting(self.wm_color),
            font=("Helvetica", 10), relief="flat",
            command=self._pick_color, cursor="hand2")
        self.color_btn.pack(fill="x", padx=18, pady=4)

        self._field_label("Opacity  ", self.text_frame)
        self._slider_row(self.text_frame, self.wm_opacity, 5, 100, "%")

        self._field_label("Tile across image", self.text_frame)
        ttk.Checkbutton(self.text_frame, text="Enable tiling",
                        variable=self.wm_tile,
                        command=self._refresh_preview
                        ).pack(anchor="w", padx=20)

        self._divider(self.sb_frame)

        # ── Section: Logo watermark ────────────────────
        self.logo_frame = tk.Frame(self.sb_frame, bg=PANEL)
        # not packed yet — toggled by radio

        self._section_label("LOGO WATERMARK", self.logo_frame)

        self._accent_button(self.logo_frame, "🖼️  Choose Logo", self._open_logo)\
            .pack(fill="x", padx=18, pady=4)

        tk.Label(self.logo_frame, textvariable=self.logo_path_var,
                 font=("Helvetica", 8), fg=SUBTEXT, bg=PANEL,
                 anchor="w", wraplength=240
                 ).pack(fill="x", padx=18, pady=2)

        self._field_label("Logo opacity", self.logo_frame)
        self._slider_row(self.logo_frame, self.logo_opacity, 5, 100, "%")

        self._field_label("Logo size (% of image width)", self.logo_frame)
        self._slider_row(self.logo_frame, self.logo_scale, 5, 80, "%")

        self._field_label("Tile across image", self.logo_frame)
        ttk.Checkbutton(self.logo_frame, text="Enable tiling",
                        variable=self.wm_tile,
                        command=self._refresh_preview
                        ).pack(anchor="w", padx=20)

        self._divider(self.sb_frame)

        # ── Section: Position ──────────────────────────
        self._section_label("POSITION", self.sb_frame)
        self._build_position_grid(self.sb_frame)

        self._divider(self.sb_frame)

        # ── Section: Export ────────────────────────────
        self._section_label("EXPORT", self.sb_frame)

        self._field_label("Output folder", self.sb_frame)
        dir_row = tk.Frame(self.sb_frame, bg=PANEL)
        dir_row.pack(fill="x", padx=18, pady=4)
        self.dir_label = tk.Label(dir_row,
            text="Same as source", font=("Helvetica", 9),
            fg=SUBTEXT, bg=PANEL, anchor="w")
        self.dir_label.pack(side="left", fill="x", expand=True)
        tk.Button(dir_row, text="…", bg=ENTRY_BG, fg=TEXT,
                  relief="flat", font=("Helvetica", 11),
                  command=self._pick_output_dir, cursor="hand2"
                  ).pack(side="right")

        self._accent_button(self.sb_frame, "💾  Save Watermarked Image",
                            self._save_image, primary=True)\
            .pack(fill="x", padx=18, pady=(10, 18))

    def _build_position_grid(self, parent):
        positions = [
            ("top-left",    "↖"), ("top-center",    "↑"), ("top-right",    "↗"),
            ("center-left", "←"), ("center",        "·"), ("center-right", "→"),
            ("bottom-left", "↙"), ("bottom-center", "↓"), ("bottom-right", "↘"),
        ]
        grid = tk.Frame(parent, bg=PANEL)
        grid.pack(padx=18, pady=6)

        self.pos_buttons = {}
        for i, (pos, sym) in enumerate(positions):
            btn = tk.Button(grid, text=sym, width=4, height=2,
                            bg=ACCENT if pos == self.wm_position.get() else ENTRY_BG,
                            fg=TEXT, relief="flat", font=("Helvetica", 12),
                            cursor="hand2",
                            command=lambda p=pos: self._set_position(p))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2)
            self.pos_buttons[pos] = btn

    def _set_position(self, pos):
        self.wm_position.set(pos)
        for p, b in self.pos_buttons.items():
            b.configure(bg=ACCENT if p == pos else ENTRY_BG)
        self._refresh_preview()

    # ─── Preview panel ────────────────────────────────
    def _build_preview(self, parent):
        # Action bar at bottom
        bar = tk.Frame(parent, bg=PANEL, height=52)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        tk.Label(bar, text="Preview  (live)", font=("Helvetica", 9),
                 fg=SUBTEXT, bg=PANEL).pack(side="left", padx=16, pady=14)

        self.status_label = tk.Label(bar, text="Open an image to begin",
                 font=("Helvetica", 9, "italic"), fg=SUBTEXT, bg=PANEL)
        self.status_label.pack(side="right", padx=16, pady=14)

        # Canvas
        self.canvas = tk.Canvas(parent, bg="#07070f",
                                highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True, padx=0, pady=0)

        # Placeholder text
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self._draw_placeholder()

    def _draw_placeholder(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()  or 600
        h = self.canvas.winfo_height() or 500
        self.canvas.create_text(w//2, h//2,
            text="🖼\n\nOpen an image to preview watermark",
            font=("Helvetica", 14), fill=SUBTEXT, justify="center")

    def _on_canvas_resize(self, event):
        if self.original_image:
            self._show_preview()
        else:
            self._draw_placeholder()

    # ─── Helpers ──────────────────────────────────────
    def _section_label(self, text, parent):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(fill="x", padx=18, pady=(14, 4))
        tk.Label(f, text=text, font=("Helvetica", 8, "bold"),
                 fg=ACCENT, bg=PANEL).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(side="left",
                                              fill="x", expand=True, padx=8)

    def _field_label(self, text, parent):
        tk.Label(parent, text=text, font=("Helvetica", 9),
                 fg=SUBTEXT, bg=PANEL, anchor="w"
                 ).pack(fill="x", padx=18, pady=(6, 0))

    def _divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1
                 ).pack(fill="x", padx=18, pady=10)

    def _accent_button(self, parent, text, cmd, primary=False):
        bg = ACCENT if primary else ENTRY_BG
        fg = "#ffffff" if primary else TEXT
        return tk.Button(parent, text=text, command=cmd,
                         bg=bg, fg=fg, activebackground=ACCENT2,
                         activeforeground="#fff", relief="flat",
                         font=("Helvetica", 10, "bold" if primary else "normal"),
                         pady=8, cursor="hand2")

    def _slider_row(self, parent, var, lo, hi, unit):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", padx=18, pady=4)
        val_lbl = tk.Label(row, text=f"{var.get()}{unit}",
                           font=("Helvetica", 9, "bold"),
                           fg=ACCENT2, bg=PANEL, width=5)
        val_lbl.pack(side="right")

        def _update(v):
            val_lbl.config(text=f"{int(float(v))}{unit}")
            self._refresh_preview()

        s = ttk.Scale(row, from_=lo, to=hi, orient="horizontal",
                      variable=var, command=_update)
        s.pack(side="left", fill="x", expand=True, padx=(0, 6))

    def _toggle_wm_type(self):
        if self.wm_type.get() == "text":
            self.logo_frame.pack_forget()
            self.text_frame.pack(fill="x", before=self.sb_frame.winfo_children()[
                [w for w in self.sb_frame.winfo_children()].index(self.text_frame)
                if self.text_frame in self.sb_frame.winfo_children() else 0])
            # Simpler: re-pack both in order
            self.text_frame.pack(fill="x")
        else:
            self.text_frame.pack_forget()
            self.logo_frame.pack(fill="x")
        self._refresh_preview()

    def _pick_color(self):
        color = colorchooser.askcolor(color=self.wm_color,
                                      title="Choose watermark colour")[1]
        if color:
            self.wm_color = color
            self.color_btn.configure(
                bg=color, fg=self._contrasting(color),
                text=f"  {color}  ")
            self._refresh_preview()

    def _contrasting(self, hex_color):
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return "#000000" if (r*299+g*587+b*114)/1000 > 128 else "#ffffff"

    def _pick_output_dir(self):
        d = filedialog.askdirectory(title="Choose output folder")
        if d:
            self.output_dir = d
            self.dir_label.config(text=d, fg=TEXT)

    def _set_status(self, msg, ok=True):
        self.status_label.config(text=msg, fg=SUCCESS if ok else DANGER)

    # ─── File loading ─────────────────────────────────
    def _open_image(self):
        path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
                       ("All files", "*.*")])
        if not path:
            return
        try:
            self.original_image = Image.open(path).convert("RGBA")
            self.input_path = path
            name = os.path.basename(path)
            w, h = self.original_image.size
            self.img_label.config(
                text=f"{name}  ({w}×{h}px)", fg=SUCCESS)
            self._set_status(f"Loaded: {name}")
            self._refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open image:\n{e}")

    def _open_logo(self):
        path = filedialog.askopenfilename(
            title="Choose Logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.svg *.webp"),
                       ("All files", "*.*")])
        if not path:
            return
        try:
            self.logo_image = Image.open(path).convert("RGBA")
            self.logo_path_var.set(os.path.basename(path))
            self._refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open logo:\n{e}")

    # ─── Watermark engine ─────────────────────────────
    def _apply_watermark(self, img: Image.Image) -> Image.Image:
        """Return a new RGBA image with the watermark applied."""
        result = img.copy().convert("RGBA")
        w, h = result.size

        if self.wm_type.get() == "text":
            wm_layer = self._make_text_layer(w, h)
        else:
            wm_layer = self._make_logo_layer(w, h)

        if wm_layer is None:
            return result

        result = Image.alpha_composite(result, wm_layer)
        return result

    # ── Text layer ────────────────────────────────────
    def _make_text_layer(self, w, h):
        text = self.wm_text.get().strip()
        if not text:
            return None

        opacity  = int(self.wm_opacity.get() * 255 / 100)
        size     = self.wm_size.get()
        hex_c    = self.wm_color.lstrip("#")
        r, g, b  = (int(hex_c[i:i+2], 16) for i in (0, 2, 4))
        color    = (r, g, b, opacity)

        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw  = ImageDraw.Draw(layer)

        # Try to load a nice font; fall back gracefully
        try:
            fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        except Exception:
            try:
                fnt = ImageFont.truetype("arial.ttf", size)
            except Exception:
                fnt = ImageFont.load_default()

        bbox  = draw.textbbox((0, 0), text, font=fnt)
        tw    = bbox[2] - bbox[0]
        th    = bbox[3] - bbox[1]
        pad   = max(16, size // 2)

        if self.wm_tile.get():
            step_x = tw + pad * 4
            step_y = th + pad * 3
            for y in range(-th, h + step_y, step_y):
                for x in range(-tw, w + step_x, step_x):
                    draw.text((x, y), text, font=fnt, fill=color)
        else:
            x, y = self._calc_pos(w, h, tw, th, pad)
            draw.text((x, y), text, font=fnt, fill=color)

        return layer

    # ── Logo layer ────────────────────────────────────
    def _make_logo_layer(self, w, h):
        if not self.logo_image:
            return None

        scale   = self.logo_scale.get() / 100.0
        opacity = self.logo_opacity.get() / 100.0
        lw      = int(w * scale)
        ratio   = lw / self.logo_image.width
        lh      = int(self.logo_image.height * ratio)

        logo = self.logo_image.resize((lw, lh), Image.LANCZOS).convert("RGBA")

        # Apply opacity
        r_, g_, b_, a_ = logo.split()
        a_ = a_.point(lambda p: int(p * opacity))
        logo = Image.merge("RGBA", (r_, g_, b_, a_))

        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        pad   = 16

        if self.wm_tile.get():
            step_x = lw + pad * 4
            step_y = lh + pad * 3
            for y in range(-lh, h + step_y, step_y):
                for x in range(-lw, w + step_x, step_x):
                    layer.paste(logo, (x, y), logo)
        else:
            x, y = self._calc_pos(w, h, lw, lh, pad)
            layer.paste(logo, (x, y), logo)

        return layer

    def _calc_pos(self, W, H, tw, th, pad):
        pos = self.wm_position.get()
        positions_map = {
            "top-left":      (pad,             pad),
            "top-center":    ((W-tw)//2,       pad),
            "top-right":     (W-tw-pad,        pad),
            "center-left":   (pad,             (H-th)//2),
            "center":        ((W-tw)//2,       (H-th)//2),
            "center-right":  (W-tw-pad,        (H-th)//2),
            "bottom-left":   (pad,             H-th-pad),
            "bottom-center": ((W-tw)//2,       H-th-pad),
            "bottom-right":  (W-tw-pad,        H-th-pad),
        }
        return positions_map.get(pos, (pad, pad))

    # ─── Preview ──────────────────────────────────────
    def _refresh_preview(self, *_):
        if not self.original_image:
            return
        self.preview_image = self._apply_watermark(self.original_image)
        self._show_preview()

    def _show_preview(self):
        if not self.preview_image:
            return

        cw = max(self.canvas.winfo_width(),  1)
        ch = max(self.canvas.winfo_height(), 1)

        img = self.preview_image.copy().convert("RGB")
        img.thumbnail((cw, ch), Image.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        x = cw // 2
        y = ch // 2
        self.canvas.create_image(x, y, anchor="center",
                                 image=self.photo_image)
        w, h = self.original_image.size
        self._set_status(f"Preview  ·  {w}×{h}px  ·  {self.wm_type.get()} watermark")

    # ─── Save ─────────────────────────────────────────
    def _save_image(self):
        if not self.original_image:
            messagebox.showwarning("No Image", "Please open an image first.")
            return

        result = self._apply_watermark(self.original_image)

        # Determine suggested file name
        base    = os.path.splitext(os.path.basename(self.input_path))[0]
        out_dir = self.output_dir or os.path.dirname(self.input_path) or os.path.expanduser("~")
        default = os.path.join(out_dir, f"{base}_watermarked.png")

        save_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(default),
            initialdir=out_dir,
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"),
                       ("BMP", "*.bmp"), ("All files", "*.*")],
            title="Save watermarked image")

        if not save_path:
            return

        try:
            ext = os.path.splitext(save_path)[1].lower()
            if ext in (".jpg", ".jpeg"):
                result.convert("RGB").save(save_path, quality=95)
            else:
                result.save(save_path)
            self._set_status(f"Saved → {os.path.basename(save_path)}", ok=True)
            messagebox.showinfo("Saved!",
                f"Watermarked image saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
            self._set_status("Save failed!", ok=False)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()