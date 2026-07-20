import tkinter as tk
from pathlib import Path

from theme import APP_BACKGROUND
from ui.content_panel import ContentPanel
from ui.sidebar import Sidebar


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        icon_path = Path(__file__).parent / "assets" / "app_icon.png"

        self.title("Charms Check DB Manager")

        if icon_path.exists():
            self.app_icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, self.app_icon)

        self.geometry("1100x700")
        self.minsize(800, 500)
        self.configure(bg=APP_BACKGROUND)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.content_panel = ContentPanel(self)
        self.content_panel.grid(row=0, column=1, sticky="nsew")

        self.sidebar = Sidebar(
            self,
            page_command=self.content_panel.show_page,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")
