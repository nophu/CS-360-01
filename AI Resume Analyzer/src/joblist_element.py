class JobListElement:

     def __init__(self, title, url, company, description, requirements = None, tags = None ):
        self.title = title
        self.url = url
        self.company = company
        self.description = description
        self.requirements = requirements if requirements else []
        self.tags = tags if tags else []
     
     def get_url(self):
         return self.url
     
     def get_requirements(self):
         return self.requirements
     
     def get_tags(self):
         return self.tags

     def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "company": self.company,
            "description": self.description,
            "requirements": self.requirements,
            "tags": self.tags,
        }

