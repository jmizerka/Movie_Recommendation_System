# Import necessary modules from tkinter for GUI components and from ttkthemes for themes
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

# Import specific classes from other modules
from source.gui.query_database import QueryDatabase
from source.gui.check_ratings import CheckRatings
from source.gui.movie_recommendation import MovieRecommendation


# Define a class for the main application, inheriting from tk.Tk
class MovieApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie App")
        self.attributes('-fullscreen', True)

        # Configure the auto_path to include a theme from a specific directory
        self.tk.call('lappend', 'auto_path',
                     'data/awthemes-10.4.0')

        # Require and set a dark theme using 'awdark'
        self.tk.call('package', 'require', 'awdark')
        self.style = ThemedStyle(self)
        self.style.set_theme("awdark")

        # Set the background color of the application to match the theme
        self.configure(background=self.style.lookup('TFrame', 'background'))

        # Configure the style for all buttons in the application
        self.style.configure('TButton', font=('Helvetica', 25))
        self.create_main_menu()

    def create_main_menu(self):
        # Destroy the current frame to avoid overlap with a new frame
        self.destroy_current_frame()

        # Create a frame for the main menu and place it in the center of the window
        main_frame = ttk.Frame(self, style='TFrame')
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

        # Define a list of buttons with their corresponding text and command
        buttons = [
            ("Query our database", self.show_query_database),
            ("Check your movie ratings", self.show_check_ratings),
            ("Ask for movie recommendation", self.show_movie_recommendation),
            ("Exit", self.destroy)
        ]

        # Create buttons based on the list and pack them into the main frame
        for text, command in buttons:
            button = ttk.Button(main_frame, text=text, command=command, width=40, padding=(20, 40),
                                style='TButton')  # Increase button size
            button.pack(pady=20)

    def show_query_database(self):
        self.destroy_current_frame()
        QueryDatabase(self)

    def show_check_ratings(self):
        self.destroy_current_frame()
        CheckRatings(self)

    def show_movie_recommendation(self):
        self.destroy_current_frame()
        MovieRecommendation(self)

    # Method to destroy the current frame, clearing the window
    def destroy_current_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
