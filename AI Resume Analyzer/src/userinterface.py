import json
import tkinter as tk
from platform import processor
from time import sleep
from tkinter import filedialog, ttk, messagebox
from dataprocess import DataProcess
from apihandler import APIHandler
from dataprocess import DataProcess

class UserInterface:
    def __init__(self, api):
        self.root = tk.Tk()
        self.root.title("AI Resume Analyzer")
        self.root.geometry("700x500")

        self.filename = None
        self.dp = None
        self.api = APIHandler()
        self.jobList = []

        self.create_upload_screen()
        self.root.mainloop()

#SCREEN 1 ===================================================

    def create_upload_screen(self):
        self.clear_screen()
        self.make_label(self.root, "AI Resume Analyzer", 24, pady=20)
        self.make_label(self.root, "Drop Resume Here or Click Upload", 16)

        upload_btn = tk.Button(self.root, text="Upload Resume", font=("Arial", 14), command=self.upload_resume)
        upload_btn.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

        self.status_label = tk.Label(self.root, text="<Loading Status>", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def upload_resume(self):
        # Step 1, user uploads resume

        self.status_label.config(text="Uploading Resume")
        self.progress.step(33)
        file_path = filedialog.askopenfilename(title="Select Resume", filetypes=[("All Files", "*.*")])
        if not file_path: return


        # Step 2, dataprocess processes resume
        self.progress.step(33)
        self.status_label.config(text="Processing Resume")

        processor = DataProcess(file_path)
        self.dp = processor

        processResults = processor.parse_headers(processor.parse_text())

        print(processResults)
        print(len(processResults))

        skills = processResults["skills"]
        self.resume_skills = skills
        print("SKILLS SENT TO API:", skills)
        if not skills:
            skills = []
            for k, category in processResults.items():
                for i in category:
                    skills.append(i)

        resume_data = { "skills": skills, "sections": processResults }
        with open("resume.json", "w", encoding="utf-8") as f: json.dump(resume_data, f, indent=4)

        processor.jfilename = "resume.json"

        # Step 3, get listings
        self.progress.step(33)
        self.status_label.config(text="Getting listings from API")

        api_results = self.api.get_listings(skills, amount=1)

        self.jobList = api_results
        self.show_job_listings()

#SCREEN 2 ===================================================

    def show_job_listings(self):
        self.clear_screen()
        tk.Label(self.root, text="Related Listings", font=("Arial", 22)).pack(pady=10)

        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True, pady=10)

        frame = self.make_scrollable(container)

        self.make_header(frame, "Job Listing", 0, 0)
        self.make_header(frame, "Match %", 0, 1)

        tk.Label(frame, text="", width=10).grid(row=0, column=2)

        c = 0 # UISCROLL PLS AND TY
        for i in self.jobList:
            self.add_job_row(frame, i, c)
            c += 1
        self.create_nav_buttons(self.create_upload_screen)

    #SCREEN 3 ===================================================
    def show_job_details(self, idx):
        jobListing = self.jobList[idx]
        self.clear_screen()

        # title
        tk.Label(self.root, text=jobListing["job_title"] + " at " + jobListing["employer_name"], font=("Arial", 22), wraplength=650, justify="center").pack(pady=10)

        # scrollable table
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)
        content_frame = self.make_scrollable(container)

        # job link
        link = tk.Label( content_frame, text=f"{jobListing['job_apply_link']}", fg="blue", cursor="hand2", font=("Arial", 12, "underline"), wraplength=650, justify="center")
        link.pack(pady=5, anchor ="w")
        link.bind("<Button-1>", lambda e, url=jobListing["job_apply_link"]: self.api.open_directlink(url))

        # scrollable job description
        tk.Label(content_frame, text=jobListing["job_description"], font=("Arial", 12), wraplength=650, justify="left").pack(pady=10, anchor="w")

        # matched + missing skills frame
        matched_frame = tk.LabelFrame(content_frame, text="Matched", font=("Arial", 12))
        missing_frame = tk.LabelFrame(content_frame, text="Missing", font=("Arial", 12))
        matched_frame.pack(padx=20, side="left", anchor="n")
        missing_frame.pack(padx=20, side="left", anchor="n")

        matched_skills, missing_skills = self.dp.match(jobListing)
        self.populate_skill_list(matched_frame, matched_skills)
        self.populate_skill_list(missing_frame, missing_skills, hover=True)

        self.create_nav_buttons(self.show_job_listings)

    # Tooltip simulation for hover
    def show_hover_tooltip(self, event, skill_name): self.show_tooltip(event, f"Full Skill Name: {skill_name}")

    def hide_hover_tooltip(self, event):
        if hasattr(self, "tooltip"): self.tooltip.destroy()

    # Helper to clear widgets
    def clear_screen(self):
        for child in self.root.winfo_children(): child.destroy()

    def create_nav_buttons(self, back_command):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        for text, command in [("Back", back_command), ("Exit", self.root.quit)]:
            tk.Button(btn_frame, text=text, width=10, command=command).pack(side="left", padx=10)

    def make_label(self, parent, text, font_size, pady=10):
        label = tk.Label(parent, text=text, font=("Arial", font_size))
        label.pack(pady=pady)
        return label

    def add_job_row(self, frame, jobListing, i):
        job_label = tk.Label(frame, text= jobListing["job_title"] + " at " + jobListing["employer_name"], font=("Arial", 12), anchor="w", width=50, wraplength=650, justify="left")
        relevance = self.dp.relevance_score(jobListing)
        match_label = tk.Label(frame, text=f"{relevance:.0f}%", font=("Arial", 12))
        more_btn = tk.Button(frame, text="+", command=lambda idx=i: self.show_job_details(idx))

        job_label.grid(row=i+1, column=0, sticky="w")
        match_label.grid(row=i+1, column=1)
        more_btn.grid(row=i+1, column=2)


    def show_tooltip(self, event, text):
        if hasattr(self, "tooltip"): self.tooltip.destroy()

        self.tooltip = tk.Toplevel()
        self.tooltip.wm_overrideredirect(True)
        x,y = event.x_root + 10, event.y_root + 10
        self.tooltip.wm_geometry(f"+{x}+{y}")

        tk.Label(self.tooltip, text=text, background="yellow", relief="solid", borderwidth=1).pack()

    def populate_skill_list(self, frame, skills, hover=False):
        for skill in skills:
            label = tk.Label(frame, text=skill, font=("Arial", 11), wraplength=200, justify="left", anchor="w")
            label.pack(anchor="w", pady=2)
            if hover:
                label.bind("<Enter>", lambda e, s=skill: self.show_hover_tooltip(e, s))
                label.bind("<Leave>", self.hide_hover_tooltip)

    def make_header(self, parent, text, row, col): tk.Label(parent, text=text, font=("Arial", 14, "bold")).grid(row=row, column=col, pady=5)

    def animate_progress(self, callback):
        for i in range(101): self.root.after(i * 30, lambda v=i: self.progress.step(1))
        self.root.after(3200, callback)  #After progress, call the callback

    def show_job_header(self, idx): # UISCROLL PLS AND TY
        tk.Label(self.root, text=f"Job Link: {self.jobList[idx]["job_apply_link"]}", fg="blue", cursor="hand2").pack(pady=5)
        tk.Label(self.root, text=self.jobList[idx]["job_description"], font=("Arial", 12), wraplength=500).pack(pady=10)

    def make_scrollable(self, parent):
        canvas = tk.Canvas(parent)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        inner = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _on_mousewheel(event): canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

        # bind mouse wheel to both the frame and canvas
        inner.bind_all("<MouseWheel>", _on_mousewheel)

        return inner
