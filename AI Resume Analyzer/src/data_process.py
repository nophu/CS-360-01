import json, os
import joblist_element
from docx import Document

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

class data_process:

    def __init__(self, file):
        self.filename = file
        self.jfilename = ""
        self.joblist = []

    def create_joblist_element(self, title, url, company, description, requirements, tags): #new method for creating joblist_element
        i = 0
        for item in url:             #creates all the joblist_elements using the six lists based on the number of urls 
            temp = joblist_element(title[i], item, company[i], description[i], requirements[i], tags[i])
            self.joblist.append(temp)
            i += 1


        return self.joblist

    def parse_resume(self, output_file = "resume.json"):
        # get file extension of resume file and convert to lowercase
        ext = os.path.splitext(self.filename)[1].lower()

        # create empty string
        text = ""

        # check if file is a docx 
        if ext == ".docx": 
            doc = Document(self.filename)

            # get all text from paragraphs and put them together
            text = " ".join(p.text for p in doc.paragraphs)
        
         # check if file is a pdf 
        elif ext == ".pdf": 
            if not PyPDF2: raise ImportError("PyPDF2 is required for PDFs!")

            # read pdf file 
            reader = PyPDF2.PdfReader(self.filename)

            # get all text from all pages and put them together
            text = " ".join(page.extract_text() for page in reader.pages) 

            # if file is not of supported file type
        else: raise ValueError("Unsupported file type!")

        # create dictionary to hold words 
        words = {}

        # loop for each word in text
        for word in text.split():

            # make the word lowercase and get rid of extra spaces
            word = word.lower().strip()

            # count each word
            if word: words[word] = words.get(word, 0) + 1
        
        # save the word counts to json file 
        with open(output_file, "w", encoding = "utf-8") as f: json.dump(words, f, indent = 4)

        # return dictionary of the count
        return words
    
    def parse_json(self, file): #parses a json to a dictionary
         with open(file, "r") as f:  
            data = json.load(f)

            return data

    def parse_Job_List(self, data):
        
        joblist = []

        for _, job in data:
            joblist.append(
                joblist_element(
                    job["job_title"],
                    job["job_apply_link"],
                    job["employer_name"],
                    job["job_description"],
                    job["job_highlights"]["Qualifications"],
                    job["job_highlights"]["Responsibilities"]
                )
            )

        return joblist
    
   

    def match_score(self, job: joblist_element): #takes a joblist_element and creates a match score for it
        match = 0
        requirements_number = 0
        requirements = job.JobListElement.get_requirements
        skills = []

        data = self.parse_json(self, self.jfilename)  #this bit gets the data from the json file of the users resume
        
        for key, value in data:   #gets user skills
            if key == "skills" or key == "Skills":
                skills.append(value)

        for item in requirements: #checks if each requirement is in the user's listed skills
            for element in skills:
                if item.lower == element.lower:
                    match += 1
            requirements_number += 1


        return (match / requirements_number) * 100 #returns match percentage

    def relevance_score(self, job: joblist_element): #returns relevance score for a give joblist_element as a percentage
        related_user_information = 0
        job_information = 0
        job_data = job.JobListElement.to_dict #gets job information to compare
        
        data = self.parse_json(self, self.jfilename) #gets user resume information
        
        for key, value in job_data: #checks how much the job qualities match with the user's resume
            if key == "description" or key == "requirements" or key == "tags":
                for tag, information in data:
                    if value == information:
                        related_user_information += 1
                job_information += 1
                

        return (related_user_information / job_information) * 100 #the percentage of how related the user resume is with the job information

    def match(self, job: joblist_element): #returns a list of skills matched and a list of missing skills
        matched = []
        missing = []
        found = False
        skills = []   
        requirements = job.JobListElement.get_requirements
        
        data = self.parse_json(self, self.jfilename)

        for key, value in data:   
            if key == "skills" or key == "Skills":
                skills.append(value)

        for item in requirements: #checks if each requirement is in the user's listed skills or not and adds to the two lists accordingly
            for element in skills:
                if item.lower == element.lower:
                    matched.append(element)
                    found = True
                    break
            if found == False:
                missing.append(item)
            found = False
            
        
        return matched, missing
    
    def exit():

        exit(0)