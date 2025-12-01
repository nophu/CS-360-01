import json, os, PyPDF2
import joblistelement
from docx import Document
class DataProcess:
    def __init__(self, file):
        self.filename = file
        self.jfilename = ""
        self.joblist = []

    def create_joblist_element(self, title, url, company, description, requirements, tags):
        # empty list
        self.joblist = []

        # create JobListElement objects
        for i in range(len(url)):
            temp = joblistelement.JobListElement(title[i], url[i], company[i], description[i], requirements[i], tags[i])

            # add JobListElement to list
            self.joblist.append(temp)

        # return list of JobListElement objects
        return self.joblist


    def parse_text(self):
        #
        ext = os.path.splitext(self.filename)[1].lower()


        if ext == ".docx":
            doc = Document(self.filename)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext == ".pdf":
            reader = PyPDF2.PdfReader(self.filename)
            return "\n".join(page.extractText() for page in reader.pages)

        else: raise ValueError("Unsupported file type")

    def parse_headers(self, text):
        section_headers = {
            "skills": ["skills", "technical skills", "skills & abilities"],
            "experience": ["experience", "work experience", "professional experience"],
            "education": ["education"],
            "certifications": ["certifications", "certificates"],
            "summary": ["summary", "professional summary", "objective"]
        }

        extracted = {key: "" for key in section_headers}
        current_section = None

        lines = text.split("\n")

        for line in lines: clean = line.strip().lower()

        for section, keywords in section_headers.items():
            if any(k in clean.lower() for k in keywords):
                current_section = section
                break

            else:
                if current_section: extracted[current_section] += line.strip() + "\n"

        if extracted["skills"]: extracted["skills"] = [s.strip() for s in extracted["skills"].replace(",", "\n") if s.strip()]
        else: extracted["skills"] = []

        return extracted

    def parse_resume(self):
        text = self.parse_text()
        sections = self.parse_headers(text)
        return sections

    def parse_json(self, file):
        # open json file, read content and then return as dictionary
        with open(file, "r") as f: return json.load(f)

    def parse_job_list(self, data):
        # empty list
        joblist = []

        # create job list element using data from dictionary
        for _, job in data:
            joblist.append(
                joblistelement.JobListElement( job["job_title"], job["job_apply_link"], job["employer_name"],
                    job["job_description"], job["job_highlights"]["Qualifications"], job["job_highlights"]["Responsibilities"] )
            )

        # return list of joblist elements
        return joblist


    def match_score(self, job):
        # get job requirements
        requirements = job.get_requirements()

        # get user's skills
        skills = self.get_user_skills()

        # if job has no requirements listed, avoid division
        if not requirements: return 0

        # keep track of all requirements that are matched by user's skills
        match = sum(1 for req in requirements if req.lower() in skills)

        # return percentage
        return match / len(requirements)

    def relevance_score(self, job):
        # load resume data
        resume_data = self.parse_json(self.jfilename)

        # convert job data into a dictionary
        job_data = job.to_dict()

        # initialize counts
        related_user_information = 0
        job_information = 0

        # convert resume data to lowercase to help match
        resume_keywords = [k.lower() for k in resume_data.keys()]

        # check for relevance for these job fields
        fields_to_check = ["description", "requirements", "tags"]

        for field in fields_to_check:

            # skip fields that do not exist in job data
            if field not in job_data: continue
            value = job_data[field]
            job_information += 1

            # organize values into a list of text sections
            if isinstance(value,list): text_list = value
            else: text_list = [value]

            # checks for overlapping resume keywords in job field
            for text in text_list:
                text = text.lower()
                for key in resume_keywords:
                    if key in text:
                        related_user_information += 1
                        break

        # if no fields were checked, avoid division
        if job_information == 0: return 0

        #return relevance percentage
        return (related_user_information / job_information) * 100


    def match(self, job):
        # get job requirements
        requirements = job.get_requirements()

        # get user's skills
        skills = self.get_user_skills()

        # compare user's skills to job requirements
        matched = [req for req in requirements if req.lower() in skills]
        missing = [req for req in requirements if req.lower() not in skills]

        return matched, missing

    # helper method for getting user skills
    def get_user_skills(self):
        # load user data
        data = self.parse_json(self.jfilename)

        # compare skills
        skills = data.get("skills") or data.get("Skills") or []

        # return user skills
        return [s.lower() for s in skills]
