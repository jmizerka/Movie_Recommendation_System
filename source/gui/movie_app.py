#movie_app.pyq
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from source.gui.query_database import QueryDatabase
from source.gui.check_ratings import CheckRatings
from source.gui.movie_recommendation import MovieRecommendation

class MovieApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie App")
        self.attributes('-fullscreen', True)  # Set to fullscreen
        self.tk.call('lappend', 'auto_path',
                     'data/awthemes-10.4.0')
        self.tk.call('package', 'require', 'awdark')
        self.style = ThemedStyle(self)
        self.style.set_theme("awdark")
        self.configure(background=self.style.lookup('TFrame', 'background'))
        self.style.configure('TButton', font=('Helvetica', 25))  # Set font size for all buttons
        self.create_main_menu()

    def create_main_menu(self):
        self.destroy_current_frame()

        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        buttons = [
            ("Query our database", self.show_query_database),
            ("Check your movie ratings", self.show_check_ratings),
            ("Ask for movie recommendation", self.show_movie_recommendation),
            ("Exit", self.destroy)
        ]

        for text, command in buttons:
            button = ttk.Button(main_frame, text=text, command=command, width=40, padding=(20, 40),
                                style='TButton')  # Increase button size
            button.pack(pady=20)

    def show_query_database(self):
        self.destroy_main_menu()
        q_db = QueryDatabase(self)
    def show_check_ratings(self):
        self.destroy_main_menu()
        CheckRatings(self)

    def show_movie_recommendation(self):
        self.destroy_main_menu()
        MovieRecommendation(self)

    def destroy_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

    def destroy_current_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
