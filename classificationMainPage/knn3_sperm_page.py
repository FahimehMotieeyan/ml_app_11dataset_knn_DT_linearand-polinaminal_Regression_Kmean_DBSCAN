import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class SpermAnalysisForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Sperm Analysis Diagnosis")
        self.root.geometry("500x450")
        x = int(self.root.winfo_screenwidth() / 2 -500 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 600 / 2)
        self.root.geometry(f'+{x}+{y}')

        # Load model and scaler
        try:
            self.model = joblib.load('final_model_knn3_sperm.joblib')
            self.scaler = joblib.load('scaler_knn3_sperm.joblib')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model files: {str(e)}")
            self.root.destroy()
            return

        # Alcohol frequency options with descriptions and corresponding scaled values
        self.alcohol_options = [
            ("Several times a day", 0.0),
            ("Every day", 0.25),
            ("Several times a week", 0.5),
            ("Once a week", 0.75),
            ("Hardly ever or never", 1.0)
        ]

        self.create_form()

    def create_form(self):
        # Main frame with better spacing
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(main_frame, text="Predict seminal quality of an indivisual",
                  font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        # Form fields
        self.fields = []

        # Field 1: Season
        ttk.Label(main_frame, text="1. Season:").grid(row=1, column=0, sticky=tk.W, pady=5)

        self.season_var = tk.StringVar(value="-1")
        season_frame = ttk.Frame(main_frame)
        season_frame.grid(row=1, column=1, sticky=tk.W, pady=5)

        seasons = [
            ("Winter", "-1"),
            ("Spring", "-0.33"),
            ("Summer", "0.33"),
            ("Fall", "1")
        ]

        for i, (text, value) in enumerate(seasons):
            rb = ttk.Radiobutton(season_frame, text=text, value=value, variable=self.season_var)
            rb.grid(row=0, column=i, padx=5, sticky=tk.W)

        self.fields.append(self.season_var)

        # Field 2: Age
        ttk.Label(main_frame, text="2. Age (18-36 years):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.age_var = tk.StringVar()
        age_entry = ttk.Entry(main_frame, textvariable=self.age_var)
        age_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.fields.append(self.age_var)

        # Field 3: Childish Diseases
        self.create_yes_no_field(main_frame, 3, "Childish Diseases",
                                 "Chicken pox, measles, mumps, polio")

        # Field 4: Accident or serious trauma
        self.create_yes_no_field(main_frame, 4, "Accident or serious trauma", "")

        # Field 5: Surgical intervention
        self.create_yes_no_field(main_frame, 5, "Surgical intervention", "")

        # Field 6: High fevers in last year
        ttk.Label(main_frame, text="6. High fevers in last year:").grid(row=6, column=0, sticky=tk.W, pady=5)

        self.fever_var = tk.StringVar(value="1")
        fever_frame = ttk.Frame(main_frame)
        fever_frame.grid(row=6, column=1, sticky=tk.W, pady=5)

        ttk.Radiobutton(fever_frame, text="No fever", value="1", variable=self.fever_var).pack(side=tk.LEFT)
        ttk.Radiobutton(fever_frame, text=">3 months ago", value="0", variable=self.fever_var).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Radiobutton(fever_frame, text="<3 months ago", value="-1", variable=self.fever_var).pack(side=tk.LEFT)

        self.fields.append(self.fever_var)

        # Field 7: Frequency of alcohol consumption (dropdown with descriptive options)
        ttk.Label(main_frame, text="7. Alcohol frequency:").grid(row=7, column=0, sticky=tk.W, pady=5)

        # Create a list of just the descriptions for the dropdown
        alcohol_descriptions = [desc for desc, val in self.alcohol_options]

        self.alcohol_var = tk.StringVar()
        self.alcohol_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.alcohol_var,
            values=alcohol_descriptions,
            state="readonly"
        )
        self.alcohol_combobox.current(4)  # Default to "Hardly ever or never"
        self.alcohol_combobox.grid(row=7, column=1, sticky=tk.W, pady=5)

        # We'll store the actual numerical value separately
        self.alcohol_numeric_var = tk.DoubleVar(value=1.0)  # Default value
        self.fields.append(self.alcohol_numeric_var)

        # Field 8: Smoking Habit
        ttk.Label(main_frame, text="8. Smoking habit:").grid(row=8, column=0, sticky=tk.W, pady=5)

        self.smoke_var = tk.StringVar(value="-1")
        smoke_frame = ttk.Frame(main_frame)
        smoke_frame.grid(row=8, column=1, sticky=tk.W, pady=5)

        ttk.Radiobutton(smoke_frame, text="Never", value="-1", variable=self.smoke_var).pack(side=tk.LEFT)
        ttk.Radiobutton(smoke_frame, text="Occasional", value="0", variable=self.smoke_var).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(smoke_frame, text="Daily", value="1", variable=self.smoke_var).pack(side=tk.LEFT)

        self.fields.append(self.smoke_var)

        # Field 9: Sitting hours
        ttk.Label(main_frame, text="9. Sitting hours (0-16):").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.sitting_var = tk.StringVar()
        sitting_entry = ttk.Entry(main_frame, textvariable=self.sitting_var)
        sitting_entry.grid(row=9, column=1, sticky=tk.W, pady=5)
        self.fields.append(self.sitting_var)

        # Output field
        ttk.Label(main_frame, text="Diagnosis result:").grid(row=10, column=0, sticky=tk.W, pady=10)
        self.output_var = tk.StringVar()
        self.output_var.set("Waiting for prediction...")
        ttk.Label(main_frame, textvariable=self.output_var, font=('Arial', 11)).grid(row=10, column=1, sticky=tk.W)

        # Buttons at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="Predict", command=self.predict).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="return to home", command=self.close_and_return).pack(side=tk.LEFT, padx=10)

    def close_and_return(self):
        """Close the form and return to home page"""
        self.root.destroy()
        from classificationMainPage.classification_first_page import classification_first_page_class
        home_page = classification_first_page_class()
        home_page.classification_first_page_load()

    def create_yes_no_field(self, parent, row, label, description):
        ttk.Label(parent, text=f"{row}. {label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
        if description:
            ttk.Label(parent, text=description, font=('Arial', 8)).grid(row=row, column=1, sticky=tk.W)

        var = tk.StringVar(value="0")
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=1, sticky=tk.W, pady=5)

        ttk.Radiobutton(frame, text="No", value="0", variable=var).pack(side=tk.LEFT)
        ttk.Radiobutton(frame, text="Yes", value="1", variable=var).pack(side=tk.LEFT, padx=5)

        self.fields.append(var)

    def get_alcohol_numeric_value(self):
        """Convert the selected alcohol description to its corresponding numeric value"""
        selected_desc = self.alcohol_var.get()
        for desc, val in self.alcohol_options:
            if desc == selected_desc:
                return val
        return 1.0  # Default value if not found

    def predict(self):
        try:
            # Validate all fields
            for i, field in enumerate(self.fields):
                # Skip alcohol check (we handle it separately)
                if i == 7:  # alcohol_numeric_var is at index 7
                    continue

                val = field.get()
                if val == "":
                    messagebox.showerror("Error", f"Please fill in all fields (Field {i + 1} is empty)")
                    return

            # Update alcohol numeric value based on selection
            self.alcohol_numeric_var.set(self.get_alcohol_numeric_value())

            # Validate and scale age (18-36 → 0-1)
            try:
                age = float(self.age_var.get())
                if age < 18 or age > 36:
                    messagebox.showerror("Error", "Age must be between 18-36 years")
                    return
                scaled_age = (age - 18) / (36 - 18)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for age (18-36)")
                return

            # Validate and scale sitting hours (0-16 → 0-1)
            try:
                sitting = float(self.sitting_var.get())
                if sitting < 0 or sitting > 16:
                    messagebox.showerror("Error", "Sitting hours must be between 0-16")
                    return
                scaled_sitting = sitting / 16
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for sitting hours (0-16)")
                return

            # Prepare data array
            values = [
                float(self.season_var.get()),
                scaled_age,
                float(self.fields[2].get()),  # Childish diseases
                float(self.fields[3].get()),  # Accident
                float(self.fields[4].get()),  # Surgery
                float(self.fever_var.get()),
                float(self.alcohol_numeric_var.get()),  # Alcohol frequency (already scaled)
                float(self.smoke_var.get()),
                scaled_sitting
            ]

            # Convert to numpy array and reshape
            new_array = np.array(values).reshape(1, -1)

            # Normalize with scaler
            new_scaled = self.scaler.transform(new_array)

            # Predict
            prediction = self.model.predict(new_scaled)[0]
            prediction_prob = self.model.predict_proba(new_scaled)

            # Display result
            result = "Normal" if prediction == 0 else "Altered"
            prob_normal = prediction_prob[0][0] * 100
            prob_altered = prediction_prob[0][1] * 100

            self.output_var.set(
                f"Result:\n Probability of being Normal={prob_normal:.1f}% \n Probability of being Altered={prob_altered:.1f}%")

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpermAnalysisForm(root)
    root.mainloop()