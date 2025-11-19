import fileinput
import json
import joblist_element
class data_process:


    def __init__(self, file):
        self.filename = file
        self.jfilename = ""
        self.joblist = []


    def parse_resume(self):

        dict1 = {}

        with open(self.filename) as fh:

            for line in fh:
                
                command, description = line.strip().split(None, 1)

                dict1[command] = description.strip()

        self.jfilename = open("resume.json", "w")
        json.dump(dict1, self.jfilename, indent = 4, sort_keys = False)
        self.jfilename.close()

        return self.jfilename

    def parse_json(self, apiFile):
        title = []                #these six lists are for storing elements for the four fields in joblist_element
        url = []
        company = []
        description = []
        requirments = []
        tags = []
        i = 0                     #used to iterate through title, requirments and tags

        with open(apiFile, "r") as f:   #parses the json file from the api
            data = json.load(f)

        for key, value in data:   #fills the six lists with the data from the json file
            if key == "job_title" :
                title.append(value)
            elif key == "job_apply_link" :
                url.append(value)
            elif key == "employer_name" :
                company.append(value)
            elif key == "job_description" :
                description.append(value)
            elif key == "Qualifications" :
                requirments.append(value)
            elif key == "Responsibilities" :
                tags.append(value)

        for item in url:             #creates all the joblist_elements using the six lists based on the number of urls 
            temp = joblist_element(title[i], item, company[i], description[i], requirments[i], tags[i])
            self.joblist.append(temp)
            i += 1


        return self.joblist

    def match_score(self, job: joblist_element): #takes a joblist_element and creates a match score for it
        match = 0
        requirments_number = 0
        requirments = job.JobListElement.get_requirements
        skills = []

        with open(self.jfilename, "r") as f:  #this bit gets the skills from the json file of the users resume
            data = json.load(f)
        for key, value in data:   
            if key == "skills" :
                skills.append(value)

        for item in requirments: #checks if each requirment is in the user's listed skills
            for element in skills:
                if item == element:
                    match += 1
            requirments_number += 1


        return (match / requirments_number) * 100 #returns match percentage

    def relevance_score(self, job: joblist_element): #returns relevance score for a give joblist_element as a percentage
        related = 0
        job_information = 0
        job_data = job.JobListElement.to_dict #gets job information to compare
        with open(self.jfilename, "r") as f: #gets user resume info from the json file
            data = json.load(f)
        
        for key, value in job_data: #checks how much the job qualities match with the user's resume
            if key == "description" or key == "requirements" or key == "tags":
                for tag, information in data:
                    if value == information:
                        related += 1
                job_information += 1
                

        return (related % job_information) * 100 #the percentage of how related the user resume is with the job information

    def match(self, job: joblist_element): #returns a list of skills matched and a list of missing skills
        matched = []
        missing = []
        found = False
        skills = []   
        requirments = job.JobListElement.get_requirements
        
        with open(self.jfilename, "r") as f:  #this bit gets the skills from the json file of the users resume
            data = json.load(f)
        for key, value in data:   
            if key == "skills" : skills.append(value)

        for item in requirments: #checks if each requirment is in the user's listed skills or not and adds to the two lists accordingly
            for element in skills:
                if item == element:
                    matched.append(element)
                    found = True
                    break
            if found == False:
                missing.append(item)
            found = False
        return matched, missing
    
    def exit(): exit(0)