from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg
from tkinter.font import Font

def run_main_page():
    firstpage = Tk()
    firstpage.title("Algorithms Selection")
    firstpage.geometry('1170x500')
    firstpage.resizable(0, 0)
    firstpage.iconbitmap('images/MIB.ico')
    x = int(firstpage.winfo_screenwidth() / 2 - 1170 / 2)
    y = int(firstpage.winfo_screenheight() / 2 - 500 / 2)
    firstpage.geometry(f'+{x}+{y}')

    def classification_openpage():
        firstpage.destroy()
        from classificationMainPage.classification_first_page import classification_first_page_class
        classificationPage_obj = classification_first_page_class()
        classificationPage_obj.classification_first_page_load()

    def clustring_openpage():
        firstpage.destroy()
        from clustringMainPage.clustring_first_page import clustring_first_page_class
        clustringPage_obj = clustring_first_page_class()
        clustringPage_obj.clustring_first_page_load()

    def regression_openpage():
        firstpage.destroy()
        from regressionMainPage.regression_first_page import regression_first_page_class
        regressionPage_obj = regression_first_page_class()
        regressionPage_obj.regression_first_page_load()



    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'), padding=10)
    style.configure('TLabel', font=('Arial', 12))

    title_font = Font(family='Helvetica', size=16, weight='bold')

    labpage = Label(firstpage, text="Choose Your Algorithm", font=title_font, fg='#333366')
    labpage.grid(row=0, column=0, columnspan=3, pady=25)

    classification_image = PhotoImage(file='images/clasification.png')
    clustring_image = PhotoImage(file='images/cluster.png')
    regression_image = PhotoImage(file='images/regresion.png')

    btnClassification = ttk.Button(
        firstpage,
        image=classification_image,
        compound=TOP,
        command=classification_openpage,
        text='Classification Models',
        style='TButton'
    )
    btnClassification.grid(row=1, column=0, padx=20, pady=20, ipadx=10, ipady=10)

    btnClusting = ttk.Button(
        firstpage,
        image=clustring_image,
        compound=TOP,
        command=clustring_openpage,
        text='Clustering Models',
        style='TButton'
    )
    btnClusting.grid(row=1, column=2, padx=20, pady=20, ipadx=10, ipady=10)

    btnregression = ttk.Button(
        firstpage,
        image=regression_image,
        compound=TOP,
        command=regression_openpage,
        text='Regression Models',
        style='TButton'
    )
    btnregression.grid(row=1, column=1, padx=20, pady=20, ipadx=10, ipady=10)

    firstpage.configure(bg='#f0f0f0')
    firstpage.mainloop()

# اجرای تابع اصلی اگر فایل مستقیماً اجرا شود
if __name__ == "__main__":
    run_main_page()

