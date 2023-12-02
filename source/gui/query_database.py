# Import necessary modules and classes from the tkinter library
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox

import pandas as pd
from ttkthemes import ThemedStyle

# Import functions from a custom database module
from source.database.db_query import show_all, query_dict

# Define a class for querying the database using a Tkinter GUI
class QueryDatabase:
    def __init__(self, master):
        # Initialize the QueryDatabase class with he main Tkinter
        self.master = master
        self.buttons = {}
        self.create_query_database_frame()
        self.query_dict = query_dict

    def create_query_database_frame(self):
        # create a frame for query buttons and place it in the center of the screen
        query_frame = ttk.Frame(self.master)
        query_frame.place(relx=0.5, rely=0.5, anchor="center")

        # define a list of query button names
        self.query_buttons = ['all_actors', 'all_movies', 'all_genres', 'actors_stats', 'highest_rated', 'lowest_rated',
                              'num_movies_genre', 'avg_score_genre', 'avg_score_actor', 'all_movies_actor',
                              'all_actors_movie', 'all_movies_genre', 'movie_info', 'movies_from_year', 'remove_data',
                              'update_data', 'new_movie', 'new_actor', 'new_genre', 'custom']

        # create query buttons and layout
        self.create_query_buttons(query_frame)

        # create return button to return to the main menu
        go_back_button = ttk.Button(
            query_frame,
            text="Go back",
            command=self.master.create_main_menu,
            style='TButton'
        )
        go_back_button.grid(
            row=6,
            column=0,
            pady=0.02 * self.master.winfo_screenheight(),
            padx=0.2 * self.master.winfo_screenwidth(),
            columnspan=4,
            sticky="ew"
        )

        # configure the grid for better layout
        for i in range(6):
            query_frame.grid_rowconfigure(i, weight=5)
        for j in range(3):
            query_frame.grid_columnconfigure(j, weight=5)

        query_frame.grid_rowconfigure(6, weight=2)

    # static method to set the style of a window
    @staticmethod
    def style(window, title):
        window.geometry("800x600")
        window.title(f"{title}")
        window.style = ThemedStyle()
        window.style.set_theme("awdark")
        window.configure(background=window.style.lookup('TFrame', 'background'))
        window.style.configure('TButton', font=('Helvetica', 25))

    def create_query_buttons(self, query_frame):
        for i, button_name in enumerate(self.query_buttons):
            # create a button for each query with corresponding command
            button = ttk.Button(
                query_frame,
                text=button_name.replace('_', ' ').title(),
                width=20,
                padding=(10, 5),
                style='TButton',
                command=lambda btn=button_name: self.button_clicked(btn)
            )
            button.grid(row=i // 4, column=i % 4, padx=0.02 * self.master.winfo_screenwidth(),
                        pady=0.02 * self.master.winfo_screenheight())
            self.buttons[button_name] = button

    # method called when a query button is clicked
    def button_clicked(self, button_name):
        if button_name in self.query_buttons[0:9]:
            # execute and show query results for queries which does not require additional parameters
            dataframe = self.get_query_result(button_name)
            self.show_in_window(dataframe)
        else:
            # show new screen to enter parameters
            self.show_new_screen(button_name)

    # get query result based on button clicked
    def get_query_result(self, button_name):
        return self.query_dict[button_name]['query']

    # method to display query results in a new window
    def show_in_window(self, dataframe):
        if dataframe is not None:
            if len(dataframe) > 1:
                new_window = tk.Toplevel(self.master)
                self.style(new_window, "Query Result Window")
                # if there are results fetched, display them ion a scrolled text widget
                text_widget = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=80, height=20, font=('Courier', 14))
                text_widget.pack(padx=20, pady=20, expand=True, fill="both")
                formatted_text = self.format_dataframe(dataframe)
                text_widget.insert(tk.END, formatted_text)
                text_widget.tag_configure("center", justify="center")
                text_widget.tag_add("center", "1.0", "end")

            # add a button to save results to a csv file
                save_button = ttk.Button(new_window, text="Save to CSV", command=lambda: self.save_to_csv(dataframe))
                save_button.pack(pady=10)
                close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
                close_button.pack(pady=10)
        else:
            new_window = tk.Toplevel(self.master)
            self.style(new_window, "Query Result Window")
            # if other action than fetching results was performed then display a label indicating completion
            label = ttk.Label(new_window, text=" Action done. You may close the window")
            label.pack(side="top", anchor="center")

    # static method to format results for display. may not work with different screen formats
    @staticmethod
    def format_dataframe(dataframe):
        columns = dataframe.columns
        data = dataframe.values
        max_widths = [max(len(str(col)), max(len(str(value)) for value in data[:, i])) for i, col in enumerate(columns)]
        min_spacing = 4

        formatted_text = "|".join(f"{col:<{width + min_spacing}}" for col, width in zip(columns, max_widths)) + "\n"
        formatted_text += "|".join("-" * (width + min_spacing) for width in max_widths) + "\n"

        for row in data:
            formatted_text += "|".join(
                f"{str(value):<{width + min_spacing}}" for value, width in zip(row, max_widths)) + "\n"

        return formatted_text

    @staticmethod
    def save_to_csv(dataframe):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            dataframe.to_csv(file_path, index=False)
            messagebox.showinfo("Save to CSV", "Data has been saved to CSV successfully.")

    # Method to show a new window for custom queries or actions
    def show_new_screen(self, button_name):
        new_window = tk.Toplevel(self.master)
        self.style(new_window, f"{button_name} Parameters")

        input_frame = ttk.Frame(new_window)
        input_frame.pack(pady=20)
        entry_dict = {}

        # create input entries
        self.create_input_entries(button_name, input_frame, entry_dict)

        close_button = ttk.Button(new_window, text="Close", command=new_window.destroy)
        close_button.pack(side="bottom", pady=10, anchor="center")

        proceed_button = ttk.Button(new_window, text="Proceed",
                                    command=lambda: self.proceed_action(button_name, entry_dict))
        proceed_button.pack(side="bottom", pady=10, anchor="center")

    # method to create input entries for additional parameteres and custom queries
    def create_input_entries(self, button_name, input_frame, entry_dict):
        for i, text in enumerate(self.query_dict[button_name]['parameter_name']):
            label = ttk.Label(input_frame, text=f"{text}")
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")
            entry = ttk.Entry(input_frame, font=('Helvetica', 14))
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="w")
            entry_dict[text] = entry

    # method to execute queries based on user input
    def proceed_action(self, button_name, entry_dict):
        if all(entry.get() for entry in entry_dict.values()):
            params = self.get_params_for_action(entry_dict)
            data = self.execute_query(button_name, params)
            self.show_in_window(data)

    # static method to convert input to tuple for use by query functions
    @staticmethod
    def get_params_for_action(entry_dict):
        return tuple(entry.get() for entry in entry_dict.values())

    # method to execute queries based on button clicked
    def execute_query(self, button_name, params):
        if button_name in self.query_buttons[14:19]:
            self.query_dict[button_name]['query'](params)
            data = None
        elif button_name == self.query_buttons[19]:
            try:
                data = self.query_dict[button_name]['query'](str(params[0]))
            except:
                messagebox.showerror("Error", "Invalid input.")
                data = pd.DataFrame()
        else:
            data = show_all(self.query_dict[button_name]['query'], params)
            if len(data) == 0:
                messagebox.showerror("Error", "Invalid input.")
        return data
