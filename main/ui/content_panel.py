import tkinter as tk
from functools import partial

from theme import (
    APP_BACKGROUND,
    BORDER,
    PRIMARY,
    PRIMARY_LIGHT,
    SURFACE,
    SURFACE_MUTED,
    TEXT_DARK,
    TEXT_MUTED,
)


class ContentPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=APP_BACKGROUND)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_menu = tk.Frame(
            self,
            bg=PRIMARY_LIGHT,
            height=55,
        )
        self.top_menu.grid(row=0, column=0, sticky="ew")
        self.top_menu.grid_propagate(False)

        self.menu_names = [
            "Overview",
            "Details",
            "Tools",
            "Settings",
        ]

        for menu_name in self.menu_names:
            menu_button = tk.Button(
                self.top_menu,
                text=menu_name,
                command=partial(self.show_menu, menu_name),
                bg=PRIMARY_LIGHT,
                fg=TEXT_DARK,
                activebackground=PRIMARY,
                activeforeground=TEXT_DARK,
                relief="flat",
                font=("Segoe UI", 10),
                padx=20,
            )
            menu_button.pack(side="left", fill="y")

        self.content_area = tk.Frame(
            self,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.content_area.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=25,
            pady=25,
        )

        self.content_area.grid_rowconfigure(1, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.page_title = tk.Label(
            self.content_area,
            text="Dashboard",
            bg=SURFACE,
            fg=TEXT_DARK,
            font=("Segoe UI", 26, "bold"),
            anchor="w",
        )
        self.page_title.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=30,
            pady=(30, 10),
        )

        self.page_content = tk.Label(
            self.content_area,
            text="Welcome to your first Python GUI.\n\n"
            "Click a tile on the left to change this area.",
            bg=SURFACE,
            fg=TEXT_MUTED,
            font=("Segoe UI", 13),
            justify="left",
            anchor="nw",
        )
        self.page_content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=10,
        )

        self.status_bar = tk.Label(
            self,
            text="Ready",
            bg=SURFACE_MUTED,
            fg=TEXT_MUTED,
            font=("Segoe UI", 9),
            anchor="w",
            padx=12,
            pady=7,
        )
        self.status_bar.grid(row=2, column=0, sticky="ew")

    def show_page(self, page_name):
        self.page_title.config(text=page_name)
        self.page_content.config(
            text=f"You are viewing the {page_name} page.\n\n"
            "The controls and information for this page will go here."
        )
        self.status_bar.config(text=f"Opened {page_name}")

    def show_menu(self, menu_name):
        self.page_content.config(
            text=f"The {menu_name} menu is selected."
        )
        self.status_bar.config(text=f"Selected {menu_name}")
