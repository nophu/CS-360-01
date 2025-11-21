import tkinter as tk
from tkinter import filedialog, ttk, messagebox
class UserInterface:
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

        #Before refactoring
        #tk.Label(self.root, text="AI Resume Reviewer", font=("Arial", 24)).pack(pady=20)
        #tk.Label(self.root, text="Drop Resume Here or Click Upload", font=("Arial", 16)).pack(pady=10)
        #After refactoring
        self.make_label(self.root, "AI Resume Reviewer", 24, pady=20)
        self.make_label(self.root, "Drop Resume Here or Click Upload", 16)

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
        #before refactoring
        #for i in range(101):
            #self.root.after(i * 30, lambda v=i: self.progress.step(1))
        #self.root.after(3200, self.show_job_listings)  #After progress, move to job list
        #after refactoring
        self.animate_progress(self.show_job_listings)


#SCREEN 2 ===================================================

    def show_job_listings(self):
        self.clear_screen()
        tk.Label(self.root, text="Related Listings", font=("Arial", 22)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        #before refactoring
        #tk.Label(frame, text="Job Listing", font=("Arial", 14, "bold"), width=25, anchor="w").grid(row=0, column=0)
        #tk.Label(frame, text="Match %", font=("Arial", 14, "bold"), width=10, anchor="center").grid(row=0, column=1)
        #after refactoring
        self.make_header(frame, "Job Listing", 0, 0)
        self.make_header(frame, "Match %", 0, 1)

        tk.Label(frame, text="", width=10).grid(row=0, column=2)

        # Dummy listings
        for i in range(10):
            #Before refactoring
            #tk.Label(frame, text=f"Job Position #{i+1}", font=("Arial", 12), anchor="w").grid(row=i+1, column=0, sticky="w")
            #tk.Label(frame, text=f"{80 - i*3}%", font=("Arial", 12)).grid(row=i+1, column=1)
            #tk.Button(frame, text="+", command=lambda idx=i: self.show_job_details(idx)).grid(row=i+1, column=2)
            #After refactoring
            self.add_job_row(frame, i)
        #Before refactoring
        #btn_frame = tk.Frame(self.root)
        #btn_frame.pack(pady=20)
        #tk.Button(btn_frame, text="Back", width=10, command=self.create_upload_screen).pack(side="left", padx=10)
        #tk.Button(btn_frame, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=10)
        #After refactoring
        self.create_nav_buttons(self.create_upload_screen)

    #SCREEN 3 ===================================================
    def show_job_details(self, idx):
        self.clear_screen()
        tk.Label(self.root, text="JOB POSITION", font=("Arial", 22)).pack(pady=10)
        #Before refactoring
        #tk.Label(self.root, text=f"Job Link: https://example.com/job/{idx+1}", fg="blue", cursor="hand2").pack(pady=5)
        #tk.Label(self.root, text=f"Job Description for Position #{idx+1}", font=("Arial", 12), wraplength=500).pack(pady=10)
        #After refactoring
        self.show_job_header(idx)

        content_frame = tk.Frame(self.root)
        content_frame.pack(pady=10)

        # Matched and Missing lists
        matched_frame = tk.LabelFrame(content_frame, text="Matched", font=("Arial", 12))
        matched_frame.grid(row=0, column=0, padx=20)
        missing_frame = tk.LabelFrame(content_frame, text="Missing", font=("Arial", 12))
        missing_frame.grid(row=0, column=1, padx=20)

        # Dummy data
        #Before refactoring
        #matched_skills = ["Python", "Machine Learning", "Data Analysis"]
        #missing_skills = ["Cloud Deployment", "CI/CD", "API Integration"]
        #After refactoring
        matched_skills, missing_skills = self.get_dummy_skills()
        #before refactoring
        #for skill in matched_skills:
        #    tk.Label(matched_frame, text=skill, font=("Arial", 11)).pack(anchor="w")
        #After refactoring
        self.populate_skill_list(matched_frame, matched_skills)

        for skill in missing_skills:
            Label = tk.Label(missing_frame, text=skill, font=("Arial", 11))
            Label.pack(anchor="w")
            Label.bind("<Enter>", lambda e, s=skill: self.show_hover_tooltip(e, s))
            Label.bind("<Leave>", self.hide_hover_tooltip)
        #Before refactoring
        #btn_frame = tk.Frame(self.root)
        #btn_frame.pack(pady=20)
        #tk.Button(btn_frame, text="Back", width=10, command=self.show_job_listings).pack(side="left", padx=10)
        #tk.Button(btn_frame, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=10)
        #after refactoring
        self.create_nav_buttons(self.show_job_listings)
     # Tooltip simulation for hover
    def show_hover_tooltip(self, event, skill_name):
        #Before refactoring
        #self.tooltip = tk.Toplevel()
        #self.tooltip.wm_overrideredirect(True)
        #x = event.x_root + 10
        #y = event.y_root + 10
        #self.tooltip.geometry(f"+{x}+{y}")
        #label = tk.Label(self.tooltip, text=f"Full Skill Name: {skill_name}", background="yellow", relief="solid", borderwidth=1)
        #label.pack()
        #After refactoring
        self.show_tooltip(event, f"Full Skill Name: {skill_name}")
    def hide_hover_tooltip(self, event):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()
    # Helper to clear widgets
    def clear_screen(self):
        #Before refactoring
        #for widget in self.root.winfo_children():
        #   widget.destroy()
        #After refactoring
        for child in self.root.winfo_children():
            child.destroy()
    def create_nav_buttons(self, back_command):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        #tk.Button(btn_frame, text="Back", width=10, command=back_command).pack(side="left", padx=10)
        #tk.Button(btn_frame, text="Exit", width=10, command=self.root.quit).pack(side="left", padx=10)
        for text, command in [("Back", back_command), ("Exit", self.root.quit)]:
            tk.Button(btn_frame, text=text, width=10, command=command).pack(side="left", padx=10)

    def make_label(self, parent, text, font_size, pady=10):
        label = tk.Label(parent, text=text, font=("Arial", font_size))
        label.pack(pady=pady)
        return label
    def add_job_row(self, frame, i):
        job_label = tk.Label(frame, text=f"Job Position #{i+1}", font=("Arial", 12), anchor="w")
        match_label = tk.Label(frame, text=f"{80 - i*3}%", font=("Arial", 12))
        more_btn = tk.Button(frame, text="+", command=lambda idx=i: self.show_job_details(idx))

        job_label.grid(row=i+1, column=0, sticky="w")
        match_label.grid(row=i+1, column=1)
        more_btn.grid(row=i+1, column=2)
    def get_dummy_skills(self):
        return (["Python", "Machine Learning", "Data Analysis"],
                ["Cloud Deployment", "CI/CD", "API Integration"])
    def show_tooltip(self, event, text):
        #self.tooltip = tk.Toplevel()
        #self.tooltip.wm_overrideredirect(True)
        #self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        #tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1).pack()
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        x,y = event.x_root + 10, event.y_root + 10
        self.tooltip.wm_geometry(f"+{x}+{y}")

        tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1).pack()
        
    def populate_skill_list(self, frame, skills, hover=False):
        for skill in skills:
            label = tk.Label(frame, text=skill, font=("Arial", 11))
            label.pack(anchor="w")
            if hover:
                label.bind("<Enter>", lambda e, s=skill: self.show_hover_tooltip(e, s))
                label.bind("<Leave>", self.hide_hover_tooltip)
    def make_header(self, parent, text, row, col):
        tk.Label(parent, text=text, font=("Arial", 14, "bold")).grid(row=row, column=col, pady=5)
    def animate_progress(self, callback):
        for i in range(101):
            self.root.after(i * 30, lambda v=i: self.progress.step(1))
        self.root.after(3200, callback)  #After progress, call the callback
    def show_job_header(self, idx):
        tk.Label(self.root, text=f"Job Link: https://example.com/job/{idx+1}", fg="blue", cursor="hand2").pack(pady=5)
        tk.Label(self.root, text=f"Job Description for Position #{idx+1}", font=("Arial", 12), wraplength=500).pack(pady=10)




if __name__ == "__main__":
    myGUI = UserInterface()