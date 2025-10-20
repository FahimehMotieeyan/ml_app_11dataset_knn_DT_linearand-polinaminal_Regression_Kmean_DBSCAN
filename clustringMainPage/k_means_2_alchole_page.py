import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import joblib
import pandas as pd

class ClusterVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cluster Visualization")
        self.root.geometry("800x480")
        x = int(self.root.winfo_screenwidth() / 2 - 800 / 2)
        y = int(self.root.winfo_screenheight() / 2 - 600 / 2)
        self.root.geometry(f'+{x}+{y}')
        self.root.configure(bg="#f5f5f5")

        # Load data
        self.loaded_model = joblib.load('kmeans_model.joblib')
        self.cluster_means = joblib.load('cluster_means.joblib')

        # Simple color palette
        self.colors = {
            "background": "#f5f5f5",
            "header": "#2c3e50",
            "button": "#3498db"
        }

        # Configure styles
        self.configure_styles()

        # Create UI components
        self.create_header()
        self.create_buttons()
        self.create_main_content()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Header style
        style.configure("Header.TLabel",
                        background=self.colors["header"],
                        foreground="white",
                        font=("Helvetica", 14, "bold"),
                        padding=10)

        # Button style
        style.configure("Custom.TButton",
                        background=self.colors["button"],
                        foreground="white",
                        font=("Helvetica", 10),
                        borderwidth=0,
                        padding=6)
        style.map("Custom.TButton",
                  background=[('active', '#2980b9'), ('pressed', '#1a5276')])

    def create_header(self):
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="Cluster Visualization Results", style="Header.TLabel").pack(side=tk.LEFT, padx=20)

    def create_buttons(self):
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Visualization button
        ttk.Button(button_frame, text="View Visualization", command=self.show_visualization, style="Custom.TButton").pack(side=tk.LEFT, padx=5)

        # Close button
        ttk.Button(button_frame, text="Return main", command=self.close_app, style="Custom.TButton").pack(side=tk.RIGHT, padx=5)

    def create_main_content(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Create scrollable canvas
        canvas = tk.Canvas(main_frame, bg=self.colors["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Prepare data
        cluster_means_df = pd.DataFrame(self.cluster_means)

        # Create a table view
        table_frame = ttk.Frame(scrollable_frame, padding=15)
        table_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Label(
            table_frame,
            text="CLUSTER MEANS BY FEATURE",
            font=("Helvetica", 12, "bold")
        ).pack(anchor=tk.W, pady=(0, 10))

        # Create Treeview for tabular data
        columns = cluster_means_df.columns.tolist()
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10,
            selectmode="none"
        )

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        # Add data to treeview
        for index, row in cluster_means_df.iterrows():
            tree.insert("", tk.END, values=row.tolist())

        tree.pack(fill=tk.X)

    def show_visualization(self):
        try:
            # Create visualization window
            vis_window = tk.Toplevel(self.root)
            vis_window.title("Cluster Visualization")
            vis_window.geometry("700x500")

            # Image display
            img = Image.open('cluster_visualization.png')

            # Maintain aspect ratio
            width, height = img.size
            ratio = min(650 / width, 400 / height)
            new_size = (int(width * ratio), int(height * ratio))

            img = img.resize(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_frame = ttk.Frame(vis_window, padding=10)
            img_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

            img_label = ttk.Label(img_frame, image=photo)
            img_label.image = photo
            img_label.pack()

            # Close button
            ttk.Button(vis_window, text="Close", command=vis_window.destroy, style="Custom.TButton").pack(pady=10)

        except FileNotFoundError:
            messagebox.showerror("Error", "Visualization image not found", parent=self.root)

    def close_app(self):
        self.root.destroy()
        from clustringMainPage.clustring_first_page import clustring_first_page_class
        opening_obj = clustring_first_page_class()
        opening_obj.clustring_first_page_load()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClusterVisualizationApp(root)
    root.mainloop()