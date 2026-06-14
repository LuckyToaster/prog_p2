import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("URL Processor App")
        self.root.geometry("800x600")

        # --- Top Frame (URL Input) ---
        top_frame = ttk.Frame(root, padding="10 10 10 5")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(top_frame, text="URL to process:").pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry = ttk.Entry(top_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.process_btn = ttk.Button(top_frame, text="Process", command=self.on_process)
        self.process_btn.pack(side=tk.LEFT)

        # --- Bottom Frame (Status & Progress) ---
        bottom_frame = ttk.Frame(root, padding="10 5 10 10")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(bottom_frame, text="Status: Ready")
        self.status_label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        
        self.progress = ttk.Progressbar(bottom_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.progress.pack(side=tk.TOP, fill=tk.X)

        # --- Middle Frame (Left Panel & Main Area) ---
        middle_frame = ttk.Frame(root, padding="10 5 10 5")
        middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Left Panel (List of stuff)
        left_panel = ttk.Frame(middle_frame, relief=tk.SUNKEN, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False) # Prevents the frame from shrinking to fit the contents exactly

        ttk.Label(left_panel, text="Items").pack(pady=(5, 0))
        self.listbox = tk.Listbox(left_panel)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Populate with dummy data
        for i in range(1, 11):
            self.listbox.insert(tk.END, f"Item {i}")

        # Main Area (Image Rendering)
        main_area = ttk.Frame(middle_frame, relief=tk.SUNKEN)
        main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(main_area, text="Image Viewport").pack(pady=(5, 0))
        self.image_canvas = tk.Canvas(main_area, bg="gray")
        self.image_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.image_canvas.create_text(250, 200, text="Image will be rendered here", fill="white")

    def on_process(self):
        url = self.url_entry.get()
        if url:
            self.status_label.config(text=f"Status: Processing {url}...")
            # Simulate progress
            self.progress['value'] = 0
            self.step_progress()
        else:
            self.status_label.config(text="Status: Please enter a URL.")

    def step_progress(self):
        if self.progress['value'] < 100:
            self.progress['value'] += 10
            self.root.after(100, self.step_progress)
        else:
            self.status_label.config(text="Status: Process complete.")

if __name__ == "__main__":
    root = tk.Tk()
    # Apply a modern theme if available
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    
    app = App(root)
    root.mainloop()
