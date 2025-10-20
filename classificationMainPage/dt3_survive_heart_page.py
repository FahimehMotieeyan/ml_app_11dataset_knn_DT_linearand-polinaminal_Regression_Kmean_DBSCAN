import tkinter as tk
from tkinter import ttk, messagebox
from joblib import load
import warnings
import sys
from io import StringIO

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class HeartAttackSurvivalForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Attack Survival Prediction")
        self.root.geometry("750x700")
        self.root.configure(bg='#f0f0f0')

        # Center the window
        x = int(self.root.winfo_screenwidth() / 2 - 750 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 800 / 2)
        self.root.geometry(f'+{x}+{y}')

        # Main frame with padding and styling
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title label with improved styling
        title_label = ttk.Label(
            self.main_frame,
            text="Heart Attack Survival Prediction",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50",
            wraplength=600
        )
        title_label.pack(pady=(0, 15))

        subtitle_label = ttk.Label(
            self.main_frame,
            text="Will the patient survive for at least one year after a heart attack?",
            font=("Arial", 12),
            foreground="#7f8c8d",
            wraplength=600
        )
        subtitle_label.pack(pady=(0, 20))

        # Form fields with improved layout
        self.create_form_fields()

        # Button frame to hold both buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        # Predict button with improved styling
        predict_btn = ttk.Button(
            button_frame,
            text="Predict",
            command=self.predict_survival,
            style='Accent.TButton'
        )
        predict_btn.pack(side=tk.LEFT, padx=10, ipadx=15)

        # Back to home button with improved styling
        back_btn = ttk.Button(
            button_frame,
            text="Back to Home",
            command=self.back_to_home,
            style='TButton'
        )
        back_btn.pack(side=tk.LEFT, padx=10, ipadx=15)

        # Result frame with improved styling
        self.result_frame = ttk.LabelFrame(
            self.main_frame,
            text="Prediction Result",
            padding=15,
            style='Card.TFrame'
        )
        self.result_frame.pack(fill=tk.X, pady=(10, 0))

        # Configure styles
        self.configure_styles()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'),
                        foreground='white', background='#3498db', padding=5)
        style.map('Accent.TButton', background=[('active', '#2980b9')])
        style.configure('Card.TFrame', background='white',
                        bordercolor='#bdc3c7', relief='solid', borderwidth=1)
        style.configure('TLabelframe.Label', font=('Arial', 11, 'bold'))
        style.configure('TLabelframe', background='#f0f0f0')

    def create_form_fields(self):
        fields = [
            ("Age-at-heart-attack", "Age in years when heart attack occurred(0-100)"),
            ("Pericardial-effusion", "Pericardial effusion is fluid around the heart (0: no fluid, 1: fluid)"),
            ("Fractional-shortening",
             "A measure of contracility around the heart (0-1, lower numbers are increasingly abnormal)"),
            ("Epss", "E-point septal separation (larger numbers are increasingly abnormal(0_40))"),
            ("Lvdd", "Left ventricular end-diastolic dimension (measure of heart size at end-diastole(2_8))"),
            ("Wall-motion-score", "A measure of how the segments of the left ventricle are moving(2_40)"),
            ("Wall-motion-index", "Wall-motion-score divided by number of segments seen (1_3) but ")
        ]

        self.entries = {}
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill=tk.X, pady=10)

        for i, (field, desc) in enumerate(fields):
            row_frame = ttk.Frame(form_frame)
            row_frame.pack(fill=tk.X, pady=5, padx=10)

            label = ttk.Label(
                row_frame,
                text=f"{field}:",
                width=25,
                anchor=tk.W,
                font=('Arial', 10)
            )
            label.pack(side=tk.LEFT)

            entry = ttk.Entry(
                row_frame,
                font=('Arial', 10),
                width=30
            )
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Add info button for tooltip
            info_btn = ttk.Button(
                row_frame,
                text="ℹ️",
                width=2,
                command=lambda d=desc: self.show_tooltip(d)
            )
            info_btn.pack(side=tk.LEFT, padx=5)

            self.entries[field] = entry

    def show_tooltip(self, text):
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+%d+%d" % (self.root.winfo_pointerx() + 15,
                                        self.root.winfo_pointery() + 15))

        frame = ttk.Frame(tooltip, style='Card.TFrame', padding=10)
        frame.pack()

        label = ttk.Label(
            frame,
            text=text,
            wraplength=300,
            justify=tk.LEFT
        )
        label.pack()

        # Close tooltip when mouse leaves
        tooltip.bind("<Leave>", lambda e: tooltip.destroy())

    def predict_survival(self):
        try:
            # Get values from form
            age = float(self.entries["Age-at-heart-attack"].get())
            pericardial = int(self.entries["Pericardial-effusion"].get())
            fractional = float(self.entries["Fractional-shortening"].get())
            epss = float(self.entries["Epss"].get())
            lvdd = float(self.entries["Lvdd"].get())
            wall_score = float(self.entries["Wall-motion-score"].get())
            wall_index = float(self.entries["Wall-motion-index"].get())

            # Prepare input for model
            new_data = [[age, pericardial, fractional, epss, lvdd, wall_score, wall_index]]

            # Load model and predict (simulated here - replace with actual model loading)
            # final_model = load('final_model_dt3_heart_survive.joblib')
            # probabilities = final_model.predict_proba(new_data)
            # prediction = final_model.predict(new_data)

            # For demonstration, we'll use simulated results
            probabilities = [[0.3, 0.7]]  # Replace with actual model output
            prediction = [1]  # Replace with actual model output

            # Display results
            self.show_results(prediction[0], probabilities[0])

        except ValueError as e:
            messagebox.showerror("Input Error", f"Please enter valid numerical values for all fields.\nError: {str(e)}")

    def show_results(self, prediction, probabilities):
        # Clear previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Prediction text with improved styling
        result_text = tk.StringVar()
        if prediction == 0:
            result_text.set("Prediction: High Risk - Patient may not survive 1 year")
            color = "#e74c3c"  # Red
        else:
            result_text.set("Prediction: Low Risk - Patient likely to survive 1 year")
            color = "#2ecc71"  # Green

        result_label = ttk.Label(
            self.result_frame,
            textvariable=result_text,
            font=("Arial", 12, "bold"),
            foreground=color
        )
        result_label.pack(pady=(0, 15))

        # Probability bars with improved styling
        prob_frame = ttk.Frame(self.result_frame)
        prob_frame.pack(fill=tk.X, pady=5)

        # Not survived probability
        not_survived_frame = ttk.Frame(prob_frame)
        not_survived_frame.pack(fill=tk.X, pady=5)

        not_survived_label = ttk.Label(
            not_survived_frame,
            text="Not Survived (0):",
            width=20,
            anchor=tk.W,
            font=('Arial', 10)
        )
        not_survived_label.pack(side=tk.LEFT)

        not_survived_prob = probabilities[0]

        canvas = tk.Canvas(
            not_survived_frame,
            height=20,
            bg='white',
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Draw the progress bar
        width = canvas.winfo_width()
        if width < 1:  # If canvas hasn't been drawn yet
            width = 200  # Default width
        canvas.create_rectangle(
            0, 0, width * not_survived_prob, 20,
            fill='#e74c3c', outline=''
        )

        not_survived_percent = ttk.Label(
            not_survived_frame,
            text=f"{not_survived_prob * 100:.1f}%",
            font=('Arial', 10)
        )
        not_survived_percent.pack(side=tk.LEFT, padx=5)

        # Survived probability
        survived_frame = ttk.Frame(prob_frame)
        survived_frame.pack(fill=tk.X, pady=5)

        survived_label = ttk.Label(
            survived_frame,
            text="Survived (1):",
            width=20,
            anchor=tk.W,
            font=('Arial', 10)
        )
        survived_label.pack(side=tk.LEFT)

        survived_prob = probabilities[1]

        canvas = tk.Canvas(
            survived_frame,
            height=20,
            bg='white',
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Draw the progress bar
        width = canvas.winfo_width()
        if width < 1:  # If canvas hasn't been drawn yet
            width = 200  # Default width
        canvas.create_rectangle(
            0, 0, width * survived_prob, 20,
            fill='#2ecc71', outline=''
        )

        survived_percent = ttk.Label(
            survived_frame,
            text=f"{survived_prob * 100:.1f}%",
            font=('Arial', 10)
        )
        survived_percent.pack(side=tk.LEFT, padx=5)

    def back_to_home(self):
        self.root.destroy()
        from classificationMainPage.classification_first_page import classification_first_page_class
        regressionPage_obj = classification_first_page_class()
        regressionPage_obj.classification_first_page_load()


if __name__ == "__main__":
    root = tk.Tk()
    app = HeartAttackSurvivalForm(root)
    root.mainloop()