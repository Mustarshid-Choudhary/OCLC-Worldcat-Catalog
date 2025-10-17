from tkinter import filedialog, messagebox, ttk, Tk, StringVar, Label, Text
from os import path
from threading import Thread
from main import run_program

class OCLCApp:

    def __init__(self, root):
        self.root = root
        self.root.title("OCLC Cataloging Widget")
        self.root.geometry("360x360")
        self.root.resizable(True, True)

        # ttk theme setup
        style = ttk.Style()
        style.theme_use("classic")
        style.configure("TButton", font=("Arial", 11), padding=3)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("Run.TButton", font=("Arial", 12), padding=3)

        self.input_file = ""
        self.output_dir = ""

        # Main layout frame
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(expand=True, fill="both")

        # Input selection
        ttk.Button(main_frame, text="Select Input File", command=self.select_input_file).grid(row=0, column=0, sticky="w", pady=5)
        self.input_label = ttk.Label(main_frame, text="No file selected", foreground="gray")
        self.input_label.grid(row=0, column=1, sticky="w", padx=10)

        # Output selection
        ttk.Button(main_frame, text="Select Output Directory", command=self.select_output_dir).grid(row=1, column=0, sticky="w", pady=5)
        self.output_label = ttk.Label(main_frame, text="No directory selected", foreground="gray")
        self.output_label.grid(row=1, column=1, sticky="w", padx=10)

        # Note to select file name
        self.note = ttk.Label(
            main_frame,
            text="*After you run the program, a window will pop up where you can name the output file.",
            font=("Arial", 11),
            foreground="black",
            wraplength=350,  # makes it wrap nicely if long
            justify="left"   # aligns text to the left
        )
        self.note.grid(row=2, columnspan=2, pady=(5, 15), sticky="w")

        # Separator
        ttk.Separator(main_frame, orient="horizontal").grid(row=3, columnspan=2, sticky="ew", pady=15)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate", length=300)
        self.progress.grid(row=4, columnspan=2, pady=5)

        # Run button
        ttk.Button(main_frame, text="Run", style="Run.TButton", command=self.run_conversion).grid(row=5, columnspan=2, pady=10)

        # Status bar
        self.status_var = StringVar(value="Ready")
        self.status_label = Label(root, textvariable=self.status_var, font=("Arial", 9), bg="#eee", anchor="w", relief="sunken")
        self.status_label.pack(side="bottom", fill="x")

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input Text File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.input_file = file_path
            self.input_label.config(text=path.basename(file_path), foreground="black")

    def select_output_dir(self):
        folder_path = filedialog.askdirectory(title="Select Output Directory")
        if folder_path:
            self.output_dir = folder_path
            self.output_label.config(text=folder_path, foreground="black")

    def run_conversion(self):
        if not self.input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Run processing in a separate thread so GUI doesn't freeze
        Thread(target=self._do_conversion, daemon=True).start()

    def _do_conversion(self):
        try:
            self.status_var.set("Processing...")
            self.status_label.config(bg="#ffeaa7")
            self.progress.start(10)

            output_path = run_program(self.input_file)

            self.status_var.set("Done!")
            self.status_label.config(bg="#72d572")  # light green for success
            self.progress.stop()

            messagebox.showinfo("Success", f"File created:\n{output_path}")

        except Exception as e:
            self.status_var.set("Error")
            self.status_label.config(bg="#f8a5a5")  # light red for error
            self.progress.stop()
            messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = Tk()
    OCLCApp(root)
    root.mainloop()