# check_ratings.py
import tkinter as tk
from tkinter import ttk, scrolledtext, Toplevel, Label, Entry
from datetime import datetime
from tkinter import messagebox
from ttkthemes import ThemedStyle
from source.database.db_query import show_all, add_rating


class CheckRatings:
    def __init__(self, master):
        self.master = master
        self.create_check_ratings_frame()

    def create_check_ratings_frame(self):
        check_ratings_frame = ttk.Frame(self.master)
        check_ratings_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.master.style = ThemedStyle()
        self.master.style.set_theme("awdark")
        self.master.configure(background=self.master.style.lookup('TFrame', 'background'))
        self.master.style.configure('TButton', font=('Helvetica', 25))

        ratings_data = show_all("SELECT * FROM your_ratings")

        text_widget = tk.Text(check_ratings_frame, wrap='none', height=10, width=50)
        text_widget.grid(row=0, column=0, padx=50, pady=10, sticky="nsew")
        text_widget.tag_configure("center", justify='center', spacing1=15, spacing3=20, spacing2=15, font=('Helvetica', 16))
        text_widget.insert('1.0', ratings_data.to_string(index=False), "center")

        add_record_button = ttk.Button(check_ratings_frame, text="Add Record", command=self.add_record_window)
        add_record_button.grid(row=1, column=0, pady=10, sticky="s")

        go_back_button = ttk.Button(check_ratings_frame, text="Go back", command=self.master.create_main_menu)
        go_back_button.grid(row=2, column=0, pady=10, sticky="s")

        check_ratings_frame.grid_rowconfigure(0, weight=1)
        check_ratings_frame.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def add_record_window(self):
        add_record_window = Toplevel(self.master)
        add_record_window.title("Add Record")
        add_record_window.style = ThemedStyle()
        add_record_window.style.set_theme("awdark")
        add_record_window.configure(background=add_record_window.style.lookup('TFrame', 'background'))
        add_record_window.style.configure('TButton', font=('Helvetica', 25))
        add_record_window.style.configure('TLabel', font=('Helvetica', 15))

        labels = ["Title:", "Rating:", "Date (YYYY-MM-DD):"]
        entries = []

        for i, label_text in enumerate(labels):
            label = Label(add_record_window, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="e")

            entry = Entry(add_record_window)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries.append(entry)

        proceed_button = ttk.Button(add_record_window, text="Proceed", command=lambda: self.proceed_add_record(*[entry.get() for entry in entries], add_record_window))
        proceed_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def proceed_add_record(self, title, rating, date, add_record_window):
        try:
            rating = float(rating)
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            add_rating(params=(title, rating, str(date_obj)))
            add_record_window.destroy()
            self.create_check_ratings_frame()  # Refresh the ratings frame after adding a new record
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid rating.")
