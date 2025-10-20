import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
from tkinter.font import Font
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class WiFiRoomPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Signal Room Predictor")
        self.root.geometry("600x800")  # Same size as before
        self.style = ttk.Style()
        self.configure_styles()

        # Center the window
        self.center_window(600, 780)

        # Model paths
        self.model_path = 'final_knn_model.pkl'
        self.scaler_path = 'standard_scaler.pkl'

        # Initialize variables
        self.wifi_vars = [tk.IntVar(value=-50) for _ in range(7)]

        # Load models
        self.model = None
        self.scaler = None
        self.load_models()

        # Create UI
        self.create_form()

    def configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f5f9ff')
        self.style.configure('TLabel', background='#f5f9ff', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=1)
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        self.style.configure('Result.TLabel', font=('Segoe UI', 11, 'bold'), foreground='#2c3e50')
        self.style.configure('ResultFrame.TFrame', background='#e8f4fc', borderwidth=2, relief='groove')
        self.style.configure('Progress.Horizontal.TProgressbar', thickness=20, troughcolor='#e0e0e0',
                             background='#3498db')

    def center_window(self, width, height):
        x = int(self.root.winfo_screenwidth() / 2 - width / 2)
        y = int(self.root.winfo_screenheight() / 2 - height / 2)
        self.root.geometry(f'+{x}+{y}')

    def load_models(self):
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model files:\n{str(e)}")
            self.root.destroy()

    def create_form(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(0, 10), fill=tk.X)

        ttk.Label(header_frame, text="WiFi Signal Room Prediction", style='Header.TLabel').pack()
        ttk.Label(header_frame,
                  text="Enter device location information (which room the device is in)",
                  style='TLabel').pack()

        # WiFi Signals Section
        signals_frame = ttk.LabelFrame(main_frame, text=" WiFi Signal Strengths (dBm) ", padding=15)
        signals_frame.pack(fill=tk.X, pady=10)

        for i in range(7):
            self.create_signal_row(signals_frame, f"Wifi {i + 1}:", self.wifi_vars[i], i)

        # Buttons Section
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=15)

        ttk.Button(buttons_frame, text="Predict Room", command=self.predict_room, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Clear", command=self.clear_form, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Back to Home", command=self.back_to_home, width=15).pack(side=tk.LEFT, padx=10)

        # Results Section (with Scrollbar)
        self.results_frame = ttk.Frame(main_frame, style='ResultFrame.TFrame', padding=10)
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create a Canvas and Scrollbar
        self.canvas = tk.Canvas(self.results_frame, bg='#e8f4fc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='ResultFrame.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Initial label
        self.result_label = ttk.Label(self.scrollable_frame,
                                      text="Please enter WiFi signal strengths and click 'Predict Room'",
                                      style='Result.TLabel')
        self.result_label.pack(fill=tk.X, pady=5)

        # Frame for progress bars (probabilities)
        self.progress_frame = ttk.Frame(self.scrollable_frame)
        self.progress_frame.pack(fill=tk.BOTH, expand=True)

    def create_signal_row(self, parent, label_text, variable, row_num):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=5)

        label = ttk.Label(row, text=label_text, width=10, anchor="e")
        label.pack(side=tk.LEFT, padx=5)

        scale = tk.Scale(row, from_=-100, to=-10, orient=tk.HORIZONTAL,
                         variable=variable, showvalue=1, resolution=1,
                         length=250, sliderlength=25,
                         troughcolor='#e0e0e0', highlightbackground='#f5f9ff',
                         bg='#f5f9ff', activebackground='#3498db')
        scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        value_label = ttk.Label(row, textvariable=variable, width=4)
        value_label.pack(side=tk.LEFT, padx=5)

    def predict_room(self):
        signals = [var.get() for var in self.wifi_vars]

        try:
            new_data = pd.DataFrame([signals],
                                    columns=[f'Wifi {i + 1}' for i in range(7)])
            scaled_data = self.scaler.transform(new_data)
            predicted_room = self.model.predict(scaled_data)[0]
            probabilities = self.model.predict_proba(scaled_data)[0]

            # Clear previous widgets
            for widget in self.progress_frame.winfo_children():
                widget.destroy()

            # Update result label
            self.result_label.config(text=f"📌 Predicted Room: Room_{predicted_room}\n\n📊 Room Probabilities:")

            # Add progress bars for each room
            for i, prob in enumerate(probabilities):
                room_frame = ttk.Frame(self.progress_frame)
                room_frame.pack(fill=tk.X, pady=3)

                ttk.Label(room_frame, text=f"Room_{i + 1}:", width=8).pack(side=tk.LEFT)

                progress = ttk.Progressbar(room_frame,
                                           orient=tk.HORIZONTAL,
                                           length=200,
                                           mode='determinate',
                                           value=prob * 100,
                                           style='Progress.Horizontal.TProgressbar')
                progress.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

                ttk.Label(room_frame, text=f"{prob * 100:.1f}%").pack(side=tk.LEFT, padx=5)

            # Auto-scroll to top
            self.canvas.yview_moveto(0)

        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred during prediction:\n{str(e)}")

    def clear_form(self):
        for var in self.wifi_vars:
            var.set(-50)
        self.result_label.config(text="Please enter WiFi signal strengths and click 'Predict Room'")
        for widget in self.progress_frame.winfo_children():
            widget.destroy()
        self.canvas.yview_moveto(0)

    def back_to_home(self):
        self.root.destroy()
        from classificationMainPage.classification_first_page import classification_first_page_class
        regressionPage_obj = classification_first_page_class()
        regressionPage_obj.classification_first_page_load()


if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiRoomPredictor(root)
    root.mainloop()