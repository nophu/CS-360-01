class job_list_element:
    # initialize basic job info
     def __init__(self, title, url, company, description, requirements = None, tags = None, rawDictionary = None):

        # save job info
        self.title = title
        self.url = url
        self.company = company
        self.description = description

        # save lists
        self.requirements = requirements if requirements else []
        self.tags = tags if tags else []

        # save raw data
        self.rawDictionary = rawDictionary if rawDictionary else {}

     # return job url
     def get_url(self):
         return self.url

     # return job requirement list
     def get_requirements(self):
         return self.requirements

     # return job tag list
     def get_tags(self):
         return self.tags

     # return job info as a dictionary
     def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "company": self.company,
            "description": self.description,
            "requirements": self.requirements,
            "tags": self.tags,
        }

