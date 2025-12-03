import json, os, PyPDF2, re
import pdfplumber
from docx import Document
class DataProcess:
    def __init__(self, file, jfilename=None):
        self.filename = file
        self.jfilename = jfilename
        self.joblist = []

    def parse_text(self):
        # get file extension
        ext = os.path.splitext(self.filename)[1].lower()

        # check if file is a docx
        if ext == ".docx":

            # load docx
            doc = Document(self.filename)

            # return all raw text in each paragraph
            return "\n".join(p.text for p in doc.paragraphs)

        # check if file is pdf
        elif ext == ".pdf":

            # empty string
            text = ""

            # open pdf
            with pdfplumber.open(self.filename) as pdf:

                # go thru each page
                for page in pdf.pages:

                    # extract data from page, if no data = empty string
                    page_text = page.extract_text() or ""

                    # add text from page to final text
                    text += page_text + "\n"

                # return full extracted text from pdf
                return text

        # if file format is neither pdf nor docx
        else: raise ValueError("Unsupported file type")

    def parse_headers(self, text):
        # dictionary of section names
        keywords = {
        "skills": ["skills", "technical skills", "skills & abilities"],
        "experience": ["experience", "work experience", "professional experience", "employment history"],
        "education": ["education", "academic background"],
        "certifications": ["certifications", "certificates", "licenses"],
        "summary": ["summary", "professional summary", "objective", "profile"],
        }

        # empty list
        sections = {}

        # pointer for each section
        current_header = None

        # split text into lines and individually process them
        for raw_text in text.split("\n"):

            # remove leading/trailing white spaces
            line = raw_text.strip()

            # skip empty lines
            if not line: continue

            # normalize line, convert to lowercase, remove alphanumeric characters except spaces
            lower_line = re.sub(r'[^a-z0-9 ]+', '', line.lower()).strip()

            # reset header
            found = None

            # check if line matches any known headers
            for header, keywordlist in keywords.items():

                # match check
                if any(lower_line == k for k in keywordlist):
                    found = header
                    break

                # match check for stuff like starts-with
                if any(lower_line.startswith(k) for k in keywordlist):
                    found = header
                    break

            # if header is found
            if found:
                current_header = found

                # initialize section list (if it does not exist already)
                if current_header not in sections: sections[current_header] = []

                # skip to next line, header is not content
                continue

            # if in a section, add line to current section
            if current_header: sections[current_header].append(line)

        # return dictionary of sections of extracted lines
        return sections

    # open json file, read content and then return as dictionary
    def parse_json(self, file):
        with open(file, "r") as f: return json.load(f)

    def match_score(self, job):
        # get job requirements
        requirements = job.get("job_highlights", {}).get("Qualifications", [])

        # get user's skills
        skills = self.get_user_skills()

        # if job has no requirements listed, avoid division
        if not requirements: return 0

        # keep track of all requirements that are matched by user's skills
        match = sum(1 for req in requirements if req.lower() in skills)

        # return percentage
        return match / len(requirements)

    def relevance_score(self, job):
        # get users skills
        user_skills = self.get_user_skills()

        # get job skills
        job_skills = job.get("job_highlights", {}).get("Qualifications", [])

        if not job_skills: return 0

        # normalize job skills to lowercase
        job_skills_lower = [str(s).lower() for s in job_skills]

        # count how many job skills match any user skill
        matched = sum(1 for s in job_skills_lower if any(us in s for us in user_skills))

        # return percentage
        return (matched / len(job_skills)) * 100


    def match(self, job):
        # get job requirements
        requirements = job.get("job_highlights", {}).get("Qualifications", [])
        if not isinstance(requirements, str): requirements = [requirements]

        # get user's skills
        skills = self.get_user_skills()

        # compare user's skills to job requirements
        matched = []
        missing = []

        # normalize skills into sets of words
        skill_words = [set(skill.lower().split()) for skill in skills]
        for req in requirements:
            req_words = set(str(req).lower().split())
            if any(sw & req_words for sw in skill_words): matched.append(req)
            else: missing.append(req)

        return matched, missing

    # helper method for getting user skills
    def get_user_skills(self):
        # load user data
        data = self.parse_json(self.jfilename)

        # compare skills
        skills = data.get("skills") or data.get("Skills") or []

        # verify that skills is a list
        if not isinstance(skills, list): skills = [skills]

        # convert everything to string and lowercase
        safe_skills = []
        for s in skills:
            try: safe_skills.append(str(s).lower())
            except Exception: continue

        # return user skills
        return safe_skills