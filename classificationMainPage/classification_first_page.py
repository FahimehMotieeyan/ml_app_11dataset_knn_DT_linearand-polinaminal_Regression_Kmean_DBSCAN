from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk, ImageFilter  # نیاز به نصب pillow با دستور: pip install pillow
import tkinter as tk

class classification_first_page_class():
    def classification_first_page_load(self):
        root = Tk()
        root.title("Algorithms Selection")
        root.geometry('900x600')
        root.resizable(0, 0)

        # Center the window
        x = int(root.winfo_screenwidth() / 2 - 900 / 2)
        y = int(root.winfo_screenheight() / 2 - 600 / 2)
        root.geometry(f'+{x}+{y}')

        # Create notebook (tab control)
        notebook = ttk.Notebook(root)
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('TLabel', font=('Arial', 12))
        title_font = Font(family='Helvetica', size=14, weight='bold')

        def open_main_form():
            root.destroy()
            from first_page import run_main_page  # وارد کردن تابع از فایل اصلی
            run_main_page()

        def csv1_2():
            root.destroy()
            from classificationMainPage.csv1 import WiFiRoomPredictor
            root5 = tk.Tk()
            app = WiFiRoomPredictor(root5)
            root5.mainloop()

        def knn2_opening():
            root.destroy()
            from classificationMainPage.knn2_car_page import CarAcceptabilityPredictor
            root6 = tk.Tk()
            app = CarAcceptabilityPredictor(root6)
            root6.mainloop()

        def knn3_opening():
            root.destroy()
            from classificationMainPage.knn3_sperm_page import SpermAnalysisForm
            root7 = tk.Tk()
            app = SpermAnalysisForm(root7)
            root7.mainloop()
        def dt1_opening():
            root.destroy()
            from classificationMainPage.dt1_bankruptcy_page import BankruptcyPredictionForm
            root8 = tk.Tk()
            app = BankruptcyPredictionForm(root8)
            root8.mainloop()
        def dt2_opening():
            root.destroy()
            from classificationMainPage.dt2_heart_disease_page import HeartDiseaseForm
            root9 = tk.Tk()
            app = HeartDiseaseForm(root9)
            root9.mainloop()
        def dt3_opening():
            root.destroy()
            from classificationMainPage.dt3_survive_heart_page import HeartAttackSurvivalForm
            root11 = tk.Tk()
            app = HeartAttackSurvivalForm(root11)
            root11.mainloop()






            # 🌸🌸🌸🌸knn Tab
        svm_frame = ttk.Frame(notebook)
        notebook.add(svm_frame, text="KNN")

        # Load and resize images
        original_img1 = Image.open('images/wifi.png')
        original_img2 = Image.open('images/car_knn.jpg')
        original_img3 = Image.open('images/sperm.jpg')

        # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        resized_img2 = original_img2.resize((130, 130), Image.Resampling.LANCZOS)
        resized_img3 = original_img3.resize((130, 130), Image.Resampling.LANCZOS)

        self.svm1_image = ImageTk.PhotoImage(resized_img1)
        self.svm2_image = ImageTk.PhotoImage(resized_img2)
        self.svm3_image = ImageTk.PhotoImage(resized_img3)

        # Create buttons with resized images
        btnsvm1 = ttk.Button(
            svm_frame,
            image=self.svm1_image,
            compound=TOP,
            command=csv1_2,
            text= 'Can you estimate the location from WIFI Signal Strength',
            style='TButton'
        )
        btnsvm1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)

        btnsvm2 = ttk.Button(
            svm_frame,
            image=self.svm2_image,
            compound=TOP,
            command= knn2_opening,
            text='                    Predict the acceptability of a car                    ',
            style='TButton'
        )
        btnsvm2.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)

        btnsvm3 = ttk.Button(
            svm_frame,
            image=self.svm3_image,
            compound=TOP,
            command= knn3_opening,
            text='           Predict the seminal quality of an individual           ',
            style='TButton'
        )
        btnsvm3.grid(row=1, column=0, padx=10, pady=10, ipadx=5, ipady=5)

        # Load Home icon for Back to Main button
        home_icon = Image.open('images/regresion.png')
        resized_home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.home_image = ImageTk.PhotoImage(resized_home_icon)

        # Create Back to Main button
        back_button = ttk.Button(
            root,
            image=self.home_image,
            text="Back to Main",
            compound=LEFT,
            command=open_main_form
        )
        back_button.pack(side=RIGHT, pady=10,padx=10)

        #🌸🌸🌸🌸 DT Tab
        knn_frame = ttk.Frame(notebook)
        notebook.add(knn_frame, text="decision tree")

        # Load and resize images
        original_img1 = Image.open('images/bank_varshekastegy.jpg')
        original_img2 = Image.open('images/heartDeases.jpg')
        original_img3 = Image.open('images/surviveHeart.jpg')

        # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        resized_img2 = original_img2.resize((130, 130), Image.Resampling.LANCZOS)
        resized_img3 = original_img3.resize((130, 130), Image.Resampling.LANCZOS)

        self.knn1_image = ImageTk.PhotoImage(resized_img1)
        self.knn2_image = ImageTk.PhotoImage(resized_img2)
        self.knn3_image = ImageTk.PhotoImage(resized_img3)

        # Create buttons with resized images
        btnknn1 = ttk.Button(
            knn_frame,
            image=self.knn1_image,
            compound=TOP,
            command=dt1_opening,
            text='  Estimate the chance of bankruptcy from  parameters  ',
            style='TButton'
        )
        btnknn1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)

        btnknn2 = ttk.Button(
            knn_frame,
            image=self.knn2_image,
            compound=TOP,
            command=dt2_opening,
            text='        Was that chest pain an indicator of a heart disease      ',
            style='TButton'
        )
        btnknn2.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)
        btnknn3 = ttk.Button(
            knn_frame,
            image=self.knn3_image,
            compound=TOP,
            command=dt3_opening,
            text=' patient survive at least one year after a heart attack ',
            style='TButton'
        )
        btnknn3.grid(row=1, column=0, padx=10, pady=10, ipadx=5, ipady=5)



        root.mainloop()

    # def open_main_form(self):
    #     """Open a new form when Back to Main button is clicked"""
    #     main_form = Toplevel()
    #     main_form.title("Main Form")
    #     main_form.geometry('600x400')
    #
    #     # Center the form
    #     x = int(main_form.winfo_screenwidth() / 2 - 600 / 2)
    #     y = int(main_form.winfo_screenheight() / 2 - 400 / 2)
    #     main_form.geometry(f'+{x}+{y}')
    #
    #     # Add a label to the form
    #     label = ttk.Label(main_form, text="Welcome to Main Form!", font=('Arial', 14))
    #     label.pack(pady=50)
    #
    #     # Add a close button
    #     close_button = ttk.Button(main_form, text="Close", command=main_form.destroy)
    #     close_button.pack(pady=20)

#
# classificationPage_obj = classification_first_page_class()
# classificationPage_obj.classification_first_page_load()