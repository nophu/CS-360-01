import tkinter as tk
from tkinter import filedialog, ttk, messagebox
class user_interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Resume Reviewer")
        self.root.geometry("700x500")
        self.filename = None

        self.create_upload_screen()
        self.root.mainloop()

#SCREEN 1 ===================================================

    def create_upload_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="AI Resume Reviewer", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Drop Resume Here or Click Upload", font=("Arial", 16)).pack(pady=10)

        upload_btn = tk.Button(self.root, text="Upload Resume", font=("Arial", 14),
                               command=self.upload_resume)
        upload_btn.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.root, text="<Loading Status>", font=("Arial", 12))
        self.status_label.pack(pady=10)
    
    def upload_resume(self):
        file_path = filedialog.askopenfilename(title="Select Resume", filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")])
        if file_path:
            self.filename = file_path
            self.status_label.config(text="Processing resume...")
            self.simulate_loading()
    
    def simulate_loading(self):
         #Simulate loading with progress bar
        for i in range(101):
            self.root.after(i * 30, lambda v=i: self.progress.step(1))
        self.root.after(3200, self.show_job_listings)  #After progress, move to job list

#SCREEN 2 ===================================================

    def show_job_listings(self):
        self.clear_screen()
        tk.Label(self.root, text="Related Listings", font=("Arial", 22)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Job Listing", font=("Arial", 14, "bold"), width=25, anchor="w").grid(row=0, column=0)
        tk.Label(frame, text="Match %", font=("Arial", 14, "bold"), width=10, anchor="center").grid(row=0, column=1)
        tk.Label(frame, text="", width=10).grid(row=0, column=2)

        # Dummy listings
        for i in range(10):
            tk.Label(frame, text=f"Job Position #{i+1}", font=("Arial", 12), anchor="w").grid(row=i+1, column=0, sticky="w")
            tk.Label(frame, text=f"{80 - i*3}%", font=("Arial", 12)).grid(row=i+1, column=1)
            tk.Button(frame, text="+", command=lambda idx=i: self.show_job_details(idx)).grid(row=i+1, column=2)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Back", width=10, command=self.create_upload_screen).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=10)

    #SCREEN 3 ===================================================
    def show_job_details(self, idx):
        self.clear_screen()
        tk.Label(self.root, text="JOB POSITION", font=("Arial", 22)).pack(pady=10)
        tk.Label(self.root, text=f"Job Link: https://example.com/job/{idx+1}", fg="blue", cursor="hand2").pack(pady=5)
        tk.Label(self.root, text=f"Job Description for Position #{idx+1}", font=("Arial", 12), wraplength=500).pack(pady=10)

        content_frame = tk.Frame(self.root)
        content_frame.pack(pady=10)

        # Matched and Missing lists
        matched_frame = tk.LabelFrame(content_frame, text="Matched", font=("Arial", 12))
        matched_frame.grid(row=0, column=0, padx=20)
        missing_frame = tk.LabelFrame(content_frame, text="Missing", font=("Arial", 12))
        missing_frame.grid(row=0, column=1, padx=20)

        # Dummy data
        matched_skills = ["Python", "Machine Learning", "Data Analysis"]
        missing_skills = ["Cloud Deployment", "CI/CD", "API Integration"]

        for skill in matched_skills:
             tk.Label(matched_frame, text=skill, font=("Arial", 11)).pack(anchor="w")
        for skill in missing_skills:
            label = tk.Label(missing_frame, text=skill, font=("Arial", 11))
            label.pack(anchor="w")
            label.bind("<Enter>", lambda e, s=skill: self.show_hover_tooltip(e, s))
            label.bind("<Leave>", self.hide_hover_tooltip)
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="Back", width=10, command=self.show_job_listings).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=10)
     # Tooltip simulation for hover
    def show_hover_tooltip(self, event, skill_name):
        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip.geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=f"Full Skill Name: {skill_name}", background="yellow", relief="solid", borderwidth=1)
        label.pack()
    def hide_hover_tooltip(self, event):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
    # Helper to clear widgets
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    



if __name__ == "__main__":
    myGUI = UserInterface()