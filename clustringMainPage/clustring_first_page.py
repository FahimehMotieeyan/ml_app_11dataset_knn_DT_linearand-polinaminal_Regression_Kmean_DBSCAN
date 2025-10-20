from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import Image, ImageTk, ImageFilter



class clustring_first_page_class():
    def clustring_first_page_load(self):
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
            from clustringMainPage.k_mean_1_student_Page import KnowledgeLevelClustering
            # root = tk.Tk()

            clustering_app = KnowledgeLevelClustering()
            # root.mainloop()


        def dbscan_1_opening():
            root.destroy()
            from clustringMainPage.DBSCAN_1_retail_page import CustomerSegmentationApp
            root44 = tk.Tk()
            app = CustomerSegmentationApp(root44)
            root44.mainloop()

        def kmean_1_opening():
            root.destroy()
            from clustringMainPage.k_means_2_alchole_page import ClusterVisualizationApp
            root88 = tk.Tk()
            app = ClusterVisualizationApp(root88)
            root88.mainloop()







            # from classificationMainPage.csv1 import csv1_class
            # csv1_obj = csv1_class()
            # csv1_obj.csv1_load()





            # 🌸🌸🌸🌸k_means Tab
        k_mean_frame = ttk.Frame(notebook)
        notebook.add(k_mean_frame, text="k_mean")

        # Load and resize images
        original_img1 = Image.open('images/student_knowledge.jpg')
        original_img2 = Image.open('images/alchol_liver.jpg')

        # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        resized_img2 = original_img2.resize((130, 130), Image.Resampling.LANCZOS)

        self.k_mean1_image = ImageTk.PhotoImage(resized_img1)
        self.k_mean2_image = ImageTk.PhotoImage(resized_img2)

        # Create buttons with resized images
        btnk_mean1 = ttk.Button(
            k_mean_frame,
            image=self.k_mean1_image,
            compound=TOP,
            command=k_mean_1_student_openPage,
            text= '           Cluster student’s knowledge level by yourself          ',
            style='TButton'
        )
        btnk_mean1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)

        btnk_mean2 = ttk.Button(
            k_mean_frame,
            image=self.k_mean2_image,
            compound=TOP,
            command= kmean_1_opening,
            text=' patterns relating to the liver disorder and alcohol consumption',
            style='TButton'
        )
        btnk_mean2.grid(row=0, column=1, padx=10, pady=10, ipadx=5, ipady=5)

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
        knn_frame = ttk.Frame(notebook)
        notebook.add(knn_frame, text="DBSCAN")
        #
        # # Load and resize images
        original_img1 = Image.open('images/retail.jpg')
        # original_img2 = Image.open('images/regresion.png')
        #
        # # Resize images (new width, new height)
        resized_img1 = original_img1.resize((130, 130), Image.Resampling.LANCZOS)
        # resized_img2 = original_img2.resize((100, 100), Image.Resampling.LANCZOS)
        #
        self.knn1_image = ImageTk.PhotoImage(resized_img1)
        # self.knn2_image = ImageTk.PhotoImage(resized_img2)
        #
        # Create buttons with resized images
        btnknn1 = ttk.Button(
            knn_frame,
            image=self.knn1_image,
            compound=TOP,
            command=dbscan_1_opening,
            text='          find patterns from spending data at wholesale           ',
            style='TButton'
        )
        btnknn1.grid(row=0, column=0, padx=10, pady=10, ipadx=5, ipady=5)
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