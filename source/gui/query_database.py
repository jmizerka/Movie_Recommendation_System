# query_database.py
import tkinter as tk
from tkinter import ttk,scrolledtext
from ttkthemes import ThemedStyle
import sys
import tkinter.filedialog
import tkinter.messagebox
sys.path.append('../database')
import pandas as pd

from queries import *
from db_query import db_connector,show_all,remove,update,add_movie,add_actor_or_genre



class QueryDatabase:
    def __init__(self, master):
        self.master = master
        self.buttons = {}
        self.create_query_database_frame()
        self.query_dict = {
            'all_actors': {'query': ALL_ACTORS, 'parameter_name': None},
            'all_movies': {'query': ALL_MOVIES, 'parameter_name': None},
            'all_genres': {'query': ALL_GENRES, 'parameter_name': None},
            'actors_stats': {'query': ACTOR_STATS, 'parameter_name': None},
            'all_movies_actor': {'query': MOVIES_OF_ACTOR, 'parameter_name': ('actor_name',)},
            'all_actors_movie': {'query': ACTORS_IN_MOVIE, 'parameter_name': ('title',)},
            'all_movies_genre': {'query': MOVIES_OF_GENRE, 'parameter_name': ('genre_name',)},
            'movie_info': {'query': MOVIE_BY_TITLE, 'parameter_name': ('movie_title',)},
            'movies_from_year': {'query': MOVIES_OF_YEAR, 'parameter_name': ('release_year',)},
            'highest_rated': {'query': HIGHEST_RATED, 'parameter_name': None},
            'lowest_rated': {'query': LOWEST_RATED, 'parameter_name': None},
            'num_movies_genre': {'query': NUM_MOVIES_BY_GENRE, 'parameter_name': None},
            'avg_score_genre': {'query': AVG_RATE_BY_GENRE, 'parameter_name': None},
            'avg_score_actor': {'query': AVG_RATE_BY_ACTOR, 'parameter_name': None},
            'new_actor': {'query': add_actor_or_genre, 'parameter_name': ('actor_name',)},
            'new_genre': {'query': add_actor_or_genre, 'parameter_name': ('genre_name',)},
            'new_movie': {'query': add_movie, 'parameter_name': ('title', 'date', 'original_lang', 'country', 'overview', 'score', 'genres',)},
            'remove_data': {'query': remove, 'parameter_name': ('table_name', 'col', 'id',)},
            'update_data': {'query': update, 'parameter_name': ('table_name', 'col_name', 'value', 'condition',)}}

    def create_query_database_frame(self):
        query_frame = ttk.Frame(self.master)
        query_frame.place(relx=0.5, rely=0.5, anchor="center")

        query_buttons = ['all_actors', 'all_movies', 'all_genres', 'all_movies_actor', 'all_actors_movie',
                         'all_movies_genre', 'movie_info', 'movies_from_year', 'actors_stats',
                         'highest_rated', 'lowest_rated', 'num_movies_genre',
                         'avg_score_genre', 'avg_score_actor', 'remove_data', 'update_data',
                         'new_movie', 'new_actor', 'new_genre', 'to_csv']
        idx = 0
        for i in range(5):
            for j in range(4):
                button_text = query_buttons[idx]
                idx += 1
                button = ttk.Button(query_frame, text=button_text, width=20, padding=(10, 5), style='TButton', command=lambda btn=button_text: self.button_clicked(btn))
                button.grid(row=i, column=j, padx=100, pady=50)
                self.buttons[button_text] = button

        go_back_button = ttk.Button(query_frame, text="Go back", command=self.master.create_main_menu, style='TButton')
        go_back_button.grid(row=6, column=0, pady=40, padx=600, columnspan=4, sticky="ew")
        for i in range(6):
            query_frame.grid_rowconfigure(i, weight=5)
        for j in range(3):
            query_frame.grid_columnconfigure(j, weight=5)

        query_frame.grid_rowconfigure(6, weight=2)

    def button_clicked(self, button_name):
        if button_name in ['all_actors', 'all_movies', 'all_genres', 'actors_stats', 'highest_rated', 'lowest_rated', 'num_movies_genre', 'avg_score_genre', 'avg_score_actor']:
            dataframe = show_all(self.query_dict[button_name]['query'],self.query_dict[button_name]['parameter_name'])
            self.show_in_window(dataframe)
        else:
            self.show_new_screen(button_name)

    # def show_in_window(self, dataframe):
    #     new_window = tk.Toplevel(self.master)
    #     new_window.geometry("800x600")  # Set the size of the new window
    #     new_window.title("Query Result Window")  # Set the title of the new window
    #     new_window.style = ThemedStyle()
    #     new_window.style.set_theme("awdark")
    #     new_window.configure(background=new_window.style.lookup('TFrame', 'background'))
    #     new_window.style.configure('TButton', font=('Helvetica', 25))  # Set font size for all buttons
    #
    #     # Add a scrollable Text widget to display the DataFrame
    #     text_widget = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=80, height=20,font=('Helvetica', 14))  # Set font size to 14
    #     text_widget.pack(padx=20, pady=20, expand=True, fill="both")  # Expand and fill the available space
    #
    #     # Insert DataFrame data into the Text widget
    #     text_widget.insert(tk.END, dataframe.to_string(index=False))
    #     text_widget.tag_configure("center", justify="center")
    #     text_widget.tag_add("center", "1.0", "end")
    #
    #
    #     # Add a close button
    #     close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
    #     close_button.pack(pady=10)
    def show_in_window(self, dataframe):
        new_window = tk.Toplevel(self.master)
        new_window.geometry("800x600")
        new_window.title("Query Result Window")
        new_window.style = ThemedStyle()
        new_window.style.set_theme("awdark")
        new_window.configure(background=new_window.style.lookup('TFrame', 'background'))
        new_window.style.configure('TButton', font=('Helvetica', 25))

        # Add a scrollable Text widget to display the DataFrame
        text_widget = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=80, height=20, font=('Helvetica', 14))
        text_widget.pack(padx=20, pady=20, expand=True, fill="both")

        # Insert DataFrame data into the Text widget
        text_widget.insert(tk.END, dataframe.to_string(index=False))
        text_widget.tag_configure("center", justify="center")
        text_widget.tag_add("center", "1.0", "end")

        # Add a save to CSV button
        save_button = ttk.Button(new_window, text="Save to CSV", command=lambda: self.save_to_csv(dataframe))
        save_button.pack(pady=10)

        # Add a close button
        close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(pady=10)

    def show_new_screen(self, button_name):
        new_window = tk.Toplevel(self.master)
        new_window.geometry("800x600")
        new_window.title(f"{button_name} Parameters")
        new_window.style = ThemedStyle()
        new_window.style.set_theme("awdark")
        new_window.configure(background=new_window.style.lookup('TFrame', 'background'))
        new_window.style.configure('TButton', font=('Helvetica', 25))

        # Frame to hold the input boxes
        input_frame = ttk.Frame(new_window)
        input_frame.pack(pady=20)

        entry_dict = {}

        for i, text in enumerate(self.query_dict[button_name]['parameter_name']):
            label = ttk.Label(input_frame, text=f"{text}")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ttk.Entry(input_frame, font=('Helvetica', 14))
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            entry_dict[text] = entry

        def proceed_action():
            # Check if all entries are filled
            if all(entry.get() for entry in entry_dict.values()):
                if button_name in ['new_actor','new_genre']:
                    entry_list = list(entry.get() for entry in entry_dict.values())
                    if button_name == 'new_actor':
                        entry_list.append('actors')
                    else:
                        entry_list.append('genres')
                    params = tuple(entry_list)
                    self.query_dict[button_name]['query'](params)
                    data = None
                elif button_name in ['new_movie','title','update_data']:
                    params = tuple(entry.get() for entry in entry_dict.values())
                    self.query_dict[button_name]['query'](params)
                    data = None
                else:
                    params = tuple(entry.get() for entry in entry_dict.values())
                    data = show_all(self.query_dict[button_name]['query'],params)
                self.show_scrollable_text(new_window, data)

        proceed_button = ttk.Button(new_window, text="Proceed", command=proceed_action)
        proceed_button.pack(side="bottom", pady=10, anchor="center")

        close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(side="bottom", pady=10, anchor="center")

    def show_scrollable_text(self, parent, data):
        text_window = tk.Toplevel(parent)
        text_window.geometry("800x600")
        text_window.title("Query result")
        text_window.style = ThemedStyle()
        text_window.style.set_theme("awdark")
        text_window.configure(background=text_window.style.lookup('TFrame', 'background'))
        if type(data) is not type(None):
            text_widget = scrolledtext.ScrolledText(text_window, wrap=tk.WORD, width=80, height=20,
                                                    font=('Helvetica', 14))
            text_widget.pack(padx=20, pady=20, expand=True, fill="both")

            # Insert DataFrame data into the Text widget
            text_widget.insert(tk.END, data.to_string(index=False))
            text_widget.tag_configure("center", justify="center")
            text_widget.tag_add("center", "1.0", "end")

            # Add a save to CSV button
            save_button = ttk.Button(text_window, text="Save to CSV", command=lambda: self.save_to_csv(data))
            save_button.pack(pady=10)
        else:
            label = ttk.Label(text_window, text="Operation is Done. You may close the window", font=('Helvetica', 16))
            label.pack(side='top', anchor='center')

    def save_to_csv(self, dataframe):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataframe.to_csv(file_path, index=False)
            tkinter.messagebox.showinfo("Save to CSV", "Data has been saved to CSV successfully.")

