import tkinter as tk
from functools import partial

from theme import (
    SIDEBAR_BACKGROUND,
    SIDEBAR_TILE,
    SIDEBAR_TILE_HOVER,
    SIDEBAR_TILE_SELECTED,
    TEXT_DARK,
    TEXT_LIGHT,
)


class Sidebar(tk.Frame):
    def __init__(self, parent, page_command):
        super().__init__(parent, width=250, bg=SIDEBAR_BACKGROUND)

        self.page_command = page_command
        self.tile_buttons = {}
        self.grid_propagate(False)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            self,
            text="MY PROJECT",
            bg=SIDEBAR_BACKGROUND,
            fg=TEXT_LIGHT,
            font=("Segoe UI", 18, "bold"),
            pady=20,
        )
        self.title_label.grid(row=0, column=0, sticky="ew")
        self.title_label.bind("<MouseWheel>", self.scroll_with_mousewheel)

        self.scroll_area = tk.Canvas(
            self,
            bg=SIDEBAR_BACKGROUND,
            highlightthickness=0,
        )
        self.scroll_area.grid(row=1, column=0, sticky="nsew")
        self.scroll_area.bind("<MouseWheel>", self.scroll_with_mousewheel)

        self.scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.scroll_area.yview,
        )
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.scroll_area.configure(
            yscrollcommand=self.scrollbar.set,
        )

        self.tile_container = tk.Frame(
            self.scroll_area,
            bg=SIDEBAR_BACKGROUND,
        )
        self.tile_container.bind(
            "<MouseWheel>",
            self.scroll_with_mousewheel,
        )

        self.tile_window = self.scroll_area.create_window(
            (0, 0),
            window=self.tile_container,
            anchor="nw",
        )

        self.tile_container.bind(
            "<Configure>",
            self.update_scroll_region,
        )

        self.scroll_area.bind(
            "<Configure>",
            self.resize_tile_container,
        )

        self.pages = [
            "Dashboard",
            "People",
            "Projects",
            "Calendar",
            "Reports",
            "Documents",
            "Messages",
            "Statistics",
            "Archive",
            "Settings",
            "Help",
            "About",
        ]

        for page_name in self.pages:
            tile = tk.Button(
                self.tile_container,
                text=page_name,
                command=partial(self.select_page, page_name),
                bg=SIDEBAR_TILE,
                fg=TEXT_LIGHT,
                activebackground=SIDEBAR_TILE_HOVER,
                activeforeground=TEXT_LIGHT,
                relief="flat",
                anchor="w",
                font=("Segoe UI", 11, "bold"),
                padx=18,
                pady=14,
                cursor="hand2",
            )
            tile.pack(fill="x", padx=12, pady=5)
            tile.bind("<MouseWheel>", self.scroll_with_mousewheel)
            self.tile_buttons[page_name] = tile

        self.select_page("Dashboard")

    def select_page(self, page_name):
        for tile_name, tile_button in self.tile_buttons.items():
            if tile_name == page_name:
                tile_button.configure(
                    bg=SIDEBAR_TILE_SELECTED,
                    fg=TEXT_DARK,
                )
            else:
                tile_button.configure(
                    bg=SIDEBAR_TILE,
                    fg=TEXT_LIGHT,
                )

        self.page_command(page_name)

    def update_scroll_region(self, event):
        self.scroll_area.configure(
            scrollregion=self.scroll_area.bbox("all")
        )

    def resize_tile_container(self, event):
        self.scroll_area.itemconfigure(
            self.tile_window,
            width=event.width,
        )

    def scroll_with_mousewheel(self, event):
        if event.delta > 0:
            self.scroll_area.yview_scroll(-3, "units")
        elif event.delta < 0:
            self.scroll_area.yview_scroll(3, "units")

        return "break"