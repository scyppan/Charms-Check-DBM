import re
import tkinter as tk
from functools import partial
from tkinter import messagebox

from preferences.defaults import THEME_COLOR_FIELDS
from shared.widgets import RoundedEntry
from shared.widgets.controls import rounded_points
from theme import (
    BORDER,
    FIELD_FOCUS,
    SURFACE,
    TEXT_DARK,
    TEXT_MUTED,
)


HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


class ColorSwatch(tk.Canvas):
    def __init__(self, parent, color):
        super().__init__(
            parent,
            bg=SURFACE,
            width=52,
            height=34,
            highlightthickness=0,
            borderwidth=0,
        )

        self.shape = self.create_polygon(
            rounded_points(52, 34, 8),
            smooth=True,
            splinesteps=24,
            fill=color,
            outline=BORDER,
            width=1,
        )
        self.bind("<Configure>", self.handle_resize)

    def handle_resize(self, event):
        self.coords(
            self.shape,
            *rounded_points(event.width, event.height, 8),
        )

    def set_color(self, color, valid):
        if valid:
            self.itemconfigure(
                self.shape,
                fill=color,
                outline=BORDER,
                width=1,
            )
        else:
            self.itemconfigure(
                self.shape,
                fill=SURFACE,
                outline="#A04C3F",
                width=2,
            )


class ThemeSettingsView(tk.Frame):
    def __init__(self, parent, controller, dirty_command):
        super().__init__(parent, bg=SURFACE)

        self.controller = controller
        self.dirty_command = dirty_command
        self.loading_settings = False
        self.form_dirty = False
        self.color_values = {}
        self.color_entries = {}
        self.color_swatches = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.introduction = tk.Label(
            self,
            text=(
                "Edit any palette color using a six-digit hex value. "
                "Saved colors apply the next time the application starts."
            ),
            bg=SURFACE,
            fg=TEXT_MUTED,
            font=("Segoe UI", 10),
            justify="left",
            anchor="w",
        )
        self.introduction.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(24, 12),
        )

        self.scroll_area = tk.Canvas(
            self,
            bg=SURFACE,
            highlightthickness=0,
            borderwidth=0,
        )
        self.scroll_area.grid(row=1, column=0, sticky="nsew")
        self.scroll_area.bind("<Configure>", self.resize_fields_frame)
        self.scroll_area.bind("<MouseWheel>", self.scroll_with_mousewheel)

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.scroll_area.yview,
            relief="flat",
            borderwidth=0,
        )
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 10))
        self.scroll_area.configure(yscrollcommand=self.scrollbar.set)

        self.fields_frame = tk.Frame(self.scroll_area, bg=SURFACE)
        self.fields_frame.grid_columnconfigure(1, weight=1)
        self.fields_frame.bind("<Configure>", self.update_scroll_region)
        self.fields_frame.bind("<MouseWheel>", self.scroll_with_mousewheel)
        self.fields_window = self.scroll_area.create_window(
            (0, 0),
            window=self.fields_frame,
            anchor="nw",
        )

        self.build_color_fields()
        self.load_values()

    def build_color_fields(self):
        current_category = None
        row_index = 0

        for category, field_key, label_text, default_value in THEME_COLOR_FIELDS:
            if category != current_category:
                category_label = tk.Label(
                    self.fields_frame,
                    text=category,
                    bg=SURFACE,
                    fg=TEXT_DARK,
                    font=("Segoe UI", 14, "bold"),
                    anchor="w",
                )
                category_label.grid(
                    row=row_index,
                    column=0,
                    columnspan=3,
                    sticky="ew",
                    padx=30,
                    pady=(18 if row_index else 6, 8),
                )
                category_label.bind(
                    "<MouseWheel>",
                    self.scroll_with_mousewheel,
                )
                current_category = category
                row_index += 1

            field_label = tk.Label(
                self.fields_frame,
                text=f"{label_text}  ({field_key})",
                bg=SURFACE,
                fg=TEXT_DARK,
                font=("Segoe UI", 10),
                anchor="w",
            )
            field_label.grid(
                row=row_index,
                column=0,
                sticky="ew",
                padx=(30, 20),
                pady=5,
            )
            field_label.bind(
                "<MouseWheel>",
                self.scroll_with_mousewheel,
            )

            color_value = tk.StringVar(value=default_value)
            color_value.trace_add(
                "write",
                partial(self.handle_color_change, field_key),
            )
            color_entry = RoundedEntry(
                self.fields_frame,
                textvariable=color_value,
                background=SURFACE,
                width=190,
                height=38,
                font=("Consolas", 11),
            )
            color_entry.grid(
                row=row_index,
                column=1,
                sticky="ew",
                padx=(0, 12),
                pady=5,
            )
            color_entry.bind_input(
                "<MouseWheel>",
                self.scroll_with_mousewheel,
            )

            color_swatch = ColorSwatch(self.fields_frame, default_value)
            color_swatch.grid(
                row=row_index,
                column=2,
                padx=(0, 30),
                pady=5,
            )
            color_swatch.bind(
                "<MouseWheel>",
                self.scroll_with_mousewheel,
            )

            self.color_values[field_key] = color_value
            self.color_entries[field_key] = color_entry
            self.color_swatches[field_key] = color_swatch
            row_index += 1

        self.bottom_spacer = tk.Frame(
            self.fields_frame,
            bg=SURFACE,
            height=24,
        )
        self.bottom_spacer.grid(
            row=row_index,
            column=0,
            columnspan=3,
            sticky="ew",
        )

    def load_values(self):
        theme_values = self.controller.load_theme_settings()
        self.loading_settings = True

        for field_key, color_value in self.color_values.items():
            saved_value = theme_values.get(field_key, color_value.get())
            color_value.set(saved_value)
            is_valid = HEX_COLOR_PATTERN.fullmatch(saved_value) is not None
            self.color_swatches[field_key].set_color(saved_value, is_valid)

        self.loading_settings = False
        self.form_dirty = False

        return "Theme colors loaded"

    def save_values(self):
        theme_values = {}
        invalid_fields = []

        for field_key, color_value in self.color_values.items():
            cleaned_value = color_value.get().strip().upper()

            if not HEX_COLOR_PATTERN.fullmatch(cleaned_value):
                invalid_fields.append(field_key)
                continue

            theme_values[field_key] = cleaned_value

        if invalid_fields:
            messagebox.showerror(
                "Invalid theme color",
                (
                    "Every theme color must use the format #RRGGBB.\n\n"
                    f"Check: {', '.join(invalid_fields)}"
                ),
                parent=self,
            )
            return False

        self.controller.save_theme_settings(theme_values)
        self.loading_settings = True

        for field_key, cleaned_value in theme_values.items():
            self.color_values[field_key].set(cleaned_value)

        self.loading_settings = False
        self.form_dirty = False

        return "Theme saved. Restart the application to apply the colors."

    def handle_color_change(self, field_key, *arguments):
        color_value = self.color_values[field_key].get().strip()
        is_valid = HEX_COLOR_PATTERN.fullmatch(color_value) is not None
        self.color_swatches[field_key].set_color(color_value, is_valid)

        if self.loading_settings:
            return

        self.form_dirty = True
        self.dirty_command()

    def has_unsaved_changes(self):
        return self.form_dirty

    def update_scroll_region(self, event):
        self.scroll_area.configure(
            scrollregion=self.scroll_area.bbox("all")
        )

    def resize_fields_frame(self, event):
        self.scroll_area.itemconfigure(
            self.fields_window,
            width=event.width,
        )

    def scroll_with_mousewheel(self, event):
        if event.delta > 0:
            self.scroll_area.yview_scroll(-3, "units")
        elif event.delta < 0:
            self.scroll_area.yview_scroll(3, "units")

        return "break"
