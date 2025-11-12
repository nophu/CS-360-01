class JobListElement:
     def __init__(self,title,url, requirements,tags ):
        self.title = title
        self.url = url
        self.requirements = requirements
        self.tags = tags
     
     def httpUrl(self): return self.url
     
     def requirements(self): return self.requirements
     
     def tags(self): return self.tags

     def showInfo(self):
        print(f"Job Title: {self.title}")
        print(f"Job URL: {self.url}")
        print(f"Job Requirements: {self.requirements}")
        print(f"Job Tags: {self.tags}")
