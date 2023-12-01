import tkinter as tk
from tkinter import ttk, scrolledtext
import pickle
from source.machine_learning.recommenders import get_recommendation


class MovieRecommendation:
    def __init__(self, master):
        self.master = master
        self.create_movie_recommendation_frame()

    def create_movie_recommendation_frame(self):
        recommendation_frame = ttk.Frame(self.master)
        recommendation_frame.place(relx=0.5, rely=0.5, anchor="center")

        go_back_button = ttk.Button(recommendation_frame, text="Go back", command=self.master.create_main_menu)
        go_back_button.pack(pady=10, side="bottom")

        entry_frame = ttk.Frame(recommendation_frame)
        entry_frame.pack(pady=10)

        ttk.Label(entry_frame, text='Movie title').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(entry_frame)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        submit_button = ttk.Button(recommendation_frame, text="Submit", command=lambda: self.show_result_window(entry))
        submit_button.pack(pady=10, side="top", anchor="center")

    def load_recommendation_variables(self):
        with open('data/my_variables.pkl', 'rb') as file:
            loaded_variables_dict = pickle.load(file)
        return loaded_variables_dict['indices'], loaded_variables_dict['similarity']

    def show_result_window(self, entry):
        indices, sim = self.load_recommendation_variables()
        recommendations = get_recommendation(indices, entry.get(), sim)

        self.clear_existing_content()

        result_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=60, height=20)
        result_text.pack(expand=True, fill='both')
        result_text.tag_configure("center", justify="center")

        go_back_button = ttk.Button(self.master, text="Go back", command=lambda: MovieRecommendation(self.master))
        go_back_button.pack(pady=10, side="bottom")

        result_string = recommendations.to_string(index=False)
        result_text.insert(tk.END, result_string)

    def clear_existing_content(self):
        for widget in self.master.winfo_children():
            widget.destroy()
