# movie_recommendation.py
import tkinter as tk
from tkinter import ttk

class MovieRecommendation:
    def __init__(self, master):
        self.master = master
        self.create_movie_recommendation_frame()

    def create_movie_recommendation_frame(self):
        recommendation_frame = ttk.Frame(self.master)
        recommendation_frame.place(relx=0.5, rely=0.5, anchor="center")

        go_back_button = ttk.Button(recommendation_frame, text="Go back", command=self.master.create_main_menu)
        go_back_button.pack(pady=10)

        checkboxes_frame = ttk.Frame(recommendation_frame)
        checkboxes_frame.pack(pady=10)

        checkboxes = []
        for i in range(1, 11):
            checkbox = ttk.Checkbutton(checkboxes_frame, text=f"Checkbox {i}")
            checkbox.grid(row=(i-1)//2, column=(i-1)%2, padx=5, pady=5, sticky="w")
            checkboxes.append(checkbox)

