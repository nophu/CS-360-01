import json
import joblist_element
class data_process:


    def __init__(self, file):
        self.filename = file
        self.jfilename = ""
        self.joblist = []

    def create_joblist_element(self, title, url, company, description, requirements, tags): #new method for creating joblist_element
        import joblist_element
        i = 0
        for item in url:             #creates all the joblist_elements using the six lists based on the number of urls 
            temp = joblist_element(title[i], item, company[i], description[i], requirements[i], tags[i])
            self.joblist.append(temp)
            i += 1

        return self.joblist

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
    
    def parse_json(self, file): #parses a json to a dictionary
         import json

         with open(file, "r") as f:  
            data = json.load(f)
            return data

    def parse_Job_List(self, data):
        import joblist_element
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

    def match_score(self, job): #takes a joblist_element and creates a match score for it
        import joblist_element
        match = 0
        requirements_number = 0
        requirements = job.JobListElement.get_requirements()
        skills = []

        data = self.parse_json(self, self.jfilename)  #this bit gets the data from the json file of the users resume
        
        for key, value in data:   #gets user skills
            if key == "skills" or key == "Skills":
                skills.append(value)

        for item in requirements: #checks if each requirement is in the user's listed skills
            for element in skills:
                if item.lower() == element.lower():
                    match += 1
            requirements_number += 1

        return (match / requirements_number) #returns match percentage

    def relevance_score(self, job): #returns relevance score for a give joblist_element as a percentage
        import joblist_element
        related_user_information = 0
        job_information = 0
        job_data = job.JobListElement.to_dict #gets job information to compare
        
        data = self.parse_json(self, self.jfilename) #gets user resume information
        
        for key, value in job_data.items(): #checks how much the job qualities match with the user's resume
            if key == "description" or key == "requirements" or key == "tags":
                for tag, information in data:
                    if value == information:
                        related_user_information += 1
                job_information += 1
                
        return (related_user_information / job_information) * 100 #the percentage of how related the user resume is with the job information

    def match(self, job): #returns a list of skills matched and a list of missing skills
        import joblist_element
        matched = []
        missing = []
        skills = []  
        found = False

        requirements = job.JobListElement.get_requirements()
        data = self.parse_json(self, self.jfilename)

        for key, value in data:   
            if key == "skills" or key == "Skills":
                skills.append(value)

        for item in requirements: #checks if each requirement is in the user's listed skills or not and adds to the two lists accordingly
            for element in skills:
                if item.lower() == element.lower():
                    matched.append(element)
                    found = True
                    break
            if found == False:
                missing.append(item)
            found = False
        
        return matched, missing
    
    def exit():
        exit(0)
