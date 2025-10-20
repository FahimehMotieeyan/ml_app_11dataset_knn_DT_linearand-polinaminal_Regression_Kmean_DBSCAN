import tkinter as tk
from tkinter import messagebox, ttk
from joblib import load
import pandas as pd


class AbaloneForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Abalone Age Prediction")
        self.root.geometry("500x600")
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 11))
        self.style.configure('TButton', font=('Helvetica', 11))
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        x = int(self.root .winfo_screenwidth() / 2 - 500 / 2)
        y = int(self.root .winfo_screenheight() / 2 - 600 / 2)
        self.root .geometry(f'+{x}+{y}')

        # Create variables
        self.sex_var = tk.StringVar(value="M")
        self.length_var = tk.DoubleVar(value=0.0)
        self.diameter_var = tk.DoubleVar(value=0.0)
        self.height_var = tk.DoubleVar(value=0.0)
        self.whole_weight_var = tk.DoubleVar(value=0.0)
        self.shucked_weight_var = tk.DoubleVar(value=0.0)
        self.viscera_weight_var = tk.DoubleVar(value=0.0)
        self.shell_weight_var = tk.DoubleVar(value=0.0)

        # Create form
        self.create_form()

    def create_form(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = ttk.Label(main_frame, text="Abalone Age Prediction", style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Sex Section
        sex_frame = ttk.LabelFrame(main_frame, text=" Sex ", padding=10)
        sex_frame.pack(fill=tk.X, pady=5)

        tk.Radiobutton(sex_frame, text="Male (M)", variable=self.sex_var, value="M",
                       bg='#f0f0f0', font=('Helvetica', 10)).pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(sex_frame, text="Female (F)", variable=self.sex_var, value="F",
                       bg='#f0f0f0', font=('Helvetica', 10)).pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(sex_frame, text="Infant (I)", variable=self.sex_var, value="I",
                       bg='#f0f0f0', font=('Helvetica', 10)).pack(anchor="w", padx=5, pady=2)

        # Measurements Section
        measures_frame = ttk.LabelFrame(main_frame, text=" Measurements ", padding=10)
        measures_frame.pack(fill=tk.X, pady=5)

        self.create_entry_row(measures_frame, "Length (mm):", self.length_var)
        self.create_entry_row(measures_frame, "Diameter (mm):", self.diameter_var)
        self.create_entry_row(measures_frame, "Height (mm):", self.height_var)

        # Weights Section
        weights_frame = ttk.LabelFrame(main_frame, text=" Weights (grams) ", padding=10)
        weights_frame.pack(fill=tk.X, pady=5)

        self.create_entry_row(weights_frame, "Whole weight:", self.whole_weight_var)
        self.create_entry_row(weights_frame, "Shucked weight:", self.shucked_weight_var)
        self.create_entry_row(weights_frame, "Viscera weight:", self.viscera_weight_var)
        self.create_entry_row(weights_frame, "Shell weight:", self.shell_weight_var)

        # Buttons Section
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20)

        ttk.Button(buttons_frame, text="Predict Age", command=self.predict_age, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(buttons_frame, text="Return Home", command=self.go_home, width=15).pack(side=tk.LEFT, padx=10)

    def create_entry_row(self, parent, label_text, variable):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=3)

        label = ttk.Label(row, text=label_text, width=15, anchor="e")
        label.pack(side=tk.LEFT, padx=5)

        entry = ttk.Entry(row, textvariable=variable, width=20, font=('Helvetica', 10))
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    def predict_age(self):
        try:
            # Collect data
            input_data = [
                self.sex_var.get(),
                self.length_var.get(),
                self.diameter_var.get(),
                self.height_var.get(),
                self.whole_weight_var.get(),
                self.shucked_weight_var.get(),
                self.viscera_weight_var.get(),
                self.shell_weight_var.get()
            ]

            # Load model
            loaded_model = load('model_regression_1_alabama.joblib')

            # Create DataFrame
            new_data = pd.DataFrame([input_data],
                                    columns=['Sex', 'Length', 'Diameter', 'Height', 'Whole_weight',
                                             'Shucked_weight', 'Viscera_weight', 'Shell_weight'])

            # Convert categorical variables
            new_data = pd.get_dummies(new_data, columns=["Sex"], drop_first=True)

            # List of expected columns
            expected_columns = ['Length', 'Diameter', 'Height', 'Whole_weight', 'Shucked_weight',
                                'Viscera_weight', 'Shell_weight', 'Sex_I', 'Sex_M']

            # Ensure all columns exist
            missing_cols = set(expected_columns) - set(new_data.columns)
            for col in missing_cols:
                new_data[col] = 0

            # Sort columns
            new_data = new_data[expected_columns]

            # Predict age
            age = loaded_model.predict(new_data)[0] + 1.5
            age = round(age, 2)

            messagebox.showinfo("Result", f"Predicted abalone age: {age} years")

        except Exception as e:
            messagebox.showerror("Error", f"Error in age prediction: {str(e)}")

    def go_home(self):
        self.root.destroy()
        from regressionMainPage.regression_first_page import regression_first_page_class
        regressionPage_obj = regression_first_page_class()
        regressionPage_obj.regression_first_page_load()


if __name__ == "__main__":
    root = tk.Tk()
    app = AbaloneForm(root)
    root.mainloop()