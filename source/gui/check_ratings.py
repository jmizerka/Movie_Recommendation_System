# check_ratings.py
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

class CheckRatings:
    def __init__(self, master):
        self.master = master
        self.create_check_ratings_frame()

    def create_check_ratings_frame(self):
        check_ratings_frame = ttk.Frame(self.master)
        check_ratings_frame.place(relx=0.5, rely=0.5, anchor="center")

        ratings_data = pd.DataFrame({
            'Movie': [f'{i}' for i in np.arange(1, 1000)],
            'Rating': [i for i in np.arange(1, 1000)],
            'Date': [np.random.randint(2015, 2023) for i in np.arange(1, 1000)],
        })

        text_widget = tk.Text(check_ratings_frame, wrap='none', height=80, width=180)
        text_widget.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")

        text_widget.tag_configure("center", justify='center', spacing1=20, spacing3=20, spacing2=20, font=('Helvetica', 16))
        text_widget.insert('1.0', ratings_data.to_string(index=False), "center")

        go_back_button = ttk.Button(check_ratings_frame, text="Go back", command=self.master.create_main_menu)
        go_back_button.grid(row=1, column=0, pady=20, sticky="s")

        check_ratings_frame.grid_rowconfigure(0, weight=1)
        check_ratings_frame.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
