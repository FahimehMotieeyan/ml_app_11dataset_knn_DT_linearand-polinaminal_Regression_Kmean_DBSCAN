import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
from pathlib import Path
import sys
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class CarAcceptabilityPredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Acceptability Predictor")
        self.root.geometry("450x620")
        self.style = ttk.Style()
        self.configure_styles()

        # Center the window
        self.center_window(450, 620)

        # Model paths
        self.model_path = 'final_knn_model_car_2.pkl'
        self.encoders_path = 'label_encoders_car_2.pkl'
        self.scaler_path = 'standard_scaler_car_2.pkl'

        # Initialize variables (empty to start)
        self.buying_var = tk.StringVar(value="")
        self.maint_var = tk.StringVar(value="")
        self.doors_var = tk.StringVar(value="")
        self.persons_var = tk.StringVar(value="")
        self.lug_boot_var = tk.StringVar(value="")
        self.safety_var = tk.StringVar(value="")

        # Class descriptions
        self.class_descriptions = {
            'unacc': 'Unacceptable',
            'acc': 'Acceptable',
            'good': 'Good',
            'vgood': 'Very Good'
        }

        # Load models
        self.model = None
        self.encoders = None
        self.scaler = None
        self.load_models()

        # Create UI
        self.create_form()

    def configure_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f5f9ff')
        self.style.configure('TLabel', background='#f5f9ff', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10, 'bold'), borderwidth=1)
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Instruction.TLabel', font=('Segoe UI', 9), foreground='#555555')
        self.style.configure('Result.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#2c3e50')
        self.style.configure('ResultFrame.TFrame', background='#e8f4fc', borderwidth=2, relief='groove')
        self.style.configure('TCombobox', padding=5)
        self.style.map('TCombobox', fieldbackground=[('readonly', '#ffffff')])

    def center_window(self, width, height):
        x = int(self.root.winfo_screenwidth() / 2 - width / 2)
        y = int(self.root.winfo_screenheight() / 2 - height / 2)
        self.root.geometry(f'+{x}+{y}')

    def load_models(self):
        try:
            self.model = joblib.load(self.model_path)
            self.encoders = joblib.load(self.encoders_path)
            self.scaler = joblib.load(self.scaler_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model files:\n{str(e)}")
            self.root.destroy()

    def create_form(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(pady=(0, 5), fill=tk.X)

        ttk.Label(header_frame, text="Car Evaluation Form", style='Header.TLabel').pack()

        # Instruction text
        instruction_frame = ttk.Frame(main_frame)
        instruction_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(instruction_frame,
                  text="Fill in the information below to find out if your car is acceptable or not",
                  style='Instruction.TLabel').pack()

        # Form fields
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buying price
        ttk.Label(form_frame, text="Buying price:").pack(anchor=tk.W, pady=(5, 0))
        buying_combo = ttk.Combobox(form_frame, textvariable=self.buying_var,
                                    values=[ "vhigh", "high", "med", "low"], state='readonly')
        buying_combo.pack(fill=tk.X, pady=(0, 5))

        # Maintenance price
        ttk.Label(form_frame, text="Maintenance price:").pack(anchor=tk.W, pady=(5, 0))
        maint_combo = ttk.Combobox(form_frame, textvariable=self.maint_var,
                                   values=[ "vhigh", "high", "med", "low"], state='readonly')
        maint_combo.pack(fill=tk.X, pady=(0, 5))

        # Number of doors
        ttk.Label(form_frame, text="Number of doors:").pack(anchor=tk.W, pady=(5, 0))
        doors_combo = ttk.Combobox(form_frame, textvariable=self.doors_var,
                                   values=[ "2", "3", "4", "5more"], state='readonly')
        doors_combo.pack(fill=tk.X, pady=(0, 5))

        # Capacity
        ttk.Label(form_frame, text="Person capacity:").pack(anchor=tk.W, pady=(5, 0))
        persons_combo = ttk.Combobox(form_frame, textvariable=self.persons_var,
                                     values=[ "2", "4", "more"], state='readonly')
        persons_combo.pack(fill=tk.X, pady=(0, 5))

        # Luggage boot size
        ttk.Label(form_frame, text="Luggage boot size:").pack(anchor=tk.W, pady=(5, 0))
        lug_boot_combo = ttk.Combobox(form_frame, textvariable=self.lug_boot_var,
                                      values=["small", "med", "big"], state='readonly')
        lug_boot_combo.pack(fill=tk.X, pady=(0, 5))

        # Safety
        ttk.Label(form_frame, text="Estimated safety:").pack(anchor=tk.W, pady=(5, 0))
        safety_combo = ttk.Combobox(form_frame, textvariable=self.safety_var,
                                    values=["low", "med", "high"], state='readonly')
        safety_combo.pack(fill=tk.X, pady=(0, 15))

        # Result label
        self.result_label = ttk.Label(main_frame, text="", style='Result.TLabel')
        self.result_label.pack(pady=(10, 15))

        # Button frame at bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="Predict", command=self.predict, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Return to Home", command=self.return_to_home, width=15).pack(side=tk.RIGHT)

    def preprocess_input(self, data):
        df = pd.DataFrame([data])

        # Convert qualitative columns
        for col in ['buying', 'maint', 'lug_boot', 'safety']:
            df[col] = self.encoders[col].transform(df[col])

        # Convert numeric columns
        df['doors'] = df['doors'].replace('5more', '5').astype(int)
        df['persons'] = df['persons'].replace('more', '5').astype(int)

        # Normalize
        df[['doors', 'persons']] = self.scaler.transform(df[['doors', 'persons']])

        return df

    def predict(self):
        # Collect data from form
        new_data = {
            'buying': self.buying_var.get(),
            'maint': self.maint_var.get(),
            'doors': self.doors_var.get(),
            'persons': self.persons_var.get(),
            'lug_boot': self.lug_boot_var.get(),
            'safety': self.safety_var.get()
        }

        try:
            # Validate all fields are filled
            if not all(new_data.values()):
                messagebox.showwarning("Warning", "Please fill in all fields")
                return

            processed_data = self.preprocess_input(new_data)
            prediction = self.model.predict(processed_data)
            predicted_class = self.encoders['class'].inverse_transform(prediction)[0]

            # Get full description of the predicted class
            class_description = self.class_descriptions.get(predicted_class, predicted_class)

            self.result_label.config(
                text=f"Predicted Car Acceptability: {class_description}",
                foreground="#2e7d32"  # Green color for success
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during prediction:\n{str(e)}")
            self.result_label.config(
                text=f"Error: {str(e)}",
                foreground="#c62828"  # Red color for error
            )

    def clear_form(self):
        self.buying_var.set("")
        self.maint_var.set("")
        self.doors_var.set("")
        self.persons_var.set("")
        self.lug_boot_var.set("")
        self.safety_var.set("")
        self.result_label.config(text="", foreground="#2c3e50")

    def return_to_home(self):
        self.root.destroy()
        # Add the parent directory to path
        # sys.path.append(str(Path(__file__).parent.parent))
        from classificationMainPage.classification_first_page import classification_first_page_class
        home_page = classification_first_page_class()
        home_page.classification_first_page_load()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarAcceptabilityPredictor(root)
    root.mainloop()