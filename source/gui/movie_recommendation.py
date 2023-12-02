import tkinter as tk
from tkinter import ttk, scrolledtext
import pickle
from source.machine_learning.recommenders import get_recommendation


class MovieRecommendation:
    # Initialize the class with the master window
    def __init__(self, master):
        self.master = master
        self.create_movie_recommendation_frame()

    # Method to create the main recommendation frame
    def create_movie_recommendation_frame(self):
        recommendation_frame = ttk.Frame(self.master)
        recommendation_frame.place(relx=0.5, rely=0.5, anchor="center")

        # create go back button that calls the create main_menu method of the master window
        go_back_button = ttk.Button(recommendation_frame, text="Go back", command=self.master.create_main_menu)
        go_back_button.pack(pady=10, side="bottom")

        # create an etry frame to take user input (title of a movie)
        entry_frame = ttk.Frame(recommendation_frame)
        entry_frame.pack(pady=10)

        # Add a label and an entry widget for the movie title
        ttk.Label(entry_frame, text='Movie title').grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry = ttk.Entry(entry_frame)
        entry.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # create a submit button that calls the show_result_window method with the entered movie title
        submit_button = ttk.Button(recommendation_frame, text="Submit", command=lambda: self.show_result_window(entry))
        submit_button.pack(pady=10, side="top", anchor="center")

    # static method to load recommendation algorithm from a pickled file
    @staticmethod
    def load_recommendation_variables():
        with open('data/my_variables.pkl', 'rb') as file:
            loaded_variables_dict = pickle.load(file)
        return loaded_variables_dict['indices'], loaded_variables_dict['similarity']

    # method to display the result window with movie recommendations
    def show_result_window(self, entry):
        # load recommendation algorithm
        indices, sim = self.load_recommendation_variables()

        # get movie recommendation based on entered title
        recommendations = get_recommendation(indices, entry.get(), sim)

        # clear existing content in the master window
        self.clear_existing_content()

        # create a scrolled text widget with recommendations
        result_text = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=60, height=20)
        result_text.pack(expand=True, fill='both')
        result_text.tag_configure("center", justify="center")

        # create a go back button that creates a new MovieRecommendation instance
        go_back_button = ttk.Button(self.master, text="Go back", command=lambda: MovieRecommendation(self.master))
        go_back_button.pack(pady=10, side="bottom")

        # convert recommendation (dataframe) to string and insert into the widget
        result_string = recommendations.to_string(index=False)
        result_text.insert(tk.END, result_string)

    def clear_existing_content(self):
        for widget in self.master.winfo_children():
            widget.destroy()
