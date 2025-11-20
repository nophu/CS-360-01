class JobListElement:
     """
     Stores Information about job posting which includes title, company, URL, description, requirements, and tags.
     """

    # initialize basic job info
     def __init__(self, title: str, url: str, company: str, description: str, requirements: list[str] | None = None, tags: list[str] | None = None, raw_dictionary: dict | None = None):

        # save job info
        self.title = title
        self.url = url
        self.company = company
        self.description = description

        # save lists
        self.requirements = requirements or [] 
        self.tags = tags if tags else []

        # save raw data
        self.raw_dictionary  = raw_dictionary  or {}

     # return job requirement list and tags
     def get(self, field): return getattr(self, field)

     # return job info as a dictionary
     fields = ["title", "url", "company", "description", "requirements", "tags"] 
     def to_dict(self): return {field: getattr(self, field) for field in self.fields}

    # f string for debugging unreadable objects 
     def __repr__(self): return f"JobListElement(title={self.title}, company={self.company})"
