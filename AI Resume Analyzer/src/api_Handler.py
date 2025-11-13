class apiHandler:
    def __init__(self):
        import http.client
        self.connection = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': "ef33a65e16msh5f5ae3dc94c29c2p1d65a3jsn4f04ffc646e9",
            'x-rapidapi-host': "jsearch.p.rapidapi.com"
        }

    def getListings(self, query): # Gets all job listings for the provided query (first) parameter
        import json
        from urllib.parse import quote

        query = quote(query)
        searchUrl = "/search?" + query + "&page=1&num_pages=1&country=us&date_posted=all"
        self.connection.request("GET", searchUrl, headers = self.headers)
        response = self.connection.getresponse()

        data = response.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        if not "data" in data:
            return self.openFailSafe()
        else:
            return data["data"]
    
    def openFailSafe(self): # In case the api dies, uses "failSafe.txt" in the relative directory.
        import json
        with open("failSafe.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["data"]

    def openDirectLink(self, jobApplicationLink): # Opens a link directly
        import webbrowser
        webbrowser.open(jobApplicationLink)
    
    def openByJSON(self, jobListingsJSON, jobIndex): # Opens a related link from getListings response and job index
        import webbrowser
        webbrowser.open(jobListingsJSON[jobIndex]["job_apply_link"])

'''
# EXAMPLE PROGRAM
api = apiHandler()

response = api.getListings("developer jobs in chicago")

api.openDirectLink(response[1]["job_apply_link"])
'''