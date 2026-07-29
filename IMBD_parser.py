"""
IMDB Actor/Actress Parser
=========================
A Tkinter-based GUI application that fetches IMDb actor/actress data
using the Cinemagoer (IMDbPY) library and displays key information.
Results can be exported to CSV or Excel.

Dependencies: cinemagoer, pandas, openpyxl
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import re
import os
import csv
from datetime import datetime

# Third-party imports
try:
    from imdb import Cinemagoer
    import pandas as pd
except ImportError as e:
    import sys
    print(f"Missing dependency: {e}")
    print("Please install required packages:")
    print("  pip install cinemagoer pandas openpyxl")
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
#  DATA FETCHING LOGIC (using Cinemagoer — no scraping needed)
# ─────────────────────────────────────────────────────────────────────────────

def extract_person_id(url: str) -> str | None:
    """Extract the numeric person ID from an IMDb URL."""
    match = re.search(r"/name/nm(\d+)", url)
    return match.group(1) if match else None


def validate_imdb_url(url: str) -> bool:
    """Check that the URL looks like a valid IMDb person page."""
    pattern = r"https?://(www\.)?imdb\.com/name/nm\d+"
    return bool(re.match(pattern, url.strip()))


def fetch_actor_data(url: str, progress_callback=None) -> dict:
    """
    Fetch actor/actress data from IMDb using Cinemagoer.
    Returns a dict with parsed results.
    """
    person_id = extract_person_id(url)
    if not person_id:
        raise ValueError("Could not extract person ID from URL.")

    ia = Cinemagoer()

    if progress_callback:
        progress_callback("Fetching basic info...")

    # Fetch person data
    person = ia.get_person(person_id)

    if not person:
        raise ValueError(f"No person found for ID: {person_id}")

    # Update with biography details
    if progress_callback:
        progress_callback("Fetching biography & filmography...")

    try:
        ia.update(person, info=["biography"])
    except Exception:
        pass  # Biography may not always be available

    result = {
        "Name": "N/A",
        "Birthplace / Nationality": "N/A",
        "Number of Movies": "N/A",
        "Present Status / Info": "N/A",
        "Known For": "N/A",
        "Birth Date": "N/A",
        "IMDb URL": url.strip(),
        "Scraped On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # ── Name ──────────────────────────────────────────────────────────────
    result["Name"] = person.get("name", "N/A")

    # ── Birthplace ────────────────────────────────────────────────────────
    birth_info = person.get("birth info", {})
    if isinstance(birth_info, dict):
        result["Birthplace / Nationality"] = birth_info.get("birth place", "N/A")
    # Also try direct key
    if result["Birthplace / Nationality"] == "N/A":
        birth_notes = person.get("birth notes", "")
        if birth_notes:
            result["Birthplace / Nationality"] = birth_notes

    # ── Birth Date ────────────────────────────────────────────────────────
    if isinstance(birth_info, dict):
        result["Birth Date"] = birth_info.get("date", "N/A")
    if result["Birth Date"] == "N/A":
        result["Birth Date"] = person.get("birth date", "N/A")

    # ── Number of Movies ──────────────────────────────────────────────────
    filmography = person.get("filmography", [])
    total_credits = 0
    acting_credits = 0

    if isinstance(filmography, list):
        for section in filmography:
            if isinstance(section, dict):
                for role_type, movies in section.items():
                    if isinstance(movies, list):
                        total_credits += len(movies)
                        if role_type.lower() in ("actor", "actress"):
                            acting_credits += len(movies)
    elif isinstance(filmography, dict):
        for role_type, movies in filmography.items():
            if isinstance(movies, list):
                total_credits += len(movies)
                if role_type.lower() in ("actor", "actress"):
                    acting_credits += len(movies)

    if acting_credits > 0:
        result["Number of Movies"] = f"{acting_credits} (acting) / {total_credits} (total credits)"
    elif total_credits > 0:
        result["Number of Movies"] = str(total_credits)
    else:
        result["Number of Movies"] = "N/A"

    # ── Known For ─────────────────────────────────────────────────────────
    known_for = person.get("known for", [])
    if known_for:
        titles = []
        for movie in known_for[:5]:  # Top 5
            if hasattr(movie, "get"):
                title = movie.get("title", str(movie))
                year = movie.get("year", "")
                titles.append(f"{title} ({year})" if year else title)
            else:
                titles.append(str(movie))
        result["Known For"] = " • ".join(titles) if titles else "N/A"

    # ── Present Status / Bio ──────────────────────────────────────────────
    bio_texts = person.get("bio", []) or person.get("biography", [])
    mini_bio = person.get("mini biography", [])

    status_parts = []

    # Check if dead
    death_info = person.get("death info", {})
    if death_info:
        death_date = ""
        death_cause = ""
        if isinstance(death_info, dict):
            death_date = death_info.get("date", "")
            death_cause = death_info.get("cause", "")
        if death_date or death_cause:
            death_str = f"Deceased: {death_date}"
            if death_cause:
                death_str += f" ({death_cause})"
            status_parts.append(death_str)
    else:
        status_parts.append("Active")

    # Add mini bio if available
    if mini_bio and isinstance(mini_bio, list) and len(mini_bio) > 0:
        bio_text = str(mini_bio[0])
        # Truncate to 400 chars
        if len(bio_text) > 400:
            bio_text = bio_text[:400] + "..."
        status_parts.append(bio_text)
    elif bio_texts and isinstance(bio_texts, list) and len(bio_texts) > 0:
        bio_text = str(bio_texts[0])
        if len(bio_text) > 400:
            bio_text = bio_text[:400] + "..."
        status_parts.append(bio_text)

    result["Present Status / Info"] = " | ".join(status_parts) if status_parts else "N/A"

    return result


# ─────────────────────────────────────────────────────────────────────────────
#  EXPORT FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def export_to_csv(data: dict, filepath: str):
    """Export result dict to a CSV file."""
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writeheader()
        writer.writerow(data)


def export_to_excel(data: dict, filepath: str):
    """Export result dict to an Excel file (appends if file exists)."""
    df_new = pd.DataFrame([data])
    if os.path.isfile(filepath):
        try:
            df_existing = pd.read_excel(filepath, engine="openpyxl")
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except Exception:
            df_combined = df_new
    else:
        df_combined = df_new
    df_combined.to_excel(filepath, index=False, engine="openpyxl")


# ─────────────────────────────────────────────────────────────────────────────
#  TKINTER GUI
# ─────────────────────────────────────────────────────────────────────────────

class IMDbParserApp:
    """Main GUI Application for the IMDb Actor/Actress Parser."""

    # ── Color Palette ─────────────────────────────────────────────────────
    BG_DARK      = "#0f0f1a"
    BG_CARD      = "#1a1a2e"
    BG_INPUT     = "#16213e"
    ACCENT       = "#e94560"
    ACCENT_HOVER = "#ff6b81"
    TEXT_PRIMARY  = "#eaeaea"
    TEXT_MUTED    = "#8892b0"
    SUCCESS      = "#00d2d3"
    BORDER       = "#2a2a4a"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🎬 IMDb Actor/Actress Parser")
        self.root.geometry("820x720")
        self.root.minsize(750, 650)
        self.root.configure(bg=self.BG_DARK)
        self.root.resizable(True, True)

        # Try to set window icon (won't crash if missing)
        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self._setup_styles()
        self._build_ui()
        self.current_data = None

    # ── Styles ────────────────────────────────────────────────────────────
    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Dark.TFrame", background=self.BG_DARK)
        self.style.configure("Card.TFrame", background=self.BG_CARD)
        self.style.configure(
            "Title.TLabel",
            background=self.BG_DARK,
            foreground=self.ACCENT,
            font=("Segoe UI", 22, "bold"),
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=self.BG_DARK,
            foreground=self.TEXT_MUTED,
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "CardTitle.TLabel",
            background=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        )
        self.style.configure(
            "CardValue.TLabel",
            background=self.BG_CARD,
            foreground=self.SUCCESS,
            font=("Segoe UI", 11),
            wraplength=500,
        )
        self.style.configure(
            "Status.TLabel",
            background=self.BG_DARK,
            foreground=self.TEXT_MUTED,
            font=("Segoe UI", 9),
        )

    # ── Build the UI ──────────────────────────────────────────────────────
    def _build_ui(self):
        # Main container
        main = ttk.Frame(self.root, style="Dark.TFrame")
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # ── Header ────────────────────────────────────────────────────────
        ttk.Label(main, text="🎬  IMDb Parser", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            main,
            text="Enter an IMDb actor/actress profile URL to extract information",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(0, 15))

        # ── URL Input Section ─────────────────────────────────────────────
        input_frame = tk.Frame(main, bg=self.BG_CARD, highlightbackground=self.BORDER,
                               highlightthickness=1, bd=0)
        input_frame.pack(fill="x", pady=(0, 10))

        inner_input = tk.Frame(input_frame, bg=self.BG_CARD)
        inner_input.pack(fill="x", padx=15, pady=12)

        lbl = tk.Label(
            inner_input, text="🔗  IMDb Profile URL",
            bg=self.BG_CARD, fg=self.TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
        )
        lbl.pack(anchor="w")

        url_row = tk.Frame(inner_input, bg=self.BG_CARD)
        url_row.pack(fill="x", pady=(5, 0))

        self.url_entry = tk.Entry(
            url_row,
            font=("Consolas", 11),
            bg=self.BG_INPUT, fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT,
            relief="flat", bd=0,
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
        )
        self.url_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.url_entry.insert(0, "https://www.imdb.com/name/nm...")
        self.url_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.url_entry.bind("<Return>", lambda e: self._start_fetching())

        self.parse_btn = tk.Button(
            url_row, text="⚡ Parse",
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT, fg="white",
            activebackground=self.ACCENT_HOVER, activeforeground="white",
            relief="flat", bd=0, padx=20, pady=6,
            cursor="hand2",
            command=self._start_fetching,
        )
        self.parse_btn.pack(side="right", padx=(10, 0))

        # Example hint
        hint = tk.Label(
            inner_input,
            text="Example: https://www.imdb.com/name/nm0000008/",
            bg=self.BG_CARD, fg=self.TEXT_MUTED,
            font=("Segoe UI", 8),
        )
        hint.pack(anchor="w", pady=(4, 0))

        # ── Progress Bar ──────────────────────────────────────────────────
        self.progress = ttk.Progressbar(main, mode="indeterminate", length=300)

        # ── Progress Label ────────────────────────────────────────────────
        self.progress_label_var = tk.StringVar(value="")
        self.progress_label = tk.Label(
            main, textvariable=self.progress_label_var,
            bg=self.BG_DARK, fg=self.SUCCESS,
            font=("Segoe UI", 9),
        )

        # ── Results Section ───────────────────────────────────────────────
        results_header = tk.Frame(main, bg=self.BG_DARK)
        results_header.pack(fill="x", pady=(10, 5))

        tk.Label(
            results_header, text="📋  Results",
            bg=self.BG_DARK, fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 14, "bold"),
        ).pack(side="left")

        # Export buttons (hidden until results are available)
        self.export_frame = tk.Frame(results_header, bg=self.BG_DARK)
        self.export_frame.pack(side="right")

        self.csv_btn = tk.Button(
            self.export_frame, text="💾 Export CSV",
            font=("Segoe UI", 9), bg="#1e3a5f", fg=self.TEXT_PRIMARY,
            activebackground="#2a4a7f", activeforeground="white",
            relief="flat", bd=0, padx=12, pady=4, cursor="hand2",
            command=lambda: self._export("csv"),
        )

        self.excel_btn = tk.Button(
            self.export_frame, text="📊 Export Excel",
            font=("Segoe UI", 9), bg="#1a5c3a", fg=self.TEXT_PRIMARY,
            activebackground="#2a7c5a", activeforeground="white",
            relief="flat", bd=0, padx=12, pady=4, cursor="hand2",
            command=lambda: self._export("excel"),
        )

        # ── Results Cards ─────────────────────────────────────────────────
        self.results_canvas = tk.Canvas(main, bg=self.BG_DARK, highlightthickness=0)
        self.results_scrollbar = ttk.Scrollbar(main, orient="vertical",
                                                command=self.results_canvas.yview)
        self.results_inner = tk.Frame(self.results_canvas, bg=self.BG_DARK)

        self.results_inner.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all")),
        )
        self.results_canvas.create_window((0, 0), window=self.results_inner, anchor="nw")
        self.results_canvas.configure(yscrollcommand=self.results_scrollbar.set)

        self.results_canvas.pack(side="left", fill="both", expand=True, pady=(5, 0))
        self.results_scrollbar.pack(side="right", fill="y", pady=(5, 0))

        # Bind mousewheel
        self.results_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.results_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        # Placeholder text
        self.placeholder_label = tk.Label(
            self.results_inner,
            text="No results yet.\nEnter an IMDb URL and click Parse to get started.",
            bg=self.BG_DARK, fg=self.TEXT_MUTED,
            font=("Segoe UI", 11), justify="center",
        )
        self.placeholder_label.pack(pady=60)

        # ── Status Bar ────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main, textvariable=self.status_var, style="Status.TLabel")
        status_bar.pack(side="bottom", anchor="w", pady=(8, 0))

    # ── Event Handlers ────────────────────────────────────────────────────
    def _on_entry_focus_in(self, event):
        """Clear placeholder text on first focus."""
        current = self.url_entry.get()
        if current.startswith("https://www.imdb.com/name/nm..."):
            self.url_entry.delete(0, tk.END)

    def _start_fetching(self):
        """Validate URL and kick off data fetching in a background thread."""
        url = self.url_entry.get().strip()

        if not url or url.startswith("https://www.imdb.com/name/nm..."):
            messagebox.showwarning("Input Required", "Please enter a valid IMDb URL.")
            return

        if not validate_imdb_url(url):
            messagebox.showerror(
                "Invalid URL",
                "Please enter a valid IMDb actor/actress URL.\n"
                "Format: https://www.imdb.com/name/nm0000008/",
            )
            return

        # Show progress
        self.parse_btn.config(state="disabled", text="⏳ Parsing...")
        self.progress.pack(fill="x", pady=(5, 0))
        self.progress.start(15)
        self.progress_label_var.set("Connecting to IMDb...")
        self.progress_label.pack(anchor="w", pady=(2, 0))
        self.status_var.set("🔄 Fetching data from IMDb...")

        # Run in background thread to keep GUI responsive
        thread = threading.Thread(target=self._fetch_worker, args=(url,), daemon=True)
        thread.start()

    def _update_progress_text(self, text: str):
        """Update the progress label from any thread."""
        self.progress_label_var.set(text)

    def _fetch_worker(self, url: str):
        """Background worker that performs the actual data fetching."""
        try:
            data = fetch_actor_data(
                url,
                progress_callback=lambda msg: self.root.after(
                    0, self._update_progress_text, msg
                ),
            )
            self.root.after(0, self._display_results, data)
        except Exception as e:
            self.root.after(0, self._show_error, f"Error fetching data:\n{e}")

    def _show_error(self, message: str):
        """Display error and reset UI."""
        self.progress.stop()
        self.progress.pack_forget()
        self.progress_label.pack_forget()
        self.parse_btn.config(state="normal", text="⚡ Parse")
        self.status_var.set("❌ Error occurred")
        messagebox.showerror("Fetch Error", message)

    def _display_results(self, data: dict):
        """Populate the results section with fetched data."""
        self.progress.stop()
        self.progress.pack_forget()
        self.progress_label.pack_forget()
        self.parse_btn.config(state="normal", text="⚡ Parse")
        self.current_data = data

        # Show export buttons
        self.csv_btn.pack(side="left", padx=(0, 5))
        self.excel_btn.pack(side="left")

        # Clear old results
        for widget in self.results_inner.winfo_children():
            widget.destroy()

        # Display each field as a styled card
        display_fields = [
            ("🎭", "Name"),
            ("🌍", "Birthplace / Nationality"),
            ("📅", "Birth Date"),
            ("🎬", "Number of Movies"),
            ("⭐", "Known For"),
            ("📝", "Present Status / Info"),
            ("🔗", "IMDb URL"),
            ("🕐", "Scraped On"),
        ]

        for icon, key in display_fields:
            card = tk.Frame(
                self.results_inner, bg=self.BG_CARD,
                highlightbackground=self.BORDER, highlightthickness=1,
            )
            card.pack(fill="x", pady=4, padx=2)

            inner = tk.Frame(card, bg=self.BG_CARD)
            inner.pack(fill="x", padx=15, pady=10)

            # Key label
            tk.Label(
                inner, text=f"{icon}  {key}",
                bg=self.BG_CARD, fg=self.TEXT_MUTED,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            ).pack(anchor="w")

            # Value label
            value = data.get(key, "N/A")
            # Truncate long values for display
            display_value = value if len(str(value)) <= 400 else str(value)[:400] + "..."

            val_label = tk.Label(
                inner, text=display_value,
                bg=self.BG_CARD, fg=self.SUCCESS,
                font=("Segoe UI", 11),
                anchor="w", justify="left",
                wraplength=700,
            )
            val_label.pack(anchor="w", pady=(2, 0))

        self.status_var.set(
            f"✅ Successfully parsed: {data.get('Name', 'Unknown')}  |  "
            f"Ready to export"
        )

    def _export(self, fmt: str):
        """Export current data to CSV or Excel."""
        if not self.current_data:
            messagebox.showwarning("No Data", "Please parse an IMDb URL first.")
            return

        if fmt == "csv":
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                initialfile=f"imdb_{self.current_data.get('Name', 'actor').replace(' ', '_')}.csv",
                title="Save CSV File",
            )
            if filepath:
                try:
                    export_to_csv(self.current_data, filepath)
                    self.status_var.set(f"💾 Exported to {os.path.basename(filepath)}")
                    messagebox.showinfo("Success", f"Data saved to:\n{filepath}")
                except Exception as e:
                    messagebox.showerror("Export Error", str(e))

        elif fmt == "excel":
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
                initialfile=f"imdb_{self.current_data.get('Name', 'actor').replace(' ', '_')}.xlsx",
                title="Save Excel File",
            )
            if filepath:
                try:
                    export_to_excel(self.current_data, filepath)
                    self.status_var.set(f"📊 Exported to {os.path.basename(filepath)}")
                    messagebox.showinfo("Success", f"Data saved to:\n{filepath}")
                except Exception as e:
                    messagebox.showerror("Export Error", str(e))


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = IMDbParserApp(root)
    root.mainloop()
