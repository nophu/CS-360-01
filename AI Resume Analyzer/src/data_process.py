import fileinput
import json
import joblist_element
class DataProcess:


    def __init__(self, file):
        self.filename = file
        self.jfilename = ""
        self.joblist = []


    def parseResume(self):

        dict1 = {}

        with open(self.filename) as fh:

            for line in fh:
                
                command, description = line.strip().split(None, 1)

                dict1[command] = description.strip()

        self.jfilename = open("resume.json", "w")
        json.dump(dict1, self.jfilename, indent = 4, sort_keys = False)
        self.jfilename.close()

        return self.jfilename

    def parseJson(self, apiFile):
        title = []                #these four lists are for storing elements for the four fields in joblist_element
        url = []
        requirments = []
        tags = []
        i = 0                     #used to iterate through title, requirments and tags

        with open(apiFile, "r") as f:   #parses the json file from the api
            data = json.load(f)

        for key, value in data:   #fills the four lists with the data from the json file
            if key == "job_title" :
                title.append(value)
            elif key == "job_apply_link" :
                url.append(value)
            elif key == "Qualifications" :
                requirments.append(value)
            elif key == "Responsibilities" :
                tags.append(value)

        for item in url:             #creates all the joblist_elements using the four lists based on the number of urls 
            temp = joblist_element(title[i], item, requirments[i], tags[i])
            self.joblist.append(temp)
            i += 1


        return self.joblist

    def matchScore():

        return 0

    def relevanceScore():

        return 0

    def match():

        return 0
    
    def exit():

        exit(0)