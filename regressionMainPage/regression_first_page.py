from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk, ImageFilter



class regression_first_page_class():
    def regression_first_page_load(self):
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

        def k_mean_1_student_openPage():
            root.destroy()
            from regressionMainPage.regression_1_alabama_page import AbaloneForm
            roo = tk.Tk()
            app_obj = AbaloneForm(roo)
            roo.mainloop()


        def polinaminal_regreesion_openPage():
            root.destroy()
            from regressionMainPage.regression_2_polynaminal_house_page import HousePriceForm
            roo2 = tk.Tk()
            app2_ong = HousePriceForm(roo2)
            roo2.mainloop()




            # 🌸🌸🌸🌸k_means Tab
        regression_frame = ttk.Frame(notebook)
        notebook.add(regression_frame, text="Multiple Regression")

        # Load and resize images
        original_img1 = Image.open('images/Abalone.png')
        # original_img2 = Image.open('images/house_price.jpg')

        # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        # resized_img2 = original_img2.resize((130, 130), Image.Resampling.LANCZOS)

        self.regression1_image = ImageTk.PhotoImage(resized_img1)
        # self.regression2_image = ImageTk.PhotoImage(resized_img2)

        # Create buttons with resized images
        btnregression1 = ttk.Button(
            regression_frame,
            image=self.regression1_image,
            compound=TOP,
            command=k_mean_1_student_openPage,
            text= 'Find out the age of Abalone from physical measurements',
            style='TButton'
        )
        btnregression1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)

        # btnregression2 = ttk.Button(
        #     regression_frame,
        #     image=self.regression2_image,
        #     compound=TOP,
        #     text='                Can you predict the price of a house?              ',
        #     style='TButton'
        # )
        # btnregression2.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)

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

        #🌸🌸🌸🌸 knn Tab
        pr_frame = ttk.Frame(notebook)
        notebook.add(pr_frame, text="Polinaminal Regression")
        #
        # # Load and resize images
        original_img1 = Image.open('images/house_price.jpg')
        # original_img2 = Image.open('images/regresion.png')
        #
        # # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        # resized_img2 = original_img2.resize((100, 100), Image.Resampling.LANCZOS)
        #
        self.pr1_image = ImageTk.PhotoImage(resized_img1)
        # self.knn2_image = ImageTk.PhotoImage(resized_img2)
        #
        # # Create buttons with resized images
        btnpr1 = ttk.Button(
            pr_frame,
            image=self.pr1_image,
            compound=TOP,
            command=polinaminal_regreesion_openPage,
            text='               Can you predict the price of a house?              ',
            style='TButton'
        )
        btnpr1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
        #
        # btnknn2 = ttk.Button(
        #     knn_frame,
        #     image=self.knn2_image,
        #     compound=TOP,
        #     text='knn2 Model 2',
        #     style='TButton'
        # )
        # btnknn2.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)



        root.mainloop()