import tkinter as tk
from tkinter import ttk
from joblib import load
import warnings


class HeartDiseaseForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Disease Prediction Form")
        self.root.geometry("700x500")
        x = int(self.root.winfo_screenwidth() / 2 - 800 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 700 / 2)
        self.root.geometry(f'+{x}+{y}')

        # Initialize variables
        self.create_variables()
        self.create_widgets()

    def create_variables(self):
        # Age
        self.age_var = tk.DoubleVar()

        # Sex (1: Male, 0: Female)
        self.sex_var = tk.IntVar(value=1)

        # Chest Pain Type
        self.cp_var = tk.IntVar(value=1)
        self.cp_options = {
            1: 'Typical Angina',
            2: 'Atypical Angina',
            3: 'Non-anginal Pain',
            4: 'Asymptomatic'
        }

        # Resting Blood Pressure
        self.trestbps_var = tk.DoubleVar()

        # Serum Cholesterol
        self.chol_var = tk.DoubleVar()

        # Fasting Blood Sugar
        self.fbs_var = tk.IntVar(value=0)

        # Resting ECG
        self.restecg_var = tk.IntVar(value=0)
        self.restecg_options = {
            0: 'Normal',
            1: 'Abnormal',
            2: 'Abnormal'
        }

        # Maximum Heart Rate
        self.thalach_var = tk.DoubleVar()

        # Exercise Induced Angina
        self.exang_var = tk.IntVar(value=0)

        # ST Depression
        self.oldpeak_var = tk.DoubleVar()

        # Slope
        self.slope_var = tk.IntVar(value=1)
        self.slope_options = {
            1: 'Upsloping',
            2: 'Flat',
            3: 'Down Sloping'
        }

        # Number of Major Vessels
        self.ca_var = tk.IntVar(value=0)
        self.ca_options = [0, 1, 2, 3]

        # Thalassemia
        self.thal_var = tk.IntVar(value=3)
        self.thal_options = {
            3: 'Normal',
            6: 'Fixed Defect',
            7: 'Reversible Defect'
        }

        # Result variable
        self.result_var = tk.StringVar()
        self.result_var.set("Please fill the form and click Predict")

    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas
        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        form_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=form_frame, anchor="nw")

        # Title
        title_label = tk.Label(form_frame, text="Heart Disease Risk Assessment", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Form fields
        row = 1

        # Age
        tk.Label(form_frame, text="Age:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.age_var).grid(row=row, column=1, sticky="w", pady=5)
        row += 1

        # Sex - Horizontal layout
        tk.Label(form_frame, text="Sex:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        sex_frame = tk.Frame(form_frame)
        sex_frame.grid(row=row, column=1, sticky="w")
        tk.Radiobutton(sex_frame, text="Male", variable=self.sex_var, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(sex_frame, text="Female", variable=self.sex_var, value=0).pack(side=tk.LEFT, padx=10)
        row += 1

        # Chest Pain Type
        tk.Label(form_frame, text="Chest Pain Type:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        cp_frame = tk.Frame(form_frame)
        cp_frame.grid(row=row, column=1, sticky="w", columnspan=3)
        for key, value in self.cp_options.items():
            tk.Radiobutton(cp_frame, text=f"{value}", variable=self.cp_var, value=key).pack(side=tk.LEFT, padx=5)
        row += 1

        # Resting Blood Pressure
        tk.Label(form_frame, text="Resting Blood Pressure (mm Hg):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.trestbps_var).grid(row=row, column=1, sticky="w", pady=5)
        row += 1

        # Serum Cholesterol
        tk.Label(form_frame, text="Serum Cholesterol (mg/dl):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.chol_var).grid(row=row, column=1, sticky="w", pady=5)
        row += 1

        # Fasting Blood Sugar - Horizontal layout
        tk.Label(form_frame, text="Fasting Blood Sugar > 120 mg/dl:").grid(row=row, column=0, sticky="e", padx=5,
                                                                           pady=5)
        fbs_frame = tk.Frame(form_frame)
        fbs_frame.grid(row=row, column=1, sticky="w")
        tk.Radiobutton(fbs_frame, text="Yes", variable=self.fbs_var, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(fbs_frame, text="No", variable=self.fbs_var, value=0).pack(side=tk.LEFT, padx=10)
        row += 1

        # Resting ECG - Horizontal layout
        tk.Label(form_frame, text="Resting ECG Results:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        restecg_frame = tk.Frame(form_frame)
        restecg_frame.grid(row=row, column=1, sticky="w")
        for key, value in self.restecg_options.items():
            tk.Radiobutton(restecg_frame, text=f"{value}", variable=self.restecg_var, value=key).pack(side=tk.LEFT,
                                                                                                      padx=5)
        row += 1

        # Maximum Heart Rate
        tk.Label(form_frame, text="Maximum Heart Rate Achieved:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.thalach_var).grid(row=row, column=1, sticky="w", pady=5)
        row += 1

        # Exercise Induced Angina - Horizontal layout
        tk.Label(form_frame, text="Exercise Induced Angina:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        exang_frame = tk.Frame(form_frame)
        exang_frame.grid(row=row, column=1, sticky="w")
        tk.Radiobutton(exang_frame, text="Yes", variable=self.exang_var, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(exang_frame, text="No", variable=self.exang_var, value=0).pack(side=tk.LEFT, padx=10)
        row += 1

        # ST Depression
        tk.Label(form_frame, text="ST Depression Induced by Exercise:").grid(row=row, column=0, sticky="e", padx=5,
                                                                             pady=5)
        tk.Entry(form_frame, textvariable=self.oldpeak_var).grid(row=row, column=1, sticky="w", pady=5)
        row += 1

        # Slope - Horizontal layout
        tk.Label(form_frame, text="Slope of Peak Exercise ST Segment:").grid(row=row, column=0, sticky="e", padx=5,
                                                                             pady=5)
        slope_frame = tk.Frame(form_frame)
        slope_frame.grid(row=row, column=1, sticky="w")
        for key, value in self.slope_options.items():
            tk.Radiobutton(slope_frame, text=f"{value}", variable=self.slope_var, value=key).pack(side=tk.LEFT, padx=5)
        row += 1

        # Number of Major Vessels - Horizontal layout
        tk.Label(form_frame, text="Number of Major Vessels (0-3):").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        ca_frame = tk.Frame(form_frame)
        ca_frame.grid(row=row, column=1, sticky="w")
        for option in self.ca_options:
            tk.Radiobutton(ca_frame, text=str(option), variable=self.ca_var, value=option).pack(side=tk.LEFT, padx=5)
        row += 1

        # Thalassemia - Horizontal layout
        tk.Label(form_frame, text="Thalassemia:").grid(row=row, column=0, sticky="e", padx=5, pady=5)
        thal_frame = tk.Frame(form_frame)
        thal_frame.grid(row=row, column=1, sticky="w")
        for key, value in self.thal_options.items():
            tk.Radiobutton(thal_frame, text=f"{value}", variable=self.thal_var, value=key).pack(side=tk.LEFT, padx=5)
        row += 1

        # Result display
        result_frame = tk.Frame(form_frame, relief=tk.SUNKEN, borderwidth=5)
        result_frame.grid(row=row, column=0, columnspan=4, pady=20,padx=20, sticky="ew")
        tk.Label(result_frame, text="Prediction Result:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.result_label = tk.Label(result_frame, textvariable=self.result_var, font=("Arial", 10))
        self.result_label.pack(anchor="w", fill=tk.X, padx=5, pady=5)
        row += 1

        # Buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        predict_btn = tk.Button(button_frame, text="Predict", command=self.predict)
        predict_btn.pack(side=tk.LEFT, padx=10)

        home_btn = tk.Button(button_frame, text="Return Home", command=self.return_home)
        home_btn.pack(side=tk.LEFT, padx=10)

        # Set default values for testing
        self.set_default_values()

    def set_default_values(self):
        # Set default values for testing
        self.age_var.set(" ")
        self.sex_var.set(' ')
        self.cp_var.set(' ')
        self.trestbps_var.set(' ')
        self.chol_var.set(' ')
        self.fbs_var.set(' ')
        self.restecg_var.set(' ')
        self.thalach_var.set(' ')
        self.exang_var.set(' ')
        self.oldpeak_var.set(' ')
        self.slope_var.set(' ')
        self.ca_var.set(' ')
        self.thal_var.set(' ')

    def predict(self):
        try:
            # Collect all data
            new_data = [
                float(self.age_var.get()),
                int(self.sex_var.get()),
                int(self.cp_var.get()),
                float(self.trestbps_var.get()),
                float(self.chol_var.get()),
                int(self.fbs_var.get()),
                int(self.restecg_var.get()),
                float(self.thalach_var.get()),
                int(self.exang_var.get()),
                float(self.oldpeak_var.get()),
                int(self.slope_var.get()),
                int(self.ca_var.get()),
                int(self.thal_var.get())
            ]

            # Load model and make prediction
            warnings.filterwarnings("ignore", category=FutureWarning)
            warnings.filterwarnings("ignore", category=UserWarning)

            final_model = load('final_model_dt2_heart_disease.joblib')
            probabilities = final_model.predict_proba([new_data])
            prediction = final_model.predict([new_data])[0]

            # Interpret results
            severity_levels = {
                0: "No heart disease",
                1: "Mild heart disease",
                2: "Moderate heart disease",
                3: "Serious heart disease",
                4: "Severe heart disease"
            }

            result_text = severity_levels.get(prediction, "Unknown heart disease status")
            probability_text = f" No disease {probabilities[0][0] * 100:.1f}%\n" \
                               f" Mild heart disease {probabilities[0][1] * 100:.1f}%\n"\
                               f" Moderate heart disease {probabilities[0][2] * 100:.1f}%\n"\
                               f" Serious heart disease {probabilities[0][3] * 100:.1f}%\n"\
                               f" Severe heart disease {probabilities[0][4] * 100:.1f}%\n"



            # Update result display
            self.result_var.set(f"{result_text}\n{probability_text}")

        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")

    def return_home(self):
        self.root.destroy()
        from classificationMainPage.classification_first_page import classification_first_page_class
        regressionPage_obj = classification_first_page_class()
        regressionPage_obj.classification_first_page_load()


if __name__ == "__main__":
    root = tk.Tk()
    app = HeartDiseaseForm(root)
    root.mainloop()