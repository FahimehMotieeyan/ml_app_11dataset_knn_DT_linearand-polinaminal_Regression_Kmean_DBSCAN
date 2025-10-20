import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from joblib import load
import pandas as pd
import sys
import os


class HousePriceForm:
    def __init__(self, root):
        self.root = root
        self.root.title("House Price Prediction")
        self.root.geometry("850x650")
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 11))
        self.style.configure('TButton', font=('Helvetica', 11))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Result.TLabel', font=('Helvetica', 12, 'bold'), foreground='blue')
        self.style.configure('Exit.TButton', foreground='red')

        # Center the window
        self.center_window()

        # Create variables
        self.house_age_var = tk.DoubleVar()
        self.distance_mrt_var = tk.DoubleVar()
        self.convenience_stores_var = tk.IntVar(value=1)
        self.latitude_var = tk.DoubleVar()
        self.longitude_var = tk.DoubleVar()
        self.prediction_var = tk.StringVar(value="Prediction will appear here")

        # Create form
        self.create_form()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'+{x}+{y}')

    def create_form(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Image Frame (Left)
        image_frame = ttk.Frame(main_frame, width=400, height=550)
        image_frame.pack_propagate(False)
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))

        # Form Frame (Right)
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Load and display image
        try:
            image = Image.open("images/house_price.jpg")
            image = image.resize((400, 550), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(image_frame, image=photo)
            image_label.image = photo
            image_label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            print(f"Error loading image: {e}")
            ttk.Label(image_frame, text="Image not available", background='#f0f0f0').pack()

        # Header
        header = ttk.Label(form_frame, text="House Price Prediction", style='Header.TLabel')
        header.pack(pady=(0, 15))

        # House Age Section
        age_frame = ttk.LabelFrame(form_frame, text="House Age", padding=10)
        age_frame.pack(fill=tk.X, pady=5)
        self.create_entry_row(age_frame, "House age (years):", self.house_age_var)

        # Distance to MRT Section
        distance_frame = ttk.LabelFrame(form_frame, text="Distance to MRT Station", padding=10)
        distance_frame.pack(fill=tk.X, pady=5)
        self.create_entry_row(distance_frame, "Distance (meters):", self.distance_mrt_var)

        # Convenience Stores Section
        stores_frame = ttk.LabelFrame(form_frame, text="Number of Convenience Stores", padding=10)
        stores_frame.pack(fill=tk.X, pady=5)
        self.create_slider(stores_frame, self.convenience_stores_var)

        # Coordinates Section
        coord_frame = ttk.LabelFrame(form_frame, text="Location Coordinates", padding=10)
        coord_frame.pack(fill=tk.X, pady=5)
        self.create_entry_row(coord_frame, "Latitude:", self.latitude_var)
        self.create_entry_row(coord_frame, "Longitude:", self.longitude_var)

        # Prediction Result Section
        result_frame = ttk.LabelFrame(form_frame, text="Price Estimation", padding=10)
        result_frame.pack(fill=tk.X, pady=15)
        result_label = ttk.Label(result_frame, textvariable=self.prediction_var, style='Result.TLabel')
        result_label.pack(pady=10)

        # Button Frame
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Predict Button
        predict_button = ttk.Button(button_frame, text="Estimate Price", command=self.validate_and_predict, width=20)
        predict_button.pack(side=tk.LEFT, padx=5)

        # Home Button
        home_button = ttk.Button(button_frame, text="Back to Home", command=self.go_home,
                                 style='Exit.TButton', width=15)
        home_button.pack(side=tk.RIGHT, padx=5)

    def create_entry_row(self, parent, label_text, variable):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=3)
        label = ttk.Label(row, text=label_text, width=20, anchor="e")
        label.pack(side=tk.LEFT, padx=5)
        entry = ttk.Entry(row, textvariable=variable, width=25, font=('Helvetica', 10))
        entry.pack(side=tk.LEFT, padx=5)

    def create_slider(self, parent, variable):
        scale = tk.Scale(parent,
                         from_=1,
                         to=10,
                         orient=tk.HORIZONTAL,
                         variable=variable,
                         showvalue=1,
                         tickinterval=1,
                         length=350)
        scale.pack(pady=5)

    def validate_and_predict(self):
        if not all([self.house_age_var.get(),
                    self.distance_mrt_var.get(),
                    self.convenience_stores_var.get(),
                    self.latitude_var.get(),
                    self.longitude_var.get()]):
            messagebox.showerror("Error", "Please fill in all fields before prediction")
            return
        self.predict_price()

    def predict_price(self):
        try:
            if not all([self.house_age_var.get() >= 0,
                        self.distance_mrt_var.get() >= 0,
                        self.convenience_stores_var.get() >= 1]):
                raise ValueError("All values must be positive and number of stores must be at least 1")

            input_data = [
                float(self.house_age_var.get()),
                float(self.distance_mrt_var.get()),
                int(self.convenience_stores_var.get()),
                float(self.latitude_var.get()),
                float(self.longitude_var.get())
            ]

            loaded_model = load('model_polynomial_regression_degree2.joblib')

            new_data = pd.DataFrame([input_data],
                                    columns=['X2 house age',
                                             'X3 distance to the nearest MRT station',
                                             'X4 number of convenience stores',
                                             'X5 latitude',
                                             'X6 longitude'])

            price = loaded_model.predict(new_data)[0]
            price = round(price, 2)

            self.prediction_var.set(f"Predicted Price: {price*-1} ")

        except ValueError as e:
            self.prediction_var.set(f"Error: {str(e)}")
        except Exception as e:
            self.prediction_var.set(f"Prediction Error: {str(e)}")

    def go_home(self):
        # Close current window first
        self.root.destroy()

        # Then import and open home page
        from regressionMainPage.regression_first_page import regression_first_page_class

        regressionPage_obj = regression_first_page_class()
        regressionPage_obj.regression_first_page_load()
        # root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = HousePriceForm(root)
    root.mainloop()