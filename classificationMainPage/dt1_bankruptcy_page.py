import tkinter as tk
from tkinter import ttk, messagebox
from joblib import load
import sys
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class BankruptcyPredictionForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Bankruptcy Prediction Form")
        self.root.geometry("800x620")
        self.root.configure(bg='#f0f0f0')
        x = int(self.root.winfo_screenwidth() / 2 -800 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 700 / 2)
        self.root.geometry(f'+{x}+{y}')

        # Load models (these would need to be in your directory)
        try:
            self.final_model = load('final_model_dt1_Bankruptcy.joblib')
            self.encoder = load('encoder_dt1_Bankruptcy.joblib')
        except FileNotFoundError:
            messagebox.showerror("Error", "Model files not found!")
            self.root.destroy()
            return

        self.create_form()

    def create_form(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50')
        header_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(header_frame, text="Bankruptcy Risk Assessment", font=('Arial', 20, 'bold'),
                 fg='white', bg='#2c3e50').pack(pady=15)

        # Form frame
        form_frame = tk.Frame(self.root, bg='#f0f0f0')
        form_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Form fields
        self.fields = [
            'Industrial Risk',
            'Management Risk',
            'Financial Flexibility',
            'Credibility',
            'Competitiveness',
            'Operating Risk'
        ]

        self.vars = []

        for i, field in enumerate(self.fields):
            frame = tk.Frame(form_frame, bg='#f0f0f0')
            frame.pack(fill='x', pady=8)

            tk.Label(frame, text=field, font=('Arial', 12), bg='#f0f0f0', width=20, anchor='w').pack(side='left')

            var = tk.StringVar(value='Average')
            self.vars.append(var)

            # Create a custom style for the scale
            style = ttk.Style()
            style.configure("Custom.Horizontal.TScale", background='#f0f0f0')

            scale = ttk.Scale(frame, from_=0, to=2, value=1, orient='horizontal',
                              style="Custom.Horizontal.TScale",
                              command=lambda val, idx=i: self.update_label(val, idx))
            scale.pack(side='left', fill='x', expand=True, padx=10)

            label = tk.Label(frame, text="Average", width=10, font=('Arial', 10), bg='#f0f0f0')
            label.pack(side='left', padx=10)

            # Store the label reference for updating
            setattr(self, f"label_{i}", label)

        # Button frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)

        # Predict button
        predict_btn = tk.Button(button_frame, text="Predict Bankruptcy Risk",
                                command=self.predict, bg='#3498db', fg='white',
                                font=('Arial', 12, 'bold'), padx=20, pady=10)
        predict_btn.pack(side='left', padx=10)

        # Home button
        home_btn = tk.Button(button_frame, text="Return Home",
                             command=self.return_home, bg='#95a5a6', fg='white',
                             font=('Arial', 12), padx=20, pady=10)
        home_btn.pack(side='left', padx=10)

        # Result frame
        self.result_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.result_frame.pack(pady=10, fill='x')

    def update_label(self, val, idx):
        value = float(val)
        if value < 0.5:
            text = "Negative"
        elif value < 1.5:
            text = "Average"
        else:
            text = "Positive"

        getattr(self, f"label_{idx}").config(text=text)
        self.vars[idx].set(text[0])  # Store P, A, or N

    def predict(self):
        # Prepare data
        new_data = [[var.get()[0] for var in self.vars]]  # Gets P, A, or N

        # Encode and predict
        try:
            new_data_encoded = self.encoder.transform(new_data)
            probabilities = self.final_model.predict_proba(new_data_encoded)

            # Clear previous results
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            # Display results
            tk.Label(self.result_frame, text="Prediction Results:",
                     font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)

            # Non-Bankruptcy
            non_bankruptcy_frame = tk.Frame(self.result_frame, bg='#f0f0f0')
            non_bankruptcy_frame.pack(fill='x', pady=5)
            tk.Label(non_bankruptcy_frame, text="Non-Bankruptcy Probability:",
                     font=('Arial', 12), bg='#f0f0f0', width=25, anchor='w').pack(side='left')
            self.create_progress_bar(non_bankruptcy_frame, probabilities[0][1], 'green')

            # Bankruptcy
            bankruptcy_frame = tk.Frame(self.result_frame, bg='#f0f0f0')
            bankruptcy_frame.pack(fill='x', pady=5)
            tk.Label(bankruptcy_frame, text="Bankruptcy Probability:",
                     font=('Arial', 12), bg='#f0f0f0', width=25, anchor='w').pack(side='left')
            self.create_progress_bar(bankruptcy_frame, probabilities[0][0], 'red')

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

    def create_progress_bar(self, parent, value, color):
        # Create a canvas for custom progress bar
        canvas = tk.Canvas(parent, width=300, height=20, bg='white', highlightthickness=0)
        canvas.pack(side='left', padx=10)

        # Draw the background
        canvas.create_rectangle(0, 0, 300, 20, fill='#ecf0f1', outline='#bdc3c7')

        # Draw the progress
        width = value * 300
        canvas.create_rectangle(0, 0, width, 20, fill=color, outline='')

        # Add text
        canvas.create_text(150, 10, text=f"{value:.2%}", font=('Arial', 10, 'bold'))

    def return_home(self):
        self.root.destroy()
        # This would need to be replaced with your actual home page import
        try:
            from classificationMainPage.classification_first_page import classification_first_page_class
            regressionPage_obj = classification_first_page_class()
            regressionPage_obj.classification_first_page_load()

        except ImportError:
            messagebox.showinfo("Info", "Returning to home page is not configured in this demo.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankruptcyPredictionForm(root)
    root.mainloop()