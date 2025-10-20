import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class KnowledgeLevelClustering:
    def __init__(self, master=None, open_main_form=None):
        if master is None:
            self.root = tk.Tk()
        else:
            self.root = master

        self.open_main_form = open_main_form  # Store the callback function
        self.cluster_var = tk.IntVar(value=3)
        self.setup_ui()

        if master is None:
            self.root.mainloop()

    @staticmethod
    def get_cluster_names(n_clusters):
        """Return appropriate labels based on number of clusters"""
        names = {
            2: ["Very Weak", "Very Strong"],
            3: ["Weak", "Medium", "Strong"],
            4: ["Very Weak", "Weak", "Medium", "Strong"],
            5: ["Very Weak", "Weak", "Medium", "Good", "Excellent"],
            6: ["Very Weak", "Weak", "Below Average", "Above Average", "Good", "Excellent"],
            7: ["Very Weak", "Weak", "Below Average", "Average", "Above Average", "Good", "Excellent"],
            8: ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8"],
            9: ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9"],
            10: ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9",
                 "Level 10"],
            11: ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9",
                 "Level 10", "Level 11"]
        }
        return names.get(n_clusters, [f"Group {i + 1}" for i in range(n_clusters)])

    @staticmethod
    def create_level_indicator(n_clusters):
        """Create a visual scale showing all levels"""
        frame = ttk.Frame()

        names = KnowledgeLevelClustering.get_cluster_names(n_clusters)
        first_level = names[0]
        last_level = names[-1]

        # Create the scale with labels
        ttk.Label(frame, text="Knowledge Level Scale:", font=('Arial', 10, 'bold')).pack()

        # Create the indicator bar with improved styling
        canvas = tk.Canvas(frame, height=40, bg='white', highlightthickness=0)
        canvas.pack(fill=tk.X, pady=5)

        # Draw the gradient bar with rounded corners
        canvas.create_rectangle(2, 2, 98, 38, outline="#cccccc", width=1)
        for i in range(3, 97):
            color = "#{:02x}{:02x}{:02x}".format(
                int(255 * (i / 100)),
                int(255 * (1 - i / 100)),
                0
            )
            canvas.create_line(i, 3, i, 37, fill=color, width=2)

        # Add level markers with better styling
        canvas.create_text(5, 20, text=first_level, anchor='w', fill='black', font=('Arial', 8, 'bold'))
        canvas.create_text(95, 20, text=last_level, anchor='e', fill='black', font=('Arial', 8, 'bold'))

        return frame

    def perform_clustering(self):
        try:
            df = pd.read_csv('filles/User Knowledge Modeling Data Set_total.csv')

            n_clusters = self.cluster_var.get()
            X = df.select_dtypes(include=['float64', 'int64'])
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(X_scaled)

            self.show_results(df, kmeans.labels_, n_clusters)
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}", foreground='red')

    def show_results(self, df, labels, n_clusters):
        result_window = tk.Toplevel(self.root)
        result_window.title("Clustering Results")
        result_window.geometry("500x550")
        result_window.configure(bg='#f0f0f0')

        # Add Back to Home button
        if self.open_main_form:
            def back_to_home():
                result_window.destroy()
                self.root.destroy()
                from clustringMainPage.clustring_first_page import clustring_first_page_class
                clustringPage_obj = clustring_first_page_class()
                clustringPage_obj.clustring_first_page_load()


            try:
                home_icon = Image.open('images/regresion.png')
                home_icon = home_icon.resize((20, 20), Image.Resampling.LANCZOS)
                self.home_image = ImageTk.PhotoImage(home_icon)

                back_button = ttk.Button(
                    result_window,
                    image=self.home_image,
                    text="Back to Home",
                    compound=tk.LEFT,
                    command=back_to_home,
                    style='Accent.TButton'
                )
            except:
                back_button = ttk.Button(
                    result_window,
                    text="← Back to Home",
                    command=back_to_home,
                    style='Accent.TButton'
                )
            back_button.pack(side=tk.BOTTOM, pady=10, padx=10, anchor=tk.E)

        cluster_counts = pd.Series(labels).value_counts().sort_index()
        cluster_names = self.get_cluster_names(n_clusters)

        main_frame = ttk.Frame(result_window, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame,
                  text="Clustering Results",
                  font=('Arial', 12, 'bold')).pack()

        # Level indicator
        level_frame = self.create_level_indicator(n_clusters)
        level_frame.pack(fill=tk.X, pady=(0, 20))

        # Results section with better styling
        result_frame = ttk.LabelFrame(
            main_frame,
            text=" Student Distribution ",
            padding=(15, 10),
            style='Card.TFrame'
        )
        result_frame.pack(fill=tk.BOTH, expand=True)

        for i in range(n_clusters):
            row_frame = ttk.Frame(result_frame)
            row_frame.pack(fill=tk.X, pady=5)

            ttk.Label(row_frame,
                      text=f"{cluster_names[i]}:",
                      width=20,
                      anchor='e',
                      font=('Arial', 9)).pack(side=tk.LEFT)

            ttk.Label(row_frame,
                      text=f"{cluster_counts[i]} students",
                      font=('Arial', 10, 'bold'),
                      foreground='#2c3e50').pack(side=tk.LEFT)

        # Total count with better styling
        ttk.Label(main_frame,
                  text=f"Total students analyzed: {len(df)}",
                  font=('Arial', 10, 'bold'),
                  foreground='#3498db').pack(pady=(15, 5))

    def setup_ui(self):
        self.root.title("Knowledge Level Clustering")
        self.root.geometry("450x300")
        self.root.configure(bg='#f0f0f0')

        # Create a custom style for widgets
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('Accent.TButton', foreground='white', background='#3498db')
        style.map('Accent.TButton',
                  background=[('active', '#2980b9'), ('pressed', '#1a5276')])
        style.configure('Card.TFrame',
                        background='white',
                        borderwidth=2,
                        relief='groove',
                        bordercolor='#e0e0e0')

        # Main container
        main_frame = ttk.Frame(self.root, padding=(30, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame,
                  text="Student Knowledge Assessment",
                  font=('Arial', 14, 'bold'),
                  foreground='#2c3e50').pack()

        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame,
                  text="Number of levels:",
                  font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 10))

        self.cluster_combobox = ttk.Combobox(
            input_frame,
            textvariable=self.cluster_var,
            values=list(range(2, 12)),
            font=('Arial', 10),
            width=15,
            state='readonly'
        )
        self.cluster_combobox.pack(side=tk.LEFT)

        # Analyze button with accent style
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        perform_button = ttk.Button(
            button_frame,
            text="Analyze Student Data",
            command=self.perform_clustering,
            style='Accent.TButton'
        )
        perform_button.pack(pady=10, ipadx=20)

        # Add Back to Home button if callback provided
        if self.open_main_form:
            def back_to_home():
                self.root.destroy()
                from classificationMainPage.classification_first_page import classification_first_page_class
                regressionPage_obj = classification_first_page_class()
                regressionPage_obj.classification_first_page_load()

            try:
                home_icon = Image.open('images/home.png')
                home_icon = home_icon.resize((20, 20), Image.Resampling.LANCZOS)
                self.home_image = ImageTk.PhotoImage(home_icon)

                back_button = ttk.Button(
                    main_frame,
                    image=self.home_image,
                    text="Back to Home",
                    compound=tk.LEFT,
                    command=back_to_home,
                    style='Accent.TButton'
                )
            except:
                back_button = ttk.Button(
                    main_frame,
                    text="← Back to Home",
                    command=back_to_home,
                    style='Accent.TButton'
                )
            back_button.pack(side=tk.BOTTOM, pady=(20, 0))

        self.result_label = ttk.Label(main_frame, text="", font=('Arial', 9))
        self.result_label.pack()